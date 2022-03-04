import os

OPCODETABLE = \
    {
        'ADD': [3, 0x18, 1], 'ADDF': [3, 0x58, 1], 'ADDR': [2, 0x90, 2], 'AND': [3, 0x40, 1], 'CLEAR': [2, 0xB4, 1],
        'COMP': [3, 0x28, 1], 'COMPF': [3, 0x88, 1], 'COMPR': [2, 0xA0, 2], 'DIV': [3, 0x24, 1], 'DIVF': [3, 0x6, 1],
        'DIVR': [2, 0x9C, 2], 'FIX': [1, 0xC4, 0], 'FLOAT': [1, 0xC0, 0], 'HIO': [1, 0xF4, 0], 'J': [3, 0x3C, 1],
        'JEQ': [3, 0x30, 1], 'JGT': [3, 0x34, 1], 'JLT': [3, 0x38, 1], 'JSUB': [3, 0x48, 1], 'LDA': [3, 0x00, 1],
        'LDB': [3, 0x68, 1], 'LDCH': [3, 0x50, 1], 'LDF': [3, 0x70, 1], 'LDL': [3, 0x08, 1], 'LDS': [3, 0x6C, 1],
        'LDT': [3, 0x74, 1], 'LDX': [3, 0x04, 1], 'LPS': [3, 0xD0, 1], 'MUL': [3, 0x20, 1], 'MULF': [3, 0x60, 1],
        'MULR': [2, 0x98, 2], 'NORM': [1, 0xC8, 0], 'OR': [3, 0x44, 1], 'RD': [3, 0xD8, 1], 'RMO': [2, 0xAC, 2],
        'RSUB': [3, 0x4C, 0], 'SHIFTL': [2, 0xA4, 2], 'SHIFTR': [2, 0xA8, 2], 'SIO': [1, 0xF0, 0], 'SSK': [3, 0xEC, 1],
        'STA': [3, 0x0C, 1], 'STB': [3, 0x78, 1], 'STCH': [3, 0x54, 1], 'STF': [3, 0x80, 1], 'STI': [3, 0xD4, 1],
        'STL': [3, 0x14, 1], 'STS': [3, 0x7C, 1], 'STSW': [3, 0xE8, 1], 'STT': [3, 0x84, 1], 'STX': [3, 0x10, 1],
        'SUB': [3, 0x1C, 1], 'SUBF': [3, 0x5C, 1], 'SUBR': [2, 0x94, 2], 'SVC': [2, 0xB0, 1], 'TD': [3, 0xE0, 1],
        'TIO': [1, 0xF8, 0], 'TIX': [3, 0x2C, 1], 'TIXR': [2, 0xB8, 1], 'WD': [3, 0xDC, 1]
    }

ADDITIONAL_REGISTERS = \
    {
        'B': 0X3, 'S': 0x4, 'T': 0x5, 'F': 0x6, 'A': 0x0, 'X': 0x1, 'L': 0x2, 'PC': 0X8, 'SW': 0X9
    }

LOC = 0
Literal = []
L = 0


def Location_Counter(Line, LOCATION):
    global LOC
    global Literal
    global L
    f = 0
    if Line[0] == '.':
        return

    Increment = 0
    LOC1 = LOC

    Instruction_Index = len(Line.split()) - 2
    if Instruction_Index < 0:
        Instruction_Index = Instruction_Index + 1

    Instruction = Line.split()[Instruction_Index]
    Value = Line.split()[len(Line.split()) - 1]

    if Value[0] == '=':
        if len(Literal) > 0:
            for i in range(len(Literal)):
                if Literal[i] == Value:
                    f = 1
                    break
            if f == 0:
                Literal.append(Value)
        else:
            Literal.append(Value)

    if Instruction[0] == '+':
        Increment = 4
    elif Instruction == "LTORG":
        LOCATION.write("{:<8}{:<6}".format('____', Line))
        if L > 0:
            for i in range(L - 1, -1, -1):
                Literal.pop(i)
        for i in range(len(Literal)):
            Name = Literal[i].strip('=')
            if Name[0] == 'X':
                Increment = 1
                LOCATION.write(
                    "{:<10}{:<6}{:<6}".format("{0:0>4}".format(hex(LOC1).split('x')[1]).upper(), '*',
                                              '     ' + Literal[i]))
            elif Name[0] == 'C':
                Increment = len(Name) - 3
                LOCATION.write(
                    "{:<10}{:<6}{:<6}".format("{0:0>4}".format(hex(LOC1).split('x')[1]).upper(), '*',
                                              '     ' + Literal[i]))
            LOCATION.write('\n')
            LOC = LOC + Increment
            LOC1 = LOC
        L = len(Literal)
        return
    elif Instruction[0] == '&':
        Increment = 3
    elif Instruction[0] == '$':
        Increment = 4
    elif Instruction == 'BASE':
        LOCATION.write("{:<8}{:<6}".format('____', Line))
        return
    elif Instruction == 'END':
        LOCATION.write("{:<8}{:<6}".format(hex(LOC1).split('x')[1].upper(), Line))
        if L > 0:
            for i in range(L - 1, -1, -1):
                Literal.pop(i)
        for i in range(len(Literal)):
            LOCATION.write('\n')
            Name = Literal[i].strip('=')
            if Name[0] == 'X':
                Increment = 1
                LOCATION.write(
                    "{:<10}{:<6}{:<6}".format("{0:0>4}".format(hex(LOC1).split('x')[1]).upper(), '*',
                                              '     ' + Literal[i]))
            elif Name[0] == 'C':
                Increment = len(Name) - 3
                LOCATION.write(
                    "{:<10}{:<6}{:<6}".format("{0:0>4}".format(hex(LOC1).split('x')[1]).upper(), '*',
                                              '     ' + Literal[i]))
            LOC = LOC + Increment
            LOC1 = LOC
        Literal.clear()
        return
    elif Instruction == 'RESB' or Instruction == 'RESW' or Instruction == 'BYTE' or Instruction == 'WORD':
        if Instruction == 'WORD':
            Increment = 3
        elif Instruction == 'BYTE':
            if Value[0] == 'X':
                Increment = 1
            elif Value[0] == 'C':
                Increment = len(Value) - 3
        elif Instruction == 'RESB':
            Increment = int(Value)
        elif Instruction == 'RESW':
            Increment = int(Value) * 3
    else:
        Increment = OPCODETABLE[Instruction][0]

    LOC = LOC + Increment
    LOCATION.write("{:<8}{:<6}".format("{0:0>4}".format(hex(LOC1).split('x')[1].upper()), Line))


########################################################################################################################

def Symble_Table(Line, SYMBLE_TABLE):
    Size = len(Line.split())
    if Size == 4:
        SYMBLE_TABLE.write("{:<8}{:<4}".format('\n' + Line.split()[1], '       ' + Line.split()[0]))


########################################################################################################################

def Literal_Table(Line, LITERAL_TABLE):
    if Line.split()[1] == '*':
        Name = Line.split()[len(Line.split()) - 1]
        Value = ''
        V = Name.strip('=')
        if V[0] == 'C':
            V = V.strip('C').strip("'")
            for j in range(len(V)):
                Value += hex(ord(str(V[j]))).split('x')[1]
        elif V[0] == 'X':
            Value = V.strip('X').strip("'")
        LITERAL_TABLE.write("{:<8}      {:<8}   {:<8}".format('\n' + Name, Value, Line.split()[0]))


########################################################################################################################

def INSTRUCTION(Line):
    Instruction_Index = len(Line.split()) - 2
    if Instruction_Index == 0:
        Instruction_Index = Instruction_Index + 1
    return Line.split()[Instruction_Index]


########################################################################################################################

def Locations_Values(Value, TABLE, S, V):
    Line = TABLE.readline()
    if S == 0:
        Value = Value.strip('X').strip(',').strip('#').strip('@')
    while True:
        if Line.split()[0] == Value:
            if V == 0:
                LOC1 = Line.split()[len(Line.split()) - 1]
                TABLE.close()
                return LOC1
            else:
                Value = Line.split()[len(Line.split()) - 2]
                TABLE.close()
                return Value

        Line = TABLE.readline()

        if not Line:
            LOC1 = 1
            TABLE.close()
            return LOC1


########################################################################################################################

def ADDRESING_MODE(Value, Op_Code):
    if Value[0] == '#':
        Op_Code = int(Op_Code) + 1
    elif Value[0] == '@':
        Op_Code = int(Op_Code) + 2
    else:
        Op_Code = int(Op_Code) + 3

    return Op_Code


########################################################################################################################

def Object_Code(Line_out, PC, BASE, ObjectCode):
    if len(Line_out.split()) < 2:
        return

    OBJECT = ''
    Instruction = INSTRUCTION(Line_out)

    if Instruction == 'BASE' or Instruction == 'RESW' or Instruction == 'RESB' or Instruction == 'END' or \
            Instruction[0] == '.':
        ObjectCode.write("{:<30}".format(Line_out))
        return
    elif Instruction == 'RSUB':
        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), "4F0000" + '\n'))
        return
    elif Instruction == 'LTORG':
        ObjectCode.write("{:<25}".format(Line_out.strip() + '\n'))
        return

    Value = Line_out.split()[len(Line_out.split()) - 1]
    if Instruction[0] == '*':
        LITERAL_TABLE = open("LiteralTable.txt", "r")
        OBJECT = Locations_Values(Value, LITERAL_TABLE, 1, 1)
        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))
        return
    elif Instruction == 'BYTE':
        if Value[0] == 'X':
            OBJECT = Value.strip('X').strip("'")
            ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))
            return
        elif Value[0] == 'C':
            OBJECT = Value.strip('C').strip("'")
            byte = ''
            for j in range(0, len(OBJECT), 1):
                byte += hex(ord(str(OBJECT[j]))).split('x')[1]
            OBJECT = byte
            ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))
            return
    elif Instruction == 'WORD':
        OBJECT = hex(int(Value, 16)).split('x')[1]
        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))
        return

    if Value[len(Value) - 1] == 'X':
        X = 8
    else:
        X = 0

    Op_Code = OPCODETABLE[Instruction.strip('+').strip('&').strip('$')][1]

    # Format (4)
    if Instruction[0] == '+':
        if Value[0] == '=':
            LITERAL_TABLE = open("LiteralTable.txt", "r")
            LOC1 = Locations_Values(Value, LITERAL_TABLE, 1, 0)
        else:
            SYMBLE_TABLE = open("symbTable.txt", "r")
            LOC1 = Locations_Values(Value, SYMBLE_TABLE, 0, 0)

        if LOC1 == 1:
            Address = hex(int(Value.strip('X').strip(',').strip('#').strip('@'), 10)).split('x')[1]
        else:
            Address = hex(int(LOC1, 16)).split('x')[1]

        Address = "{0:0>5}".format(Address)

        Op_Code = ADDRESING_MODE(Value, Op_Code)

        Op_Code = hex(int(Op_Code)).split('x')[1]
        Op_Code = Op_Code + hex(X + 1).split('x')[1]
        OBJECT = "{0:0>8}".format(Op_Code + Address)

        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))

    # Format (5)
    elif Instruction[0] == '&':
        if Value[0] == '=':
            LITERAL_TABLE = open("LiteralTable.txt", "r")
            LOC1 = Locations_Values(Value, LITERAL_TABLE, 1, 0)
        else:
            SYMBLE_TABLE = open("symbTable.txt", "r")
            LOC1 = Locations_Values(Value, SYMBLE_TABLE, 0, 0)

        if LOC1 == 1:
            Displacement = int(Value.strip('X').strip(',').strip('#').strip('@'))
            p = 0
            b = 0
        else:
            if 2047 >= int(LOC1, 16) - int(PC, 16) >= -2048:
                Displacement = int(LOC1, 16) - int(PC, 16)
                p = 2
                b = 0
            elif 4095 >= int(LOC1, 16) - int(BASE, 16) >= 0:
                Displacement = int(LOC1, 16) - int(BASE, 16)
                p = 0
                b = 4
            else:
                raise Exception("Something wrong with the input file pls check again.")

        if Displacement == 0:
            F2 = F3 = 1
            F1 = 2
        else:
            F3 = 0
            if Displacement < 0:
                F2 = 1
                # 2'complement
                Displacement = 0xfff & Displacement
            else:
                F2 = 0

            if Displacement % 2 == 0:
                F1 = 2
            else:
                F1 = 0

        OBJECT = hex(int(Op_Code) + F1 + F2).split('x')[1] + hex(X + b + p + F3).split('x')[1] + \
                 "{0:0>3}".format(hex(Displacement).split('x')[1])
        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), "{0:0>6}".format(OBJECT).upper() + '\n'))

    # Format(6)
    elif Instruction[0] == '$':
        if Value[0] == '=':
            LITERAL_TABLE = open("LiteralTable.txt", "r")
            LOC1 = Locations_Values(Value, LITERAL_TABLE, 1, 0)
        else:
            SYMBLE_TABLE = open("symbTable.txt", "r")
            LOC1 = Locations_Values(Value, SYMBLE_TABLE, 0, 0)

        if LOC1 == 1:
            Address = int(Value.strip('X').strip(',').strip('#').strip('@'))
        else:
            Address = int(LOC1, 16)

        if LOC1 == BASE:
            F6 = 0
        else:
            F6 = 1

        if Address == 0:
            F4 = F5 = 0
        else:
            F5 = 2
            if Address % 2 == 0:
                F4 = 0
            else:
                F4 = 4

        Op_Code = ADDRESING_MODE(Value, Op_Code)
        Op_Code = hex(int(Op_Code)).split('x')[1]

        OBJECT = Op_Code + hex(X + F4 + F5 + F6).split('x')[1] + "{0:0>5}".format(hex(Address).split('x')[1])
        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), "{0:0>8}".format(OBJECT).upper() + '\n'))

    # Format (1)
    elif OPCODETABLE[Instruction][0] == 1:
        OBJECT = hex(Op_Code).split('x')[1]
        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))
        return

    # Format (2)
    elif OPCODETABLE[Instruction][0] == 2:
        if OPCODETABLE[Instruction][2] == 1:
            OBJECT = hex(Op_Code).split('x')[1] + hex(ADDITIONAL_REGISTERS[Value]).split('x')[1] + '0'

        elif OPCODETABLE[Instruction][2] == 2:
            OBJECT = hex(Op_Code).split('x')[1] + hex(ADDITIONAL_REGISTERS[Value[0]]).split('x')[1] + \
                     hex(ADDITIONAL_REGISTERS[Value[2]]).split('x')[1]

        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))

    # Format (3)
    elif OPCODETABLE[Instruction][0] == 3:
        if Value[0] == '=':
            LITERAL_TABLE = open("LiteralTable.txt", "r")
            LOC1 = Locations_Values(Value, LITERAL_TABLE, 1, 0)
        else:
            SYMBLE_TABLE = open("symbTable.txt", "r")
            LOC1 = Locations_Values(Value, SYMBLE_TABLE, 0, 0)

        Op_Code = ADDRESING_MODE(Value, Op_Code)
        Op_Code = hex(int(Op_Code)).split('x')[1]
        if LOC1 == 1:
            Op_Code = Op_Code + hex(X + 0).split('x')[1]
            Displacement = hex(int(Value.strip('X').strip(',').strip('#').strip('@'), 16)).split('x')[1]
        else:
            if 2047 >= (int(LOC1, 16) - int(PC, 16)) >= -2048:
                Displacement = int(LOC1, 16) - int(PC, 16)
                Op_Code = Op_Code + hex(X + 2).split('x')[1]
            elif 4095 >= (int(LOC1, 16) - int(BASE, 16)) >= 0:
                Displacement = int(LOC1, 16) - int(BASE, 16)
                Op_Code = Op_Code + hex(X + 4).split('x')[1]
            else:
                raise Exception("Something wrong with the input file pls check again.")

            # 2'complement
            if Displacement < 0:
                Displacement = 0xfff & int(Displacement)

            Displacement = hex(int(Displacement)).split('x')[1]

        # Formatting
        Displacement = "{0:0>3}".format(Displacement)

        OBJECT = "{0:0>6}".format(Op_Code + Displacement)

        ObjectCode.write("{:<40}     {:<}".format(Line_out.strip(), OBJECT.upper() + '\n'))


########################################################################################################################

def HTEM_RECORD(Start, End, Name):
    HTEM = open("HTEM RECORD.txt", 'w')
    while len(Name) < 6:
        Name = Name + "_"

    Size = hex(int(Start, 16) - int(End, 16)).split('x')[1]
    Size = str(Size)

    while len(Size) < 6:
        Size = '0' + Size

    while len(Start) < 6:
        Start = '0' + Start

    HTEM.write('H' + '.' + Name + '.' + Start + '.' + Size + '\n')

    ObjectCode = open("Object Code.txt", "r")
    LOCATION = open("out.txt", "r")
    Line = ObjectCode.readline()
    Line_in = LOCATION.readline()
    TSize = 0
    TRecord = ''
    MRecord = ''
    NO = 0
    S = 0
    while True:
        if NO == 0:
            Line_in = LOCATION.readline()
            Line = ObjectCode.readline()
            if not Line:
                if len(TRecord) > 0:
                    TSize = hex(int((TSize / 2))).split('x')[1]
                    HTEM.write('T.' + "{0:0>6}".format(Start) + '.' + "{0:0>2}".format(TSize.upper()) + TRecord + '\n')
                LOCATION.seek(0)
                Line = LOCATION.readline()
                HTEM.write(MRecord)
                HTEM.write('E.' + "{0:0>6}".format(Line.split()[0]))
                LOCATION.close()
                ObjectCode.close()
                HTEM.close()
                return
        if S == 1:
            Start = Line.split()[0]

        NO = 0
        S = 0
        Instruction = INSTRUCTION(Line_in)
        if Instruction == 'BASE' or Instruction == 'LTORG' or Instruction == 'END':
            End = Line_in.split()[0]
            Line_in = LOCATION.readline()
            Line = ObjectCode.readline()
            if len(Line_in.split()) > 0:
                Instruction = INSTRUCTION(Line_in)
            else:
                continue

        if Instruction == 'RESW' or Instruction == 'RESB' or Instruction[0] == '.':
            if len(TRecord) > 10:
                End = Line_in.split()[0]
                TSize = hex(int((TSize / 2))).split('x')[1]
                HTEM.write('T.' + "{0:0>6}".format(Start) + '.' + "{0:0>2}".format(TSize.upper()) + TRecord + '\n')
                Start = End
                TSize = 0
                TRecord = ''
            S = 1
            continue

        elif Instruction[0] == '+' or Instruction[0] == '$':
            if Line.split()[len(Line_in.split()) - 1][0] != '#':
                MRecord = MRecord + 'M.' + "{0:0>6}".format(
                    hex(int(Line.split()[0], 16) + 1).split('x')[1]) + '.' + '05' + '\n'

        OC = Line.split()[len(Line.split()) - 1]
        TSize += len(OC)
        End = Line_in.split()[0]
        if TSize < 60:
            TRecord = TRecord + '.' + OC
        else:
            TSize = hex(int(((TSize - len(OC)) / 2))).split('x')[1]
            HTEM.write('T.' + "{0:0>6}".format(Start) + '.' + "{0:0>2}".format(TSize.upper()) + TRecord + '\n')
            TRecord = ''
            Start = End
            TSize = 0
            NO = 1


########################################################################################################################

def main():
    global LOC
    FILEIN = input("Please enter the name of the input file: ")
    FILEIN = open(FILEIN, 'r')
    LOCATION = open("out.txt", "w")
    SYMBLE_TABLE = open("symbTable.txt", "w")
    LITERAL_TABLE = open("LiteralTable.txt", "w")

    Line = FILEIN.readline()
    LOC = int(str(Line.split()[len(Line.split()) - 1]), 16)
    LOCATION.write("{:<8}{:<6}".format("{0:0>4}".format(hex(LOC).split('x')[1].upper()), Line))

    while True:
        Line = FILEIN.readline()
        if not Line:
            break
        Location_Counter(Line, LOCATION)

    LOCATION = open("out.txt", "r")
    SYMBLE_TABLE.write("{:<8}{:<8}".format('SYMBOL', '      ' + 'LOCATION'))
    SYMBLE_TABLE.write('\n......................')
    LOCATION.readline()

    while True:
        Line = LOCATION.readline()
        if not Line:
            break
        Symble_Table(Line, SYMBLE_TABLE)

    LOCATION = open("out.txt", "r")
    LITERAL_TABLE.write("{:<8}   {:<8}   {:<8}".format('Name', '  Value', '  Address'))
    LITERAL_TABLE.write('\n................................')
    LOCATION.readline()

    while True:
        Line = LOCATION.readline()
        if not Line:
            break
        Literal_Table(Line, LITERAL_TABLE)

    LITERAL_TABLE.close()

    LOCATION = open("out.txt", "r")
    LOCATION1 = open("out.txt", "r")
    Line = LOCATION.readline()

    i = 0
    while i < 2:
        LOCATION1.readline()
        i = i + 1

    ObjectCode = open("Object Code.txt", "w")
    ObjectCode.write("{:<8}".format(Line))

    LOCATION2 = open("out.txt", "r")
    BASE = LOCATION2.readline()
    while BASE.split()[len(BASE.split()) - 2] != 'BASE':
        BASE = LOCATION2.readline()

    SYMBLE_TABLE = open("symbTable.txt", "r")
    BASE = BASE.split()[len(BASE.split()) - 1]
    BASE = Locations_Values(BASE, SYMBLE_TABLE, 0, 0)

    while True:
        Line = LOCATION.readline()
        Line1 = LOCATION1.readline()

        if not Line1:
            if not Line:
                break
            else:
                Line1 = Line

        PC = Line1.split()[0]
        if PC == '____':
            Temploc = open("out.txt", "r")
            Temp = Temploc.readline().split()[0]
            while Temp != '____':
                Temp = Temploc.readline().split()[0]
            Temp = Temploc.readline().split()[0]
            PC = Temp
            Temploc.close()
        Object_Code(Line, PC, BASE, ObjectCode)

    ObjectCode = open("Object Code.txt", "r")
    ObjectCode.readline()
    LOCATION = open("out.txt", "r")

    Start = LOCATION.readline()
    Name = Start.split()[1]
    Start = LOCATION.readline().split()[0]

    End = hex(LOC)
    End = End.split()[0]
    HTEM_RECORD(Start, End, Name)

    ObjectCode.close(), SYMBLE_TABLE.close(), LITERAL_TABLE.close(), FILEIN.close(), LOCATION.close(), LOCATION1.close()
    LOCATION2.close()
    os.remove("out.txt")


main()
