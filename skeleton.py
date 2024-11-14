
MAX_CONSTANTS = 10
BINARY_CONNECTIVES = ["=>", "/\\", "\/"]
PROPOSITIONS = ["p", "q", "r", "s"]
PREDICATES = ["P", "Q", "R", "S"]
VARIABLES = ["w", "x", "y", "z"]
OPENING_BRACKET = "("
CLOSING_BRACKET = ")"
COMMA = ","
NOT = "~"
AND = "/\\"
OR = "\/"
IMPLIES = "=>"
EXIST = "E"
FOR_ALL = "A"

def is_valid_prop(fmla):
    stack = []
    i = 0
    while i < len(fmla):
        # print(stack)
        if fmla[i] == CLOSING_BRACKET:
            binary_connective_seen = False
            comma_seen = False
            while len(stack) > 0 and stack[-1] != OPENING_BRACKET:
                if stack[-1] in BINARY_CONNECTIVES:
                    binary_connective_seen = True
                if stack[-1] == COMMA:
                    comma_seen = True
                stack.pop()
            if len(stack) == 0:
                return False
            if comma_seen is False and binary_connective_seen is False:
                return False
            stack.pop()
            if comma_seen:
                if len(stack) == 0 or stack[-1] not in PREDICATES:
                    return False
                else:
                    stack.pop()
            stack.append("@")
        elif fmla[i] in [NOT]:
            i += 1
            continue
        elif fmla[i] in [EXIST, FOR_ALL]:
            i += 2
            continue
        else:
            if i < len(fmla) and fmla[i:i + 2] in BINARY_CONNECTIVES:
                stack.append(fmla[i:i+2])
                i += 1
            else:
                stack.append(fmla[i])
        i += 1
    return len(stack) == 1

def is_valid_fol(fmla):
    return False

def propositional(fmla):
    for i in range(len(fmla)):
        if  fmla[i] in VARIABLES or fmla[i] in PREDICATES or fmla[i] in [FOR_ALL, EXIST]:
            return 0
    if not is_valid_prop(fmla):
        return 0
    if len(fmla) == 1 and fmla[0] in PROPOSITIONS:
        return 6
    if fmla[0] == NOT:
        return 7
    return 8

def first_order(fmla):
    #assume fmla is valid for now
    for i in range(len(fmla)):
        if fmla[i] in PROPOSITIONS:
            return 0
    if not is_valid_prop(fmla):
        return 0
    if fmla[0] == NOT:
        return 2
    elif fmla[0] == EXIST:
        return 4
    elif fmla[0] == FOR_ALL:
        return 3
    for i in range(0, len(fmla) - 1):
        if fmla[i:i + 2] in BINARY_CONNECTIVES:
            return 5
    return 1

# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    prop_idx = propositional(fmla)
    fol_idx = first_order(fmla)
    if 6 <= prop_idx <= 8:
        return prop_idx
    if 1 <= fol_idx <= 5:
        return fol_idx
    return 0

# Return the LHS of a binary connective formula
def lhs(fmla):
    stack = []
    result = ""
    for i in range(1, len(fmla) - 1):
        if len(stack) == 0 and fmla[i:i + 2] in BINARY_CONNECTIVES:
            break
        elif fmla[i] == OPENING_BRACKET:
            stack.append(fmla[i])
        elif fmla[i] == CLOSING_BRACKET and len(stack) == 0:
            return False
        elif fmla[i] == CLOSING_BRACKET:
            stack.pop()
        result += fmla[i]
    return result

# Return the connective symbol of a binary connective formula
def con(fmla):
    stack = []
    for i in range(1, len(fmla) - 1):
        if len(stack) == 0 and fmla[i:i + 2] in BINARY_CONNECTIVES:
            return fmla[i:i+2]
        elif fmla[i] == OPENING_BRACKET:
            stack.append(OPENING_BRACKET)
        elif fmla[i] == CLOSING_BRACKET:
            stack.pop()
    return None 

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    stack = []
    result = ""
    for i in range(len(fmla) - 2, 1, -1):
        if len(stack) == 0 and fmla[i - 1:i + 1] in BINARY_CONNECTIVES:
            break
        if fmla[i] == CLOSING_BRACKET:
            stack.append(fmla[i])
        elif fmla[i] == OPENING_BRACKET and len(stack) == 0:
            return False
        elif fmla[i] == OPENING_BRACKET:
            stack.pop()
        result = fmla[i] + result

    return result


# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return None

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0

#------------------------------------------------------------------------------------------------------------------------------:
#                   DO NOT MODIFY THE CODE BELOW. MODIFICATION OF THE CODE BELOW WILL RESULT IN A MARK OF 0!                   :
#------------------------------------------------------------------------------------------------------------------------------:

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
