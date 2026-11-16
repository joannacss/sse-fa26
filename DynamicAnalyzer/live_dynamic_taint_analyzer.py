# coding=utf8
import linecache
import re
import sys

from examples.shell_example import execute_cmd

SINK_REGEX = re.compile(r"[ \t]+os\.system\((.*)\)")


class TaintAnalyzer:

    def __init__(self):
        # TODO: initialize the analyzer
        pass


    def mark_as_tainted(self, var):
        # TODO: mark a specific variable as tainted
        pass


    def generate_inputs(self):
        # TODO: generates inputs (hardcoded)

        # TODO: mark generated inputs as tainted
        pass

    def check_taint(self, frame, event, arg, code_line):
        # TODO: checks whether a tainted variable reached a sink!
        pass


    def run(self):
        # Tracer function
        def tracer(frame, event, arg):
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

        # TODO: run the tracer for each input




        # TODO: return the vulnerable paths




if __name__ == '__main__':
    analyzer = TaintAnalyzer()
    vuln_paths = analyzer.run()
    if len(vuln_paths) > 0:
        print("\033[95m❌ Vulnerable:\033[00m")
        for i in range(len(vuln_paths)):
            print(f"\033[91m\tPath {i + 1}\033[00m")
            for line in vuln_paths[i]:
                print(f"\033[94m\t\t» {line}\033[00m")
    else:
        print("\033[92m✅ Not vulnerable\033[00m")