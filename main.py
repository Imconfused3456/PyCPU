from tabulate import tabulate
import time
import os
import keyboard
import sys


class CPU:
    def __init__(self, driveout):
        self.clock = 0
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        with open('comp.pyasm', 'r') as file:
            content = file.read()
        self.stack = content.split("\n")
        self.ram = {i: [0] * 64 for i in range(1, 65)}
        self.screen = {i: [0] * 32 for i in range(1, 33)}
        self.driveout = driveout

    class I_O:
        def __init__(self, cpu):
            self.ports = {1: "KEYBOARD", 2: "DRIVE"}
            self.cpu = cpu

        def load_from_port(self, port, identifier, identifier2):
            if port == 2:
                with open(cpu.driveout, 'r') as drive:
                    drivecontents = drive.read()
                drivecontents = drivecontents.strip("=").split("=\n")
                #print(drivecontents)
                for file in drivecontents:
                    file = file.split(">")
                    #print(file)
                    name = file[0]
                    type = file[1]
                    content = file[2]
                    if name == identifier and type == identifier2:
                        #print("Located file:", identifier, "with type:", type, "and content:", content)
                        row = 1
                        i = 1
                        for data in content:
                            print(data, i, sep=" ")
                            if i > 32:
                                row += 1
                                i = 1
                            char_encoded = "9999999" + data
                            self.cpu.stack.append(f"SET 1 {data}")
                            self.cpu.stack.append(f"SCRNSAVE {row} {i} 1")
                            #print(self.cpu.stack)
                            i += 1
                        self.cpu.stack.append("SCRNSHOW")

    class ALU:
        def __init__(self, cpu):
            self.cpu = cpu

        def get_reg_as_rom(self):
            self.r = self.cpu.registers

        def add(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            add = int(self.r[reg_a - 1]) + int(self.r[reg_b - 1])
            self.cpu.registers[reg_c - 1] = add

        def sub(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            sub = int(self.r[reg_a - 1]) - int(self.r[reg_b - 1])
            self.cpu.registers[reg_c - 1] = sub

        def mul(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            mul = int(self.r[reg_a - 1]) * int(self.r[reg_b - 1])
            self.cpu.registers[reg_c - 1] = mul

        def div(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            div = int(self.r[reg_a - 1]) / int(self.r[reg_b - 1])
            self.cpu.registers[reg_c - 1] = div

        def mod(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            mod = int(self.r[reg_a - 1]) % int(self.r[reg_b - 1])
            self.cpu.registers[reg_c - 1] = mod

        def and_(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            and_ = int(self.r[reg_a - 1]) & int(self.r[reg_b - 1])

            self.cpu.registers[reg_c - 1] = and_

        def or_(self, reg_a, reg_b, reg_c):
            self.get_reg_as_rom()
            or_ = int(self.r[reg_a - 1]) | int(self.r[reg_b - 1])

            self.cpu.registers[reg_c - 1] = or_

        def not_(self, reg_a, reg_c):
            self.get_reg_as_rom()
            not_ = ~int(self.r[reg_a - 1])
            self.cpu.registers[reg_c - 1] = not_

    class Multiplexer:

        def __init__(self, cpu):
            self.cpu = cpu

        def get_ram_as_rom(self):
            self.r = self.cpu.ram

        def load(self, y, x, reg_c):
            self.cpu.registers[reg_c - 1] = self.cpu.ram[y][x - 1]

        def save(self, reg_c, y, x):
            self.cpu.ram[y][x - 1] = self.cpu.registers[reg_c - 1]

        def del_(self, y, x):
            self.cpu.ram[y][x - 1] = 0

    class Graphics:

        def __init__(self, cpu):
            self.cpu = cpu

            self.black = '\033[30m'
            self.red = '\033[31m'
            self.green = '\033[32m'
            self.orange = '\033[33m'
            self.blue = '\033[34m'
            self.purple = '\033[35m'
            self.cyan = '\033[36m'
            self.lightgrey = '\033[37m'
            self.darkgrey = '\033[90m'
            self.lightred = '\033[91m'
            self.ghtgreen = '\033[92m'
            self.yellow = '\033[93m'
            self.lightblue = '\033[94m'
            self.pink = '\033[95m'
            self.lightcyan = '\033[96m'
            self.end = '\033[0m'

        def load(self, y, x, reg_c):
            self.cpu.registers[reg_c - 1] = self.cpu.screen[y][x - 1]

        def save(self, reg_c, y, x):
            self.cpu.screen[y][x - 1] = self.cpu.registers[reg_c - 1]

        def del_(self, y, x):
            self.cpu.screen[y][x - 1] = 0

        def decode_to_char(self, num):
            number_to_symbol_mapping = {
                0: '0',
                1: '1',
                2: '2',
                3: '3',
                4: '4',
                5: '5',
                6: '6',
                7: '7',
                8: '8',
                9: '9',
                10: ' ',
                11: 'A',
                12: 'B',
                13: 'C',
                14: 'D',
                15: 'E',
                16: 'F',
                17: 'G',
                18: 'H',
                19: 'I',
                20: 'J',
                21: 'K',
                22: 'L',
                23: 'M',
                24: 'N',
                25: 'O',
                26: 'P',
                27: 'Q',
                28: 'R',
                29: 'S',
                30: 'T',
                31: 'U',
                32: 'V',
                33: 'W',
                34: 'X',
                35: 'Y',
                36: 'Z',
                37: '.',
                38: ',',
                39: '!',
                40: '?'
            }
            return number_to_symbol_mapping[num]

        def display(self):
            screen = []
            for i in range(1, 33):
                screenrow = []
                for j in range(32):
                    value = self.cpu.screen[i][j]
                    if self.cpu.screen[i][j] == 1:
                        screenrow.append("\u25A6")
                    elif value == 2:
                        screenrow.append(self.red + "\u25A6" + self.end)
                    elif value == 3:
                        screenrow.append(self.orange + "\u25A6" + self.end)
                    elif value == 4:
                        screenrow.append(self.yellow + "\u25A6" + self.end)
                    elif value == 5:
                        screenrow.append(self.green + "\u25A6" + self.end)
                    elif value == 6:
                        screenrow.append(self.blue + "\u25A6" + self.end)
                    elif value == 7:
                        screenrow.append(self.purple + "\u25A6" + self.end)
                    elif self.cpu.screen[i][j] >= 9999999:
                        screenrow.append(
                            self.decode_to_char(self.cpu.screen[i][j] %
                                                9999999))
                    else:
                        screenrow.append(" ")
                screen.append(screenrow)
            os.system('cls' if os.name == 'nt' else 'clear')
            border = "-" * 32
            print(border)
            print(tabulate(screen, tablefmt="plain"))
            print(border)

    def fetcher(self):
        commands_to_remove = []
        for command in self.stack:
            cmd = command.split(" ")

            if command.startswith("ADD"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.add(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)
            elif command.startswith("SUB"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.sub(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)
            elif command.startswith("REM"):
                reg_a = int(cmd[1].strip())
                self.registers[reg_a - 1] = 0
                commands_to_remove.append(command)

            elif command.startswith("MOV"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                self.registers[reg_b - 1] = self.registers[reg_a - 1]
                self.registers[reg_a - 1] = 0
                commands_to_remove.append(command)

            elif command.startswith("MUL"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.mul(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)

            elif command.startswith("DIV"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.div(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)

            elif command.startswith("MOD"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.mod(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)

            elif command.startswith("AND"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.and_(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)

            elif command.startswith("OR"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.alu.or_(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)
            elif command.startswith("NOT"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())

                self.alu.not_(reg_a, reg_b)
            elif command.startswith("LOAD"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.multiplexer.load(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)

            elif command.startswith("SAVE"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())
                self.multiplexer.save(reg_c, reg_a, reg_b)

                commands_to_remove.append(command)

            elif command.startswith("DEL"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())

                self.multiplexer.del_(reg_a, reg_b)

                commands_to_remove.append(command)

            elif command.startswith("SCRNLOAD"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())

                self.graphics.load(reg_a, reg_b, reg_c)
                commands_to_remove.append(command)

            elif command.startswith("SCRNSAVE"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                reg_c = int(cmd[3].strip())
                self.graphics.save(reg_c, reg_a, reg_b)

                commands_to_remove.append(command)

            elif command.startswith("SCRNDEL"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())

                self.graphics.del_(reg_a, reg_b)

                commands_to_remove.append(command)

            elif command.startswith("SCRNSHOW"):

                self.graphics.display()

                commands_to_remove.append(command)
            elif command.startswith("SCRNCLR"):
                for i in range(1, 33):
                    for j in range(16):
                        if self.screen[i][j]:
                            self.screen[i][j] = 0
                commands_to_remove.append(command)
            elif command.startswith("SET"):
                reg_a = int(cmd[1].strip())
                reg_b = int(cmd[2].strip())
                self.registers[reg_a - 1] = reg_b

                commands_to_remove.append(command)
            elif command.startswith("WAIT"):
                reg_a = float(cmd[1].strip())
                time.sleep(reg_a)

                commands_to_remove.append(command)
            elif command.startswith("INC"):
                file_path = cmd[1].strip()

                with open(file_path, 'r') as file:
                    content = file.read()
                content = content.split("\n")

                index_of_inc = self.stack.index(command)

                for line in content:
                    self.stack.insert(index_of_inc + 1, line)

                self.stack.insert(index_of_inc + len(content) + 1, "SCRNSHOW")

                commands_to_remove.append(command)
            elif command.startswith("HLT"):
                sys.exit()

            else:
                commands_to_remove.append(command)
        for command in commands_to_remove:
            self.stack.remove(command)

    def clock_up(self):
        if self.clock == 0:
            self.clock = 1
            self.fetcher()
            #print(self.stack)
        else:
            self.clock = 0


cpu = CPU("c.drive")
cpu.alu = cpu.ALU(cpu)
cpu.multiplexer = cpu.Multiplexer(cpu)
cpu.graphics = cpu.Graphics(cpu)
cpu.i_o = cpu.I_O(cpu)
while cpu.stack != []:
    cpu.clock_up()
    #userinput = input("-")
    #cpu.stack.insert(0, userinput)
    #print(cpu.stack)
    #cpu.clock_up()
