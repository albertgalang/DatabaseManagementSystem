import sys
from Parser import *
from Executer import Executer


# Main entry of the application
# determines the queries and runs them
def main(argv):
    settings = {"database": None}
    while True:
        inp = input()

        if inp.strip() == ".EXIT":
            print("\nAll done")
            break
        if inp.strip()[0:2] == "--":
            continue

        parser = Parser()
        executer = Executer()
        for line in inp.strip().split(';')[:-1]:
            inp_line = line + ";"
            tokens = parser.tokenize(inp_line.lower())
            # print(tokens)
            if parser.validate_syntax(tokens) and parser.validate_query(tokens):
                query = executer.generate_context(tokens, settings)
                executer.run(query)
            else:
                print("!Error: invalid syntax detected.")


if __name__ == "__main__":
    main(sys.argv[0])
