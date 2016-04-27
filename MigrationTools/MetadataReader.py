import csv
import os
from collections import defaultdict, namedtuple

import re

Items = namedtuple("collection", ['name', 'files'])

class CDM_md_base:
    def __init__(self, tsv_file):
        self.records = self.load_data(tsv_file)

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    def __contains__(self, item):
        for record in self.records:
            if record['CONTENTdm number'] == str(item):
                return True
        return False

    def get_record(self, contentDM_number):
        pass
        for record in self.records:
            if record['CONTENTdm number'] == str(contentDM_number):
                return record
        raise IndexError("No record for \"{}\" was not found in the metadata".format(contentDM_number))


    @staticmethod
    def load_data(tsv_file):
        records = []
        with open(tsv_file) as f:

            data = csv.DictReader(f, delimiter='\t')
            for row in data:
                records.append(row)
        return records


class CDMMetadata(CDM_md_base):
    def has_column(self, metadata_type):
        try:
            self.records[0][metadata_type]
            return True
        except KeyError:
            return False

    @property
    def columns(self):
        keys = sorted(self.records[0].keys())
        return keys

