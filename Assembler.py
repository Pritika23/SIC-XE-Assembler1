#import sys
#inputFile = sys.argv[1]
OPTAB = {"ADD": "18", "ADDR": "58", "CLEAR": "B4", "COMP": "28", "COMPR": "A0", "J": "3C", "JEQ": "30", "JLT": "38", "JSUB": "48", "LDA": "00", "LDB": "68",
         "LDCH": "50", "LDT": "74", "LDX": "04", "RD": "D8", "RSUB": "4C", "STA": "0C", "STCH": "54", "STL": "14", "STX": "10", "TD": "E0", "TIX": "2C", "TIXR": "B8", "WD": "DC"}
LOCCTR = '000000'
BASE = ''
ADCT = 0
FORMAT2 = ["ADDR", "CLEAR", "COMPR", "TIXR"]
KEYWORDS = ["BYTE", "RESW", "RESB", "WORD"]
REGISTERS = {"A": "0", "X": "1", "L": "2", "B": "3",
             "S": "4", "T": "5", "F": "6", "PC": "7", "SW": "8"}
#f1 = open(inputFile, "r")
f1 = open("input1.txt", "r")
f2 = open("Intermediate.txt", "w+")
SYMTAB = {}
l1 = f1.readline()
l2 = l1.split()
PROGNAME = l2[0].ljust(6)  # ljust is used to fill out spaces -> left justified
f2.write(LOCCTR + "    ")
f2.write(l1)
# PASS 1
for line in f1:
    temp = line.split()
    # SYMTAB POPULATION
    if len(temp) == 3:
        if temp[0] in SYMTAB:
            print(temp[0])
            print("Error! Symbol is already defined")
        else:
            SYMTAB[temp[0]] = str(LOCCTR)
    # writing to intermediate file
    if '.' in temp or 'BASE' in temp:
        f2.write('          '+line)
    else:
        f2.write(LOCCTR+"    ")
        f2.write(line)
    if len(temp) > 1 and temp[-2] == "START":
        SYMTAB[temp[0]] = LOCCTR
        LOCCTR = LOCCTR.zfill(6)
    if len(temp) == 3 or len(temp) == 2 and temp[-2] != 'BASE':
        # format 3
        if temp[-2] not in FORMAT2 and '+' not in temp[-2] and temp[-2] not in KEYWORDS:
            ADCT += 3
            s = hex(ADCT)
            LOCCTR = s.replace('0x', '')
            LOCCTR = LOCCTR.upper()
            LOCCTR = LOCCTR.zfill(6)
        # format 4
        elif temp[-2] not in FORMAT2 and '+' in temp[-2] and temp[-2] not in KEYWORDS:
            ADCT += 4
            s = hex(ADCT)
            LOCCTR = s.replace('0x', '')
            LOCCTR = LOCCTR.upper()
            LOCCTR = LOCCTR.zfill(6)
        # format 2
        elif temp[-2] in FORMAT2:
            ADCT += 2
            s = hex(ADCT)
            LOCCTR = s.replace('0x', '')
            LOCCTR = LOCCTR.upper()
            LOCCTR = LOCCTR.zfill(6)
        # declarations
        elif temp[-2] in KEYWORDS:
            if temp[-2] == "BYTE":
                if temp[-1][0] == 'X':
                    ADCT += 1
                elif temp[-1][0] == 'C':
                    ADCT += (len(temp[-1])-3)
                s = hex(ADCT)
                LOCCTR = s.replace('0x', '')
                LOCCTR = LOCCTR.upper()
                LOCCTR = LOCCTR.zfill(6)
            elif temp[-2] == "RESW":
                ADCT += (3*int(temp[2]))
                s = hex(ADCT)
                LOCCTR = s.replace('0x', '')
                LOCCTR = LOCCTR.upper()
                LOCCTR = LOCCTR.zfill(6)
            elif temp[-2] == "WORD":
                ADCT += 3
                s = hex(ADCT)
                LOCCTR = s.replace('0x', '')
                LOCCTR = LOCCTR.upper()
                LOCCTR = LOCCTR.zfill(6)
            elif temp[-2] == "RESB":
                ADCT += int(temp[-1])
                s = hex(ADCT)
                LOCCTR = s.replace('0x', '')
                LOCCTR = LOCCTR.upper()
                LOCCTR = LOCCTR.zfill(6)
    # handling RSUB
    if "RSUB" in temp:
        ADCT += 3
        s = hex(ADCT)
        LOCCTR = s.replace('0x', '')
        LOCCTR = LOCCTR.upper()
        LOCCTR = LOCCTR.zfill(6)
    # checking for symbol defining statements
    if len(temp) == 3 and "EQU" in temp[-2]:  # create symdef
        SYMTAB[temp[0]] = int(temp[-1])
    if len(temp) > 1 and temp[-2] == "END":
        ADCT -= 3
        s = hex(ADCT)
        LOCCTR = s.replace('0x', '')
        LOCCTR = LOCCTR.upper()
        LOCCTR = LOCCTR.zfill(6)
f1.close()
f2.close()
print("Intermediate file generated as - Intermediate.txt")
# PASS 2


def tohex(val, nbits):  # for converting negative hex numbers in FF.. format
    return hex((val + (1 << nbits)) % (1 << nbits))


def calc_disp(TA, PC, BASE):
    if TA-PC >= -2048 and TA-PC <= 2047:
        return TA-PC
    return TA-BASE


def generate_obj_code(OPCODE, str, last_dig):
    i2 = int(OPCODE[1], 16)
    b1 = bin(i2)
    b1 = b1[:-2]+str
    b1 = b1.replace('0b', '')
    i2 = int(b1, 2)
    h1 = hex(i2)
    h1 = h1.replace('0x', '')
    return OPCODE[0] + h1.upper() + last_dig


f3 = open("Intermediate.txt", "r")
f4 = open("Object_Program.txt", "w+")
temp1 = f3.readlines()
l = len(temp1)
OBJ_CODES = {}  # dict to store instructions and their corresponding object codes
for i in range(l-1):
    line = temp1[i]
    temp = line.split()
    # comments
    if temp[0] == '.':
        continue
    # BASE directive
    if len(temp) > 1 and temp[-2] == 'BASE':
        BASE = int(SYMTAB[temp[-1]], 16)
    elif temp1[i+1][0] != 'BASE' and len(temp) > 1 and temp[-2] != "END" and temp1[i+1][0] != '.':
        line1 = temp1[i+1]
        l1 = line1.split()
        if l1[0] != 'BASE' and l1[0] != '.':
            PC = int(l1[0], 16)
        elif l1[0] == 'BASE':
            line2 = temp1[i+2]
            l4 = line2.split()
            PC = int(l4[0], 16)
        # header
        if len(temp) > 1 and temp[-2] == "START":
            f4.write("H^"+PROGNAME+"^"+"000000^"+LOCCTR)
        # text records
        # Format 4 instructions without immediate addressing
        elif len(temp) > 1 and temp[-2].replace('+', '') in OPTAB and '+' in temp[-2] and '#' not in temp[-1]:
            t = temp[-2].replace('+', '')
            OPCODE = OPTAB[t.replace('\n', '')]
            obj_code = generate_obj_code(OPCODE, '11', '1')
            TA = SYMTAB[temp[-1]]
            obj_code += TA[-5]+TA[-4]+TA[-3]+TA[-2]+TA[-1]
            OBJ_CODES[line] = obj_code
        # normal format 3 instructions AND indirect: not F4, not F2, not indexed, not a declaration, not immediate, not indirect
        elif len(temp) > 1 and temp[-2] in OPTAB and '+' not in temp[-2] and temp[-2] not in FORMAT2 and ',X' not in temp[-1] and temp[-2] not in KEYWORDS and '#' not in temp[-1] and '@' not in temp[-1]:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            TA = int(SYMTAB[temp[-1]], 16)
            if TA-PC >= -2048 and TA-PC <= 2047:
                obj_code = generate_obj_code(OPCODE, '11', '2')
            else:
                obj_code = generate_obj_code(OPCODE, '11', '4')
            disp = calc_disp(TA, PC, BASE)
            disps = tohex(disp, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            OBJ_CODES[line] = obj_code
        # indirect addressing in F3
        elif '@' in temp[-1] and temp[-2] in OPTAB and '+' not in temp[-2] and temp[-2] not in FORMAT2 and ',X' not in temp[-1] and temp[-2] not in KEYWORDS and '#' not in temp[-1]:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            obj_code = generate_obj_code(OPCODE, '10', '2')
            o = temp[-1].replace('@', '')
            TA = int(SYMTAB[o], 16)
            disp = calc_disp(TA, PC, BASE)
            disps = tohex(disp, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            OBJ_CODES[line] = obj_code
        # immediate addressing in F3
        elif '#' in temp[-1] and '+' not in temp[-2] and temp[-2] not in FORMAT2 and ',X' not in temp[-1] and temp[-2] not in KEYWORDS and '@' not in temp[-1]:
            o = temp[-1].replace('#', '')
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            if o in SYMTAB:  # for #LENGTH
                TA = int(SYMTAB[o], 16)
                if TA-PC >= -2048 and TA-PC <= 2047:
                    obj_code = generate_obj_code(OPCODE, '01', '2')
                else:
                    obj_code = generate_obj_code(OPCODE, '11', '4')
                disp = calc_disp(TA, PC, BASE)
                disps = tohex(disp, 12)
            else:
                obj_code = generate_obj_code(OPCODE, '01', '0')
                val = int(temp[-1].replace('#', ''))
                disps = tohex(val, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            OBJ_CODES[line] = obj_code
        # indexed addressing
        elif ',X' in temp[-1]:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            TA = int(SYMTAB[(temp[-1])[:-2]], 16)
            if TA-PC >= -2048 and TA-PC <= 2047:
                obj_code = generate_obj_code(OPCODE, '11', 'A')
            else:
                obj_code = generate_obj_code(OPCODE, '11', 'C')
            disp = calc_disp(TA, PC, BASE)
            disps = tohex(disp, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            OBJ_CODES[line] = obj_code
        # format 2
        elif temp[-2] in FORMAT2:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            if ',' in temp[-1]:
                r1 = REGISTERS[temp[-1][0]]
                r2 = REGISTERS[temp[-1][2]]
                obj_code = OPCODE+r1+r2
            else:
                r = REGISTERS[temp[-1]]
                obj_code = OPCODE+r+'0'
            OBJ_CODES[line] = obj_code
        # format 4 with immediate addressing
        elif '#' in temp[-1] and '+' in temp[-2]:
            o = temp[-1].replace('#', '')
            OPCODE = OPTAB[(temp[-2].replace('\n', '')).replace('+', '')]
            obj_code = generate_obj_code(OPCODE, '01', '1')
            if o in SYMTAB:  # for #VAL
                TA = hex(int(str(SYMTAB[o]), 16)).replace(
                    '0x', '').upper().zfill(5)
            elif o not in SYMTAB:
                TA = ((hex(int(o)).replace('0x', '')).upper()).zfill(5)
            obj_code += TA
            OBJ_CODES[line] = obj_code
        # handling RSUB
        elif temp[-1] == 'RSUB':
            obj_code = '4F0000'
            OBJ_CODES[line] = obj_code
        # for BYTE declaration
        elif temp[-2] == 'BYTE':
            obj_code = ""
            if temp[-1][0] == 'C':
                for i in range(2, len(temp[-1])-1):
                    obj_code += ((hex(ord(temp[-1][i])
                                      ).replace('0x', '')).upper())
            elif temp[-1][0] == 'X':
                obj_code += temp[-1][2:len(temp[-1])-1]
            OBJ_CODES[line] = obj_code
        # for WORD declaration
        elif temp[-2] == 'WORD':
            obj_code = temp[-1].zfill(6)
            OBJ_CODES[line] = obj_code
        else:  # case for RESW, RESB
            OBJ_CODES[line] = temp[-2]

# generating text records
t_counter = 0
tr = "\nT^"+'000000'
for i in OBJ_CODES:
    line = i.split()
    if line[-2] != "EQU" and line[-2] != "RESW" and line[-2] != "RESB" and line[1] != "." and line[-2] != "BASE":
        loc = line[0]
        if len(OBJ_CODES[i]) == 4:
            t_counter += 2
        elif len(OBJ_CODES[i]) == 6:
            t_counter += 3
        elif len(OBJ_CODES[i]) == 8:
            t_counter += 4
        elif 'BYTE' in line and line[-1][0] == 'X':
            t_counter += 1
        else:
            t_counter += len(OBJ_CODES[i])
    # case for declarations
    elif line[-2] == "EQU" or line[-2] == "RESW" or line[-2] == "RESB":
        f4.write('')
        t_counter = t_counter+30
        continue
    if t_counter <= 30 and line[1] != "." and line[-2] != "EQU" and line[-2] != "RESW" and line[-2] != "RESB" and line[-2] != "BASE":
        tr += "^"+OBJ_CODES[i]
        size = hex(t_counter).replace('0x', '').upper()
    elif t_counter > 30 or line[-2] == "END":
        loc = line[0]
        tr = tr[0:9]+"^"+size.zfill(2)+tr[9:]
        f4.write(tr)
        tr = '\nT^'+loc+"^"+OBJ_CODES[i]
        t_counter = int(len(OBJ_CODES[i])/2)
loc = line[0]
tr = tr[0:9]+"^"+size.zfill(2)+tr[9:]
f4.write(tr)

# generating modification records
for i in OBJ_CODES:
    line = i.split()
    if line[-2][0] == '+' and '#' not in line[-1]:
        loc = hex(int(line[0], 16)+1).replace('0x', '').zfill(6).upper()
        f4.write("\nM^"+loc+"^05")

# end record
f4.write("\nE^000000")
f3.close()
f4.close()
print("Object program generated as - Object_Program.txt")
