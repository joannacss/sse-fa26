from examples.triangle import triangle
import sys
import inspect

def analyze(frame, event, arg):
    # TODO: get function code, name, and line number

    # TODO: print f"{event} --> {function_name}:{lineno}"



    # TODO: returns the function itself to track the new scope
	return analyze



if __name__ == '__main__':
	# TODO: start tracing the invocation
	output = triangle(2, 2, 1)
	# TODO: stop tracing the invocation
	print("Output at main()", output)
