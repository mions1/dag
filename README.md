# dag
Dictionary Attack Generator. As the most famous 'crunch', this script allow to generate a custom dictionary for brute force attack.
So, this is my version of crunch, I needed for some features and then I shared it with all.

Create a dictionary passing a pattern with special symbols which will be replaced with relative char set.

Symbols:
    
    @: alphabetic lower case
    ,: alphabetic upper case
    %: digit
    ^: symbol
    *: any
	
Options:

    --out <file>: set output file
    --print: print words list
    --fill: fill blank space with all character
    --help: print this text
    --verbose: print some informations
    --save: save directly on file without save first on array
    --multiple: you can pass multiple pattern at once
	
Usage:
    
    python3 dag.py <min> <max> [options value],... <pattern>
	
Example:
    
    python3 dag.py 5 7 --fill --save --out example.output --multiple mi^mi di@i%
    (example.output -> 55MB, 7116426 words)
	
Tips:
    
    min must be at least the size of pattern
    max must be at least as min
