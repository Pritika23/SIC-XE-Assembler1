OPTAB = {"ADD": "18", "ADDR": "58", "CLEAR": "B4", "COMP": "28", "COMPR": "A0", "J": "3C", "JEQ": "30", "JLT": "38", "JSUB": "48", "LDA": "00", "LDB": "68",
         "LDCH": "50", "LDT": "74", "RD": "D8", "RSUB": "4C", "STA": "0C", "STCH": "54", "STL": "14", "STX": "10", "TD": "E0", "TIXR": "B8", "WD": "DC"}
LOCCTR = '000000'
BASE = ''
ADCT = 0
FORMAT2 = ["ADDR", "CLEAR", "COMPR", "TIXR"]
KEYWORDS = ["BYTE", "RESW", "RESB", "WORD"]
REGISTERS = {"A": "0", "X": "1", "L": "2", "B": "3",
             "S": "4", "T": "5", "F": "6", "PC": "7", "SW": "8"}
f1 = open("Input.txt", "r")
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
    print(temp)
    print(LOCCTR)
    # SYMTAB POPULATION
    if len(temp) == 3:
        if temp[0] in SYMTAB:
            print(temp[0])
            print("Error! Symbol is already defined")
        else:
            SYMTAB[temp[0]] = str(LOCCTR)
    # writing to intermediate file
    f2.write(LOCCTR+"    ")
    f2.write(line)
    if len(temp) > 1 and temp[-2] == "START":
        SYMTAB[temp[0]] = LOCCTR
        LOCCTR = LOCCTR.zfill(6)
    if len(temp) == 3 or len(temp) == 2:
        # checking if its format 3
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
                ADCT += len(temp[2])-3
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
print(SYMTAB)
# PASS 2


def tohex(val, nbits):  # for converting negative hex numbers in FF.. format
    return hex((val + (1 << nbits)) % (1 << nbits))


def calc_disp(TA, PC):
    if TA-PC >= -2048 and TA-PC <= 2047:
        return TA-PC
    return TA-BASE


f3 = open("Intermediate.txt", "r")
f4 = open("Object_Program.txt", "w+")
temp1 = f3.readlines()
l = len(temp1)
for i in range(l):
    line = temp1[i]
    temp = line.split()
    # BASE directive
    if temp[-2] == 'BASE':
        BASE = int(SYMTAB[temp[-1]], 16)
    if temp[-2] != "END":
        line1 = temp1[i+1]
        l1 = line1.split()
        PC = int(l1[0], 16)
        # header
        if temp[-2] == "START":
            f4.write("H^"+PROGNAME+"^"+"000000^"+LOCCTR)
        # text records
        # Format 4 instructions without immediate addressing
        elif temp[-2].replace('+', '') in OPTAB and '+' in temp[-2] and '#' not in temp[-1]:
            t = temp[-2].replace('+', '')
            OPCODE = OPTAB[t.replace('\n', '')]
            i2 = int(OPCODE[1], 16)
            b1 = bin(i2)
            b1 = b1[:-2]+'11'
            b1 = b1.replace('0b', '')
            i2 = int(b1, 2)
            h1 = hex(i2)
            h1 = h1.replace('0x', '')
            obj_code = OPCODE[0] + h1.upper() + '1'
            TA = SYMTAB[temp[-1]]
            obj_code += TA[-5]+TA[-4]+TA[-3]+TA[-2]+TA[-1]
            f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")
        # Format 4 instructions with immediate addressing
        elif temp[-2].replace('+', '') in OPTAB and '+' in temp[-2] and '#' in temp[-1]:
            t = temp[-2].replace('+', '')
            OPCODE = OPTAB[t.replace('\n', '')]
            i2 = int(OPCODE[1], 16)
            b1 = bin(i2)
            b1 = b1[:-2]+'11'
            b1 = b1.replace('0b', '')
            i2 = int(b1, 2)
            h1 = hex(i2)
            h1 = h1.replace('0x', '')
            obj_code = OPCODE[0] + h1.upper() + '1'
            if temp[-1].replace('#', '') in SYMTAB:
                TA = SYMTAB[temp[-1].replace('#', '')]
                TA = str(TA).zfill(5)
                obj_code += TA[-5]+TA[-4]+TA[-3]+TA[-2]+TA[-1]
            elif temp[-1].replace('#', '') not in SYMTAB:
                TA = temp[-1].replace('#', '')
                TA = TA.zfill(5)
                obj_code += TA
                f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")

        # normal format 3 instructions AND indirect: not F4, not F2, not indexed, not a declaration, not immediate, not indirect
        elif temp[-2] in OPTAB and '+' not in temp[-2] and temp[-2] not in FORMAT2 and ',X' not in temp[-1] and temp[-2] not in KEYWORDS and '#' not in temp[-1] and '@' not in temp[-1]:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            i2 = int(OPCODE[1], 16)
            b1 = bin(i2)
            b1 = b1[:-2]+'11'
            b1 = b1.replace('0b', '')
            i2 = int(b1, 2)
            h1 = hex(i2)
            h1 = h1.replace('0x', '')
            obj_code = OPCODE[0] + h1.upper() + '2'
            TA = int(SYMTAB[temp[-1]], 16)
            disp = calc_disp(TA, PC)
            disps = tohex(disp, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")
        # indirect addressing in F3 -> doesn't work
        elif '@' in temp[-1] and temp[-2] in OPTAB and '+' not in temp[-2] and temp[-2] not in FORMAT2 and ',X' not in temp[-1] and temp[-2] not in KEYWORDS and '#' not in temp[-1]:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            i2 = int(OPCODE[1], 16)
            b1 = bin(i2)
            b1 = b1[:-2]+'10'
            b1 = b1.replace('0b', '')
            i2 = int(b1, 2)
            h1 = hex(i2)
            h1 = h1.replace('0x', '')
            obj_code = OPCODE[0] + h1.upper() + '2'
            o = temp[-1].replace('@', '')
            TA = int(SYMTAB[o], 16)
            disp = calc_disp(TA, PC)
            disps = tohex(disp, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")
        # immediate addressing in F3
        elif '#' in temp[-1] and '+' not in temp[-2] and temp[-2] not in FORMAT2 and ',X' not in temp[-1] and temp[-2] not in KEYWORDS and '@' not in temp[-1]:
            o = temp[-1].replace('#', '')
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            i2 = int(OPCODE[1], 16)
            b1 = bin(i2)
            b1 = b1[:-2]+'01'
            b1 = b1.replace('0b', '')
            i2 = int(b1, 2)
            h1 = hex(i2)
            h1 = h1.replace('0x', '')
            obj_code = OPCODE[0] + h1.upper() + '2'
            if o in SYMTAB:  # for #LENGTH
                disps = SYMTAB[o][-3] + SYMTAB[o][-2] + SYMTAB[o][-1]
            else:
                val = int(temp[-1][-1])
                disps = tohex(val, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")
        # indexed addressing  -> hard coded for BUFFER, X
        elif ',X' in temp[-1]:
            OPCODE = OPTAB[temp[-2].replace('\n', '')]
            i2 = int(OPCODE[1], 16)
            b1 = bin(i2)
            b1 = b1[:-2]+'11'
            b1 = b1.replace('0b', '')
            i2 = int(b1, 2)
            h1 = hex(i2)
            h1 = h1.replace('0x', '')
            obj_code = OPCODE[0] + h1.upper() + 'C'
            TA = int(SYMTAB[(temp[-1])[:-2]], 16)
            disp = calc_disp(TA, PC)
            disps = tohex(disp, 12)
            disps = disps.replace('0x', '')
            obj_code += (disps.upper()).zfill(3)
            #print('\n'+line+"    "+obj_code.ljust(4)+"    ")
            f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")
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
            f4.write('\n'+line+"    "+obj_code.ljust(4)+"    ")
