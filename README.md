# Calculus Constructio
A programming language involving the construction of lines, circles, polynomial and parametric curves, and intersections.

To execute, run `python main.py` along with the necessary arguments below.
## Links
* [Esolangs.org entry](https://esolangs.org/wiki/Calculus_Constructio#List_of_instructions)
## Command line arguments
### `-p`, `--program`
Insert the file path to the program here.
### `-f`, `--flag`
Insert the flag here, as an integer. The flags are in the binary representation of the integer.
#### List of flags
* `UseUnicodeInput` means that the input is given as a string of Unicode characters, and is translated into a list of points with x coordinates corresponding to the indices of the characters in the string. It has a value of 1.
* `UseUnicodeOutput` means the same thing as UseUnicodeOutput, except it is done in reverse, and only affects output that has been assigned to the `output` variable. It has a value of 2. It is incompatible with `OutputAllVars`.
* `OutputAllVars` means the program will output the value of all the variables when the program is finished executing, as a dictionary. It has a value of 4. It is incompatible with `UseUnicodeOutput`.

Multiple flags can be passed on by adding these values together.
### `-i` `--input`
Insert the file path to the input here. If your program does not require input, you may omit this completely.

## Programs
### Syntax
Each program is a series of newline separated instructions. Each instruction looks like this:

`variable_name:instruction arg,arg,...`

* The `instruction` is applied...
* ...to the `arg,arg,...` (arguments), which must be variables...
* ...and the result is assigned to the variable called `variable_name`.

### Constants
There are two default constants that every module, function and program has access to:
* `zero`, which is the point (0, 0).
* `one`, which is the point (1, 0).

### Input
Input is given through the `input` variable. When no input is given, it will be an empty list.

### Output
The program can output through three ways:
* Assigning to the `output` variable: This is the preferred method as it is the only output method where flags are able to modify the output. The other two instructions are meant for debugging purposes. A program will error at the end if this variable has not been assigned to.
* The `Halt` or `H` instruction: This accepts one argument, prints the argument to `STDOUT`, and terminates the program, printing `Program has halted.` to STDERR.
* The `Print` or `>` instruction: This accepts one argument and prints the argument to `STDOUT`. It does not terminate the program.

### Valid Variable Names
All variable names are valid apart from those which contain `:`. Note that this also means that variables with zero-length names are valid (e.g. you can provide the arguments `,arg1,,arg2,` to an instruction, meaning the first, third, and last arguments are of the zero-length variable). It is also worth noting that it is possible to assign a value to variables containing `,`, but then these cannot be used inside arguments, as the comma will be interpreted as separating two variable names.

### Modules
Modules can be imported using the `Import` or `!` instruction, assigning it to a variable name. The only argument to it is the module name. It is given as a filepath, or as a relative directory (probably). You should omit the file extension, and it is assumed that it is a `.cns` file. Then, the functions and other things inside can be used as the variable `variable_name.function_or_other_variable_name`.

### Functions
Functions can be defined starting with the `Define` or `$` instruction, followed by its arguments as comma-separated names, assigning it to the variable name. The body of the function is just normal syntax, except the return value of the function should be assigned to the `return` variable. The function should be ended by using the same variable name with the `EndDefine` or `%` function, with no arguments following. Functions can be applied using the `Apply` or `Y` instruction. Functions must have at least one argument, however that argument can just be a dummy argument that isn't used if necessary. Functions cannot access any external variables apart from modules, other functions, and arguments passed in to it.

### Types
Here is a list of types and what they mean:
* A `CModule` represents a module imported into a program. It is also what the main program is turned into before being run.
* A `CFunction` is a custom function defined in a program.
* A `List` is just a list.
* A `Construction` is an object created using points, or one of:
  * `Line`
  * `Circle`
  * `Polynomial`
  * `Parametric`

### List of instructions
It is worth noting that each instruction has a long form and a short form, and when a `Point` is given to a function that should seemingly accept a number, the number is taken from the point's x coordinate.

| Long Form    | Short Form | Arguments                           | Behaviour Description                                                                                                                                                         |
|--------------|------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Line`       | `L`        | `Point, Point`                      | Constructs a line from the two given points. Can sometimes be treated as a line segment.                                                                                      |
| `Circle`     | `C`        | `Point, Point`                      | Constructs a circle, with the center as the first point, and the second point being on the circumference.                                                                     |
| `Intersect`  | `X`        | `Construction, Construction`        | Returns a list of points where the two constructions intersect.                                                                                                               |
| `Unfurl`     | `^`        | `Circle, Construction`              | Unfurls the circumference of a circle such that one end of the line touches the center of the circle and the other end touches a given construction.                          |
| `Collapse`   | `V`        | `Line, Point`                       | Collapses a line into a circle with the given point as its center.                                                                                                            |
| `Index`      | `I`        | `List, Point`                       | Returns the item in the list with the given index.                                                                                                                            |
| `Slice`      | `S`        | `List, Point, Point`                | Returns a slice of the list from the start index up to but not including the end index.                                                                                       |
| `Polynomial` | `P`        | `Point, ...`                        | Returns the minimal polynomial that goes through all the points.                                                                                                              |
| `Parametric` | `A`        | `Point, ...`                        | Returns the minimal parametric curve that gives the given points when t is equal to 0, 1, 2, etc.                                                                             |
| `Concat`     | `+`        | `List, Any`                         | Adds the value onto the list, if it is not a list. Otherwise, concatenates the lists together.                                                                                |
| `SwapXY`     | `~`        | `Point`                             | Returns another point with swapped X and Y coordinates.                                                                                                                       |
| `NewList`    | `*`        | `Any, ...`                          | Returns a new list containing all of the arguments.                                                                                                                           |
| `Apply`      | `Y`        | `CFunction, List`                   | Applies the function, with the given list as arguments to that function.                                                                                                      |
| `Closer`     | `@`        | `Point, Point, Point`               | Returns which of the last two points is closer to the first point.                                                                                                            |
| `Equal`      | `=`        | `Any, Any`                          | Returns if the two objects are equal.                                                                                                                                         |
| `ToList`     | `/`        | `Point \| Construction`             | If it is a point, returns a list with the X and Y coordinates, as two points with those as X coordinates. If it is a construction, returns a list of the points that form it. |
| `ToPoint`    | `.`        | `List`                              | Returns a point with the X and Y coordinates given in the list, taken from the X coordinates of the two points in the list.                                                   |
| `If`         | `?`        | `Point, CFunction, CFunction, List` | If the given point is truthy (non-zero X coordinate), applies the first function to the given arguments, otherwise, applies the second function to the given arguments.       |
| `While`      | `W`        | `CFunction, CFunction, List`        | While the second function returns a truthy value for the current list, changes the current list to a new list from the result of applying the first function to the old list. |
| `Transfer`   | `T`        | `Any`                               | Returns the value given to it, intended for if you need to set a variable equal to another variable.                                                                          |
| `Halt`       | `H`        | `Any`                               | Prints the given value to STDOUT, prints `Program has halted.` to STDERR, and terminates the program. Useful for debugging.                                                   |
| `Print`      | `>`        | `Any`                               | Prints the given value to STDOUT. Does not terminate the program. Useful for debugging.                                                                                       |
