# Utils functions. Simple reusable function belong here.
# Also helps to declutter code.


# Removes whitespaces.
# Will eventually target a regular string or a query.
def clean(target, target_type):
    if target_type == "query":
        pass
    if target_type == "string":
        return clean_string(target)
        pass

# Testing
def clean_string(query):
    return query.strip()