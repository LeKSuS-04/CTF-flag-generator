#!/usr/bin/python3

import json
import os
import shlex
import sys
import random

CONFIGFILENAME = 'config.json'
CONFIGFILEPATH = "/".join(os.path.realpath(__file__).split('/')[:-1]) + '/'
OUTPUTTOFILE = False
OUTPUTFILENAME = ''

PREFIX = ''
POSTFIX = ''
ALWAYSCHANGE = dict()
SOMETIMESCHANGE = dict()
CHANGECASE = False
SETCASE = 'lower'

HelloMessage = '''
#################################
#                               #
#     @@@@    @@@@@    @@@@     #
#    @          @      @        #
#    @          @      @@@      #
#    @          @      @        #
#     @@@@      @      @        #
#                               #
#  F L A G   G E N E R A T O R  #
#################################
                   brought to you
                        by LeKSuS
'''
HelpMessage = '''
ctfgen - tool for generating CTF flags.
Usage: ctfgen [options] [flags]
    * You can provide multiple flags;
    * Everything from the first parameter that cannot be interpreted as option will be interpreted as flags.

Options:
    -c, --count         <integer>   Amount of variations generated for each flag. Set to 1 by default;
    -f, --file          <file>      Read flags from file. Each line will be interpreted as separate flag;
    -h, --help                      Display this help message;
    -i, --interactive               Run in interactive mode;
    -o, --output        <file>      Redirect output into file instead of console;
    -s, --settings      <file>      Provide custom configuration file (you can modify standart instead).

Examples:
    ctfgen this is flag         | Generates three flags, from "this", "is" and "flag"
    ctfgen "this is flag"       | Generates flag from string "this is flag"
    ctfgen -c 15 yoooooooo      | Generates 15 random flags from "yoooooooo"
    ctfgen -c 4 -f input.txt -o flags.txt   | Generates 4 random flags from each line from input.txt file 
                                            | and outputs them into flags.txt
    ctfgen -s ~/custom.json "Hello, world!" | Generates flag from "Hello, world!" using rules from ~/custom.json

Configuration file:
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
    }                                   |       * random    - mix of both cases
'''
InteractiveHelpMessage = '''
ctfgen - tool for generating CTF flags.
You're in interactive mode. To transform anything to flag, just type it in

Command list:
    options                                 List all settings variables;
    set <variable name|id> <value>          Assign new value to variable;

    write <file>                            Redirect output to file instead of console;
    console                                 Redirect output back to console;
    clearoutput                             Clear output file;
    read <file>                             Read flags from file. Each line will be
                                            interpreted as separate flag;

    help                                    Display this help message;
    exit                                    Exit interactive mode;
'''

def read_config(file = CONFIGFILEPATH + CONFIGFILENAME):
    global PREFIX, POSTFIX, ALWAYSCHANGE, SOMETIMESCHANGE, CHANGECASE, SETCASE
    with open(file, 'r') as f:
        try:
            conf = json.loads(f.read())
        except:
            print('Error while reading configuration file')

        try:
            PREFIX = conf['Prefix']
            POSTFIX = conf['Postfix']
            ALWAYSCHANGE = conf['AlwaysChange'][0]

            SOMETIMESCHANGE = conf['SometimesChange'][0]

            CaseSettings = conf['CaseSettings'][0]
            CHANGECASE = CaseSettings['ChangeCase']
            SETCASE = CaseSettings['SetCase'].lower()
        except KeyError as e:
            raise ValueError("Wrong configuration file format:", e)

def write_config():
    save = {
        "Prefix" : PREFIX,
        "Postfix" : POSTFIX,
        "AlwaysChange" : [ALWAYSCHANGE],
        "SometimesChange" : [SOMETIMESCHANGE],
        "CaseSettings" : [{
            "ChangeCase" : CHANGECASE,
            "SetCase" : SETCASE
        }]
    }
    with open(CONFIGFILENAME, 'w') as f:
        f.write(json.dumps(save, indent=4, sort_keys=True))



def modify(string):
    letters = list(string.lower())

    i = 0
    while i < len(letters):
        if letters[i] in ALWAYSCHANGE:
            if len(ALWAYSCHANGE[letters[i]]) < 1:
                raise ValueError(f'No matches for letter {letters[i]} in AlwaysChange section of configuration file')
            else:
                variants = ALWAYSCHANGE[letters[i]].copy()
                new_letters = random.choice(variants)
                del letters[i]
                
                for c in new_letters[::-1]:
                    letters.insert(i, c)
        
        if letters[i] in SOMETIMESCHANGE:
            if len(SOMETIMESCHANGE[letters[i]]) < 1:
                raise ValueError(f'No matches for letter {letters[i]} in SometimesChange section of configuration file')
            else:
                variants = SOMETIMESCHANGE[letters[i]].copy()
                variants.append(letters[i])
                letters[i] = random.choice(variants)
        
        if CHANGECASE and letters[i].isalpha():
            if SETCASE == "lower":
                letters[i] = letters[i].lower()
            elif SETCASE == "upper":
                letters[i] = letters[i].upper()
            elif SETCASE == "random":
                letters[i] = random.choice([letters[i].upper(), letters[i].lower()])
            else:
                raise ValueError(f'SetCase value from configuration file doesn\'t match any of given options.\n' +
                                 f'Possible options: upper, lower, random;\n' +
                                 f'Given option: {SETCASE}')
        
        i += 1

    return PREFIX + "".join(letters) + POSTFIX



def output(flag):
    if OUTPUTTOFILE:        
        with open(OUTPUTFILENAME, 'a') as f:
            f.write(modify(flag) + '\n')
    else:
        print(modify(flag))




def interactive():
    global OUTPUTTOFILE, OUTPUTFILENAME, PREFIX, POSTFIX, ALWAYSCHANGE, SOMETIMESCHANGE, CHANGECASE, SETCASE

    print(HelloMessage)
    print(InteractiveHelpMessage)

    msg = ''
    while msg not in ['quit', 'exit']:
        msg = input(' > ').strip().lower()

        if msg == 'options':
            print(f" ID |     Name        |              Value                        \n" +
                  f"====|=================|===========================================\n" +
                  f"  0 | Prefix          | {PREFIX}" +(42-len(PREFIX))*" "+         "\n" +
                  f"  1 | Postfix         | {POSTFIX}" +(42-len(POSTFIX))*" "+       "\n" +
                  f"  2 | ChangeCase      | {CHANGECASE}" +(42-len(str(CHANGECASE)))*" "+ "\n" +
                  f"  3 | SetCase         | {SETCASE}" +(42-len(SETCASE))*" "+       "\n" +
                  f"    |                 |                                           \n" +
                  f"  - | AlwaysChange    | This options can be viewed and            \n" +
                  f"  - | SometimesChange | edited only in configuration file         ")
        elif msg.startswith('set'):
            args = shlex.split(msg)

            if args[1] in ['0', 'prefix']:
                PREFIX = args[2]
            elif args[1] in ['1', 'postfix']:
                POSTFIX = args[2]
            elif args[1] in ['2', 'changecase']:
                if args[2] in ['0', 'false']:
                    CHANGECASE = False
                else:
                    CHANGECASE = True
            elif args[1] in ['3', 'setcase']:
                if args[2] in ['lower', 'upper', 'random']:
                    SETCASE = args[2]
                else:
                    print(f'SetCase can be only set to "upper", "lower" or "random"; given option: "{args[2]}"')
            write_config()
        elif msg.startswith('write'):
            args = shlex.split(msg)

            OUTPUTTOFILE = True
            OUTPUTFILENAME = args[1]
        elif msg == 'console':
            OUTPUTTOFILE = False
        elif msg == 'clearoutput':
            if os.path.isfile(OUTPUTFILENAME):
                open(OUTPUTFILENAME, 'w').close()
            else:
                print('Sorry, I can\'t clear something non-existing!')

        elif msg == "help":
            print(InteractiveHelpMessage)

        elif msg in ["exit", "quit"]:
            ... ### Do nothing

        elif msg.startswith("read"):
            args = shlex.split(msg)

            if os.path.isfile(args[1]):
                with open(args[1], 'r') as f:
                    flag = f.readline().replace('\n', '')
                    while flag:
                        output(flag)
                        flag = f.readline().replace('\n', '')
            else:
                print("Given path doesn't exist or isn't a file")
        else:
            output(msg)

            

if __name__ == '__main__':
    read_config()

    if len(sys.argv) == 1 or (len(sys.argv) == 2  and sys.argv[1].lower in ['-i', '--interactive']):
        interactive()
    elif len(sys.argv) == 2  and sys.argv[1].lower in ['-h', '--help']:
        print(HelpMessage)
    else:
        flags_from = 1
        repeat = 1

        read_from_file = False
        input_file_name = ''

        flags = ['-c', '--count', '-f', '--file', '-o', '--output', '-s', '--settings']

        while flags_from < len(sys.argv):
            if sys.argv[flags_from] in flags:
                if sys.argv[flags_from] in ['-c', '--count']:
                    count = sys.argv[flags_from + 1]

                    try:
                        repeat = int(count)
                    except:
                        raise ValueError(f'Error: exspected integer after -c flag; got {count}')

                elif sys.argv[flags_from] in ['-f', '--file']:
                    file = sys.argv[flags_from + 1]

                    if os.path.isfile(file):
                        read_from_file = True
                        input_file_name = file
                    else:
                        raise ValueError("Error: Path to input file doesn't exist or isn't a file")

                elif sys.argv[flags_from] in ['-o', '--output']:
                    OUTPUTTOFILE = True
                    OUTPUTFILENAME = sys.argv[flags_from + 1]
                    open(OUTPUTFILENAME, 'w').close()

                elif sys.argv[flags_from] in ['-s', '--settings']:
                    read_config(sys.argv[flags_from + 1])

                flags_from += 2
            else:
                break
        
        if read_from_file:
            with open(input_file_name, 'r') as f:
                flag = f.readline().replace('\n', '')
                while flag:
                    for i in range(repeat):
                        output(flag)

                    flag = f.readline().replace('\n', '')
        else:
            while flags_from < len(sys.argv):
                flag = sys.argv[flags_from]
                flags_from += 1

                for i in range(repeat):
                    output(flag)