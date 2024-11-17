
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
BASE_PROPOSITIONS = ["p", "q", "r", "s", NOT + "p", NOT + "q", NOT + "r", NOT + "s"]

def is_valid_prop(fmla):
    stack = []
    i = 0
    while i < len(fmla):
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

def recursive(queue, result, seen):
    while len(queue) > 0:
        formula = queue.pop(0)
        if formula in BASE_PROPOSITIONS:
            seen.append(formula)
        elif formula[0] == NOT:
            if formula[1] == NOT:
                queue.append(formula[2:])
            else:
                connective = con(formula[1:])
                left_formula = lhs(formula[1:])
                right_formula = rhs(formula[1:])
                if connective == OR:
                    connective = AND
                elif connective == OR:
                    connective = AND
                else:
                    connective = AND
                    right_formula = NOT + right_formula
                queue.append(OPENING_BRACKET + left_formula + connective + right_formula + CLOSING_BRACKET)
        else:
            connective = con(formula)
            left_formula = lhs(formula)
            right_formula = rhs(formula)
            if connective == AND:
                queue.append(left_formula)
                queue.append(right_formula)

            elif connective == OR:
                copy_queue = queue[:]
                copy_queue.append(left_formula)
                copy_seen = seen[:]
                recursive(copy_queue, result, copy_seen)
                copy_queue = queue[:]
                copy_queue.append(right_formula)
                copy_seen = seen[:]
                recursive(copy_queue, result, copy_seen)
            else:
                left_formula = NOT + left_formula
                connective = OR
                queue.append(OPENING_BRACKET + left_formula + connective + right_formula + CLOSING_BRACKET)
    if len(seen) > 0:
        result.append(seen)
    return result

# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    queue = [fmla]
    result = recursive(queue, [], [])
    return result

#check for satisfiability
def sat(tableau): #output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    paths = tableau[0]
    print(paths) 
    # [[p, ~p], [q, p], [q, ~q]]
    for b in paths:
        satisfiable = True
        if len(b) >= MAX_CONSTANTS:
            return 2
        s = set(b)
        for prop in s:
            if prop[0] == NOT and prop[1] in s or NOT + prop[0] in s:
                satisfiable = False
                break
        if satisfiable:
            return 1
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
