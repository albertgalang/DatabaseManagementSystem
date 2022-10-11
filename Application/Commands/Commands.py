import json
import os

# STATIC variables
# used to check for command words
commands = [
    "create",
    "drop",
    "select",
    "alter",
    "use"
]
database_entities = [
    "table",
    "database"
]
data_access_commands = [
    "select",
    "from"
]
expects_params_commands = [
    "table",
    "database"
    "select",
    "from",
    "add"
]


# Selects the database to use
# Allows to switch databases if multiple exists
def use_database(params, settings):
    title = params
    check_path = os.path.abspath(f"./DBMS/{title}")
    is_exist = os.path.exists(check_path.strip())
    if is_exist:
        settings["database"] = title
        print(f"Using database {title}.")
    else:
        print(f"Database {title} does not exist.")


# Function to create a database
# It creates a folder inside DBMS
def create_database(title, settings):
    # check if database exist
    check_path = os.path.abspath(f"./DBMS/{title}")
    is_exist = os.path.exists(check_path.strip())
    if is_exist:
        print(f"!Failed to create database {title} because it already exists.")
    else:
        os.system(f'cd DBMS && mkdir {title}')
        settings["database"] = title
        print(f"Database {title} created.")

    # stream = os.popen('cd ')
    # print(stream.read())


# Deletes a database
# goes into DBMS folder and delete the database (folder) if it exist
def drop_database(title, settings):
    check_path = os.path.abspath(f"./DBMS/{title}")
    is_exist = os.path.exists(check_path.strip())
    if is_exist:
        os.system(f"rm -rf DBMS/{title}")
        print(f"Database {title} deleted.")
        if settings["database"] == title:
            settings["database"] = None
    else:
        print(f"Database {title} does not exist.")


# Creates a table in the selected database
# It creates a file with its data
def create_table(params, database):
    parameters = params.split()
    columns = {}
    prop_title = ""
    prop_type = ""
    for prop in parameters[1:]:
        if prop_title and prop_type:
            if prop_type == "varchar" or prop_type == "char":
                prop_type += f'({parameters[parameters.index(prop_type) + 2]})'
            columns[prop_title] = prop_type
            prop_title = ""
            prop_type = ""
        if prop != "(" and prop != ")":
            if not prop_title:
                prop_title = prop
            else:
                prop_type = prop

    if database:
        check_path = os.path.abspath(f"./DBMS/{database.strip()}/{parameters[0]}.txt")
        is_exist = os.path.exists(check_path)
        if is_exist:
            print(f"!Failed to create table {parameters[0]} because it already exist.")
        else:
            os.system(f'cd DBMS/{database.strip()} && touch {parameters[0]}.txt')
            with open(f'DBMS/{database.strip()}/{parameters[0]}.txt', 'w') as table:
                table.write(json.dumps(columns))
            print(f"Table {parameters[0]} created.")
    else:
        print("No database being used.")


# Deletes a table from the selected database
# Goes into the database folder and deletes the table file if it exists
def drop_table(params, settings):
    title = params.strip()
    if settings["database"]:
        check_path = os.path.abspath(f"./DBMS/{settings['database'].strip()}/{title}.txt")
        is_exist = os.path.exists(check_path)
        if is_exist:
            os.system(f"rm DBMS/{settings['database'].strip()}/{title}.txt")
            print(f"Table {title} deleted.")
        else:
            print(f"Failed to delete table {title} because it does not exist.")
    else:
        print("No database being used.")


# Modifies a table
# Opens the file in the selected database and modifies its metadata values
def alter_table(title, params, settings):
    database = settings["database"]

    if database is None or database is "":
        print("No database being used.")
        return

    check_path = os.path.abspath(f"./DBMS/{database.strip()}/{title}.txt")
    is_exist = os.path.exists(check_path)
    if is_exist:
        with open(f"./DBMS/{database.strip()}/{title}.txt") as table:
            data = json.load(table)


        columns = {}
        prop_title = ""
        prop_type = ""
        for prop in params.split():
            if prop_title and prop_type:
                if prop_type == "varchar" or prop_type == "char":
                    prop_type += f'({params.split()[params.split().index(prop_type) + 2]})'
                columns[prop_title] = prop_type
                prop_title = ""
                prop_type = ""
            if prop != "(" and prop != ")":
                if not prop_title:
                    prop_title = prop
                else:
                    prop_type = prop

            # params_split = params.split()
            # data[params_split[0]] = params_split[1]

        if len(columns) == 0:
            columns[prop_title] = prop_type
        for k, v in columns.items():
            data[k] = v
        os.system(f'cd DBMS/{database.strip()} && touch {title}.txt')
        with open(f'DBMS/{database.strip()}/{title}.txt', 'w') as table:
            table.write(json.dumps(data))
        print(f"Table {title} modified.")
    else:
        print(f"table {title} does not exist.")


# Query a table
# Allows to access the data inside a table from a database
# Works with Select command
def table_query(select_cond, from_table, settings):
    database = settings["database"]

    if database is None or database is "":
        print("No database being used.")
        return

    check_path = os.path.abspath(f"./DBMS/{database.strip()}/{from_table}.txt")
    is_exist = os.path.exists(check_path)
    if is_exist:
        with open(f"./DBMS/{database.strip()}/{from_table}.txt") as table:
            data = json.load(table)
            ss = ""
            for k, v in data.items():
                ss += f"{k} {v} | "
            print(ss[:-2])
    else:
        print(f"table {from_table} does not exist.")