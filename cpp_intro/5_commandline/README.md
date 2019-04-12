# Commandline Arguments

Change the main function of our executable,
so that the user can provide an argument
on the commandline for which fibonacci number should be printed


## Hints

* `std::stoi`
* Signature of main must now be: `int main(int argc, char* argv[])`,
  first is the number of arguments, the second is the array of 
  C-Strings (`char*`) with the arguments

## Bonus

* Give a nice error message if the user gives a wrong number of arguments
* Give a nice error message, if the argument is not convertible to an int
* Show what the program does when given `--help`
