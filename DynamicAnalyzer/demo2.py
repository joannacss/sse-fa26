from examples.triangle import triangle
import sys
import inspect

def analyze(frame, event, arg):
	# TODO: get function code, name, and line number


	# TODO: get all source lines

	# TODO: get all variables to capture their values


	# TODO: prints them f"{event} --> {function_name}:{lineno} {statement} ({variables})"


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