# coding=utf8
import ast
import inspect
import linecache
import re
import sys
import textwrap

import z3

from examples.shell_example import execute_cmd
from symbolic_fuzzer import StateManager

SINK_REGEX = re.compile(r"[ \t]+os\.system\((.*)\)")


class TaintAnalyzer:

    def __init__(self, target_function):
        # TODO: initialize the analyzer
        self.tainted_variables = set()
        self.inputs = []
        self.vulnerable_paths = []
        self.target_function = target_function


    def mark_as_tainted(self, var):
        # TODO: mark a specific variable as tainted
        self.tainted_variables.add(id(var))

    def generate_inputs(self):
        function_source = textwrap.dedent(inspect.getsource(self.target_function))
        function_ast = ast.parse(function_source)
        input_name = next(iter(inspect.signature(self.target_function).parameters))
        manager = StateManager(function_ast)
        path_tree = manager.build_tree()

        for i, state in enumerate(path_tree, start=1):
            print(f"Path {i}: ", state.constraints)
            symbols = {name: z3.String(name) for name in state.store}
            path_constraints = ",".join(state.constraints)
            # Z3 uses PrefixOf(prefix, string) for Python's string.startswith(prefix).
            path_constraints = re.sub(
                r"(\w+)\.startswith\(([^()]*)\)",
                r"z3.PrefixOf(\2, \1)",
                path_constraints,
            )
            constraint = f"z3.And({path_constraints})"

            solver = z3.Solver()
            solver.add(eval(constraint, {"z3": z3}, symbols))

            result = solver.check()
            if result == z3.sat:
                print("Satisfiable!", solver.model())
                tainted_input = solver.model().eval(
                    symbols[input_name], model_completion=True
                ).as_string()
                self.inputs.append(tainted_input)
                self.mark_as_tainted(tainted_input)
            elif result == z3.unsat:
                print("Unsatisfiable!")
            else:
                print("Unknown:", solver.reason_unknown())

    def check_taint(self, frame, event, arg, code_line):
        # TODO: checks whether a tainted variable reached a sink!
        if event == "line":
            m = SINK_REGEX.match(code_line)
            if m:
                var_name = m.group(1)
                var_id = id(frame.f_locals[var_name])
                if var_id in self.tainted_variables:
                    self.vulnerable_paths.append(self.current_path)


    def run(self):
        # TODO: implement the tracer function
        def tracer(frame, event, arg):
            if frame.f_code != self.target_function.__code__:
                return None
            function_code = frame.f_code
            function_name = function_code.co_name
            lineno = frame.f_lineno
            executed_line = linecache.getline(function_code.co_filename, lineno).rstrip()
            variable_values = ", ".join([f"{name}={frame.f_locals[name]}" for name in frame.f_locals])
            self.current_path.append(f"{function_name}:{lineno} {executed_line} ({variable_values})")
            print(self.current_path[-1])
            self.check_taint(frame, event, arg, executed_line)
            return tracer

        # TODO: generate inputs
        self.generate_inputs()
        for tainted_input in self.inputs:
            # TODO: run the tracer for each input
            self.current_path = []
            sys.settrace(tracer)
            try:
                self.target_function(tainted_input)
            finally:
                sys.settrace(None)

        # TODO: return the vulnerable paths
        return self.vulnerable_paths



if __name__ == '__main__':
    analyzer = TaintAnalyzer(execute_cmd)
    vuln_paths = analyzer.run()
    if len(vuln_paths) > 0:
        print("\033[95m❌ Vulnerable:\033[00m")
        for i in range(len(vuln_paths)):
            print(f"\033[91m\tPath {i + 1}\033[00m")
            for line in vuln_paths[i]:
                print(f"\033[94m\t\t» {line}\033[00m")
    else:
        print("\033[92m✅ Not vulnerable\033[00m")
