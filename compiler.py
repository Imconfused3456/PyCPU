with open('prog.pybas', 'r') as file:
  content = file.read()

#code = content.split('\n')
class Parser:
    def __init__(self, output, code, allocated):
        self.code = code
        self.code = code.split('\n')
        self.allocated_ram = [allocated]
        self.output = output
        self.variables = {}
        self.most_recent_if_eval = False
        self.in_if_statement = False
  
    def parse(self):
        out_line = 1
        skip_block = False
        self.in_loop = False
        self.parsing_content_of_loop = False
        print(self.code)
        for line_num, line in enumerate(self.code):
            line = line.strip()
            #print(self.variables)
            #print(self.in_if_statement)
            #print(self.most_recent_if_eval)
            if skip_block:
                #print("Skipped code because IF evaluated to false.")
                if line == "ENDIF":
                    skip_block = False
                    #print("Ending IF block.")
                continue  # Skip to next line
            if self.in_loop and line.startswith("NEXT $"):
                    self.parsing_content_of_loop = True
            if line.startswith("VAR $"):
                line_var_parsed = line
                for variable in self.variables:
                    line_var_parsed = line_var_parsed.replace(variable, str(self.variables[variable]))
                decode_args = line_var_parsed.split(' ')
                key = decode_args[1]
                value = eval(decode_args[3])
                print("Found variable declaration:", key, value, sep=" ")
                self.variables[key] = value
            else:
                line_var_parsed = line
                for variable in self.variables:
                    line_var_parsed = line_var_parsed.replace(variable, str(self.variables[variable]))
                decode_args = line_var_parsed.split(' ', 1)
                if line_var_parsed.startswith("PRINT "):
                    #self.output.write(decode_args[1].strip("\""), 1, out_line)
                    print(eval(decode_args[1]))
                    self.output.write(eval(decode_args[1]), 1, out_line)
                    out_line += 1
                elif line_var_parsed.startswith("IF "):
                    comparison = decode_args[1].replace("=", "==")
                    eval_comparison = eval(comparison)
                    #print(eval_comparison)
                    if eval_comparison:
                        skip_block = False
                        #print("IF statement is true")
                        self.most_recent_if_eval = True
                    else:
                        skip_block = True
                        #print("IF statement is false")
                        self.most_recent_if_eval = False
                elif line_var_parsed.startswith("FOR "):
                    decode_args = line_var_parsed.split(' ')
                    var_init = decode_args[1]
                    var_init = var_init.split('=')
                    var_name = var_init[0]
                    var_value = var_init[1]
                    to = decode_args[2]
                    step = decode_args[3]
                    print("For loop created with variable", var_name, "initialized at", var_value, "going to", to, "stepping", step, sep=" ")
                    self.in_loop = True
                    self.parsing_content_of_loop = True
class Output:
    def __init__(self):
        self.char_encoding = {
            0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
            10: ' ', 11: 'A', 12: 'B', 13: 'C', 14: 'D', 15: 'E', 16: 'F', 17: 'G', 18: 'H', 
            19: 'I', 20: 'J', 21: 'K', 22: 'L', 23: 'M', 24: 'N', 25: 'O', 26: 'P', 27: 'Q', 
            28: 'R', 29: 'S', 30: 'T', 31: 'U', 32: 'V', 33: 'W', 34: 'X', 35: 'Y', 36: 'Z', 
            37: '.', 38: ',', 39: '!', 40: '?'
        }
        self.commands = []
    def write(self, text, reg_a, y):
        i = 0
        for char in str(text):
          if i+1 > 32:
            i = 0
            y += 1
          i+=1
          chr = char.capitalize()
          char_encoded = "9999999" + str(list(self.char_encoding.keys())[list(self.char_encoding.values()).index(chr)])
          self.commands.append(f"SET {reg_a} {char_encoded}")
          self.commands.append(f"SCRNSAVE {y} {i} {reg_a}")
          #self.commands.append("SCRNSHOW")
        self.commands.append("SCRNSHOW")
    def hlin(self, y, reg_a, color):
        for x in range(1, 33):
            self.commands.append(f"SET {reg_a} {color}")
            self.commands.append(f"SCRNSAVE {y} {x} {reg_a}")
            #self.commands.append("SCRNSHOW")
    def vlin(self, x, reg_a, color):
        for y in range(1, 33):
            self.commands.append(f"SET {reg_a} {color}")
            self.commands.append(f"SCRNSAVE {y} {x} {reg_a}")
            #self.commands.append("SCRNSHOW")
    def show(self):
        self.commands.append("SCRNSHOW")
    
output = Output()
parser = Parser(output, content, 5)
parser.parse()
print(output.commands)
with open('comp.pyasm', 'w') as outfile:
  for line in output.commands:
    outfile.write(line + '\n')

print("Succesfully compiled")