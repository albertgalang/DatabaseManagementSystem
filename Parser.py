from Application.Commands.Commands import commands, expects_params_commands, data_access_commands, database_entities
from Services.Utils import clean


# Parser class
# Used to parse the input and can organize and validate the queries.
class Parser:
    def __int__(self):
        pass

    # Breaks down input by tokens
    def tokenize(self, query):
        trimmed = []
        buffer = ""
        for char in query:
            if char == ' ':
                if not buffer:
                    continue
                else:
                    trimmed.append(buffer)
                    buffer = ""
            elif char == '(' or char == ')' or char == ';':
                if not buffer:
                    trimmed.append(char)
                else:
                    trimmed.append(buffer)
                    trimmed.append(char)
                    buffer = ""
            else:
                buffer += char

        if buffer:
            trimmed.append(buffer)
        for trim in trimmed:
            if ',' in trim:
                trimmed[trimmed.index(trim)] = trim.replace(',', '')
        return trimmed

    # validates the syntax of the input
    # def validate_syntax(self, tokens):
    #     if tokens[0] not in commands:
    #         return False
    #     if tokens[-1] is not ";":
    #         return False
    #
    #     open_parenthesis = 0
    #     for token in tokens[1:]:
    #         if token is "(":
    #             open_parenthesis += 1
    #         if token is ")":
    #             open_parenthesis -= 1
    #
    #     if open_parenthesis is not 0:
    #         return False
    #
    #     return True

    # Testing new validate
    # Validates the input commands
    # return true or false
    def validate(self, inputs):
        try:
            queries = self.get_queries(clean(inputs, "string"))
        except ValueError as e:
            print(f"Invalid syntax: {e}")
            return False
        pass

    def get_queries(self, inputs):
        queries = inputs.replace(";", ";%").split("%")

        if queries[-1] is not '':
            raise ValueError("Missing ';'")

        return queries[:-1]

    # Validates the actual query structure.
    def validate_query(self, tokens):
        for token in tokens:
            if token in expects_params_commands or token in commands:
                current_index = tokens.index(token)
                if self.validate_command[token](self, tokens[current_index:]) is False:
                    return False
        return True

    # validates the create command
    def validate_create_query(self, tokens):
        if tokens[1] in database_entities:
            return True
        else:
            return False

    # validates the drop command
    def validate_drop_query(self, tokens):
        if tokens[1] in database_entities:
            return True
        else:
            return False

    # validates the alter command
    def validate_alter_query(self, tokens):
        if tokens[1] not in database_entities:
            return False

        if tokens[3] not in expects_params_commands:
            return False


    # validates the table command
    def validate_table_query(self, tokens):
        params = tokens[1:]

        if params[0] in commands or params[0] in data_access_commands:
            return False
        if params[0] is "(" or params[0] is ")":
            return False

        primitives = ["int", "float", "varchar", "char"]
        primitives_expects_param = ["varchar", "char"]
        delay = False
        check_type = False
        open_parenthesis = 0
        for param in params[1:]:
            if param is "(":
                open_parenthesis += 1
                continue
            if param is ")":
                open_parenthesis -= 1
                if delay:
                    delay = False
            if open_parenthesis is 0:
                break
            if delay:
                continue
            if check_type:
                check_type = False
                if param not in primitives:
                    return False
                elif param in primitives_expects_param:
                    delay = True
            else:
                check_type = True

    # validates the select command
    def validate_select_query(self, tokens):
        if tokens[1] in commands:
            return False
        else:
            return True

    # validates the database command
    def validate_database_query(self, tokens):
        if tokens[1] in commands:
            return False
        else:
            return True

    # validates the from commmand
    def validate_from_query(self, tokens):
        if tokens[1] in commands:
            return False
        else:
            return True

    # validates the use command
    def validate_use_query(self, tokens):
        if tokens[1] in database_entities:
            return False
        else:
            return True

    # validates the add command
    def validate_add_query(self, tokens):
        primitives = ["int", "float", "varchar", "char"]
        primitives_expects_param = ["varchar", "char"]
        check_type = False
        delay = False
        open_parenthesis = 0
        for param in tokens[1:-1]:
            if param is "(":
                open_parenthesis += 1
                continue
            if param is ")":
                open_parenthesis -= 1
                check_type = False
                if delay:
                    delay = False
            if check_type:
                check_type = False
                if param not in primitives:
                    return False
                elif param in primitives_expects_param:
                    delay = True
            else:
                check_type = True

    # command validate function delagate
    validate_command = {
        "table": validate_table_query,
        "select": validate_select_query,
        "database": validate_database_query,
        "from": validate_from_query,
        "create": validate_create_query,
        "drop": validate_drop_query,
        "alter": validate_alter_query,
        "use": validate_use_query,
        "add": validate_add_query
    }
