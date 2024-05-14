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
        pref = f'../../data_files/samples/{self.pattern}'
        logic = get_pattern(self.pattern, db_session)
        self.data = dict()

        for i in logic.keys():
            doc = docx.Document(os.path.join(pref, f'{i}.docx'))
            self.data[i] = dict()
            self.data[i]["doc"] = doc
            self.data[i]["name"] = logic[i]
        print(self.data)


pattern_list = list()
for patt in get_pattern_list(db_session):
    pattern_list.append(Pattern(patt))
print(pattern_list[0].data)

