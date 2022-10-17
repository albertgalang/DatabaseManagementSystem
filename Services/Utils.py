def clean(target, target_type):
    if target_type == "query":
        pass
    if target_type == "string":
        return clean_string(target)
        pass

def clean_string(query):
    return query.strip()