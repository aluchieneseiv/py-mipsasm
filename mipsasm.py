import argparse
from mips import Assembler
import traceback
import io

parser = argparse.ArgumentParser(description="Compile mips code")

parser.add_argument('-ram', default='ram.mem', help="output ram file (default: ram.mem)")
parser.add_argument('-rom', default='rom.mem', help="output rom file (default: rom.mem)")
parser.add_argument('-debug', action='store_const', dest='debug', const=True, default=False, help="enable debug prints")
parser.add_argument('input', help="input assembly file")

args = parser.parse_args()

print(f"Assembling file {args.input} to '{args.ram}' and '{args.rom}'")
try:
    asm = Assembler(args.ram, args.rom, debug=args.debug)

    with io.open(args.input, "r") as f:
        asm.assemble(f.read())

    asm.finalize()
    print("Done!")
except Exception as ex:
    print(ex)

    if args.debug:
        traceback.print_exc()