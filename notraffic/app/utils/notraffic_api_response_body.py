import json


class NotrafficApiResponseBody:
    def __init__(self, data, errors):
        self.data = data
        self.errors = errors

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
