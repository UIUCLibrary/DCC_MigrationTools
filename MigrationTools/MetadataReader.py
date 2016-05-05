import csv
import os
from collections import namedtuple


Items = namedtuple("collection", ['name', 'files'])

class _CDM_md_base:
    def __init__(self, tsv_file):
        self.filename = tsv_file
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

    def __str__(self):
        return str("{}: \"{}\"".format(type(self), self.filename))


    @staticmethod
    def load_data(tsv_file):
        records = []
        with open(tsv_file, 'r', encoding="utf-8") as f:

            data = csv.DictReader(f, delimiter='\t')
            for row in data:
                records.append(row)
        return records


class cdm_metadata_tsv(_CDM_md_base):
    """Use for reading the data found in an ContentDM exported TSV file.

        Args:
          tsv_file: ContentDM Metadata TSV file name

        An example of how you can load your tsv file is as follows

            >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")




    """
    def has_column(self, metadata_type):
        """
        Used for find out if the TSV file imported includes a certain metadata field.

        :param metadata_type: A type of metadata such as a "filename"
        :returns: bool -- if it exists in the metadata tsv or not



        Examples:


            Assuming that the metadata file doesn't have a "filename" field ...

                .. doctest::

                    >>> from MigrationTools import cdm_metadata_tsv
                    >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")
                    >>> my_metadata.has_column("filename")
                    False

            But it does have "CONTENTdm file name" field ...

                .. doctest::

                    >>> from MigrationTools import cdm_metadata_tsv
                    >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")
                    >>> my_metadata.has_column("CONTENTdm file name")
                    True

        """
        try:
            assert self.records[0][metadata_type] is not None
            return True
        except KeyError:
            return False

    @property
    def columns(self):
        """Return all the column headers found in the tsv files.

        Examples:
            If you wanted to know all the columns found you could try this ...

            .. doctest::
               :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

               >>> from MigrationTools import cdm_metadata_tsv
               >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")
               >>> my_metadata.columns
               ['Bibliography', 'CONTENTdm file name', 'CONTENTdm file path', 'CONTENTdm number', 'Collection', 'Collection Publisher', 'Color', 'Coverage-Spatial', 'Creator', 'Date', 'Date created', 'Date modified', 'Dimensions', 'File Name', 'Format', 'JPEG2000 URL', 'Keyword', 'Language', 'Local Call Number', 'Map No. in Bassett Bibliography', 'Notes', 'OCLC number', 'Physical Location', 'Place of Publication', 'Reference URL', 'Rights', 'Scale', 'Source', 'Subject', 'Technique', 'Title', 'Type']



        """
        keys = sorted(self.records[0].keys())
        return keys
