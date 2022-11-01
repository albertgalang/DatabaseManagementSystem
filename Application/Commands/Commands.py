import json
import os

from Application.Models.Table import Table, serialize, deserialize
from Application.Variables import DBMS_PATH

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
    "from",
    "where",
    # "update",
    # "insert"
]
expects_params_commands = [
    "table",
    "database"
    "select",
    "from",
    "add"
]

metadata_commands = [
    "create",
    "drop",
    "alter",
    "use"
]

data_change_commands = [
    "update",
    "delete",
    "set",
    "where"
]

insert_commands = [
    "insert",
    "into",
    "values"
]

# data access query execution
def data_access(query, settings):
    if settings["database"] is None:
        print("No database being used.")
        return

    # from
    table = get_table(query.from_key, settings)

    # where
    if query.where_key is not None and query.where_key != []:
        inequalities = {
            "=": equal,
            "!=": not_equal,
            ">": greater_than,
            "<": less_than
        }
        aggregated_records = []
        key = query.where_key[0]
        ineq = query.where_key[1]
        b = query.where_key[2]
        key_index = list(table.metadata).index(key)
        for record in table.records:
            a = record[key_index]
            if inequalities[ineq](a, b):  # if true
                aggregated_records.append(record)

    if query.select_key[0] is not '*':
        keys = []
        for column in query.select_key:
            column_index = list(table.metadata).index(column)
            keys.append(column_index)

        final_table = []
        for record in aggregated_records:
            transformed_record = []
            for key in keys:
                transformed_record.append(record[key])
            final_table.append(transformed_record)

        new_metadata = {}
        for column in query.select_key:
            new_metadata[column] = table.metadata[column]

        return Table(new_metadata, final_table)

    # return original table if no select/where
    return table

# check inequality functions below
def equal(a, b):
    return a == b
    pass

def not_equal(a, b):
    return a != b
    pass

def greater_than(a, b):
    return float(a) > float(b)

def less_than(a, b):
    return float(a) < float(b)


# update type query execution
def update(query, settings):
    if settings["database"] is None:
        print("No database being used.")
        return

    table = get_table([query.from_key], settings)

    # where
    if query.where_key is not None and query.where_key != []:
        inequalities = {
            "=": equal,
            "!=": not_equal,
            ">": greater_than,
            "<": less_than
        }
        counter = 0
        key = query.where_key[0]
        ineq = query.where_key[1]
        b = query.where_key[2]
        key_index = list(table.metadata).index(key)
        set_key = query.set_key[0]
        set_key_index = list(table.metadata).index(set_key)
        for record in table.records:
            a = record[key_index]
            if inequalities[ineq](a, b):
                counter += 1
                record[set_key_index] = query.set_key[2]

        database = settings["database"]
        table_title = query.from_key
        with open(f"DBMS/{database}/{table_title}.txt", "w") as table_file:
            table_file.write(json.dumps(serialize(table)))

        print(f"{counter} {'records' if counter > 1 else 'record'} modified.")


# delete type query execution
def delete(query, settings):
    if settings["database"] is None:
        print("No database being used.")
        return

    table = get_table([query.from_key], settings)

    # where
    if query.where_key is not None and query.where_key != []:
        inequalities = {
            "=": equal,
            "!=": not_equal,
            ">": greater_than,
            "<": less_than
        }
        counter = 0
        new_records = []
        key = query.where_key[0]
        ineq = query.where_key[1]
        b = query.where_key[2]
        key_index = list(table.metadata).index(key)
        for record in table.records:
            a = record[key_index]
            if inequalities[ineq](a, b):
                counter += 1
                continue
            new_records.append(record)

        database = settings["database"]
        table_title = query.from_key
        new_table = Table(table.metadata, new_records)
        with open(f"DBMS/{database}/{table_title}.txt", "w") as table_file:
            table_file.write(json.dumps(serialize(new_table)))

        print(f"{counter} {'records' if counter > 1 else 'record'} deleted.")


# insert type query execution
def insert(query, settings):
    if settings["database"] is None:
        print("No database being used.")
        return

    table_title = query.title
    table = get_table([table_title], settings)
    table.records.append(query.values)

    database = settings["database"]
    os.system(f"cd {DBMS_PATH}/{database} && touch {table_title}.txt")
    with open(f"DBMS/{database}/{table_title}.txt", "w") as table_file:
        table_file.write(json.dumps(serialize(table)))
    print("1 new record inserted.")


# retrieve table
def get_table(table, settings):
    database = settings["database"]
    check_path = os.path.abspath(f"{DBMS_PATH}/{database.strip()}/{table[0]}.txt")
    is_exist = os.path.exists(check_path)
    if is_exist:
        with open(f"./DBMS/{database.strip()}/{table[0]}.txt") as table:
            table_serialized = json.load(table)
            table = deserialize(table_serialized)
        return table


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


def create_table(title, params, settings):
    if settings["database"] is None:
        print("No database being used.")
        return

    database = settings["database"]
    table_title = title
    check_path = os.path.abspath(f"./DBMS/{database}/{table_title}.txt")
    is_exist = os.path.exists(check_path)
    if is_exist:
        print(f"!Failed to create table {table_title} because it already exist.")
        return

    columns = {}
    for param in params:
        data = param.split(' ')
        columns[data[0]] = data[1]

    table = Table(columns, [])

    os.system(f"cd DBMS/{database} && touch {table_title}.txt")
    with open(f"DBMS/{database}/{table_title}.txt", "w") as table_file:
        table_file.write(json.dumps(serialize(table)))
    print(f"Table {table_title} created.")


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

    check_path = os.path.abspath(f"{DBMS_PATH}/{database}/{title}.txt")
    is_exist = os.path.exists(check_path)
    if is_exist:
        with open(f"./DBMS/{database.strip()}/{title}.txt") as table:
            data = json.load(table)

        columns = {}
        prop_title = ""
        prop_type = ""
        for prop in params[1].split():
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