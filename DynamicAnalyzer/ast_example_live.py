# TODO: import required modules
import ast
import inspect
from examples.twice import test
# TODO: get source code (use inspect module)
test_source = inspect.getsource(test)

# TODO: get source code's AST
test_ast = ast.parse(test_source)

# TODO: print the AST of the code
print(ast.dump(test_ast))

