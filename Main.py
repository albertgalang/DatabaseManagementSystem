import sys
from fileinput import filename

from Parser import Parser
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


    file_detected = len(argv) > 1
    if file_detected:
        file_path = argv[1]
        try:
            with open(file_path, 'r') as file:
                inputs = file.readlines()
        except FileNotFoundError:
            print("Invalid file path.")
        else:
            for inp in inputs:
                if inp.strip().lower() == ".exit":
                    print("All done.")
                    return

                if inp[0] == '-':
                    continue

                # build input
                if parser.validate(inp) is False:
                    continue

                query = parser.query
                parser.clean()  # remove saved query in parser

                query = parser.parse(query)
                context = execute.create_context(query, settings)
                result = context["run"](*context["params"])
                if result:
                    print(result.to_string())
    else:
        while True:
            inp = input()

            if inp.lower() == ".exit":
                print("All done.")
                break

            # build input
            if parser.validate(inp) is False:
                continue

            query = parser.query
            parser.clean()  # remove saved query in parser

            query = parser.parse(query)
            context = execute.create_context(query, settings)
            result = context["run"](*context["params"])
            if result:
                print(result.to_string())


if __name__ == "__main__":
    main(sys.argv)
