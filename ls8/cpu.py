"""CPU functionality."""

import sys

# Instruction Constants
LDI  = 0b10000010
PRN  = 0b01000111    # Print
HLT  = 0b00000001    # Halt
MUL  = 0b10100010    # Multiply
ADD  = 0b10100000    # Addition
PUSH = 0b01000101   # Push in stack
POP  = 0b01000110    # Pop from stack
CALL = 0b01010000
RET  = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg =[0] * 8
        self.reg[7] = 0xF4
        self.halted = False

    def ram_read(self, mar):
        try:
            mdr = self.ram[mar]
        except:
            mdr = None
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []

        # make sure the correct number of args are passed in
        if len(sys.argv) != 2:
            print('Wrong number of arguments.')
            sys.exit(1)

        # get only the binary numbers
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    # split on the comment to make numbers accecible
                    comment_split = line.split("#")
                    num = comment_split[0]
                    try:
                        # add the number as a binary to the program
                        x = int(num,2)
                        program.append(x)
                    except:
                        continue
        # error handling if wrong file name
        except:
            print("File not found!")
            sys.exit(1)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if ir == HLT:
                self.halted = True
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == MUL:
                product = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = product
                self.pc += 3
            else:
                print("ERROR: Unknown command.")
                sys.exit(1)
        return