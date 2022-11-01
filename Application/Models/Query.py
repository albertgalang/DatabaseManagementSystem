# Query types allows to organize different queries.
# This also eases the mapping of execution.

from Application.Commands.Commands import data_access_commands, data_change_commands


class Metadata:
    def __init__(self, query_type, entity, title, params):
        self.query_type = query_type
        self.entity = entity
        self.title = title
        self.params = params


class DataAccess:
    def __init__(self, select_key, from_key, where_key, group_key, order_key):
        self.select_key = select_key
        self.from_key = from_key
        self.where_key = where_key
        self.group_key = group_key
        self.order_key = order_key


class DataChange:
    def __init__(self, change_type, set_key, from_key, where_key):
        self.change_type = change_type
        self.set_key = set_key
        self.from_key = from_key
        self.where_key = where_key


class Insert:
    def __init__(self, title, values):
        self.title = title
        self.values = values


primitives = ["int", "float"]
primitives_expects_param = ["varchar", "char"]
actions = ["add", "and"]


# Builds a query type.
# Returns a query type with the appropriate values.
def query_builder(tokens, query_type):
    if query_type is "metadata":
        qt, e, t, p = (None,) * 4

        if tokens[0] == "use":
            qt = tokens[0]
            t = tokens[1]

        if tokens[0] == "create" or tokens[0] == "drop":

            qt = tokens[0]
            e = tokens[1]
            t = tokens[2]
            if len(tokens[:-1]) > 3:
                p = get_params(tokens[4:-2])

        if tokens[0] == "alter":
            qt = tokens[0]
            e = tokens[1]
            t = tokens[2]
            p = [tokens[3]]  # action
            p += get_params(tokens[4:-1])

        return Metadata(qt, e, t, p)

    if query_type is "dataAccess":
        f, w, g, o, s = (None,) * 5

        s = []
        for token in tokens[1:]:
            if token in data_access_commands:
                break
            s.append(token)

        f = []
        from_param_start = tokens.index("from") + 1
        for token in tokens[from_param_start:-1]:
            if token in data_access_commands:
                break
            f.append(token)

        try:
            w = []
            where_param_start = tokens.index("where") + 1
            # w.append(tokens[where_param_start:-1].join(' '))
            for token in tokens[where_param_start:]:
                if token is "'":
                    continue
                if token is ';':
                    break
                w.append(token)
        except:
            pass

        return DataAccess(s, f, w, g, o)

    if query_type is "dataChange":
        ct, s, f, w = (None,) * 4

        ct = tokens[0]
        if ct == "update":
            f = tokens[1]
            s = []
            set_param_index = tokens.index("set") + 1
            for token in tokens[set_param_index:]:
                if token is "'":
                    continue
                if token in data_change_commands:
                    break
                s.append(token)
        if ct == "delete":
            f = tokens[2]

        w = []
        where_param_start = tokens.index("where") + 1
        for token in tokens[where_param_start:]:
            if token is "'":
                continue
            if token is ';':
                break
            w.append(token)

        return DataChange(ct, s, f, w)

    if query_type is "insert":

        t = tokens[2]
        v = []
        append = True
        quotes = 0
        values_param_start = tokens.index("values") + 1
        for token in tokens[values_param_start:]:
            if token is ';':
                break
            if token is '(' or token is ')':
                continue
            if token is "'":
                continue
                # if quotes is 0:
                #     quotes += 1
                #     v.append(token)
                #     append = False
                #     continue
                # if quotes is not 0:
                #     quotes -= 1
                #     v[-1] += token
                #     append = True
                #     continue
            if append:
                v.append(token)
            else:
                v[-1] += token

        return Insert(t, v)


# retrieves parameters from () encapsulated values.
# isolates from the higher level parameters.
def get_params(tokens):
    p = []
    append = True
    parenthesis = 0
    for token in tokens:
        if append:
            p.append(token)
            append = False
        else:
            if token in primitives:
                p[-1] += f" {token}"
                append = True
                continue
            if token in primitives_expects_param:
                p[-1] += f" {token}"
                append = False
                continue
            if token is '(':
                p[-1] += token
                parenthesis += 1
                continue
            if token is ')':
                p[-1] += token
                parenthesis -= 1
                if parenthesis is 0:
                    append = True
                continue
            p[-1] += token
    return p
