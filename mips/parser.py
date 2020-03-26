from lark import Transformer, Lark, v_args
import mips.regs as regs
from mips.parsetypes import *
from mips.instructions import resolve_instruction
from os import path

@v_args(inline = True)
class ConstTransformer(Transformer):
    def integer_const(self, val):
        return Constant(int(val))

    def hex_const(self, val):
        return Constant(int(val[2:], base=16))

    def string_const(self, val):
        return StringConstant(val[1:-1])

@v_args(inline=True)
class RegisterTransformer(Transformer):
    def offset_reg(self, offset, reg):
        return OffsetRegister(reg, int(offset))

    def numeric_reg(self, reg_id):
        try:
            return regs.from_id(int(reg_id))
        except Exception as ex:
            raise Exception(f"line {reg_id.line}: {ex}")

    def named_reg(self, name):
        try:
            return regs.from_name(name)
        except Exception as ex:
            raise Exception(f"line {name.line}: {ex}")

@v_args(inline=True)
class LabelTransformer(Transformer):
    def create_label_ref(self, name):
        return LabelRef(name)

    def create_label(self, lbl_ref):
        return Label(lbl_ref.name)

    def create_mem_label(self, addr):
        return MemLabel(int(addr[2:], base=16))

@v_args(inline=True)
class InstrTransformer(Transformer):
    def create_instr(self, mnemonic, args):
        try:
            return resolve_instruction(mnemonic, args.children)
        except Exception as ex:
            raise Exception(f"line {mnemonic.line}: {ex}")

_decl_types = {
    "word": lambda val: WordDecl(val.numeric_val()),
    "half": lambda val: HalfDecl(val.numeric_val()),
    "word": lambda val: WordDecl(val.numeric_val()),
    "byte": lambda val: ByteDecl(val.numeric_val()),
    "asciiz": lambda val: AsciizDecl(val.val)
}

@v_args(inline=True)
class DeclTransformer(Transformer):
    def create_decl(self, decl_type, val):
        if decl_type not in _decl_types:
            raise Exception(f"line {decl_type.line}: No such declaration type: .{decl_type}")

        return _decl_types[decl_type](val)

class SegmentTransformer(Transformer):
    def text_segm(self, lst):
        return TextSegment(lst)

    def data_segm(self, lst):
        return DataSegment(lst)

transformer = RegisterTransformer() * ConstTransformer() * DeclTransformer() * LabelTransformer() * InstrTransformer() * SegmentTransformer()
grammar_path = path.dirname(path.abspath(__file__))
parser = Lark.open(f"{grammar_path}/mipsasm.lark", parser='lalr')

def parse(text):
    if text[-1] != '\n':
        text = text + '\n'
    
    tree = parser.parse(text)
    tree = transformer.transform(tree)

    return tree.children
