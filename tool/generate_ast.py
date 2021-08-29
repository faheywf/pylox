import argparse
import os
from typing import List


def define_ast(output_dir: str, base_name: str, types: List[str], internal_dependencies: List[str] = []):
    output_path = os.path.join(output_dir, f"{base_name.lower()}.py")

    output : List[str] = []
    output.append("from abc import ABC")
    output.append("from typing import Any, Generic, List, Optional, TypeVar")
    output.append("import attr")
    output += internal_dependencies
    output.append("")
    output.append("R = TypeVar(\"R\")")
    output.append("")
    output.append("@attr.s(auto_attribs=True)")
    output.append(f"class {base_name}(ABC):")
    output.append(f"\tdef accept(self, visitor: \"{base_name}Visitor\"):")
    output.append(f"\t\traise NotImplemented()")
    output.append("")
    output.append("")

    for t in types:
        class_name, fields = [x.strip() for x in t.split(":")]
        define_type(output, base_name, class_name, fields)
        output.append("")
        output.append("")

    define_visitor(output, base_name, types)

    with open(output_path, 'w') as f:
        f.writelines([line + "\n" for line in output])

def define_visitor(output: List[str], base_name: str, types: List[str]):
    output.append("@attr.s(auto_attribs=True)")
    output.append(f"class {base_name}Visitor(ABC, Generic[R]):")
    for t in types:
        type_name = t.split(":")[0].strip()
        output.append(f"\tdef visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: {type_name}) -> R:")
        output.append(f"\t\traise NotImplemented()")
        output.append("")


def define_type(output: List[str], base_name: str, class_name: str, fields: str):
    output.append("@attr.s(auto_attribs=True)")
    output.append(f"class {class_name}({base_name}):")

    fields = fields.split(",")
    for field in fields:
        t, n = field.split()
        output.append(f"\t{n}: {t}")

    output.append("")
    
    output.append(f"\tdef accept(self, visitor: \"{base_name}Visitor[R]\") -> R:")
    output.append(f"\t\treturn visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate ast")
    parser.add_argument("--output-dir", help="output directory")
    args = parser.parse_args()

    define_ast(args.output_dir, "Expr", [
        "Assign   : Token name, Expr value",
        "Binary   : Expr left, Token operator, Expr right",
        "Call     : Expr callee, Token paren, List[Expr] arguments",
        "Grouping : Expr expression",
        "Literal  : Any value",
        "Logical  : Expr left, Token operator, Expr right",
        "Unary    : Token operator, Expr right",
        "Variable : Token name"
        ],
        ["from tokens import Token"]
    )

    define_ast(args.output_dir, "Stmt", [
        "Block      : List[Stmt] statements",
        "Break      : Token keyword",
        "Expression : Expr expression",
        "Function   : Token name, List[Token] params, List[Stmt] body",
        "If         : Expr condition, Stmt then_branch, Optional[Stmt] else_branch",
        "Print      : Expr expression",
        "Return     : Token keyword, Expr value",
        "Var        : Token name, Expr initializer",
        "While      : Expr condition, Stmt body"
      ],
      ["from expr import Expr",
      "from tokens import Token"]
    )