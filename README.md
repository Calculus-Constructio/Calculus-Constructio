# Calculus Constructio
A programming language involving the construction of lines, circles, polynomial and parametric curves, and intersections.

## Installation
```
pip install git+https://github.com/Calculus-Constructio/Calculus-Constructio.git
``` 
## Execution
```
calculus_constructio -p PROGRAM -i INPUT -f FLAGS
```
## Links
* [Esolangs.org entry](https://esolangs.org/wiki/Calculus_Constructio#List_of_instructions)
* [Online interpreter](https://calculus-constructio-web.onrender.com/)
## Command line arguments
### `-p`, `--program`
Insert the file path to the program here.
### `-f`, `--flag`
Insert the flag here, as an integer. The flags are in the binary representation of the integer.
#### List of flags
* `UseUnicodeInput` means that the input is given as a string of Unicode characters, and is translated into a list of points with x coordinates corresponding to the indices of the characters in the string. It has a value of 1.
* `UseUnicodeOutput` means the same thing as UseUnicodeInput, except it is done in reverse, and only affects output that has been assigned to the `output` variable. It has a value of 2. It is incompatible with `OutputAllVars`.
* `OutputAllVars` means the program will output the value of all the variables when the program is finished executing, as a dictionary. It has a value of 4. It is incompatible with `UseUnicodeOutput`.

Multiple flags can be passed on by adding these values together.
### `-i` `--input`
Insert the file path to the input here. If your program does not require input, you may omit this completely.

## Programs
See the entry on esolangs.org please.
