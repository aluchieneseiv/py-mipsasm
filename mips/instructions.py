from construct import BitStruct, BitsInteger
from mips.parsetypes import *
import mips.regs as regs

RType = BitStruct(
    "op" / BitsInteger(6),
    "rs" / BitsInteger(5),
    "rt" / BitsInteger(5),
    "rd" / BitsInteger(5),
    "shamt" / BitsInteger(5),
    "funct" / BitsInteger(6)
)

IType = BitStruct(
    "op" / BitsInteger(6),
    "rs" / BitsInteger(5),
    "rt" / BitsInteger(5),
    "imm" / BitsInteger(16, signed=True)
)

IType_s = IType

JType = BitStruct(
    "op" / BitsInteger(6),
    "addr" / BitsInteger(26)
)

# Instructions

class Instruction:
    def __repr__(self):
        return str(self)

    def __len__(self):
        return 1

class Add(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            rd = self.dest.reg_id,
            shamt = 0,
            funct = 0x20
        ))
    
    def __str__(self):
        return f"add {self.dest}, {self.a}, {self.b}"

class Addi(Instruction):
    def __init__(self, dest, a, imm):
        self.dest = dest
        self.a = a
        self.imm = imm

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x8,
            rt = self.dest.reg_id,
            rs = self.a.reg_id,
            imm = self.imm.val
        ))
    
    def __str__(self):
        return f"addi {self.dest}, {self.a}, {self.imm}"

class Addiu(Instruction):
    def __init__(self, dest, a, imm):
        self.dest = dest
        self.a = a
        self.imm = imm

    def to_bytes(self, ctx):
        return IType.build(dict(
            op = 0x9,
            rt = self.dest.reg_id,
            rs = self.a.reg_id,
            imm = self.imm.val
        ))
    
    def __str__(self):
        return f"addiu {self.dest}, {self.a}, {self.imm}"

class Addu(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            rd = self.dest.reg_id,
            shamt = 0,
            funct = 0x21
        ))
    
    def __str__(self):
        return f"addu {self.dest}, {self.a}, {self.b}"

class And(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b
    
    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            rd = self.dest.reg_id,
            shamt = 0,
            funct = 0x24
        ))

    def __str__(self):
        return f"and {self.dest}, {self.a}, {self.b}"

class Andi(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return IType.build(dict(
            op = 0xc,
            rt = self.dest.reg_id,
            rs = self.a.reg_id,
            imm = self.b.val
        ))

    def __str__(self):
        return f"andi {self.dest}, {self.a}, {self.b}"

class Beq(Instruction):
    def __init__(self, a, b, lbl):
        self.a = a
        self.b = b
        self.lbl = lbl

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x4,
            rt = self.b.reg_id,
            rs = self.a.reg_id,
            imm = ctx.relative_jmp(self.lbl.name)
        ))

    def __str__(self):
        return f"beq {self.a}, {self.b}, {self.lbl}"

class Bne(Instruction):
    def __init__(self, a, b, lbl):
        self.a = a
        self.b = b
        self.lbl = lbl

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x5,
            rt = self.b.reg_id,
            rs = self.a.reg_id,
            imm = ctx.relative_jmp(self.lbl.name)
        ))
    
    def __str__(self):
        return f"bne {self.a}, {self.b}, {self.lbl}"

class J(Instruction):
    def __init__(self, lbl):
        self.lbl = lbl

    def to_bytes(self, ctx):
        return JType.build(dict(
            op = 0x2,
            addr = ctx.absolute_jmp(self.lbl.name)
        ))
    
    def __str__(self):
        return f"j {self.lbl}"

class Jal(Instruction):
    def __init__(self, lbl):
        self.lbl = lbl

    def to_bytes(self, ctx):
        return JType.build(dict(
            op = 0x3,
            addr = ctx.get_label(self.lbl.name)
        ))

    def __str__(self):
        return f"jal {self.lbl}"

class Jr(Instruction):
    def __init__(self, reg):
        self.reg = reg

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x8,
            rs = self.reg.reg_id,
            rt = 0,
            rd = 0,
            shamt = 0
        ))

    def __str__(self):
        return f"jr {self.reg}"

class Lbu(Instruction):
    def __init__(self, dest, offsetreg):
        self.dest = dest
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x24,
            rt = self.dest.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"lbu {self.dest}, {self.offsetreg}"

class Lhu(Instruction):
    def __init__(self, dest, offsetreg):
        self.dest = dest
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x25,
            rt = self.dest.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))
    
    def __str__(self):
        return f"lhu {self.dest}, {self.offsetreg}"

class Ll(Instruction):
    def __init__(self, dest, offsetreg):
        self.dest = dest
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x30,
            rt = self.dest.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"ll {self.dest}, {self.offsetreg}"

class Lui(Instruction):
    def __init__(self, dest, imm):
        self.dest = dest
        self.imm = imm

    def to_bytes(self, ctx):
        return IType.build(dict(
            op = 0xf,
            rs = 0x0,
            rt = self.dest.reg_id,
            imm = self.imm.val
        ))

    def __str__(self):
        return f"lui {self.dest}, {self.imm}"

class Lw(Instruction):
    def __init__(self, dest, offsetreg):
        self.dest = dest
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x23,
            rt = self.dest.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"lw {self.dest}, {self.offsetreg}"

class Nor(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x27,
            shamt = 0,
            rd = self.dest.reg_id,
            rs = self.a.reg_id,
            rt = self.b.reg_id
        ))

    def __str__(self):
        return f"nor {self.dest}, {self.a}, {self.b}"

class Or(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x25,
            shamt = 0,
            rd = self.dest.reg_id,
            rs = self.a.reg_id,
            rt = self.b.reg_id
        ))

    def __str__(self):
        return f"or {self.dest}, {self.a}, {self.b}"

class Ori(Instruction):
    def __init__(self, dest, reg, imm):
        self.dest = dest
        self.reg = reg
        self.imm = imm

    def to_bytes(self, ctx):
        return IType.build(dict(
            op = 0xd,
            rt = self.dest.reg_id,
            rs = self.reg.reg_id,
            imm = self.imm.val
        ))

    def __str__(self):
        return f"ori {self.dest}, {self.reg}, {self.imm}"

class Slt(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x2a,
            rd = self.dest.reg_id,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            shamt = 0,
        ))

    def __str__(self):
        return f"slt {self.dest}, {self.a}, {self.b}"

class Slti(Instruction):
    def __init__(self, dest, reg, imm):
        self.dest = dest
        self.reg = reg
        self.imm = imm

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0xa,
            rt = self.dest.reg_id,
            rs = self.reg.reg_id,
            imm = self.imm.val
        ))

    def __str__(self):
        return f"slti {self.dest}, {self.reg}, {self.imm}"

class Sltiu(Instruction):
    def __init__(self, dest, reg, imm):
        self.dest = dest
        self.reg = reg
        self.imm = imm

    def to_bytes(self, ctx):
        return IType.build(dict(
            op = 0xb,
            rt = self.dest.reg_id,
            rs = self.reg.reg_id,
            imm = self.imm.val
        ))

    def __str__(self):
        return f"sltiu {self.dest}, {self.reg}, {self.imm}"

class Sltu(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x2b,
            shamt = 0,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            rd = self.dest.reg_id,
        ))

    def __str__(self):
        return f"sltu {self.dest}, {self.a}, {self.b}"

class Sll(Instruction):
    def __init__(self, dest, reg, shamt):
        self.dest = dest
        self.reg = reg
        self.shamt = shamt

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0,
            rs = 0,
            rt = self.reg.reg_id,
            rd = self.dest.reg_id,
            shamt = self.shamt.val
        ))

    def __str__(self):
        return f"sll {self.dest}, {self.reg}, {self.shamt}"

class Srl(Instruction):
    def __init__(self, dest, reg, shamt):
        self.dest = dest
        self.reg = reg
        self.shamt = shamt

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x2,
            rs = 0,
            rt = self.reg.reg_id,
            rd = self.dest.reg_id,
            shamt = self.shamt.val
        ))

    def __str__(self):
        return f"srl {self.dest}, {self.reg}, {self.shamt}"

class Sb(Instruction):
    def __init__(self, source, offsetreg):
        self.source = source
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x28,
            rt = self.source.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"sb {self.source}, {self.offsetreg}"

class Sc(Instruction):
    def __init__(self, source, offsetreg):
        self.source = source
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x38,
            rt = self.source.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"sc {self.source}, {self.offsetreg}"

class Sh(Instruction):
    def __init__(self, source, offsetreg):
        self.source = source
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x29,
            rt = self.source.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"sh {self.source}, {self.offsetreg}"

class Sw(Instruction):
    def __init__(self, source, offsetreg):
        self.source = source
        self.offsetreg = offsetreg

    def to_bytes(self, ctx):
        return IType_s.build(dict(
            op = 0x2b,
            rt = self.source.reg_id,
            rs = self.offsetreg.reg.reg_id,
            imm = self.offsetreg.offset
        ))

    def __str__(self):
        return f"sw {self.source}, {self.offsetreg}"

class Sub(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x22,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            rd = self.dest.reg_id,
            shamt = 0
        ))
    
    def __str__(self):
        return f"sub {self.dest}, {self.a}, {self.b}"

class Subu(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def to_bytes(self, ctx):
        return RType.build(dict(
            op = 0x0,
            funct = 0x23,
            rs = self.a.reg_id,
            rt = self.b.reg_id,
            rd = self.dest.reg_id,
            shamt = 0
        ))
    
    def __str__(self):
        return f"sub {self.dest}, {self.a}, {self.b}"

# Special instructions

class Nop(Instruction):
    def to_bytes(self, ctx):
        return JType.build(dict(
            op = 0,
            addr = 0
        ))
    
    def __str__(self):
        return f"nop"

# Pseudoinstructions

class PseudoInstruction(Instruction):
    def __init__(self, string, instr):
        self.string = string
        self.instr = instr

    def to_bytes(self, ctx):
        return b"".join(i.to_bytes(ctx) for i in self.instr)

    def __str__(self):
        return self.string

    def __len__(self):
        return sum(len(i) for i in self.instr)

def Move(dest, source):
    return PseudoInstruction(f"move {dest}, {source}", (
        Addu(dest, source, regs.zero),
    ))

def Li(dest, imm):
    return PseudoInstruction(f"li {dest}, {imm}", (
        Addiu(dest, regs.zero, Constant(imm.val & 0xFFFF)),
        Lui(dest, Constant(imm.val >> 16)),
    ))

class La(PseudoInstruction):
    def __init__(self, reg, lbl):
        self.reg = reg
        self.lbl = lbl

    def to_bytes(self, ctx):
        return Li(self.reg, Constant(ctx.get_label(self.lbl.name))).to_bytes(ctx)

    def __str__(self):
        return f"la {self.reg}, {self.lbl}"

    def __len__(self):
        return 2

def Jf(lbl):
    return PseudoInstruction(f"jf {lbl}", (
        La(regs.at, lbl),
        Jr(regs.at)
    ))

def Blt_rr(reg, tst, lbl):
    return PseudoInstruction(f"blt {reg}, {tst}, {lbl}", (
        Slt(regs.at, reg, tst),
        Bne(regs.at, regs.zero, lbl)
    ))

def Blt_ri(reg, imm, lbl):
    return PseudoInstruction(f"blt {reg}, {imm}, {lbl}", (
        Li(regs.at, imm),
        Blt_rr(reg, regs.at)
    ))

def Bge_rr(reg, tst, lbl):
    return PseudoInstruction(f"bge {reg}, {tst}, {lbl}", (
        Slt(regs.at, reg, tst),
        Beq(regs.at, regs.zero, lbl)
    ))

def Bge_ri(reg, imm, lbl):
    return PseudoInstruction(f"bge {reg}, {imm}, {lbl}", (
        Li(regs.at, imm),
        Bge_rr(reg, regs.at)
    ))

def Bgt_rr(reg, tst, lbl):
    return PseudoInstruction(f"bgt {reg}, {tst}, {lbl}", (
        Slt(regs.at, tst, a),
        Bne(regs.at, regs.zero, lbl)
    ))

def Bgt_ri(reg, imm, lbl):
    return PseudoInstruction(f"bgt {reg}, {imm}, {lbl}", (
        Li(regs.at, imm),
        Bgt_rr(reg, regs.at, lbl)
    ))

def Ble_rr(reg, tst, lbl):
    return PseudoInstruction(f"ble {reg}, {tst}, {lbl}", (
        Slt(regs.at, tst, reg),
        Beq(regs.at, regs.zero, lbl)
    ))

def Ble_ri(reg, imm, lbl):
    return PseudoInstruction(f"ble {reg}, {imm}, {lbl}", (
        Li(regs.at, imm),
        Ble_rr(reg, regs.at, lbl)
    ))

# Instruction resolving

setattr(regs.Register, '_hack_hash', "reg")
setattr(Constant, '_hack_hash', "imm")
setattr(OffsetRegister, '_hack_hash', "off")
setattr(LabelRef, '_hack_hash', "lbl")

_instruction_resolve = {
    # Instructions

    ("add", "reg", "reg", "reg"): Add,
    ("addi", "reg", "reg", "imm"): Addi,
    ("addiu", "reg", "reg", "imm"): Addiu,
    ("addu", "reg", "reg", "reg"): Addu,
    ("and", "reg", "reg", "reg"): And,
    ("andi", "reg", "reg", "imm"): Andi,
    ("beq", "reg", "reg", "lbl"): Beq,
    ("bne", "reg", "reg", "lbl"): Bne,
    ("j", "lbl"): J,
    ("jal", "lbl"): Jal,
    ("jr", "reg"): Jr,
    ("lbu", "reg", "off"): Lbu,
    ("lhu", "reg", "off"): Lhu,
    ("ll", "reg", "off"): Ll,
    ("lui", "reg", "imm"): Lui,
    ("lw", "reg", "off"): Lw,
    ("nor", "reg", "reg", "reg"): Nor,
    ("or", "reg", "reg", "reg"): Or,
    ("ori", "reg", "reg", "imm"): Ori,
    ("slt", "reg", "reg", "reg"): Slt,
    ("slti", "reg", "reg", "imm"): Slti,
    ("sltiu", "reg", "reg", "imm"): Sltiu,
    ("sltu", "reg", "reg", "reg"): Sltu,
    ("sll", "reg", "reg", "imm"): Sll,
    ("srl", "reg", "reg", "imm"): Srl,
    ("sb", "reg", "off"): Sb,
    ("sc", "reg", "off"): Sc,
    ("sh", "reg", "off"): Sh,
    ("sw", "reg", "off"): Sw,
    ("sub", "reg", "reg", "reg"): Sub,
    ("subu", "reg", "reg", "reg"): Subu,

    ("nop",): Nop,

    # Pseudoinstructions

    ("move", "reg", "reg"): Move,
    ("li", "reg", "imm"): Li,
    ("la", "reg", "lbl"): La,
    ("jf", "lbl"): Jf,

    ("blt", "reg", "reg", "lbl"): Blt_rr,
    ("blt", "reg", "imm", "lbl"): Blt_ri,

    ("ble", "reg", "reg", "lbl"): Ble_rr,
    ("ble", "reg", "imm", "lbl"): Ble_ri,

    ("bgt", "reg", "reg", "lbl"): Bgt_rr,
    ("bgt", "reg", "imm", "lbl"): Bgt_ri,

    ("bge", "reg", "reg", "lbl"): Bge_rr,
    ("bge", "reg", "imm", "lbl"): Bge_ri,

    # Instruction aliases

    # Not
    ("not", "reg", "reg"): lambda dest, reg: PseudoInstruction(f"not {dest}, {reg}", (
        Nor(dest, reg, reg.zero),
    )),

    # Mov, because why not
    ("mov", "off", "reg"): lambda dest, source: PseudoInstruction(f"mov {dest}, {source}", (
        Sw(source, dest),
    )),
    ("mov", "reg", "off"): lambda dest, source: PseudoInstruction(f"mov {dest}, {source}", (
        Lw(dest, source),
    )),
    ("mov", "reg", "reg"): lambda dest, source: PseudoInstruction(f"mov {dest}, {source}", (
        Move(dest, source),
    )),
    ("mov", "reg", "imm"): lambda dest, source: PseudoInstruction(f"mov {dest}, {source}", (
        Li(dest, source),
    )),
}

def _type_match(args, form):
    if len(form) != len(args):
        return False

    for val, type_str in zip(args, form):
        if not isinstance(val, _types_dict[type_str]):
            return False

    return True

def resolve_instruction(mnemonic, args):
    needed_form = (mnemonic,) + tuple(map(lambda obj: type(obj)._hack_hash, args))
    if needed_form in _instruction_resolve:
        return _instruction_resolve[needed_form](*args)

    raise Exception(f"Unknown instruction: {mnemonic} {', '.join(map(lambda x: str(type(x)), args))}")