from MigrationTools.MetadataReader import cdm_metadata_tsv
from operator import itemgetter
import pytest

test_file = "tests/test.tsv"
test_field = ("Title", "Creator", "Place of Publication", "Date", "Coverage-Spatial", "Subject", "Keyword", "Type",
                "Dimensions", "Language", "Source", "Physical Location", "Bibliography",
                "Scale", "Notes", "Color", "Local Call Number", "Map No. in Bassett Bibliography",
                "File Name", "Format", "Technique", "JPEG2000 URL", "Rights", "Collection",
                "Collection Publisher", "OCLC number", "Date created", "Date modified", "Reference URL",
                "CONTENTdm number", "CONTENTdm file name", "CONTENTdm file path")



@pytest.fixture()
def CDMdata():
    """Loads in the contentdm metadata tsv file and creates a CDMMetadata object"""
    return cdm_metadata_tsv(test_file)


def test_cdm_metadata_tsv_fieldmn(CDMdata):
    # dummy = CDMMetadata(test_file)
    # for x in dummy:
    #     print(x)
    assert CDMdata.has_field("Date modified")
    for column in test_field:
        assert CDMdata.has_field(column)
    assert CDMdata.has_field("foo") == False


def test_cdm_metadata_tsv_fields_unsorted(CDMdata):
    limited_expected_results = [
        {'Creator': 'Mallet, Alain Manesson', 'Title': 'Aegypte Ancienne.'},
        {'Creator': 'Rossari, Carlo', 'Title': 'Africa'},
        {'Creator': 'Nicolosi, Giovanni Battista', 'Title': 'Africa Ioanne Baptista Nicolosio S.T.D. Sic Describente'},
        {'Creator': 'Nicolosi, Giovanni Battista', 'Title': 'Africa Ioanne Baptista Nicolosio S.T.D. Sic Describente'},
        {'Creator': 'Nicolosi, Giovanni Battista', 'Title': 'Africa Ioanne Baptista Nicolosio S.T.D. Sic Describente'},
        {'Creator': 'Nicolosi, Giovanni Battista', 'Title': 'Africa Ioanne Baptista Nicolosio S.T.D. Sic Describente'},
        {'Creator': 'Nicolosi, Giovanni Battista', 'Title': 'Africa Ioanne Baptista Nicolosio S.T.D. Sic Describente'},
        {'Creator': 'Revue GÃ©ographique Internationale', 'Title': 'Afrique Centrale la RÃ©gion du Kongo'},
        {'Creator': 'Pech, L.', 'Title': "Carte d'une Partie de l'Afrique Septentrionale Résumant les Travaux des Missions Dirigées en 1879 & 1881 par M.M. Flatters, Lieutenant Colonel"},
        {'Creator': 'FranÃ§ois, Curt von;  Grenfell, George', 'Title': 'Die NebenflÃ_sse des Mittleren Congo, Lulongo, Tschuapa, Mobangi u.a.'},
        {'Creator': 'Coello, D. Francisco', 'Title': 'Exploraciones de los Sres. Iradier, Montes de Oca y Ossorio en los territorios espaÃ±oles del Golfo de Guinea'},
        {'Creator': 'Ravenstein, E. G.', 'Title': 'French Explorations in the Basin of Ogowe-Kongo 1879-1886'},
        {'Creator': 'Lenz, Oscar', 'Title': 'Karte des Congostromes zwischen Kasonge und der Station der StanleyfÃ_lle'},
        {'Creator': 'Brinkman, C.L.', 'Title': 'Map with tributaries to Congo River, Mpozo River'},
        {'Creator': 'FranÃ§ois, Curt von', 'Title': 'Originalkarte der Itinerar-Aufnahmen & Erkundicungen des Prem. Lieut. Curt von FranÃ§ois...im Stromgebiet des Kassai 16.Juni 1884 bis 17 Juli 1885'},
        {'Creator': 'Chavanne, Josef', 'Title': 'Originalkarte des Gebietes der Muschi-Congo im Portugiesischen West-Afrika'},
        {'Creator': 'Pech, L.', 'Title': 'Page 1'},
        {'Creator': 'Pech, L.', 'Title': 'Page 2'},
        {'Creator': 'Pech, L.', 'Title': 'Page 3'},
        {'Creator': 'Pech, L.', 'Title': 'Page 4'},
        {'Creator': 'Baumann, Oscar', 'Title': 'Route von Ango-Ango nach Leopoldville....'},
        {'Creator': 'Zller, Hugo', 'Title': 'Sketch Map of the Batanga or Moanya River (German Cameroon Territory)'},
        {'Creator': 'Oudney, Denham, and Clapperton', 'Title': 'Skizze der von dem Dr. Oudney, Hrn. Denham u. Lt . Clapperton in Jahr 1823 gemachten Entdeckungen'},
        {'Creator': 'Petermann, August Heinrich', 'Title': 'Skizze des mittlern Kongo-Laufes Von v. FranÃ§ois'},
        {'Creator': 'Baumann, Oscar', 'Title': 'Umgebung von Ango-Ango im Anschlusse an Vivi am Kongo...der Ã–sterr. Kongo-Expedition Oskar Baumann....'},
        {'Creator': 'Hansen, J.', 'Title': 'Vallée du Kouilou-Niari d’apres les levés de Léon Jacob ingénieur 1886-88.'}]


    my_fields = ('Title','Creator')

    returned_results = list(CDMdata.with_fields(*my_fields))


    assert len(limited_expected_results) == len(returned_results)

    for expected, received in zip(sorted(limited_expected_results, key=itemgetter(my_fields[0])),
                                  sorted(returned_results, key=itemgetter(my_fields[0]))):
        for field in my_fields:
            assert expected[field] == received[field]




def test_cdm_metadata_tsv_columns(CDMdata):

    for expected, recieved in zip(sorted(test_field), CDMdata.columns):
        assert expected == recieved


def test_cdm_metadata_tsv_bad_file():
    with pytest.raises(FileNotFoundError):
        cdm_metadata_tsv("badfile.txt")