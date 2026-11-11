# Code based on the code from the FuzzingBook.org
# But modified to match the explanation in the slides

import ast
import copy
import inspect
import textwrap

from examples.twice import test

# Reading guide:
# main -> collect_path_states -> traverse -> traverse_statements / traverse_branch.
# Example: function entry gives {x: x, y: y}; z = 2 * y adds {z: 2 * y};
# if x == z then forks into paths with x == 2 * y and (x == 2 * y) == False.
# Store values are AST expressions; constraints are readable Python strings.
# This teaching example handles simple assignments, ifs, and stopping at returns.
# It does not execute calls, explore loops, or check path satisfiability.


class State:
    """A snapshot of one path: current statement, symbolic values, and conditions."""

    def __init__(self, stmt, store, constraints):
        self.stmt = stmt  # An AST node; None means no statement is selected yet.
        # Maps variable names to symbolic expressions (AST nodes).
        self.store = store
        self.constraints = constraints  # Python strings; all must hold on this path.

    def branch(self, stmt, condition):
        """Fork this path without changing the parent state's store or conditions."""
        # copy() creates a separate dictionary; + creates a separate list.
        # The AST values can be shared here because substitution copies expressions
        # and assignments replace dictionary entries rather than edit stored ASTs.
        return State(stmt, self.store.copy(), self.constraints + [condition])


class SymbolicStore(ast.NodeTransformer):
    """Replace variable references with expressions from the store dictionary.

    NodeTransformer walks an AST. Its visit() method dispatches to visit_Name()
    for ast.Name nodes, visit_BinOp() for ast.BinOp nodes, etc. Inherited methods
    handle traversal through nodes for which we have not defined a visit method.
    Despite this class's name, the actual store is the dictionary passed to it.
    """

    def __init__(self, store):
        self.store = store

    def visit_Name(self, node):
        # node.id is the variable's name, e.g. "z" in the condition x == z.
        # get() returns its stored expression, or the original node if absent.
        # Example: store["z"] is the AST for 2 * y, so z becomes 2 * y.
        # deepcopy() prevents the replacement from sharing mutable AST nodes.
        # Stored expressions already refer to the values at assignment time.
        # Do not substitute inside the returned expression again: if x was
        # assigned x + 1, its inner x denotes the original input value.
        return copy.deepcopy(self.store.get(node.id, node))


class StateManager:
    """Process statements in order, forking the current state at each if."""

    def __init__(self, f_ast):
        self.function_ast = f_ast
        self.states = []  # One final state per collected path.

    def collect_path_states(self):
        """Start exploration and return a flat list of final path states."""
        # Begin at the root AST node, with no known bindings or path conditions.
        initial_state = State(self.function_ast, {}, [])
        self.states = self.traverse(initial_state)
        return self.states

    def symbolic_expression(self, expression, store):
        """Return an expression AST with stored variable values substituted."""
        # .visit() starts the NodeTransformer traversal. Copy the input AST so
        # substitution on one path does not change the original program's AST.
        return SymbolicStore(store).visit(copy.deepcopy(expression))

    def traverse(self, state):
        """Process one node and return a list of resulting states.

        An assignment returns one updated state. An if can return several states
        because its branches (including nested branches) are explored separately.
        """
        node = state.stmt
        if isinstance(node, ast.Module):
            # ast.parse() wraps the function definition in a Module node.
            return self.traverse_statements(node.body, state)
        if isinstance(node, ast.FunctionDef):
            # Each input starts as an unknown symbolic value with its own name.
            # These lists cover positional-only, regular, and keyword-only inputs.
            for parameter in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                name = parameter.arg
                # Name("x") represents the unknown input x, not the string "x".
                # Load means this node reads a variable's value.
                state.store[name] = ast.Name(id=name, ctx=ast.Load())
            return self.traverse_statements(node.body, state)
        if isinstance(node, ast.Assign):
            # For z = 2 * y, node.value is 2 * y and node.targets contains z.
            # Substitute BEFORE updating the store, so x = x + 1 uses old x.
            value = self.symbolic_expression(node.value, state.store)
            # Multiple targets also allow assignments such as a = b = 2 * y.
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    raise NotImplementedError("Only assignments to variable names are supported")
                state.store[target.id] = value  # e.g. store["z"] = AST for 2 * y
        elif isinstance(node, ast.If):
            # node.test is the condition AST. Substitute z, then turn the result
            # into readable Python text: x == z becomes "x == 2 * y".
            condition = ast.unparse(self.symbolic_expression(node.test, state.store))
            # body holds the true branch; orelse holds the false branch.
            # An omitted else has orelse = [], but its false path still exists.
            true_states = self.traverse_branch(node.body, state, condition)
            false_states = self.traverse_branch(node.orelse, state, f"({condition}) == False")
            return true_states + false_states
        # Other statements, such as print("ERROR"), are not executed here.
        # Returns are recognized by traverse_statements() to stop that path;
        # their return-value expressions are not evaluated by this example.
        return [state]

    def traverse_statements(self, statements, state):
        """Carry every current path through a sequence of statements."""
        # Start with one path. An if may expand this list into several paths.
        states = [state]
        for stmt in statements:
            # Collect the states produced by this statement on every path.
            next_states = []
            for current in states:
                # A returned path does not execute subsequent statements.
                if isinstance(current.stmt, ast.Return):
                    next_states.append(current)
                else:
                    current.stmt = stmt
                    # extend() adds each returned state to the flat list.
                    # append() would incorrectly add a nested list of states.
                    next_states.extend(self.traverse(current))
            # The next statement receives the updated stores and constraints.
            states = next_states
        return states

    def traverse_branch(self, statements, state, condition):
        """Copy the incoming state, add a condition, and explore this branch."""
        # None is a placeholder; processing the branch selects its statements.
        # An empty branch simply returns the copied state with its new condition.
        branch_state = state.branch(None, condition)
        return self.traverse_statements(statements, branch_state)


def main():
    # Read test() as Python source, remove shared indentation, and parse its AST.
    function_source = textwrap.dedent(inspect.getsource(test))
    function_ast = ast.parse(function_source)
    # Explore the function symbolically
    manager = StateManager(function_ast)
    path_tree = manager.collect_path_states()
    for i, state in enumerate(path_tree, start=1):
        # The real store contains AST nodes. Convert them to text for display.
        store = {name: ast.unparse(value) for name, value in state.store.items()}
        print(f"Path {i}","\n\t",state.constraints, "\n\t",store)


if __name__ == '__main__':
    main()
