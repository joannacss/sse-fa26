# Code based on the code from the FuzzingBook.org
# But modified to match the explanation in the slides

import ast
import copy
import inspect
import textwrap
import z3

from examples.twice import test


class State:
	def __init__(self, stmt, store, constraints):
		self.stmt = stmt
		# Maps variable names to symbolic expressions (AST nodes).
		self.store = store
		self.constraints = constraints

	def branch(self, stmt, condition):
		return State(stmt, self.store.copy(), self.constraints + [condition])


class SymbolicStore(ast.NodeTransformer):
	def __init__(self, store):
		self.store = store

	def visit_Name(self, node):
		# Stored expressions already refer to the values at assignment time.
		return copy.deepcopy(self.store.get(node.id, node))


class StateManager:
	def __init__(self, f_ast):
		self.function_ast = f_ast
		self.states = []  # One final state per collected path.

	def build_tree(self):
		initial_state = State(self.function_ast, {}, [])
		self.states = self.traverse(initial_state)
		return self.states

	def symbolic_expression(self, expression, store):
		return SymbolicStore(store).visit(copy.deepcopy(expression))

	def traverse(self, state):
		node = state.stmt
		if isinstance(node, ast.Module):
			return self.traverse_statements(node.body, state)
		if isinstance(node, ast.FunctionDef):
			# Each input starts as an unknown symbolic value with its own name.
			for parameter in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
				name = parameter.arg
				state.store[name] = ast.Name(id=name, ctx=ast.Load())
			return self.traverse_statements(node.body, state)
		if isinstance(node, ast.Assign):
			value = self.symbolic_expression(node.value, state.store)
			for target in node.targets:
				if not isinstance(target, ast.Name):
					raise NotImplementedError("Only assignments to variable names are supported")
				state.store[target.id] = value
		elif isinstance(node, ast.If):
			condition = ast.unparse(self.symbolic_expression(node.test, state.store))
			true_states = self.traverse_branch(node.body, state, condition)
			false_states = self.traverse_branch(node.orelse, state, f"({condition}) == False")
			return true_states + false_states
		return [state]

	def traverse_statements(self, statements, state):
		states = [state]
		for stmt in statements:
			next_states = []
			for current in states:
				# A returned path does not execute subsequent statements.
				if isinstance(current.stmt, ast.Return):
					next_states.append(current)
				else:
					current.stmt = stmt
					next_states.extend(self.traverse(current))
			states = next_states
		return states

	def traverse_branch(self, statements, state, condition):
		branch_state = state.branch(None, condition)
		return self.traverse_statements(statements, branch_state)


def main():
	function_source = textwrap.dedent(inspect.getsource(test))
	function_ast = ast.parse(function_source)
	manager = StateManager(function_ast)
	path_tree = manager.build_tree()

	for i, state in enumerate(path_tree, start=1):
		print(f"Path {i}: ", state.constraints)
		symbols = {name: z3.Int(name) for name in state.store}
		path_constraints = ",".join(state.constraints)
		constraint = f"z3.And({path_constraints})"

		solver = z3.Solver()
		solver.add(eval(constraint, {"z3": z3}, symbols))

		result = solver.check()
		if result == z3.sat:
			print("Satisfiable!", solver.model())
		elif result == z3.unsat:
			print("Unsatisfiable!")
		else:
			print("Unknown:", solver.reason_unknown())


if __name__ == '__main__':
	main()
