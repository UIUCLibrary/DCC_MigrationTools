import csv
import os
import warnings
from abc import abstractmethod
from collections import namedtuple, defaultdict, MutableMapping
import re
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
Items = namedtuple("collection", ['name', 'files'])

REMOVE_WSPACE_PATTERN = "\n\s*"

# FullRecord = namedtuple("FullRecord", ["object_level", "item_level"])


class RecordMismatch(Exception):
    pass


class FullRecord(MutableMapping):
    def __init__(self, object_level, item_level: list):
        assert isinstance(item_level, list)
        self.object_level = object_level
        self._item_level = item_level
        self.additional_info = dict()
        self._combined = dict()

    def __iter__(self):
        return self._combined_dict().__iter__()

    def __delitem__(self, key):
        return self.additional_info.__delitem__(key)

    def __setitem__(self, key, value):
        self.additional_info[key] = value

    def __getitem__(self, key):
        result = self._combined_dict().__getitem__(key)
        if isinstance(result, list):
            return ";".join(result)
        return result

    def __len__(self):
        # if self.item_level is not None and len(self.item_level) > 0:
        #     return len(self.item_level)
        # else:
        #     return 1
        return len(self._combined_dict())

    @property
    def item_level(self):
        # return {k: ";".join(v) for k,v in self._item_level.items()}
        # return self._flatten(self._item_level)
        return self._item_level
        # if self._item_level is not None:
        #     return self._item_level
        # else:
        #     return []

    def __str__(self):
        return str({'object_level': str(self.object_level), 'item_level': str(self.item_level)})

    def _combined_dict(self):
        if self.item_level is not None and len(self._item_level) > 0:
            # FIXME: something missing for getting a dictionary
            combined = self._flatten(self._item_level)

            # combined_items = defaultdict(str)
            # for item in self.item_level:

                # for key, value in item.data:
                #     combined_items[key] = combined_items[key]
                # combined_items[item]
            # return {**self.object_level, **self.additional_info}
            # self._combined = {**self.object_level, **combined, **self.additional_info}

            return {**self.object_level, **combined, **self.additional_info}
        else:
            # self._combined = {**self.object_level, **self.additional_info}
            return {**self.object_level, **self.additional_info}

    def _flatten(self, full_list):
        combined = {k: v for d in full_list for k, v in d.items()}
        combined = {k: ";".join(v) for k, v in combined.items()}
        return combined

    def __repr__(self):
        object_level = 'object_level : {}\n'.format(self.object_level)
        item_level = 'item_level   : {}\n'.format("None" if self.item_level is None
                                                  else ("\n{}".format(" " * 15).join([repr(x)
                                                                                      for x
                                                                                      in self.item_level])))
        # item_level = 'item_level   : {}\n'.format("None" if self.item_level is None else ("\n{}".format(" " * 15).join([str(x) for x in self.item_level])))
        additional = 'additional   : {}'.format(self.additional_info)
        return object_level + item_level + additional + "\n"
        # return str(self._combined_dict())

    @property
    def fields(self):
        fields = set()
        n = self.object_level.fields
        fields.update(n)
        if self.item_level is not None:
            for page in self.item_level:
                # keys =
                fields.update(page.keys())
        return fields

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

            data = csv.DictReader(f, dialect="excel-tab")
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


def build_branch(branch: str, element: Element)->dict:
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
    def build_record(xml_element_record: Element, field_names)->defaultdict(list):
        metadata = defaultdict(list, {key: [] for key in field_names})

        for element in xml_element_record:
            if element.text is not None:
                metadata[element.tag].append(cleanup_string(element.text))


        pages_records = xml_element_record.findall("structure/page")
        if len(pages_records) == 0:
            pages_records = xml_element_record.findall("structure/node/page")
        new_record = Record(metadata)
        for page in pages_records:
            new_record.add_page(cdm_metadata_xml.build_page_metadata(page))

        return new_record

    @staticmethod
    def build_page_metadata(page: Element)->dict:
        new_page = defaultdict(list)
        # new_page[]
        foo = page.find("pagemetadata")
        for x in foo.iter():
            if x.text is not None and x.text.strip():
                new_page[x.tag].append(cleanup_string(x.text))
        new_page['pagetitle'].append(page.find("pagetitle").text)
        new_page['pageptr'].append(page.find("pageptr").text)

        return dict(new_page)

    @staticmethod
    def get_field_names(records)->set:
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

    def parts(self):
        """Yields records that are broken down into a single part. Meaning, the object level and the item level are returned
        separately.

        .. Note::

            This is really only useful for matching the size of records with the size of the TSV file.

        :yields: list of dictionary objects.

        """

        for record in self.records:
            yield dict(record.data)
            for page in record.pages:
                yield page


def CDM_Metadata_factory(filename):
    ext = os.path.splitext(filename)[1]
    if ext == ".xml":
        return cdm_metadata_xml(filename)
    if ext == ".tsv":
        return cdm_metadata_tsv(filename)
    else:
        raise Exception("Files with a {} extension are not supported".format(ext))


class Record(MutableMapping):
    def __init__(self, data: dict):
        self.data = data
        self._pages = []

    def __str__(self):
        return str(self._combined_dict())

    def __len__(self):
        return len(self._combined_dict())

    def __repr__(self):
        combined = self._combined_dict()
        text = ""
        for k,v in combined.items():
            text += "'{}':{}".format(k, "\n".join(v))
        return text
        # return combined

    def __iter__(self):
        return self._combined_dict().__iter__()

    def __delitem__(self, key):
        raise NotImplementedError("Unable to delete this information")

    def __setitem__(self, key, value):
        raise NotImplementedError("Unable to modify this information")

    def _combined_dict(self):
        combined = {k: v for d in self.pages for k, v in d.items()}
        everything = {**self.data, **combined}
        return everything

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

    @property
    def fields(self):
        return list(self.data.keys())

    def has_field(self, fieldname):
        if fieldname in self.data.keys():
            return True
        else:
            return False

    @property
    def pages(self):
        return [dict(x) for x in self._pages]


class CDM_Metadata:
    """This is the high level function for using the metadata exports from CONTENTdm. It's meant to be iterated over
     with a for loop.

     You can use either a single xml or tsv exported filed, or you one of each. When used both, the class will attempt
     to join the data together.

    .. note::

       As of now, CONTENTdm tsv files will need to have the extension .tsv to work. At the time of writing this, tsv
       files exported from CONTENTdm are saved with the .txt extension. As a workaround, change the extension of these
       files from .txt to .tsv.

    """
    def __init__(self, *files):
        tsv_file = None
        xml_file = None

        if len(files) > 2:
            raise AttributeError("Current limit of 2 files to merge. Maximum 1 xml and 1 tsv file.")
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == ".tsv":
                if tsv_file is None:
                    tsv_file = file
                else:
                    AttributeError("Only one tsv is supported at this time")
            elif ext == ".xml":
                if xml_file is None:
                    xml_file = file
                else:
                    AttributeError("Only one xml is supported at this time")
            else:
                raise AttributeError("{} is an unsupported file type".format(file))

        if tsv_file is not None:
            self.tsv_metadata = cdm_metadata_tsv(tsv_file)
        else:
            self.tsv_metadata = None

        if xml_file is not None:
            self.xml_metadata = cdm_metadata_xml(xml_file)
        else:
            self.xml_metadata = None

        # join if both Xml and TSV are given
        if self.tsv_metadata is not None and self.xml_metadata is not None:
            self._data = CDM_Metadata.create_full(xml_metadata=self.xml_metadata, tsv_metadata=self.tsv_metadata)

        # if only a tsv file is given, Full record with only the object level data and nothing for the page/item level
        elif self.tsv_metadata is not None:
            self._data = CDM_Metadata.create_full(tsv_metadata=self.tsv_metadata)


        # if only a xml file is given, use only that data
        elif self.xml_metadata is not None:
            self._data = CDM_Metadata.create_full(xml_metadata=self.xml_metadata)
        else:
            raise AttributeError("Need a valid xml, tsv or both")
        pass

    @property
    def fields(self):
        all_fields = set()
        all_fields.add('group_id')

        for record in self._data:
            all_fields.update(record.fields)
        return list(all_fields)

    def has_field(self, field):
        return field in self.fields

    def __len__(self):
        items = 0
        for item in self._data:
            items += len(item.item_level)

        return len(self._data) + items

    def __iter__(self):
        for i, object_record in enumerate(self._data):
            object_record['group_id'] = i
            yield object_record
            for item in object_record.item_level:
                santized = {k: ";".join(v) for k, v in item.items()}

                object_info = dict(object_record.object_level)
                for key in santized.keys():
                    if key in object_info.keys():
                        del object_info[key]

                matching = self.tsv_metadata.get_record(int(santized['pageptr']))
                item = {**object_info, **santized, **matching}
                item['group_id'] = i
                yield item


    @staticmethod
    def create_full(xml_metadata: cdm_metadata_xml=None, tsv_metadata: cdm_metadata_tsv=None)->FullRecord:
        """Factory function that takes a xml file and/or a tsv metadata object and builds a FullRecord object.
        If only a xml_metadata or a tsv_metadata object is give, the FullRecord is simply constructed based on that
        data alone. However if both are used in the, the data is joined.

        :param xml_metadata: cdm_metadata_xml object contained the data for a CONTENTdm xml export
        :type xml_metadata: cdm_metadata_xml
        :param tsv_metadata: cdm_metadata_tsv object contained the data for a CONTENTdm tsv export
        :type tsv_metadata: cdm_metadata_tsv

        :returns: FullRecord object containing the data

        """

        if xml_metadata is None and tsv_metadata is None:
            raise ValueError("Needs either xml_metadata or tsv_metadata")

        full_records = []
        if xml_metadata is not None:
            if tsv_metadata is not None:
                # If an XML file and a TSV file is given, Join them

                # Check that the number of lines in the TSV match the number of XML records plus
                # any elements that contains pages.
                # Note: This doesn't match to see if these records matches.
                total_xml_parts = len(list(xml_metadata.parts()))
                total_tsv_records = len(tsv_metadata)
                if total_tsv_records != total_xml_parts:
                    raise RecordMismatch


                for record in xml_metadata:
                    pages = []
                    cdmid = int(record['cdmid'])
                    object_level = tsv_metadata.get_record(cdmid)
                    if len(record.pages) > 0:
                        for page in record.pages:
                            # item = tsv_metadata.get_record(int(page['pageptr'][0]))
                            pages.append(page)

                    full_records.append(FullRecord(Record(object_level), pages))

            else:
                for record in xml_metadata:
                    pages = record.pages
                    object_level = record
                    full_records.append(FullRecord(object_level, pages))
        elif tsv_metadata is not None:
            full_records = [FullRecord(Record(rec), []) for rec in tsv_metadata]
        return full_records