import json
import os

import docx

from db.connection import get_session
from db.storage import get_pattern_list, get_pattern


db_session = get_session()


class Pattern:
    def __init__(self, pattern: list) -> None:

        self.pattern = pattern[0]
        self.name = pattern[1]
        pref = f'data_files/samples/{self.pattern}'
        logic = get_pattern(self.pattern, db_session)
        self.data = dict()
        self.data["id"] = self.pattern
        self.data["name"] = self.name

        for i in range(len(logic)):
            for j in range(len(logic[i]["components"])):
                doc = docx.Document(os.path.join(pref, logic[i]["components"][j]["doc"]))
                logic[i]["components"][j]["doc"] = doc
        self.data["components"] = logic


pattern_list = list()
for patt in get_pattern_list(db_session):
    pattern_list.append(Pattern(patt))
