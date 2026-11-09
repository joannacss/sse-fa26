from examples.triangle import triangle
import sys
import inspect

def analyze(frame, event, arg):
    # TODO: get function code, name, and line number
	function_name = frame.f_code.co_name
	lineno = frame.f_lineno
    # TODO: print f"{event} --> {function_name}:{lineno}"
	print(f"{event} --> {function_name}:{lineno}")


    # TODO: returns the function itself to track the new scope
	return analyze



if __name__ == '__main__':
	# TODO: start tracing the invocation
	sys.settrace(analyze)
	output = triangle(2, 2, 1)
	sys.settrace(None)
	# TODO: stop tracing the invocation
	print("Output at main()", output)
