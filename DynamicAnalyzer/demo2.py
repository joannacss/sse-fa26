from examples.triangle import triangle
import sys
import inspect

def analyze(frame, event, arg):
	# TODO: get function code, name, and line number
	function_name = frame.f_code.co_name
	lineno = frame.f_lineno

	# TODO: get all source lines
	source_lines, starting_no = inspect.getsourcelines(frame.f_code)
	statement = source_lines[lineno - starting_no].strip()

	# TODO: get all variables to capture their values
	local_vars = frame.f_locals
	vars = []
	for var_name, var_value in local_vars.items():
		vars.append(f"{var_name}={var_value}")
	variables = ";".join(vars)
	# TODO: prints them f"{event} --> {function_name}:{lineno} {statement} ({variables})"
	print(f"{event} --> {function_name}:{lineno} {statement} ({variables})")

	# returns the function itself to track the new scope
	return analyze


    

def main():
	# start tracing the invocation
	sys.settrace(analyze)
	output = triangle(2, 2, 1)
	# stop tracing the invocation
	sys.settrace(None)
	print("Output at main()", output)
    

if __name__ == '__main__':
	main()