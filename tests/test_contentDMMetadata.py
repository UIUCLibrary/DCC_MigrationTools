# from unittest import TestCase
import pytest
from MigrationTools.MetadataReader import _CDM_md_base

test_file = "tests/test.tsv"
test_columns = ("Title", "Creator", "Place of Publication", "Date", "Coverage-Spatial", "Subject", "Keyword", "Type",
                "Dimensions", "Language", "Source", "Physical Location", "Bibliography",
                "Scale", "Notes", "Color", "Local Call Number", "Map No. in Bassett Bibliography",
                "File Name", "Format", "Technique", "JPEG2000 URL", "Rights", "Collection",
                "Collection Publisher", "OCLC number", "Date created", "Date modified", "Reference URL",
                "CONTENTdm number", "CONTENTdm file name", "CONTENTdm file path")


@pytest.fixture
def CDM_base(request):
    """Loads in the contentdm metadata tsv file and creates a _CDM_md_base object"""
    return _CDM_md_base(test_file)


def test_get_record(CDM_base):
    assert CDM_base.get_record(43)['Title'] == "Map with tributaries to Congo River, Mpozo River"


def test_iterate(CDM_base):
    i = iter(CDM_base)
    assert next(i)['CONTENTdm file name'] == "100.jp2"


def test_contains(CDM_base):
    assert 44 in CDM_base


def test_iter_forloop(CDM_base):
    for i, record in enumerate(CDM_base):
        assert isinstance(record, dict)
        assert i < len(CDM_base), "The class is try to pull more records than exists"

