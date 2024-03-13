from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str

    @staticmethod
    def get_schema():
        return '''{
            "type": "record",
            "name": "User",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "name", "type": "string"},
                {"name": "email", "type": "string", "default": ""}
            ]
        }'''