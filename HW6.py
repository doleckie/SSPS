# Eliza Dolecki
# HW6 SSPS
# Written in Mac Terminal and Xcode

import sys, re

scope = ""

#----------
# Debugging
debugging = False
def debug(s):
    if debugging: print(s)

#-------------------------
# Operator Stack Function

opStack = []

def opPop():
    #pop the top value of opStack
    return opStack.pop()

def opPush(value):
    #push a value onto the top of opStack
    opStack.append(value)

#---------------------------
# Dictionary stack functions

dictStack = []

def dictPop():
    #pop the top value of dictStack (only used by end() function)
    return dictStack.pop()

def define(name, value):
    d = {name : value}
    if dictStack == []:
        #dictionary stack does not have any entries yet
        dictPush((0, d))
    else:
        #dictionary stack does have entries, pop top dictionary off stack, add the new name and value to that dictionary and push it back to the top of the dictionary stack
        (link, dict) = dictPop()
        addToDict(dict, name, value)
        dictPush((link, dict))

def dictPush(hold):
    #push a dictionary onto the top of dictStack (only used by begin() function)
    dictStack.append(hold)

#old lookup function for SPS
#def lookup(name):
    #because names when entered in as a token for calling do not have the '/' character add it
    #   name = '/' + name
    #if dictStack is empty return false
    #if len(dictStack) == 0:
    #    return False
    #if dictStack is not empty, going from the top dictionary and working backwards look at each dictionary and if the name is in the stack return the value associated with it else return false
    #for d in reversed(dictStack):
    #    if name in d.keys():
    #        return d[name]
    #return False

#>>>New lookup function for SSPS<<<
def lookup(name, scope):
    name = '/' + name
    #if dynamic scope go from top of stack down
    if scope == "dynamic":
        for (link, d) in reversed(dictStack):
            if isInDict(name, d):
                return d[name]
    else:
        #if static scope get the link and then return the definition from the linked dictionary
        linker = getFinder(name[1:])
        (l, dict) = dictStack[linker]
        return dict[name]
    return False

def getFinder(name):
    #Helper funtion to get the correct link
    name = '/' + name
    lenDict = len(dictStack)
    if lenDict == 0:
        #there is nothing in the dictionary stack
        return 0
    else:
        #set to the top end of the dictionary stack
        currIndex = lenDict - 1
    while True:
        #while time is not found in stack and index does not equal 0
        for d in dictStack[currIndex][1]:
            #for each dictionary in the dictionary stack
            if isInDict(name, d):
                #if the name is found return our index which is our link
                return currIndex
        if currIndex == 0:
            #if 0 return 0 because we are at the end of the stack
            return 0
        else:
            #set the index to the static link index
            currIndex = dictStack[currIndex][0]


def addToDict(d, name, value):
    #helper fuction to add to dictionary stack
    d[name] = value

def isInDict(name, d):
    #helper function to check if name is in dictionary returns True or False
    return name in d


#----------------------
# Arithmetic Operations

def add():
    #pop top two values of opStack (due to commutative rule doesn't matter order of numbers) and add them
    op1 = opPop()
    op2 = opPop()
    opPush(op2 + op1)

def sub():
    #pop top two values of opStack, the first number is op2 the second number is op1, subtract op1 from op2
    op1 = opPop()
    op2 = opPop()
    opPush(op2 - op1)

def mul():
    #pop top two values of opStack (due to commutative rule doesn't matter order of the numbers) and multiply them
    op1 = opPop()
    op2 = opPop()
    opPush(op1 * op2)

def div():
    #pop top two values of opStack, the first number is op2 the second number is op1 divide op2 by op1
    op1 = opPop()
    op2 = opPop()
    
    #divide by 0 check
    if op1 == 0:
        opPush("Divide by 0 error")
        return
    
    opPush(op2/op1)

def eq():
    #pop top two values of opStack, if op1 is equal to op2 return True
    op1 = opPop()
    op2 = opPop()
    opPush(op1 == op2)

def lt():
    #pop top two values of opStack, if op2 is less than op1 return True
    op1 = opPop()
    op2 = opPop()
    opPush(op2 < op1)

def gt():
    #pop top two values of opStack, if op2 is greater than op1 return True
    op1 = opPop()
    op2 = opPop()
    opPush(op2 > op1)

#------------------
# String Operations

def length():
    str = opPop()
    
    #input fails check
    if str == "" or str == "()":
        opPush("Empty string")
        return
    
    opPush(len(str) - 2)
    #The string length is minus two due to the () surrounding it

def get():
    #pop value and string and return the element value at value in the string
    val = opPop()
    str = opPop()
    
    #Input fails checks
    if str == "" or str == "()":
        opPush("Empty string")
        return
    if val > (len(str) - 1):
        opPush("Index not in string")
        return
    
    final = ord(str[val + 1]) #add one due to the beginning '('
    opPush(final)

def getInterval():
    #get the number of characters, the starting index and the string, substring is created with the () surrounding and index must have +1 to account for the starting '(' character
    count = opPop()
    index = opPop()
    str = opPop()
    
    #Input fails checks
    if str == "" or str == "()":
        opPush("Empty string")
        return
    if ((index + 1) > (len(str) - 1)):
        opPush("Index not in string")
        return
    if ((index + 1 + count) > (len(str) - 1)):
        opPush("Past end of string")
        return
    
    substr = '(' + str[(index + 1):((index + 1) + count)] + ')'
    opPush(substr)

#------------------
# Boolean operators

def psAnd():
    #take top two values of opStack and return the boolean value of and (true & true = true, true & false = false, false & true = false, false & false = false)
    op1 = opPop()
    op2 = opPop()
    
    #input fails check
    if type(op1) != bool or type(op2) != bool:
        opPush("One of the values is not a boolean")
        return
    
    opPush(op2 and op1)

def psOr():
    #take top two values of opStack and return the boolean value of or (true or true = true, true or false = true, false or true = true, false or false = false)
    op1 = opPop()
    op2 = opPop()
    
    #input fails check
    if type(op1) != bool or type(op2) != bool:
        opPush("One of the values is not a boolean")
        return
    
    opPush(op2 or op1)

def psNot():
    #take the top value of opStack and return boolean value of not (true = false, false = true)
    op1 = opPop()
    
    #input fails check
    if type(op1) != bool:
        opPush("The value is not a boolean")
        return
    
    opPush(not op1)

#----------------------------
# Operator Stack Manipulation

def dup():
    #take top value of opStack and push it onto stack twice
    val = opPop()
    opPush(val)
    opPush(val)

def exch():
    #take top two values op opStack op2 is the first value op1 is the second value, push op1 on first then op2
    op1 = opPop()
    op2 = opPop()
    opPush(op1)
    opPush(op2)

def pop():
    #pop top value on stack
    opPop()

def roll():
    #pop top two values on the stack, op2 is the number of objects, op1 is the number of shifts
    op1 = opPop()
    op2 = opPop()
    
    #create a stack that starts at length of opStack - the number of objects to the end of the stack
    hold = opStack[len(opStack) - op2:]
    
    if op1 > 0:
        #if number is not negative, then rotate right
        temp = hold[op1:]
        hold[op1:] = []
        hold[:0] = temp
    elif op1 < 0:
        #else if negative rotate left
        temp = hold[0:(-1 * op1)]
        hold[:(-1 * op1)] = []
        hold[len(hold):] = temp
    
    #pop the values off of opStack
    for i in range(0,op2):
        opStack.pop()
    
    #push the new values onto the opStack
    for x in hold:
        opPush(x)

def copy():
    #create a blank stack, take the top value of opStack which is the number of items from opStack to copy and put in hold then add the new items to the end of the stack
    hold = []
    val = opPop()
    hold[:] = opStack[-val:]
    for x in hold:
        opStack.append(x)

def clear():
    #delete all items in opStack
    del opStack[:]

def stack():
    #print the stack
    print("==============")
    for x in reversed(opStack):
        print(x)
    print("==============")
    #print dictStack as well for SSPS
    index = len(dictStack) - 1
    for (link, d) in reversed(dictStack):
        print('----' + str(index) + '----' + str(link) + '----')
        for (k,v) in d.items():
            print(str(k) + "    " + str(v) )
        index -= 1
    print("==============")

#------------------------------
# Dictionary Stack Manipulation

#NOT USED IN SSPS
def psDict():
    #pop value on opStack, ignore it, and push blank dictionary onto opStack
    opPop()
    opPush({})

#NOT USED IN SSPS
def begin():
    #pop the blank dictionary on opStack and push a new dictionary onto dictStack
    temp = opPop()
    dictPush(temp)

#NOT USED IN SSPS
def end():
    #pop the top dictionary off of dictStack
    dictPop()

def psDef():
    #get the name of the definition and it's value from the opStack and define them in the dictionary
    value = opPop()
    name = opPop()
    define(name, value)

def dictClear():
    #clear the dictionary stack, used between testing only, not a function callable for the interpreter
    del dictStack[:]

#------------------------
# if and ifelse operators
def psif():
    #pop the code array and the boolean value from opStack
    code = opPop()
    bool = opPop()
    #if boolean is True then send the code through the interpreter otherwise do nothing
    if bool == True:
        interpretSPS(code)

def psifelse():
    #pop the else code, the if code, and boolean value from opStack
    else_code = opPop()
    if_code = opPop()
    bool = opPop()
    #if boolean is True then do the if code, otherwise do the else code
    if bool == True:
        interpretSPS(if_code)
    else:
        interpretSPS(else_code)

#---------------------
# Tokenize and Parsing

# Tokenizes a string passed into it
def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[(][a-zA-Z0-9_\s!]*[)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

def groupMatching(it):
    rest = [] #create temp array
    for c in it:
        #for each character in the current array (having seen a '{') if '}' return the code array, if '{' go through group matching again to match the internal '{' '}' else append the character to the temp array, if none of these options work then return False
        if c == '}':
            return rest
        elif c == '{':
            rest.append(groupMatching(it))
        else:
            rest.append(c)
    return False

#from assignment instructions
#def group(s):
#    if s[0] == '{':
#        return groupMatching(iter(s[1:]))
#    else: return False

def parse(s):
    #takinging the input array of tokens create a temp array and create an iterable object from the input array
    res = []
    it = iter(s)
    for x in it:
        #for each token in the iterable array if '}' without seeing a '{' first return false as the code array is mismatched, if token is '{' send to group matching to get a code array for the tokens between '{ and it's matching '}', else append the token to the temp array
        if x == '}':
            return False
        elif x == '{':
            res.append(groupMatching(it))
        else:
            res.append(x)
    #Having completet looping through the entire input array return the temp array as the final code
    return res

#------------
# Interpreter

def interpretSSPS(code, scope):
    link = 0
    for token in code:
        debug("Current token is: " + str(token))
        debug("Current opStack: " + str(opStack))
        debug("Current dictStack: " + str(dictStack))
        try:
            #attempt to create an integer and push onto the opStack
            opPush(int(token))
        #if the token is any of these, perform their associated function
        except:
            if token == "add":
                add()
            elif token == "sub":
                sub()
            elif token == "mul":
                mul()
            elif token == "div":
                div()
            elif token == "eq":
                eq()
            elif token == "lt":
                lt()
            elif token == "gt":
                gt()
            elif token == "length":
                length()
            elif token == "get":
                get()
            elif token == "getinterval":
                getInterval()
            elif token == "and":
                psAnd()
            elif token == "or":
                psOr()
            elif token == "not":
                psNot()
            elif token == "if":
                psif()
            elif token == "ifelse":
                psifelse()
            elif token == "dup":
                dup()
            elif token == "exch":
                exch()
            elif token == "pop":
                pop()
            elif token == "roll":
                roll()
            elif token == "copy":
                copy()
            elif token == "clear":
                clear()
            elif token == "stack":
                stack()
            elif token == "dict":
                psDict()
            elif token == "begin":
                begin()
            elif token == "end":
                end()
            elif token == "def":
                psDef()
            elif token == "true":
                opPush(True)
            elif token == "false":
                opPush(False)
            elif token[0] == '/': #token is the name of a definition and needs to be pushed onto the opStack as a string
                opPush(str(token))
            elif token[0] == '(': #token is a string and needs to be pushed onto the opStack as a string
                opPush(str(token))
            elif type(token) == type([]):
                opPush(token)
            else:
                defn = lookup(str(token), scope) #check if token is the name of a definition and set the value of the definition to defn (lookup returns False if the name is not in the dictStack
                debug("Definition lookup returned: " + str(defn))
                if defn != False: #if the defn is not False
                    #check if defn is a code array, if yes send through the interpreter, else push the definition onto the opStack
                    if type(defn) == type([]):
                        if scope == "static":
                            #static scoping rules
                            link = getFinder(str(token))
                            dictStack.append((link, {}))
                            interpretSSPS(defn, scope)
                            dictPop()
                        else:
                            #dynamic scoping rules
                            dictStack.append((link, {}))
                            interpretSSPS(defn, scope)
                            dictPop()
                    else:
                        opPush(defn)
                else:
                #else the token is something not covered above so push onto the opStack
                    opPush(token)

def interpreter(s, scope):
    #take the input string and first put through tokenizer to create list of tokens, then parse the list so that the '{' '}' characters are matched up and finally push the list through the interpreter
    interpretSSPS(parse(tokenize(s)), scope)


#----------------------------------------------------
#----------------------------------------------------
# Test Functions for Operators and Stack manipulation
# Not used in this version of the code

#test the add operation
def testAdd():
    #test case 1
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3: return False
    
    #test case 2
    opPush(0)
    opPush(0)
    add()
    if opPop() != 0: return False
    
    #test case 3
    opPush(-1)
    opPush(-3)
    add()
    if opPop() != -4: return False
    
    return True

#test the subtraction operation
def testSub():
    #test case 1
    opPush(3)
    opPush(1)
    sub()
    if opPop() != 2: return False
    
    #test case 2
    opPush(0)
    opPush(0)
    sub()
    if opPop() != 0: return False
    
    #test case 3
    opPush(-2)
    opPush(-3)
    sub()
    if opPop() != 1: return False
    
    return True

#test the multiplication operation
def testMul():
    #test case 1
    opPush(3)
    opPush(4)
    mul()
    if opPop() != 12: return False
    
    #test case 2
    opPush(0)
    opPush(0)
    mul()
    if opPop() != 0: return False
    
    #test case 3
    opPush(-3)
    opPush(-2)
    mul()
    if opPop() != 6: return False
    
    return True

#test the division operation
def testDiv():
    #test case 1
    opPush(12)
    opPush(4)
    div()
    if opPop() != 3: return False
    
    #test case 2
    opPush(10)
    opPush(0)
    div()
    if opPop() != "Divide by 0 error": return False
    
    #test case 3
    opPush(1)
    opPush(1)
    div()
    if opPop() != 1: return False
    
    return True

#test the equal comparison operation
def testEq():
    #test case 1
    opPush(5)
    opPush(5)
    eq()
    if opPop() != True: return False
    
    #test case 2
    opPush(5)
    opPush(3)
    eq()
    if opPop() != False: return False
    
    #test case 3
    opPush(1)
    opPush(4)
    eq()
    if opPop() != False: return False
    
    return True

#test the less than comparison operation
def testLt():
    #test case 1
    opPush(3)
    opPush(4)
    lt()
    if opPop() != True: return False
    
    #test case 2
    opPush(5)
    opPush(5)
    lt()
    if opPop() != False: return False
    
    #test case 3
    opPush(5)
    opPush(3)
    lt()
    if opPop() != False: return False
    
    return True

#test the greater than comparison operation
def testGt():
    #test case 1
    opPush(5)
    opPush(1)
    gt()
    if opPop() != True: return False
    
    #test case 2
    opPush(5)
    opPush(5)
    gt()
    if opPop() != False: return False
    
    #test case 3
    opPush(1)
    opPush(4)
    gt()
    if opPop() != False: return False
    
    return True

#test the length operation
def testLength():
    #test case 1
    opPush("(This is a test)")
    length()
    if opPop() != 14: return False
    
    #test case 2
    opPush("()")
    length()
    if opPop() != "Empty string": return False
    
    #test case 3
    opPush("")
    length()
    if opPop() != "Empty string": return False
    
    return True

#test the get operation
def testGet():
    #test case 1
    opPush("(Hello)")
    opPush(3)
    get()
    if opPop() != 108: return False
    
    #test case 2
    opPush("")
    opPush(2)
    get()
    if opPop() != "Empty string": return False
    
    #test case 3
    opPush("(Testing)")
    opPush(10)
    get()
    if opPop() != "Index not in string": return False
    
    return True

#test the getInterval operation
def testGetInterval():
    #test case 1
    opPush("(This is a test)")
    opPush(0)
    opPush(4)
    getInterval()
    if opPop() != "(This)": return False
    
    #test case 2
    opPush("")
    opPush(0)
    opPush(3)
    getInterval()
    if opPop() != "Empty string": return False
    
    #test case 3
    opPush("(Test this string)")
    opPush(16)
    opPush(5)
    getInterval()
    if opPop() != "Past end of string": return False
    
    #test case 4
    opPush("(Last test)")
    opPush(13)
    opPush(3)
    getInterval()
    if opPop() != "Index not in string": return False
    
    return True

#test the and comparison
def testAnd():
    #test case 1
    opPush(True)
    opPush(False)
    psAnd()
    if opPop() != False: return False
    
    #test case 2
    opPush(False)
    opPush(4)
    psAnd()
    if opPop() != "One of the values is not a boolean": return False
    
    return True

#test the or comparison
def testOr():
    #test case 1
    opPush(True)
    opPush(False)
    psOr()
    if opPop() != True: return False
    
    #test case 2
    opPush(0)
    opPush(True)
    psOr()
    if opPop() != "One of the values is not a boolean": return False
    
    return True

#test the not comparison
def testNot():
    #test case 1
    opPush(False)
    psNot()
    if opPop() != True: return False
    
    #test case 2
    opPush(3)
    psNot()
    if opPop() != "The value is not a boolean": return False
    
    return True

#test the duplication operation
def testDup():
    clear()
    opPush(3)
    dup()
    result = [3,3]
    
    #debugging
    if debugging:
        print("\n--Debugging dup--")
        stack()
    debug("^ testDup should be [3,3]")
    
    if opStack != result: return False
    return True

#test the exchange operation
def testExch():
    clear()
    opPush(4)
    opPush(3)
    exch()
    result = [3,4]
    
    #debugging
    if debugging:
        print("\n--Debugging exch--")
        stack()
    debug("^ testExch should be [3,4]")
    
    if opStack != result: return False
    return True

#test the pop operation
def testPop():
    clear()
    opPush(3)
    opPush(4)
    pop()
    result = [3]
    
    #debugging
    if debugging:
        print("\n--Debugging pop--")
        stack()
    debug("^ testPop should be [3]")
    
    if opStack != result: return False
    return True

#test the roll operation
def testRoll():
    clear()
    opPush(5)
    opPush(4)
    opPush(3)
    opPush(2)
    opPush(1)
    opPush(3)
    opPush(1)
    roll()
    result1 = [5,4,2,1,3]
    if opStack != result1: return False
    
    #debugging
    if debugging:
        print("\n--Debugging Roll--")
        stack()
    debug("^ testRoll with 3 items and 1 move should be [5,4,2,1,3]")

    opPush(3)
    opPush(-1)
    roll()
    result2 = [5,4,1,3,2]
    if opStack != result2: return False
    
    #debugging
    if debugging: stack()
    debug("^ testRoll with 3 items and -1 move should be [5,4,1,3,2]")
    
    opPush(3)
    opPush(2)
    roll()
    result3 = [5,4,2,1,3]
    if opStack != result3: return False
    
    #debugging
    if debugging: stack()
    debug("^ testRoll with 3 items and 2 moves should be [5,4,2,1,3]")
    
    opPush(3)
    opPush(-2)
    roll()
    result4 = [5,4,3,2,1]
    if opStack != result4: return False
    
    #debugging
    if debugging: stack()
    debug("^ testRoll wiht 3 items and -2 moves should be [5,4,3,2,1]")
    return True

#test the copy and clear operations
def testCopyandclear():
    clear()
    opPush(3)
    opPush(5)
    opPush(4)
    opPush(2)
    opPush(2)
    copy()
    result = [3,5,4,2,4,2]
    if opStack != result: return False
    
    #debugging
    if debugging:
        print("\n--Debugging copy--")
        stack()
    debug("^ testCopy should be [3,5,4,2,4,2]")
    clear()
    if opStack != []: return False
    
    #debugging
    if debugging:
        print("\n--Debugging clear--")
        stack()
    debug("^ testClear should be blank")
    return True

#test the define operation
def testpsDef():
    clear()
    dictClear()
    opPush(2)
    opPush("/s3")
    opPush(4)
    psDef()
    result = [{'/s3':4}]
    
    #debugging
    if debugging:
        print("\n--Debugging psDef--")
        print(dictStack)
    debug("^ dictionary stack should look like [{'s3':4}]")
    
    if dictStack != result: return False
    return True

#test the dict, begin, and end operations
def testDictBeginEnd():
    clear()
    dictClear()
    opPush(5)
    opPush("/s0")
    opPush(2)
    psDef()
    opPush("/s1")
    opPush(4)
    psDef()
    psDict()
    begin()
    opPush("/s2")
    opPush(5)
    psDef()
    result1 = [{'/s0':2, '/s1':4}, {'/s2':5}]
    if dictStack != result1: return False
    
    #debugging
    if debugging:
        print("\n--Debugging DictBeginEnd--")
        print(dictStack)
    debug("^ Dictionary 1 with '/s0' and '/s1' is the original dictstack, Dictionary 2 should be '/s2'")
    
    end()
    result2 = [{'/s0':2, '/s1':4}]
    
    #debugging
    if debugging: print(dictStack)
    debug("^ Dictionary 2 should be removed")
    
    if dictStack != result2: return False
    return True

#test the lookup operation
def testLookup():
    clear()
    dictClear()
    opPush(2)
    opPush("/s3")
    opPush(4)
    psDef()
    result = lookup("s3")
    
    #debugging
    if debugging:
        print("\n--Debugging lookup--")
        print(result)
    debug("^ lookup('s3') should return 4")
    if result != 4: return False
    return True

#-------------------
#-------------------
# Main for old tests

#def main():
#testCases = [('add', testAdd),('sub', testSub), ('mul', testMul), ('div', testDiv), ('eq', testEq), ('lt', testLt), ('gt', testGt), ('length', testLength), ('get', testGet), ('getInterval', testGetInterval), ('and', testAnd), ('or', testOr), ('not', testNot), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('roll', testRoll), ('Copy and clear', testCopyandclear), ('psDef', testpsDef), ('lookup', testLookup), ('Dict, Begin, and End', testDictBeginEnd)]

#failedTests = [testName for (testName, testProc) in testCases if not testProc()]

#if failedTests:
#    print('Some tests failed', failedTests)
#else:
#    print('All tests passed')

#---------------------------------------------
# Testing for tokenize, parse, and interpreter
#def testSPS():
#    input1 = """/square {
#        dup mul
#        } def
#        (square)
#        4 square
#        dup 16 eq true and
#        {(pass)} {(fail)} ifelse
#        stack"""
    
    #   input2 = """(facto) dup length /n exch def
    #        /fact {
        #       0 dict begin
        #      /n exch def
        #n 2 lt
        #{1}
        #{n 1 sub fact n mul}
        #ifelse
        #end
        #} def
#n fact stack"""
    
    #input3 = """/lt6 {6 lt} def
    #    1 2 3 4 5 6 4 -3 roll
        #    dup dup lt6 exch 3 gt and {mul mul} if
#    stack
#   clear"""
    
    #    input4 = """(CptS355_HW5) 4 3 getinterval
    # (355) eq
    #    {(You_are_in_CptS355)} if
#   stack"""
    
    #for debugging purposes
#    if debugging:
#        print("Input 1 string\n")
#        print(input1)
#        print("======")
#        print("\n--Test tokenize on input1--")
#        print(tokenize(input1))
#        print("\n--Test parse on input1--")
#        print(parse(tokenize(input1)))

#    interpreter(input1)
    #clear opStack and dictStack for next test
#    clear()
#    dictClear()

#for debugging purposes
#if debugging:
#    print("\nInput 2 string\n")
#    print(input2)
#    print("======")
#    print("\n--Test tokenize on input2--")
#    print(tokenize(input2))
#    print("\n--Test parse on input2--")
#    print(parse(tokenize(input2)))
    
#    interpreter(input2)
    #clear opStack and dictStack for next test
#    clear()
#    dictClear()
    
    #for debugging purposes
#    if debugging:
#        print("\nInput 3 string\n")
#        print(input3)
#        print("======")
#        print("\n--Test tokenize on input3--")
#        print(tokenize(input3))
#        print("\n--Test parse on input3--")
#        print(parse(tokenize(input3)))

#    interpreter(input3)
    #clear opStack and dictStack for next test
#    clear()
#    dictClear()

#if debugging:
#    print("\nInput 4 string\n")
#    print(input4)
#    print("======")
#    print("\n--Test tokenize on input4--")
#    print(tokenize(input4))
#    print("\n--Test parse on input4--")
#    print(parse(tokenize(input4)))
    
#    interpreter(input4)
#    clear opStack and dictStack for next test
#    clear()
#    dictClear()

#-------------
# SSPS testing
def testSSPS():
    input1 = """/x 4 def
        /g { x stack } def
        /f { /x 7 def g } def
        f
        """
    
    input2 = """/m 50 def
        /n 100 def
        /egg1 {/m 25 def n} def
        /chic {
            /n 1 def
            /egg2 { n } def
            m n
            egg1
            egg2
            stack } def
        n
        chic
        """
    input3 = """/x 10 def
        /A { x } def
        /C { /x 40 def A stack } def
        /B { /x 30 def /A { x } def C } def
        B
        """
    
    #test case 1: input string 1, static
    print("--Input 1--")
    print("Scope set to static")
    interpreter(input1, "static")
    
    #clear for next test
    clear()
    dictClear()

    #test case 2: input string 1, dynamic
    print("Scope set to dynamic")
    interpreter(input1, "dynamic")
    
    #clear for next test
    clear()
    dictClear()

    #test case 3: input string 2, static
    print("\n----------------")
    print("--Input 2--")
    print("Scope set to static")
    interpreter(input2, "static")
    
    #clear for next test
    clear()
    dictClear()
    
    #test case 4: input string 2, dynamic
    print("Scope set to dynamic")
    interpreter(input2, "dynamic")
    
    #clear for next test
    clear()
    dictClear()

    #test case 5: input string 3, static
    print("\n-----------------")
    print("--Input 3--")
    print("Scope set to static")
    interpreter(input3, "static")
    
    #clear for next test
    clear()
    dictClear()
    
    #test case 6: input string 3, dynamic
    print("Scope set to dynamic")
    interpreter(input3, "dynamic")
    
    #clear stacks
    clear()
    dictClear()

#-----
# Main
def main():
    testSSPS()

if __name__ == "__main__":
    main()





