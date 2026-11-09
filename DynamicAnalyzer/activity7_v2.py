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


    
def fuzzzzzzy():
	x = 1
	y = 1
	z = 1
	output = triangle(x,y,z)
	sys.settrace(None)
	for i in range(1,5):
		for j in range(1,5):
			x = i
			y = j
			z = i%j
			if j == 4:
				z = 4
			# stop tracing the invocation
			output = triangle(x,y,z)
			print("Output at main()", output)
			sys.settrace(None)
	

def main():
	# start tracing the invocation
	sys.settrace(analyze)
	fuzzzzzzy()

    

if __name__ == '__main__':
	main()
