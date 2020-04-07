import io
from .parser import parse
from .parsetypes import *
from .instructions import Instruction
from typing import Dict

class MemoryFile:
    def __init__(self, filename, cell_size = 1, align = None):
        self.file = io.open(filename, "w")
        self.addr = 0
        self.cell_size = cell_size
        self.align = align

    def _write_cell(self, cell):
        self.file.write(cell.hex())

        self.addr = self.addr + 1

    def write_bytes(self, bytes, comment=None):
        if len(bytes) % self.cell_size:
            raise Exception("Bytes not multiple of cell size!")

        align = self.align or 1

        cells = [bytes[i:i+self.cell_size] for i in range(0, len(bytes), self.cell_size)]
        aligned = [cells[i:i+align] for i in range(0, len(cells), align)]

        for line in aligned[:-1]:
            for cell in line[:-1]:
                self._write_cell(cell)
                self.file.write(" ")

            self._write_cell(line[-1])
            self.file.write("\n")
        
        for cell in aligned[-1][:-1]:
            self._write_cell(cell)
            self.file.write(" ")

        self._write_cell(aligned[-1][-1])

        if comment is not None:
            self.file.write(f" // {comment}")
        
        self.file.write('\n')

    def write_comment(self, comment):
        self.file.write(f"// {comment}\n")

    def set_addr(self, addr):
        self.file.write(f"\n@{addr:X}\n")
        self.addr = addr

    def close(self):
        self.file.close()

class Context:
    def __init__(self, ram: MemoryFile, rom: MemoryFile, debug=False):
        self._labels: Dict[str, int] = dict()
        self.ram = ram
        self.rom = rom
        self.debug = debug

    def get_label(self, label):
        if label in self._labels:
            return self._labels[label]

        raise Exception(f"Label is not defined: {label}")

    def set_label(self, label, val):
        if label in self._labels:
            raise Exception(f"Label is already defined: {label}")

        self._labels[label] = val

    def relative_jmp(self, label):
        return self.get_label(label) - self.rom.addr

    def absolute_jmp(self, label):
        new_pc = self.get_label(label)

        if self.rom.addr >> 26 == new_pc >> 26:
            return ~((-1) << 26) & new_pc
        
        raise Exception(f"Jump to label {label} is too far")

class FirstPass:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def visit_DataSegment(self, segm: DataSegment):
        self.data_addr = self.ctx.ram.addr

        self.segm = 'data'
        for line in segm.lines:
            line.accept(self)

    def visit_TextSegment(self, segm: TextSegment):
        self.text_addr = self.ctx.rom.addr

        self.segm = 'text'
        for line in segm.lines:
            line.accept(self)

    def visit_Decl(self, line: Decl):
        self.data_addr = self.data_addr + len(line)

    def visit_Label(self, lbl: Label):
        self.ctx.set_label(lbl.name, self.data_addr)

    def visit_MemLabel(self, lbl: MemLabel):
        if self.segm == 'data':
            self.data_addr = lbl.addr
        else:
            self.text_addr = lbl.addr

    def visit_Instruction(self, instr: Instruction):
        self.text_addr = self.text_addr + len(instr)

class SecondPass:
    def __init__(self, ctx: Context, debug):
        self.ctx = ctx
        self.debug = debug

    def visit_DataSegment(self, segm: DataSegment):
            if self.debug:
                print(".data")

            self.segm = 'data'
            for line in segm.lines:
                line.accept(self)

    def visit_TextSegment(self, segm: TextSegment):
            if self.debug:
                print(".text")

            self.segm = 'text'
            for line in segm.lines:
                line.accept(self)

    def visit_Decl(self, line: Decl):
        b = line.to_bytes()
        
        if self.debug:
            self.ctx.ram.write_bytes(b, comment=line)
            print(b.hex(), line)
        else:
            self.ctx.ram.write_bytes(b)

    def visit_Label(self, lbl: Label):
        if self.debug:
            print(lbl)

            if self.segm == 'data':
                self.ctx.ram.write_comment(lbl)
            else:
                self.ctx.rom.write_comment(lbl)

    def visit_MemLabel(self, lbl: MemLabel):
        if self.debug:
            print(lbl)

        if self.segm == 'data':
            self.ctx.ram.set_addr(lbl.addr)
        else:
            self.ctx.rom.set_addr(lbl.addr)

    def visit_Instruction(self, instr: Instruction):
        b = instr.to_bytes(self.ctx)

        if self.debug:
            print(b.hex(), instr)
            self.ctx.rom.write_bytes(b, comment=instr)
        else:
            self.ctx.rom.write_bytes(b)

class Assembler:
    def __init__(self, outram, outrom, debug=False):
        self._debug = debug
        self._rom = MemoryFile(outrom, cell_size=4)
        self._ram = MemoryFile(outram, align=4)

    def assemble(self, lines):
        ctx = Context(self._ram, self._rom, debug=self._debug)
        segments = parse(lines)

        # first pass
        first_pass = FirstPass(ctx)

        for segm in segments:
            segm.accept(first_pass)

        if self._debug:
            print("First pass complete!")
            print("=" * 20)
            print("Labels:")
            print("-" * 20)
            for lbl, val in ctx._labels.items():
                print(f"{val.to_bytes(4, 'big').hex()}: {lbl}")

            print("=" * 20)
                    

        # second pass
        second_pass = SecondPass(ctx, self._debug)

        for segm in segments:
            segm.accept(second_pass)


        if self._debug:
            print("=" * 20)
            print("Second pass complete!")

    def finalize(self):
        self._rom.close()
        self._ram.close()