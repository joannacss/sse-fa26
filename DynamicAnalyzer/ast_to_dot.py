"""
Simple script to redner the AST using Dot format.
Prior to executing this script, make sure to install the following:
brew install graphviz
brew install dot
pip install graphviz
"""
import inspect
import ast
from html import escape
from examples.twice import test


def visualize_ast(tree):
	# CODE FROM: https://earthly.dev/blog/python-ast/
	from graphviz import Digraph

	# Create a Graphviz Digraph object
	dot = Digraph()
	# Operator and context nodes do not have standalone source code.
	symbols = {
	    ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.MatMult: '@',
	    ast.Div: '/', ast.FloorDiv: '//', ast.Mod: '%', ast.Pow: '**',
	    ast.LShift: '<<', ast.RShift: '>>', ast.BitOr: '|',
	    ast.BitXor: '^', ast.BitAnd: '&', ast.And: 'and', ast.Or: 'or',
	    ast.Invert: '~', ast.Not: 'not', ast.UAdd: '+', ast.USub: '-',
	    ast.Eq: '==', ast.NotEq: '!=', ast.Lt: '<', ast.LtE: '<=',
	    ast.Gt: '>', ast.GtE: '>=', ast.Is: 'is', ast.IsNot: 'is not',
	    ast.In: 'in', ast.NotIn: 'not in',
	    ast.Load: 'read', ast.Store: 'write', ast.Del: 'delete',
	}

	# Define a function to recursively add nodes to the Digraph
	def add_node(node, parent=None):
	    node_name = str(node.__class__.__name__)
	    if isinstance(node, ast.Module):
	        code = ''
	    elif isinstance(node, (ast.If, ast.While)):
	        code = ast.unparse(node.test)
	    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
	        code = node.name
	    elif type(node) in symbols:
	        code = symbols[type(node)]
	    else:
	        code = ast.unparse(node)
	    # Graphviz HTML labels support italics; escape Python's <, > and &.
	    code = escape(code).replace('\n', '<BR/>')
	    label = f'<{node_name}<BR/><I>{code}</I>>' if code else node_name
	    dot.node(str(id(node)), label)
	    if parent:
	        dot.edge(str(id(parent)), str(id(node)))
	    for child in ast.iter_child_nodes(node):
	        add_node(child, node)

	# Add nodes to the Digraph
	add_node(tree)

	# Render the Digraph as a PNG file
	dot.format = 'png'
	dot.render('test', view=True)


def main():
	test_source = inspect.getsource(test)
	test_ast = ast.parse(test_source)
	visualize_ast(test_ast)
	print(ast.dump(test_ast, indent=2))




if __name__ == '__main__':
	main()
