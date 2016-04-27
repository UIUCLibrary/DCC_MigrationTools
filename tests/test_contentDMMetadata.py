from unittest import TestCase
from MigrationTools.MetadataReader import CDM_md_base
from MigrationTools import CDMMetadata

test_file = "test.tsv"
test_columns = ("Title", "Creator", "Place of Publication", "Date", "Coverage-Spatial", "Subject", "Keyword", "Type",
                "Dimensions", "Language", "Source", "Physical Location", "Bibliography",
                "Scale", "Notes", "Color", "Local Call Number", "Map No. in Bassett Bibliography",
                "File Name", "Format", "Technique", "JPEG2000 URL", "Rights", "Collection",
                "Collection Publisher", "OCLC number", "Date created", "Date modified", "Reference URL",
                "CONTENTdm number", "CONTENTdm file name", "CONTENTdm file path")

class TestCDM_md_base(TestCase):

    def setUp(self):
        self.md = CDM_md_base(test_file)

    def test_get_record(self):
        self.assertEquals(self.md.get_record(43)['Title'], "Map with tributaries to Congo River, Mpozo River")

    def test_iterate(self):
        i = iter(self.md)
        self.assertEquals(next(i)['CONTENTdm file name'], "100.jp2")


    def test_contains(self):
        self.assertTrue(44 in self.md)

    def test_iter_forloop(self):
        for i, record in enumerate(self.md):
            self.assertIsInstance(record, dict)
            self.assertLess(i, len(self.md), msg="The class is try to pull more records than exists")


class TestContentDMMetadata(TestCase):

    def setUp(self):
        self.md = CDMMetadata(test_file)

    def test_has_column(self):
        self.assertTrue(self.md.has_column("Date modified"))
        self.assertFalse(self.md.has_column("foo"))
        
    def test_columns(self):
        for expected, recieved in zip(sorted(test_columns), self.md.columns):
            self.assertEquals(expected, recieved)
        # self.assertEquals(, test_columns)
        