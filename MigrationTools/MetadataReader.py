import csv
import os
from collections import defaultdict, namedtuple

import re

Items = namedtuple("collection", ['name', 'files'])

class _CDM_md_base:
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
        """
        Get a single record from a ContentDM number

        :param contentDM_number: The ContentDM number
        :returns:   dict -- Single item record
        """
        for record in self.records:
            if record['CONTENTdm number'] == str(contentDM_number):
                return record
        raise IndexError("No record for \"{}\" was not found in the metadata".format(contentDM_number))


    @staticmethod
    def load_data(tsv_file):
        records = []
        with open(tsv_file, 'r', encoding="utf-8") as f:

            data = csv.DictReader(f, delimiter='\t')
            for row in data:
                records.append(row)
        return records


class CDMMetadata(_CDM_md_base):
    """
    Use for reading the data found in an ContentDM exported TSV file.

      Args:
        tsv_file: the file name of the tsv file that contains ContentDM Metadata

    """
    def has_column(self, metadata_type):
        """
        Used for find out if the TSV file imported includes a certain metadata field.

        :param metadata_type: A type of metadata such as a "filename"
        :returns: bool -- if it exists in the metadata tsv or not

        """
        try:
            assert self.records[0][metadata_type] is not None
            return True
        except KeyError:
            return False

    @property
    def columns(self):
        """Return all the column headers found in the tsv files"""
        keys = sorted(self.records[0].keys())
        return keys

