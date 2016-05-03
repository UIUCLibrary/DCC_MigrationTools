from MigrationTools.MetadataReader import CDMMetadata
import pytest

test_file = "tests/test.tsv"
test_columns = ("Title", "Creator", "Place of Publication", "Date", "Coverage-Spatial", "Subject", "Keyword", "Type",
                "Dimensions", "Language", "Source", "Physical Location", "Bibliography",
                "Scale", "Notes", "Color", "Local Call Number", "Map No. in Bassett Bibliography",
                "File Name", "Format", "Technique", "JPEG2000 URL", "Rights", "Collection",
                "Collection Publisher", "OCLC number", "Date created", "Date modified", "Reference URL",
                "CONTENTdm number", "CONTENTdm file name", "CONTENTdm file path")



@pytest.fixture()
def CDMdata():
    '''Loads in the contentdm metadata tsv file and creates a CDMMetadata object'''
    return CDMMetadata(test_file)


def test_CDMMetadata_has_column(CDMdata):
    # dummy = CDMMetadata(test_file)
    # for x in dummy:
    #     print(x)
    assert CDMdata.has_column("Date modified")
    for column in test_columns:
        assert CDMdata.has_column(column)
    assert CDMdata.has_column("foo") == False


def test_CDMMetadata_columns(CDMdata):

    for expected, recieved in zip(sorted(test_columns), CDMdata.columns):
        assert expected == recieved


def test_CDMMetadata_bad_file():
    with pytest.raises(FileNotFoundError):
        CDMMetadata("badfile.txt")