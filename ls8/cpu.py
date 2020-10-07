"""CPU functionality."""

import sys

# Instruction Constants
HLT  = 0b00000001    # Halt
LDI  = 0b10000010
PRN  = 0b01000111    # Print
MUL  = 0b10100010    # Multiply
ADD  = 0b10100000    # Addition
SUB  = 0b10100001    # Subtraction
DIV  = 0b10100011    # Division
MOD  = 0b10100100    # Modupasslous
PUSH = 0b01000101
POP  = 0b01000110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg =[0] * 8
        self.reg[7] = 0xF4
        self.halted = False
        # set up the branchtable
        self.branchtable = {}
        self.branchtable[HLT]  = self.handle_HLT
        self.branchtable[LDI]  = self.handle_LDI
        self.branchtable[PRN]  = self.handle_PRN
        self.branchtable[MUL]  = self.handle_MUL
        self.branchtable[ADD]  = self.handle_ADD
        self.branchtable[SUB]  = self.handle_SUB
        self.branchtable[DIV]  = self.handle_DIV
        self.branchtable[MOD]  = self.handle_MOD
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP]  = self.handle_POP

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

    ######Function Handling######

    def handle_HLT(self, a, b):
        self.halted = True

    def handle_LDI(self, a, b):
        self.reg[a] = b

    def handle_PRN(self, a, b):
        print(self.reg[a])

    def handle_MUL(self, a, b):
        self.reg[a] = self.reg[a] * self.reg[b]

    def handle_ADD(self, a, b):
        self.reg[a] = self.reg[a] + self.reg[b]

    def handle_SUB(self, a, b):
        self.reg[a] = self.reg[a] - self.reg[b]

    def handle_DIV(self, a, b):
        if self.reg[b] == 0:
            print("ERROR: Cannot devide by zero.")
        else:
            self.reg[a] = self.reg[a] / self.reg[b]

    def handle_MOD(self, a, b):
        if self.reg[b] == 0:
            print("ERROR: Cannot devide by zero.")
        else:
            self.reg[a] = self.reg[a] % self.reg[b]

    def handle_PUSH(self, a, b):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[a]

    def handle_POP(self, a, b):
        self.reg[a] = self.ram[self.reg[7]]
        self.reg[7] += 1

    #############################

    def run(self):
        """Run the CPU."""
        while not self.halted:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            # Call the branchtable
            try:
                self.branchtable[ir](operand_a, operand_b)
            except:
                print("ERROR: Unknown command.")
                sys.exit(1)

            # Use bit shifting to advance the pc
            advance = ir >> 6
            self.pc += advance + 1