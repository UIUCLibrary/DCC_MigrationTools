# from unittest import TestCase
import os

import pytest
from MigrationTools.MetadataReader import _CDM_md_base

test_file = os.path.join(os.path.dirname(__file__), "test.tsv")
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




