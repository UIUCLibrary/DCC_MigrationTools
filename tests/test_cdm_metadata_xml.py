# from unittest import TestCase
import os
from collections import defaultdict

from MigrationTools.MetadataReader import cdm_metadata_xml, cleanup_string
import pytest

TEST_FILE = os.path.join(os.path.dirname(__file__), "export.xml")


def test_cleanup_string():
    test_text = """Rights to this item are owned by the American Library Association and managed by the
                        American Library Association Archives at the University of Illinois Urbana-Champaign. Please
                        contact the ALA Archives (ala-archives@library.illinois.edu) if you would like to use this item
                        or obtain a high-res copy.
                    """

    processed_text = "Rights to this item are owned by the American Library Association and managed by the American " \
                     "Library Association Archives at the University of Illinois Urbana-Champaign. Please contact " \
                     "the ALA Archives (ala-archives@library.illinois.edu) if you would like to use this item or " \
                     "obtain a high-res copy."
    assert cleanup_string(test_text) == processed_text

@pytest.fixture()
def CDMdata():
    return cdm_metadata_xml(TEST_FILE)


def test_has_field(CDMdata):
    assert CDMdata.has_field("title")

def test_fields(CDMdata):
    expected_fields = ["unmapped", "type", "title", "description", "creator", "contributor", "subject", "date", "unmapped",
              "source", "rights", "isPartOf", "publisher", "format", "fullResolution", "cdmid", "cdmaccess",
              "cdmcreated", "cdmmodified", "cdmoclc", "cdmfile", "cdmpath", "thumbnailURL", "structure", "viewerURL"]
    for field in CDMdata.fields():
        assert field in expected_fields


def test_doesnt_have_field(CDMdata):
    assert CDMdata.has_field("spam") is False


def test_len(CDMdata):
    assert len(CDMdata) == 5


def test_get_record(CDMdata):
    record = CDMdata.get_record(1)
    assert record["cdmfile"] == "10.jp2"


def test_get_invalid_record(CDMdata):
    with pytest.raises(IndexError):
        CDMdata.get_record(5)


def test_get_compound_record_has_subpages(CDMdata):
    record = CDMdata.get_record(155)
    assert isinstance(record.pages, list)
    assert len(record.pages) == 2
    assert isinstance(record.pages[0], dict)


def test_compound_record_get_subpage(CDMdata):
    record = CDMdata.get_record(155)
    assert isinstance(record.pages, list)
    assert record.pages[0]["pagetitle"][0] == "Side 1"
    assert record.pages[1]["pagetitle"][0] == "Side 2"


def test_multiple_tags(CDMdata):
    record = CDMdata.get_record(155)
    description_list = record.as_list("description")
    assert isinstance(description_list, list)

    assert description_list[0] == "1998 wall calendar featuring covers of past Coretta Scott King winners. " \
                                  "Shades of orange. Laminated, two sided, 6 months on each side."
    assert description_list[1] == "26 x 38 in."
    assert description_list[2] == "American Library Association;"


def test_concat_multi_item(CDMdata):
    record = CDMdata.get_record(155)
    assert record["unmapped"] == "ALA0001389; University Archives, Room 19 Library; Drawer 3, Folder 8; RS 12/3/12; 2014-01-22"