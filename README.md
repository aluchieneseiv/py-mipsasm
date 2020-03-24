# py-mipsasm
A mips assembler... in python?

## What's implemented
All non-fp instructions from [here](http://www-inst.eecs.berkeley.edu/~cs61c/resources/MIPS_Green_Sheet.pdf) (currently not all are tested), labels, hex constants and the possibility to specify assembled code's place in memory.

The assembler creates two files:
- `rom.mem`
- `ram.mem`
Both files are in Verilog's format for `$readmemh`.

## Requirements
- `python3 -m pip install lark-parser construct`

## Running it
I recommend having an alias for this so you can run it from anywhere
- `python3 mipsasm.py --help`
