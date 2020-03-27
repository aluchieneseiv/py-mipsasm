import re

class Constant:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return f"Constant({self.val})"

    def numeric_val(self):
        return self.val

class StringConstant(Constant):
    def numeric_val(self):
        try:
            return ord(self.val.encode().decode('unicode_escape').encode())
        except:
            raise Exception("Cannot take numeric value of string")

class OffsetRegister:
    def __init__(self, reg, offset):
        self.reg = reg
        self.offset = offset

    def __str__(self):
        return f"{self.offset}({self.reg})"

    def __repr__(self):
        return f"OffsetRegister({self.reg}, {self.offset})"

class Label:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name}:"

    def __repr__(self):
        return f"Label({self.name})"

class LabelRef:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"LabelRef({self.name})"

class MemLabel:
    def __init__(self, addr):
        self.addr = addr
    
    def __str__(self):
        return f"@0x{self.addr:X}"

class Decl:
    def __init__(self, val):
        self.val = val

class WordDecl(Decl):
    def __str__(self):
        return f".word {self.val}"

    def to_bytes(self):
        return self.val.to_bytes(4, 'big')

    def __len__(self):
        return 4

class HalfDecl(Decl):
    def __str__(self):
        return f".half {self.val}"

    def to_bytes(self):
        return self.val.to_bytes(2, 'big')

    def __len__(self):
        return 2

class ByteDecl(Decl):
    def __str__(self):
        return f".byte {self.val}"

    def to_bytes(self):
        return self.val.to_bytes(1, 'big')

    def __len__(self):
        return 1

class AsciizDecl(Decl):
    def __str__(self):
        return f".asciiz \"{self.val}\""

    def to_bytes(self):
        return self.val.encode().decode('unicode_escape').encode() + b'\0'

    def __len__(self):
        return len(self.val) + 1

class SpaceDecl(Decl):
    def __str__(self):
        return f".space {self.val}"

    def to_bytes(self):
        return b'\0' * self.val

    def __len__(self):
        return self.val

class DataSegment:
    def __init__(self, lines):
        self.lines = lines

    def __str__(self):
        return "<Data segment>"

class TextSegment:
    def __init__(self, lines):
        self.lines = lines

    def __str__(self):
        return "<Text segment>"

