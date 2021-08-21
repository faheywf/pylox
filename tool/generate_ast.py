import argparse
import os
from typing import List


def define_ast(output_dir: str, base_name: str, types: List[str]):
    output_path = os.path.join(output_dir, f"{base_name.lower()}.py")

    output : List[str] = []
    output.append("from abc import ABC")
    output.append("from typing import Any, Generic, TypeVar")
    output.append("import attr")
    output.append("from tokens import Token")
    output.append("")
    output.append("R = TypeVar(\"R\")")
    output.append("")
    output.append("@attr.s(auto_attribs=True)")
    output.append(f"class {base_name}(ABC):")
    output.append("\tdef accept(self, visitor: \"Visitor\"):")
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
    output.append(f"class Visitor(ABC, Generic[R]):")
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
    
    output.append("\tdef accept(self, visitor: \"Visitor[R]\") -> R:")
    output.append(f"\t\treturn visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate ast")
    parser.add_argument("--output-dir", help="output directory")
    args = parser.parse_args()

    define_ast(args.output_dir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Any value",
        "Unary    : Token operator, Expr right"
        ]
    )    