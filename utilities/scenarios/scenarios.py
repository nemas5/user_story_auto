import json
import os
from typing import Optional

import docx
from docxcompose.composer import Composer

from utilities.patterns import Pattern, pattern_list
from db.storage import get_scenario, get_scenario_subs, get_scenario_mains
from db.connection import get_session


db_session = get_session()


class Scenario:
    def __init__(self, scenario=None) -> None:
        self.subs = dict()
        self.mains = dict()
        self.name = ''
        if scenario is None:
            for pattern in pattern_list:
                self.mains[pattern.pattern] = 0
                for sub in pattern.data.keys():
                    self.subs[sub] = 0
        elif isinstance(scenario, int):
            scenario = get_scenario(scenario, db_session)
            mains = get_scenario_mains(scenario[0], db_session)
            self.mains = {mains[i][2]: mains[i][1] for i in range(len(mains))}
            self.subs = dict()
            self.name = scenario[1]
            for main in mains:
                subs = get_scenario_subs(main[0], db_session)
                self.subs[main[2]] = {subs[i][2]: subs[i][1] for i in range(len(subs))}
        else:
            self.name = scenario["name"]
            self.mains = scenario["mains"]
            self.subs = scenario["subs"]
            print(scenario)

    def build_docx(self, user):
        doc = docx.Document()
        composer = Composer(doc)
        doc.add_heading(self.name, 0)
        for pattern in pattern_list:
            print(pattern.pattern, pattern.name)
            if self.mains[pattern.pattern] == 1:
                doc.add_heading(pattern.name, 1)
                for sub in self.subs[pattern.pattern].keys():
                    if self.subs[pattern.pattern][sub] == 1:
                        doc.add_heading(pattern.data[sub]["name"], 2)
                        composer.append(pattern.data[sub]["doc"])
        doc.save(f'data_files/user_data/{user}/{self.name}.docx')
