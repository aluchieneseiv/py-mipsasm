# py-mipsasm
A mips assembler... in python?

## What's implemented
All non-fp instructions from [here](http://www-inst.eecs.berkeley.edu/~cs61c/resources/MIPS_Green_Sheet.pdf) (~~currently not all are tested~~base instructions have been tested, but no pseudoinstructions), labels, hex constants and the possibility to specify assembled code's place in memory.

The assembler creates two files:
- `rom.mem`
- `ram.mem`

Both files are in Verilog's format for `$readmemh`.

Keep in mind that the rom is made with 32-bit words in mind so 0x400000 bytes is actually 0x100000 in words.
The ram is made with 8-bit words.

## Requirements
- `python3 -m pip install lark-parser construct`

## Running it
I recommend having an alias for this so you can run it from anywhere
- `python3 mipsasm.py --help`
