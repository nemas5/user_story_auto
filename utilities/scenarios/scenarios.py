import json
import os
from typing import Optional

import docx
from utilities.patterns import Pattern, pattern_list
from db.storage import get_scenario, get_scenario_subs, get_scenario_mains
from db.connection import get_session


db_session = get_session()


class Scenario:
    def __init__(self, scenario: Optional[int] = None) -> None:
        self.subs = dict()
        self.mains = dict()
        if scenario is None:
            for pattern in pattern_list:
                self.mains[pattern.pattern] = 0
                for sub in pattern.data.keys():
                    self.subs[sub] = 0
        else:
            scenario = get_scenario(scenario, db_session)
            print(scenario)
            mains = get_scenario_mains(scenario[0], db_session)
            self.mains = {mains[i][2]: mains[i][1] for i in range(len(mains))}
            self.subs = dict()
            for main in mains:
                subs = get_scenario_subs(main[0], db_session)
                self.subs[main[2]] = {subs[i][2]: subs[i][1] for i in range(len(subs))}
        print(self.subs, self.mains)


Scenario(1)
