import json


class Pattern:
    def __init__(self, pattern: str) -> None:
        with open(f'../../data_files/samples/{pattern}/{pattern}.json', 'r', encoding='utf8') as file:
            self.logic = json.load(file)
            self.pattern = pattern
        print(self.logic)



Pattern('authorization')


