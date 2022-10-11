from Application.Commands.Commands import *


# Executer class
# Adds execution context to the parsed query.
# This allows for function mapping based on commands and its respective parameters.
class Executer:
    def __int__(self):
        pass

    # Generates the execution context of the parsed queries.
    # Returns an organized function calls blueprint.
    def generate_context(self, tokens, settings):
        context = {}
        self.command_context[tokens[0]](self, tokens, context, settings)
        return context

    # runs the generated execution context
    def run(self, query):
        for key, value in query.items():
            params = value["params"]
            value["run"](*params)

    # create command execution context
    def create_command_context(self, tokens, context, settings):
        if tokens[1] == "database":
            context["create"] = {
                "run": create_database,
                "params": [tokens[2], settings]
            }
        elif tokens[1] == "table":
            expects_command = ["create", "drop", "alter", "use"]
            expects_params = ["database", "table"]
            data_access = ["select", "from", "add"]

            prev_command = ""
            command = ""
            params = ""
            for token in tokens[2:]:
                if token in expects_command:
                    prev_command = token
                elif tokens in expects_params:
                    command = token
                elif token in data_access:
                    command += token + ' '
                elif token == ";":
                    continue
                else:
                    params += token + " "

            context["create"] = {
                "run": create_table,
                "params": [params, settings["database"]] # title, columns, database
            }

        # if tokens[3] is not ';':
        #     self.command_context[tokens[3]](self, tokens[3:], context, settings)

    # drop command execution context
    def drop_command_context(self, tokens, context, settings):
        if tokens[1] == "database":
            context["drop"] = {
                "run": drop_database,
                "params": [tokens[2], settings]
            }
        elif tokens[1] == "table":
            context["drop"] = {
                "run": drop_table,
                "params": [tokens[2], settings]
            }

    # use command execution context
    def use_command_context(self, tokens, context, settings):
        context["use"] = {
            "run": use_database,
            "params": [tokens[1], settings]
        }

    # select command execution context
    def select_command_context(self, tokens, context, settings):
        context["select"] = {
            "run": table_query,
            "params": [tokens[1], tokens[3], settings]
        }

    # database command execution context
    def database_command_context(self, tokens, context, settings):
        pass

    # alter command execution context
    def alter_command_context(self, tokens, context, settings):
        expects_command = ["create", "drop", "alter", "use"]
        expects_params = ["database", "table"]
        data_access = ["select", "from", "add"]

        prev_command = ""
        command = ""
        params = ""
        for token in tokens[3:]:
            if token in expects_command:
                prev_command = token
            elif tokens in expects_params:
                command = token
            elif token in data_access:
                command += token + ' '
            elif token == ";":
                continue
            else:
                params += token + " "

        context["alter"] = {
            "run": alter_table,
            "params": [tokens[2], params.strip(), settings]
        }


    # command context generator function delegate
    command_context = {
        "table": None,
        "select": select_command_context,
        "database": None,
        "from": None,
        "create": create_command_context,
        "drop": drop_command_context,
        "alter": alter_command_context,
        "use": use_command_context
    }