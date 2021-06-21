# CTF flag generator

### Flexible tool for generation flags for CTFs
### Usage: 
    ctfgen [options] [flags]
    * You can provide multiple flags;
    * Everything from the first parameter that cannot be interpreted as option will be interpreted as flags.

### Options:
    -c, --count         <integer>   Amount of variations generated for each flag. Set to 1 by default;
    -f, --file          <file>      Read flags from file. Each line will be interpreted as separate flag;
    -h, --help                      Display this help message;
    -i, --interactive               Run in interactive mode;
    -o, --output        <file>      Redirect output into file instead of console;
    -s, --settings      <file>      Provide custom configuration file (you can modify standart instead).

### Examples:
    ctfgen this is flag         | Generates three flags, from "this", "is" and "flag"
    ctfgen "this is flag"       | Generates flag from string "this is flag"
    ctfgen -c 15 yoooooooo      | Generates 15 random flags from "yoooooooo"
    ctfgen -c 4 -f input.txt -o flags.txt   | Generates 4 random flags from each line from input.txt file 
                                            | and outputs them into flags.txt
    ctfgen -s ~/custom.json "Hello, world!" | Generates flag from "Hello, world!" using rules from ~/custom.json

### Configuration file:
    The configuration file must be named "config.json" and placed in the same directory as the script; Otherwise, you have to specify path to configuration file using --settings option.

    Configuration file is a JSON file with following structure:
    {
        "FlagPrefix" : "flag{",         | Prefix used to each flag;
        "FlagPostfix" : "}",            | Postfix used to each flag;
                                        | Prefix and postfix are not affected by following settings;
                                        |
                                        |
        "AlwaysChange" : [              | Dictionary of phrases that will always be changed ;
            {                           |
                "'" : [""],             | "'" symbol will be removed;
                " " : ["_", "-"],       | " " symbol will be changed randomly to "_" or "-".;
                "lol" : ["lul"]         | "lol" will be changed to "lul";
            }                           |
        ],                              | All rules in this section must be written in lower case;
                                        |
                                        |
        "SometimesChange" : [           | Dictionary of phrases that will sometimes be changed;
            {                           |
                "a" : ["4"],            | "a" symbol has a chance to be changed to "4";
                "b" : ["6"],            | "b" symbol has a chance to be changed to "6";
                "e" : ["3"],            | "e" symbol has a chance to be changed to "3";
                "g" : ["6", "9"],       | "g" symbol has a chance to be changed to "6" or "9";
                "i" : ["1"],            | "i" symbol has a chance to be changed to "1";
                "j" : ["1"],            | "j" symbol has a chance to be changed to "1";
                "l" : ["1"],            | "l" symbol has a chance to be changed to "1";
                "o" : ["0"],            | "o" symbol has a chance to be changed to "0";
                "q" : ["9"],            | "q" symbol has a chance to be changed to "9";
                "s" : ["5"],            | "s" symbol has a chance to be changed to "5";
                "t" : ["7"],            | "t" symbol has a chance to be changed to "7";
                                        |
                "for" : ["4"],          | "for" has a chance to be changed to "4";
                "to" : ["2"],           | "to" has a chance to be changed to "2";
                "ate" : ["8"]           | "ate" has a chance to be changed to "8";
            }                           |
        ],                              | All rules in this section must be written in lower case;
                                        |
                                        |
        "CaseSettings" : [              | Settings defining case of flag;
            {                           | 
                "ChangeCase" : true,    | Determines whether to change the case of given flag (true/false);
                "SetCase" : "random"    | If "ChangeCase" is set to true, this determines case
                                        | of genereated flag. Could be set to:
            }                           |       * lower     - only lowercase
        ]                               |       * upper     - only uppercase
    }