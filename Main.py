import sys
from fileinput import filename

from Parser import *
from Executer import Executer


# Main entry of the application
# determines the queries and runs them
def main(argv):
    # Load the program
    # - variables
    # - make sure DBMS folder exists
    # - settings
    # - parser
    settings = {"database": None}
    parser = Parser()
    execute = Executer()

    # reading inputs from file
    # inputs is a list that includes the ';'
    file_detected = len(argv) > 1
    if file_detected:
        file_path = argv[1]
        try:

            with open(file_path, 'r') as file:
                inputs = file.readlines()

        except filename:

            print("Invalid file path.")

        else:

            for inp in inputs:
                if parser.validate_syntax(inp):
                    pass

    # manual command/query input in the terminal
    else:
        while True:
            inputs = input()

    # while True:
    #     inp = input()
    #
    #     if inp.strip() == ".EXIT":
    #         print("\nAll done")
    #         break
    #     if inp.strip()[0:2] == "--":
    #         continue
    #
    #     parser = Parser()
    #     executer = Executer()
    #     for line in inp.strip().split(';')[:-1]:
    #         inp_line = line + ";"
    #         tokens = parser.tokenize(inp_line.lower())
    #         # print(tokens)
    #         if parser.validate_syntax(tokens) and parser.validate_query(tokens):
    #             query = executer.generate_context(tokens, settings)
    #             executer.run(query)
    #         else:
    #             print("!Error: invalid syntax detected.")


if __name__ == "__main__":
    main(sys.argv)
