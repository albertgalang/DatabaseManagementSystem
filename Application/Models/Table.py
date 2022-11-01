class Table:
    def __init__(self, metadata, records):
        self.metadata = metadata
        self.records = records

    def to_string(self):
        header = ""
        for column in self.metadata:
            header += f"{column} {self.metadata[column]} | "
        header = header[:-2]
        header += '\n'

        records = ""
        for record in self.records:
            for data in record:
                records += f"{data} | "
            records = records[:-2]
            records += '\n'

        return header + records

def serialize(table):
    serialized = {
        "metadata": table.metadata,
        "records": table.records
    }
    return serialized

def deserialize(json):
    return Table(json["metadata"], json["records"])