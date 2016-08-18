import csv
import os
import warnings
from abc import abstractmethod
from collections import namedtuple, defaultdict
from typing import Union
import re
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
Items = namedtuple("collection", ['name', 'files'])

REMOVE_WSPACE_PATTERN = "\n\s*"

class _CDM_md_base:
    def __init__(self, filename):
        self.filename = filename
        self._fields, self.records = self.load_data(filename)

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    def __contains__(self, item):
        for record in self.records:
            if record['CONTENTdm number'] == str(item):
                return True
        return False

    @abstractmethod
    def get_record(self, contentDM_number):
        pass

    def __str__(self):
        return str("{}: \"{}\"".format(type(self), self.filename))

    def has_field(self, metadata_type):
        """
        Used for find out if the TSV file imported includes a certain metadata field.

        :param metadata_type: A type of metadata such as a "filename"
        :returns: bool -- if it exists in the metadata tsv or not



        Example usage:

            Let's say you have the following .tsv file amd you want to know if you have the tsv files contains the
            field "filename" or "CONTENTdm file name" but you to don't want to open the file in Excel.

            +------------------+---------------------+-------------------------------------------+
            | CONTENTdm number | CONTENTdm file name | Title                                     |
            +==================+=====================+===========================================+
            | 41               | 1001.jp2            | Africa                                    |
            +------------------+---------------------+-------------------------------------------+
            | 42               | 1002.jp2            | Umgebung von Ango-Ango im Anschlusse an   |
            |                  |                     | Vivi am Kongo...der Ã–sterr.              |
            |                  |                     | Kongo-Expedition Oskar Baumann....        |
            +------------------+---------------------+-------------------------------------------+
            | 50               | 101.jp2             | Route von Ango-Ango nach Leopoldville.... |
            +------------------+---------------------+-------------------------------------------+

            You could find out if it has the fields this way.

                .. doctest::

                    >>> from MigrationTools import cdm_metadata_tsv
                    >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")
                    >>> my_metadata.has_field("filename")
                    False

            As you'd expect, it doesn't have a field called "filename" so you get False back.

                .. doctest::

                    >>> from MigrationTools import cdm_metadata_tsv
                    >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")
                    >>> my_metadata.has_field("CONTENTdm file name")
                    True

            However if you ask for "CONTENTdm file name", you recieve True back.

        """
        try:
            assert self.records[0][metadata_type] is not None
            return True
        except KeyError:
            return False

    @property
    def columns(self):
        warnings.warn("Use fields() instead", DeprecationWarning)
        return self.fields

    def with_fields(self, *requested_fields):
        """Generator function that returns all the records with only requested fields

        :param requested_fields: fields requested
        :return: List of records as dictionaries

        For example::

            my_metadata = cdm_metadata_tsv("tests/test.tsv")
            for record in my_metadata.with_fields("Title", "Creator"):
                print(record)

        """

        for field in requested_fields:
            if not self.has_field(field):
                raise KeyError


        for record in self.records:
            yield {k: record[k] for k in (requested_fields)}

    @property
    def fields(self):
        """Return all the column headers found in the tsv files.

        Examples:
            If you wanted to know all the fields found you could try this ...

            .. doctest::

               >>> from MigrationTools import cdm_metadata_tsv
               >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")
               >>> my_metadata.fields
               ['Bibliography', 'CONTENTdm file name', 'CONTENTdm file path', 'CONTENTdm number', 'Collection', 'Collection Publisher', 'Color', 'Coverage-Spatial', 'Creator', 'Date', 'Date created', 'Date modified', 'Dimensions', 'File Name', 'Format', 'JPEG2000 URL', 'Keyword', 'Language', 'Local Call Number', 'Map No. in Bassett Bibliography', 'Notes', 'OCLC number', 'Physical Location', 'Place of Publication', 'Reference URL', 'Rights', 'Scale', 'Source', 'Subject', 'Technique', 'Title', 'Type']



        """

        return sorted(self._fields)
        # return keys

    @staticmethod
    @abstractmethod
    def load_data(tsv_file)->list:
        pass

class cdm_metadata_tsv(_CDM_md_base):
    """Use for reading the data found in an ContentDM exported TSV file.


    Args:
      tsv_file: ContentDM Metadata TSV file name

    **NOTE: The tsv file must be encoded as utf-8 to work properly!**

    Example:

        >>> my_metadata = cdm_metadata_tsv("tests/test.tsv")


    """

    @staticmethod
    def load_data(tsv_file)->list:
        records = []
        with open(tsv_file, 'r', encoding="utf-8") as f:

            data = csv.DictReader(f, delimiter='\t')
            for row in data:
                records.append(row)

        fields = records[0].keys()
        return fields, records

    def get_record(self, contentDM_number):
        """Get a single record from a ContentDM number

        :param contentDM_number: The ContentDM number
        :returns:   dict -- Single item record
        """
        for record in self.records:
            if record['CONTENTdm number'] == str(contentDM_number):
                return record
        raise IndexError("No record for \"{}\" was not found in the metadata".format(contentDM_number))


def has_children(element: Element):
    if len(element) > 1:
        return True
    else:
        return False


def build_branch(branch: str, element: Element) -> Union[list, str]:
    results = dict()
    children = element.findall("{}".format(branch))
    if len(children) > 1:
        spam = []
        for child in children:
            spam.append(build_branch(child.tag, child))
        results[children[0].tag] = spam
    elif len(children) == 1:
        results[children[0].tag] = children[0].text
    return results[branch]


def cleanup_string(text: str):
    p = re.compile(REMOVE_WSPACE_PATTERN)
    return p.sub(" ", text).strip()


class cdm_metadata_xml(_CDM_md_base):

    def fields(self):
        return sorted(self._fields)

    @staticmethod
    def load_data(xml_file)->list:
        tree = ET.parse(xml_file)
        records = []
        fieldnames = cdm_metadata_xml.get_field_names(tree.getroot())

        for record in tree.getroot():
            records.append(cdm_metadata_xml.build_record(record, fieldnames))
        return fieldnames, records

    @staticmethod
    def build_record(xml_element_record: Element, field_names):
        metadata = defaultdict(list, {key: [] for key in field_names})

        # TODO: build_record

        for element in xml_element_record:
            # current_value = str(record[element.tag])
            if element.text is not None:
                metadata[element.tag].append(cleanup_string(element.text))
            # if len(current_value) > 0:
            #     current_value += ";"
            # if element.text:
            #     record[element.tag] = current_value + element.text

        pages_records = xml_element_record.findall("structure/page")
        new_record = Record(metadata)
        for page in pages_records:
            new_record.add_page(cdm_metadata_xml.build_page_metadata(page))

        return new_record

    @staticmethod
    def build_page_metadata(page: Element):
        new_page = defaultdict(list)
        # new_page[]
        foo = page.find("pagemetadata")
        for x in foo.iter():
            if x.text is not None and x.text.strip():
                new_page[x.tag].append(cleanup_string(x.text))
        new_page['pagetitle'].append(page.find("pagetitle").text)
        new_page['pageptr'].append(page.find("pageptr").text)

        return new_page

    @staticmethod
    def get_field_names(records):
        field_names = set()
        for record in records:
            for x in record:
                field_names.add(x.tag)
        return field_names

    def has_field(self, metadata_type):
        return metadata_type in self.fields()

    def get_record(self, contentDM_number):
        """Get a single record from a ContentDM number

        :param contentDM_number: The ContentDM number
        :returns:   dict -- Single item record
        """
        for record in self.records:
            if record.data['cdmid'][0] == str(contentDM_number):
                return record
        raise IndexError("No record for \"{}\" was not found in the metadata".format(contentDM_number))

    def __iter__(self):
        return iter(self.records)


def CDM_Metadata_factory(filename):
    ext = os.path.splitext(filename)[1]
    if ext == ".xml":
        return cdm_metadata_xml(filename)
    if ext == ".tsv":
        return cdm_metadata_tsv(filename)
    else:
        raise Exception("Files with a {} extension are not supported".format(ext))


class Record:
    def __init__(self, data: dict):
        self.data = data
        self._pages = []

    def __str__(self):
        return str(dict(self.data))

    def __getitem__(self, item):
        if isinstance(self.data[item], list):
            size = len(self.data[item])

            if size > 1:
                return "; ".join(self.data[item])

            elif size == 1:
                x = self.data[item][0]
                return x

            elif self == 0:
                return None
        else:
            return self.data[item]

    def as_list(self, item):
        if isinstance(self.data[item], list):
            return self.data[item]

    def add_page(self, page):
        self._pages.append(page)

    def fields(self):
        return self.data.keys()

    def has_field(self, fieldname):
        if fieldname in self.data.keys():
            return True
        else:
            return False

    @property
    def pages(self):
        return self._pages


class CDM_Metadata:
    def __init__(self, tsv_file=None, xml_file=None):

        if tsv_file is not None:
            self.tsv_metadata = cdm_metadata_tsv(tsv_file)

        if xml_file is not None:
            self.xml_metadata = cdm_metadata_xml(xml_file)

    def __iter__(self):
        # TODO
        pass