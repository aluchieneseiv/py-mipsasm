import io
from .parser import parse
from .parsetypes import *
from .instructions import Instruction

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
            raise Exception("Bytes not aligned with cell size!")

        align = self.align or 1

        cells = [bytes[i:i+self.cell_size] for i in range(0, len(bytes), self.cell_size)]
        aligned = [cells[i:i+align] for i in range(0, len(cells), align)]

        for i in range(len(aligned) - 1):
            for cell in aligned[i]:
                self._write_cell(cell)
                self.file.write(" ")

            self.file.write("\n")
        
        for cell in aligned[-1]:
            self._write_cell(cell)
            self.file.write(" ")

        if comment is not None:
            self.file.write(f"// {comment}")
        
        self.file.write('\n')

    def write_comment(self, comment):
        self.file.write(f"// {comment}\n")

    def set_addr(self, addr):
        self.file.write(f"\n@{addr:X}\n")
        self.addr = addr

    def close(self):
        self.file.close()

class Context:
    def __init__(self, ram, rom, debug=False):
        self._labels = dict()
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
        return self.get_label(label) - self.rom.addr + 1

    def absolute_jmp(self, label):
        new_pc = self.get_label(label)

        if self.rom.addr >> 30 == new_pc >> 30:
            return ~((-1) << 30) & new_pc
        
        raise Exception(f"Jump to label {label} is too far")

class Assembler:
    def __init__(self, outram, outrom, debug=False):
        self._debug = debug
        self._rom = MemoryFile(outrom, cell_size=4)
        self._ram = MemoryFile(outram, align=4)

    def assemble(self, lines):
        ctx = Context(self._ram, self._rom, debug=self._debug)
        segments = parse(lines)

        # first pass

        for segm in segments:
            if isinstance(segm, DataSegment):
                data_addr = self._ram.addr

                for line in segm.lines:
                    if isinstance(line, Decl):
                        data_addr = data_addr + len(line)
                    elif isinstance(line, Label):
                        ctx.set_label(line.name, data_addr)
                    elif isinstance(line, MemLabel):
                        data_addr = line.addr
                
            elif isinstance(segm, TextSegment):
                text_addr = self._rom.addr

                for line in segm.lines:
                    if isinstance(line, Instruction):
                        text_addr = text_addr + len(line)
                    elif isinstance(line, Label):
                        ctx.set_label(line.name, text_addr)
                    elif isinstance(line, MemLabel):
                        text_addr = line.addr

        if self._debug:
            print("First pass complete!")
            print("=" * 20)
            print("Labels:")
            print("-" * 20)
            for lbl, val in ctx._labels.items():
                print(f"{val.to_bytes(4, 'big').hex()}: {lbl}")

            print("=" * 20)
                    

        # second pass

        for segm in segments:
            if isinstance(segm, DataSegment):
                
                if self._debug:
                    print(".data")

                for line in segm.lines:
                    if isinstance(line, Decl):
                        b = line.to_bytes()
                        
                        if self._debug:
                            self._ram.write_bytes(b, comment=line)
                            print(b.hex(), line)
                        else:
                            self._ram.write_bytes(b)

                    elif isinstance(line, MemLabel):
                        self._ram.set_addr(line.addr)

                        if self._debug:
                            print(line)

                    elif self._debug:
                        print(line)
                        self._ram.write_comment(line)

            if isinstance(segm, TextSegment):

                if self._debug:
                    print(".text")

                for line in segm.lines:
                    if isinstance(line, Instruction):
                        b = line.to_bytes(ctx)

                        if self._debug:
                            print(b.hex(), line)
                            self._rom.write_bytes(b, comment=line)
                        else:
                            self._rom.write_bytes(b)
                    
                    elif isinstance(line, MemLabel):
                        self._rom.set_addr(line.addr)

                        if self._debug:
                            print(line)

                    elif self._debug:
                        print(line)
                        self._rom.write_comment(line)


        if self._debug:
            print("=" * 20)
            print("Second pass complete!")

    def finalize(self):
        self._rom.close()
        self._ram.close()