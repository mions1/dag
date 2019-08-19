import sys

#--------------Helper text-------------------------
help = "Create a dictionary passing a pattern with special symbols which will be replaced with relative char set.\n\n"
help += "Symbols:\n"
help += "\t@: alphabetic lower case\n"
help += "\t,: alphabetic upper case\n"
help += "\t%: digit\n"
help += "\t^: symbol\n"
help += "\t*: any\n\n"
help += "Options:\n"
help += "\t--out <file>: set output file\n"
help += "\t--print: print words list\n"
help += "\t--fill: fill blank space with all character\n"
help += "\t--help: print this text\n"
help += "\t--verbose: print some informations\n"
help += "\t--save: save directly on file without save first on array\n\n"
help += "Usage:\n"
help += "\tpython3 dag.py <min> <max> [options value],... <pattern>\n\n"
help += "Example:\n"
help += "\tpython3 dag.py 6 10 --out list.txt --fill h@llo%\n\n"
help += "Tips:\n"
help += "\tmin must be at least the size of pattern\n"
help += "\tmax must be at least as min\n"
#-----------------------------------------------

alias_set = { "@":"lower", ",":"upper", "%":"digit", "^":"symbol", "*":"all_char" } #translater symbols

upper = [str(chr(i)) for i in range(65,91)]     #upper case char set
lower = [str(chr(i)) for i in range(97,123)]    #lower case char set
digit = [str(i) for i in range(0,10)]           #digit char set
symbol = [str(chr(i)) for i in range(32,65)]    #symbol char set
for i in range(91,97):
    symbol.append(str(chr(i)))
for i in range(123,127):
    symbol.append(str(chr(i)))
all_char = [str(chr(i)) for i in range(32,127)] #all_char char set

"""Create a list in which link symbol with its position in pattern string

Parameters:
    patter (str): Pattern. Ex, h@llo%
    
Returns:
    alias (dict): Container of map. Ex, patter=h@llo% -> alias=[ 1:"@", 5:"%" ]
"""
def map(pattern):
    alias = dict()
    for i in range(len(pattern)):
        if pattern[i] in alias_set:
            alias[i] = pattern[i]
    return alias

"""Return char at index in char set associated with symbol

Parameters:
    symbol (char): Symbol of char set
    index (int): Index of char to return in char set
    
Returns:
    char: Char at index in char set. Ex, return digit[3]
"""
def next_symbol(symbol, index):
    return eval(alias_set[symbol]+"["+str(index)+"]")  

"""Change a char in a string

Parameters:
    string (str): String in which change a char
    char (char): Char in what change
    index (int): Index of char to change in string
    
Returns:
    string: Modified string    
"""
def change(string, char, index):
    return string[:index]+char+string[index+1:]

"""Return lenght of a char set

Parameters:
    symbol (char): Symbol of a char set
    
Returns:
    int: lenght of char set associated with symbol
"""
def alias_len(symbol):
    return eval("len("+alias_set[symbol]+")")

"""Create a list of all word according with pattern and options

Parameters:
    alias (dict): Container of mapping about symbols and their position in pattern
    pattern (str): Pattern of words list
    save (bool): If true, save directly on file
                (default False)
    file_name (str): With save=True, file_ name of output file
                (default None)
    
Returns:
    strings: List of words
"""
def create(alias, pattern, save=False, file_name=None):
    strings = []
    for_exec = ""
    change_exec = ""
    #Open file
    if save:
        f = open(file_name, "a")
        
    j = 1    #Used to compute how much tab put
    #Setting a for for each symbol in pattern
    for key in alias:
        for_exec += "for i"+str(key)+" in range(alias_len(alias["+str(key)+"])):"+("\n")+("\t"*j)
        change_exec += "pattern = change(pattern, next_symbol(alias["+str(key)+"], i"+str(key)+"), "+str(key)+")\n"+("\t"*(len(alias)))
        j += 1
    
    #If save, write on file, else add to strings array
    if save:
        change_exec += "f.write(pattern+'\\n')"
    else:
        change_exec += "strings.append(pattern)"
    for_exec += change_exec
    #Execute code
    exec(for_exec)
    
    #Close file
    if save:
        f.close()
    return strings                   

"""Set passed params (from shell)

Parameters:
    params (dict): Dict to fill with passed params
"""
def set_params(params):
    if "--help" in sys.argv or len(sys.argv)<3:
        print(help)
        exit()
    params["min"] = sys.argv[1]
    params["max"] = sys.argv[2]
    params["output_file"] = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else False
    params["fill"] = True if "--fill" in sys.argv else False
    params["patterns"] = []
    params["patterns"].append(sys.argv[len(sys.argv)-1])
    if "--multiple" in sys.argv:
        for i in range(sys.argv.index("--multiple")+1, len(sys.argv)-1):
            params["patterns"].append(sys.argv[i])
    params["print"] = True if "--print" in sys.argv else False
    params["save"] = True if "--save" in sys.argv else False

"""Save words in file

Parameters:
    file (str): File name of output file
    strings (list): Words list to save
"""
def save(file, word_lists):
    if params["print"]:
        with open(file, "a") as f:
            for wl in word_lists:
                for s in wl:
                    f.write(s+"\n")
                    print(s)
    else:
        with open(file, "a") as f:
            for wl in word_lists:
                for s in wl:
                    f.write(s+"\n")

"""Shift a string

Parameters:
    string (str): String to shift
    direction (char): Shift to right (r) or to left (l)
                        (default r)

Returns:
    shifted (str): Shifted string
"""
def shift(string, direction='l'):
    if direction == 'r':
        shifted = string[:len(string)-1]
        shifted = string[len(string)-1] + shifted
    elif direction == 'l':
        shifted = string[1:len(string)]
        shifted = shifted + string[0]
    
    return shifted
    
"""If fill is set, create all patterns according with min-max size. Ex, 6 8 h@ll%->@h@ll%, h@ll%@, @@h@ll%, @h@ll%@, ...

Parameters:
    patter (str): Pattern
    min (int): Min size of pattern
    max (int): Max size of pattern
"""
def create_patterns(pattern, min, max, patterns):
    tmp = "" #actual pattern
    
    #Loop for every size
    for i in range(min, max+1):
        #Create default pattern (ex, **h@ll%)
        tmp = "*"*(i-len(pattern))
        tmp += pattern
        patterns.append(tmp)
        #Then shift '*' to generate others (**h@ll%, *h@ll%*, h@ll%**)
        for j in range(i-len(pattern)):
            tmp = shift(tmp, 'l')
            patterns.append(tmp)

def print_debug(string):
    if "--verbose" in sys.argv:
        print(string)
    pass
    
params = dict() #dict with passed params (--out, --fill, etc)
set_params(params)  #set passed params
strings = []

min = int(params["min"]) #min size of words in words list
max = int(params["max"]) #max size of words in words list
pattern = params["patterns"] #save passed pattern(s) (from shell)
file_name = params["output_file"] #save passed output file name
just_save = params["save"] #save directly on file, without save first on array
fill = params["fill"] #fill left char with *

#Just to erase file_name
if file_name:
    f = open(file_name, "w")
    f.close()

alias = dict() #dict of symbols and their position in pattern
patterns = []
if fill:
    print_debug("Creating patterns...")
    for p in pattern:
        create_patterns(p, min, max, patterns)
    print_debug("Done!")
    print_debug(patterns)
else:
    for p in pattern:
        patterns.append(p)
word_lists = []
print_debug("Creating words lists...")
i = 1
pat_len = str(len(patterns))
for p in patterns:
    print("Creating pattern "+str(i)+"/"+pat_len)
    i = i+1
    alias = map(p)
    print_debug("\tcreating "+p)
    word_lists.append(create(alias, p, just_save, file_name)) #create words list
    print_debug("\tdone")
print_debug("Done!")

#Save or just print words list
if not just_save:
    if file_name:
        save(file_name, word_lists)

if not file_name:
    for wl in word_lists:
        for s in wl:
            f.write(s+"\n")
        print(s)
