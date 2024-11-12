import os
import subprocess
from pyverilog.vparser.parser import parse
from pyverilog.vparser.ast import ModuleDef, Input, Output, Wire, Assign, Identifier, IntConst, Partselect

class VerilogChecker(object):
    def __init__(self):
        self.errors = []

    def check(self, ast):
        self.visit(ast)

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        for child in node.children():
            self.visit(child)

    def visit_ModuleDef(self, node):
        for item in node.items:
            if isinstance(item, (Input, Output)):
                if not isinstance(item, Wire):
                    self.errors.append(f"Module input/output {item.name} must be a wire")

    def visit_Assign(self, node):
        if isinstance(node.left, Identifier):
            self.errors.append(f"Consecutive assignment to variable {node.left.name} is not allowed")

    def visit_Partselect(self, node):
        if isinstance(node.var, Identifier) and (node.lb.value > node.rb.value or node.lb.value < 0):
            self.errors.append("Selected bits are out of range")

    def visit_Identifier(self, node):
        if node.scope is None:
            self.errors.append(f"Use of undeclared variable or wire {node.name}")


def code_inspect():
    verilog_file = "rtl.v"

    ast, _ = parse([verilog_file])

    checker = VerilogChecker()
    checker.check(ast)

    if checker.errors:
        for error in checker.errors:
            print(error)
    else:
        print("No errors found.")

    print("Code check completed.")


# code_inspect()
