from csv import DictReader
from typing import List
from tqdm import tqdm
from pathlib import Path
from frs.utils import resolve
from functools import wraps

class Table:
    fieldnames = []
    enums = {}
    entity = None
    folder = "tab"
    filename = None
    delimiter = "\t"

    @staticmethod
    def parse(entity: dict, line: dict) -> dict:
        return NotImplementedError()

class Entity:
    def __init__(self):
        self.entries = {}

    @staticmethod
    def id(line: dict) -> int:
        return NotImplementedError()

class Person(Entity):
    @staticmethod
    def id(line: dict) -> int:
        return 1000000 + int(line["sernum"]) * 10 + int(line["PERSON"])

class BenUnit(Entity):
    @staticmethod
    def id(line: dict) -> int:
        return 2000000 + int(line["sernum"]) * 10 + int(line["BENUNIT"])

class Household(Entity):
    @staticmethod
    def id(line: dict) -> int:
        return 3000000 + int(line["sernum"]) * 10

class Dataset:
    def __init__(self, tables: List[Table]):
        self.tables = tables
        self.entities = []
        for table in tables:
            if isinstance(table.entity, list):
                self.entities += table.entity
            elif issubclass(table.entity, Entity):
                self.entities += [table.entity]
        self.entities = list(set(self.entities))
    
    def parse(self) -> dict:
        data = {}
        fieldnames = {}
        for entity in self.entities:
            data[entity] = entity()
            fieldnames[entity] = []
        for table in self.tables:
            table_entities = table.entity
            if not isinstance(table_entities, list):
                table_entities = [table_entities]
            for entity in table_entities:
                if isinstance(table.fieldnames, list):
                    fieldnames[entity] += table.fieldnames
                elif isinstance(table.fieldnames, dict):
                    fieldnames[entity] += table.fieldnames[entity]
            with open(Path(resolve(table.folder)) / table.filename, encoding="utf-8") as f:
                reader = DictReader(f, fieldnames=next(f).split("\t"), delimiter=table.delimiter)
                first_line = True
                for line in tqdm(reader, desc="Reading " + table.filename):
                    identities = []
                    entities = []
                    for entity in table_entities:
                        entity_id = entity.id(line)
                        if entity_id not in data[entity].entries:
                            data[entity].entries[entity_id] = SafeDict()
                        identities += [entity_id]
                        entities += [data[entity].entries[entity_id]]
                    result = table.parse(*entities, SafeDict(line))
                    if not isinstance(result, tuple):
                        result = (result,)
                    for entity, identity, res in zip(table_entities, identities, result):
                        data[entity].entries[identity] = res
                        if first_line:
                            fieldnames[entity] += list(res.keys())
                    first_line = False
        for entity in self.entities:
            fieldnames[entity] = list(set(fieldnames[entity]))
        return data, fieldnames

class SafeDict(dict):
    def __getitem__(self, item):
        try:
            return float(super().__getitem__(item))
        except:
            return 0