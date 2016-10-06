# from unittest import TestCase
import os

import pytest
from MigrationTools.MetadataReader import CDM_Metadata

test_file1_tsv = os.path.join(os.path.dirname(__file__), "test.tsv")
test_file_xml = os.path.join(os.path.dirname(__file__), "export.xml")
test_file_tsv = os.path.join(os.path.dirname(__file__), "export.tsv")
test_columns = ("group_id", "Title", "Creator", "Place of Publication", "Date", "Coverage-Spatial", "Subject",
                "Keyword", "Type",
                "Dimensions", "Language", "Source", "Physical Location", "Bibliography",
                "Scale", "Notes", "Color", "Local Call Number", "Map No. in Bassett Bibliography",
                "File Name", "Format", "Technique", "JPEG2000 URL", "Rights", "Collection",
                "Collection Publisher", "OCLC number", "Date created", "Date modified", "Reference URL",
                "CONTENTdm number", "CONTENTdm file name", "CONTENTdm file path")


# @pytest.fixture
# def CDM_base(request):
#     """Loads in the contentdm metadata tsv file and creates a _CDM_md_base object"""
#     return _CDM_md_base(test_file)


@pytest.fixture()
def CDMdata_tsv():
    return CDM_Metadata(test_file1_tsv)


def test_tsv_fields(CDMdata_tsv):
    for field in CDMdata_tsv.fields:
        assert field in test_columns


def test_tsv_doesnt_have_field(CDMdata_tsv):
    assert CDMdata_tsv.has_field("spam") is False


def test_tsv_len(CDMdata_tsv):
    assert len(CDMdata_tsv) == 26

@pytest.fixture()
def CDMdata_xml():
    return CDM_Metadata(test_file_xml)


def test_xml_fields(CDMdata_xml):
    xml_fields = ['isPartOf',
                  'group_id',
                  'pageptr',
                  'pagetitle',
                  'description',
                  'fullResolution',
                  'contributor',
                  'cdmoclc',
                  'cdmid',
                  'publisher',
                  'title',
                  'creator',
                  'viewerURL',
                  'subject',
                  'unmapped',
                  'cdmcreated',
                  'structure',
                  'thumbnailURL',
                  'rights',
                  'format',
                  'type',
                  'source',
                  'cdmfile',
                  'date',
                  'cdmpath',
                  'cdmmodified',
                  'cdmaccess']
    fields = CDMdata_xml.fields
    for field in fields:
        assert field in xml_fields


def test_xml_doesnt_have_field(CDMdata_xml):
    assert CDMdata_xml.has_field("spam") is False


def test_xml_len(CDMdata_xml):
    assert len(CDMdata_xml) == 5


@pytest.fixture()
def CDMdata_joined():
    return CDM_Metadata(test_file_xml, test_file_tsv)

def test_joined_fields(CDMdata_joined):

    joined_fields = ['isPartOf',
                     'group_id',
                     'pagetitle',
                     'pageptr',
                     'description', 
                     'fullResolution', 
                     'contributor', 
                     'cdmoclc',
                     'cdmid',
                     'publisher',
                     'title',
                     'creator',
                     'viewerURL',
                     'subject',
                     'unmapped',
                     'cdmcreated',
                     'structure',
                     'thumbnailURL',
                     'rights',
                     'format',
                     'type',
                     'source',
                     'cdmfile',
                     'date',
                     'cdmpath',
                     'cdmmodified',
                     'cdmaccess',
                     'Identifier',
                     'Type',
                     'Title',
                     'Poster Text',
                     'Artist',
                     'Printer',
                     'Description',
                     'Subject',
                     'Date',
                     'Dimensions',
                     'Sponsor',
                     'Location - Room',
                     'Location - Folder',
                     'Location - RS',
                     'Source',
                     'Rights',
                     'Collection Title',
                     'Creating Unit',
                     'Scanning Date',
                     'Format',
                     'OCLC number',
                     'Date created',
                     'Date modified',
                     'Reference URL',
                     'CONTENTdm number',
                     'CONTENTdm file name',
                     'CONTENTdm file path']
    fields = CDMdata_joined.fields
    for field in fields:
        assert field in joined_fields