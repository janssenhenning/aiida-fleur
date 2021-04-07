# -*- coding: utf-8 -*-
'''Contains tests for xml_utils within aiida-fleur, some test are autogenerated.'''

from __future__ import absolute_import
import os
import pytest
import aiida_fleur

aiida_path = os.path.dirname(aiida_fleur.__file__)
TEST_INP_XML_PATH = os.path.join(aiida_path, '../tests/files/inpxml/FePt/inp.xml')


def test_xml_set_attribv_occ(inpxml_etree):
    from aiida_fleur.tools.xml_util import xml_set_attribv_occ, eval_xpath
    etree = inpxml_etree(TEST_INP_XML_PATH)

    xml_set_attribv_occ(etree, '/fleurInput/calculationSetup/cutoffs', 'Gmax', 11.00)
    assert float(eval_xpath(etree, '/fleurInput/calculationSetup/cutoffs/@Gmax')) == 11

    xml_set_attribv_occ(etree, '/fleurInput/atomGroups/atomGroup', 'species', 'TEST-1', [1])
    assert eval_xpath(etree, '/fleurInput/atomGroups/atomGroup/@species') == ['Fe-1', 'TEST-1']

    xml_set_attribv_occ(etree, '/fleurInput/atomGroups/atomGroup', 'species', 'TEST-2', [-1])
    assert eval_xpath(etree, '/fleurInput/atomGroups/atomGroup/@species') == ['TEST-2', 'TEST-2']


def test_xml_set_first_attribv(inpxml_etree):
    from aiida_fleur.tools.xml_util import xml_set_first_attribv, eval_xpath
    etree = inpxml_etree(TEST_INP_XML_PATH)

    xml_set_first_attribv(etree, '/fleurInput/calculationSetup/cutoffs', 'Gmax', 11.00)
    assert float(eval_xpath(etree, '/fleurInput/calculationSetup/cutoffs/@Gmax')) == 11

    xml_set_first_attribv(etree, '/fleurInput/atomGroups/atomGroup', 'species', 'TEST-1')
    assert eval_xpath(etree, '/fleurInput/atomGroups/atomGroup/@species') == ['TEST-1', 'Pt-1']


def test_xml_set_all_attribv(inpxml_etree):
    from aiida_fleur.tools.xml_util import xml_set_all_attribv, eval_xpath
    etree = inpxml_etree(TEST_INP_XML_PATH)

    xml_set_all_attribv(etree, '/fleurInput/calculationSetup/cutoffs', 'Gmax', 11.00)
    assert float(eval_xpath(etree, '/fleurInput/calculationSetup/cutoffs/@Gmax')) == 11

    xml_set_all_attribv(etree, '/fleurInput/atomGroups/atomGroup', 'species', 'TEST-1')
    assert eval_xpath(etree, '/fleurInput/atomGroups/atomGroup/@species') == ['TEST-1', 'TEST-1']

    xml_set_all_attribv(etree, '/fleurInput/atomGroups/atomGroup', 'species', ['TEST-1', 23])
    assert eval_xpath(etree, '/fleurInput/atomGroups/atomGroup/@species') == ['TEST-1', '23']


def test_xml_set_text(inpxml_etree):
    from aiida_fleur.tools.xml_util import xml_set_text, eval_xpath2
    etree = inpxml_etree(TEST_INP_XML_PATH)

    second_text = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text

    xml_set_text(etree, '/fleurInput/atomGroups/atomGroup/filmPos', 'test_text')
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[0].text == 'test_text'
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text == second_text


def test_xml_set_text_occ(inpxml_etree):
    from aiida_fleur.tools.xml_util import xml_set_text_occ, eval_xpath2
    etree = inpxml_etree(TEST_INP_XML_PATH)

    first_text = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[0].text
    second_text = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text

    xml_set_text_occ(etree, '/fleurInput/atomGroups/atomGroup/filmPos', 'test_text', occ=0)
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[0].text == 'test_text'
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text == second_text

    etree = inpxml_etree(TEST_INP_XML_PATH)
    xml_set_text_occ(etree, '/fleurInput/atomGroups/atomGroup/filmPos', 'test_text', occ=1)
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[0].text == first_text
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text == 'test_text'


def test_xml_set_all_text(inpxml_etree):
    from aiida_fleur.tools.xml_util import xml_set_all_text, eval_xpath2
    etree = inpxml_etree(TEST_INP_XML_PATH)

    xml_set_all_text(etree, '/fleurInput/atomGroups/atomGroup/filmPos', 'test_text')
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[0].text == 'test_text'
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text == 'test_text'

    xml_set_all_text(etree, '/fleurInput/atomGroups/atomGroup/filmPos', ['test_text2', 'test_ext3'])
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[0].text == 'test_text2'
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos')[1].text == 'test_ext3'


def test_create_tag(inpxml_etree):
    from aiida_fleur.tools.xml_util import create_tag, eval_xpath3
    etree = inpxml_etree(TEST_INP_XML_PATH)

    create_tag(etree, '/fleurInput/cell/filmLattice/bravaisMatrix', 'TEST_TAG', create=False)
    assert eval_xpath3(etree, '/fleurInput/cell/filmLattice/bravaisMatrix')[0][3].tag == 'TEST_TAG'

    create_tag(etree, '/fleurInput/cell/filmLattice/bravaisMatrix', 'TEST_TAG2', create=False, place_index=1)
    tag_names = [x.tag for x in eval_xpath3(etree, '/fleurInput/cell/filmLattice/bravaisMatrix')[0]]
    assert tag_names == ['row-1', 'TEST_TAG2', 'row-2', 'row-3', 'TEST_TAG']

    create_tag(etree,
               '/fleurInput/cell/filmLattice/bravaisMatrix',
               'TEST_TAG3',
               create=False,
               place_index=True,
               tag_order=['row-1', 'TEST_TAG2', 'TEST_TAG3', 'row-2', 'row-3', 'TEST_TAG'])
    tag_names = [x.tag for x in eval_xpath3(etree, '/fleurInput/cell/filmLattice/bravaisMatrix')[0]]
    assert tag_names == ['row-1', 'TEST_TAG2', 'TEST_TAG3', 'row-2', 'row-3', 'TEST_TAG']

    create_tag(etree,
               '/fleurInput/cell/filmLattice/bravaisMatrix',
               'TEST_TAG4',
               create=False,
               place_index=True,
               tag_order=['row-1', 'TEST_TAG2', 'TEST_TAG3', 'row-2', 'TEST_TAG4', 'row-3', 'TEST_TAG'])
    tag_names = [x.tag for x in eval_xpath3(etree, '/fleurInput/cell/filmLattice/bravaisMatrix')[0]]
    assert tag_names == ['row-1', 'TEST_TAG2', 'TEST_TAG3', 'row-2', 'TEST_TAG4', 'row-3', 'TEST_TAG']

    create_tag(etree,
               '/fleurInput/cell/filmLattice/bravaisMatrix',
               'TEST_TAG0',
               create=False,
               place_index=True,
               tag_order=['TEST_TAG0', 'row-1', 'TEST_TAG2', 'TEST_TAG3', 'row-2', 'TEST_TAG4', 'row-3', 'TEST_TAG'])
    tag_names = [x.tag for x in eval_xpath3(etree, '/fleurInput/cell/filmLattice/bravaisMatrix')[0]]
    assert tag_names == ['TEST_TAG0', 'row-1', 'TEST_TAG2', 'TEST_TAG3', 'row-2', 'TEST_TAG4', 'row-3', 'TEST_TAG']

    with pytest.raises(ValueError) as excinfo:
        create_tag(etree,
                   '/fleurInput/cell/filmLattice/bravaisMatrix',
                   'TEST_TAG5',
                   create=False,
                   place_index=True,
                   tag_order=[
                       'TEST_TAG0', 'row-1', 'TEST_TAG3', 'TEST_TAG2', 'TEST_TAG5', 'row-2', 'TEST_TAG4', 'row-3',
                       'TEST_TAG'
                   ])
    assert str(excinfo.value) == 'Existing order does not correspond to tag_order list'

    with pytest.raises(ValueError) as excinfo:
        create_tag(
            etree,
            '/fleurInput/cell/filmLattice/bravaisMatrix',
            'TEST_TAG5',
            create=False,
            place_index=True,
            tag_order=['TEST_TAG0', 'row-1', 'TEST_TAG3', 'TEST_TAG2', 'row-2', 'TEST_TAG4', 'row-3', 'TEST_TAG'])
    assert str(excinfo.value) == 'Did not find element name in the tag_order list'


def test_delete_att(inpxml_etree):
    from aiida_fleur.tools.xml_util import delete_att, eval_xpath2
    etree = inpxml_etree(TEST_INP_XML_PATH)

    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos/@label')[0] == '                 222'

    delete_att(etree, '/fleurInput/atomGroups/atomGroup/filmPos', 'label')
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos/@label') == []


def test_delete_tag(inpxml_etree):
    from aiida_fleur.tools.xml_util import delete_tag, eval_xpath2
    etree = inpxml_etree(TEST_INP_XML_PATH)

    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos') != []

    delete_tag(etree, '/fleurInput/atomGroups/atomGroup/filmPos')
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos') == []


def test_replace_tag(inpxml_etree):
    from aiida_fleur.tools.xml_util import replace_tag, eval_xpath2
    etree = inpxml_etree(TEST_INP_XML_PATH)

    to_insert = eval_xpath2(etree, '/fleurInput/calculationSetup/cutoffs')[0]
    print(to_insert)
    print(eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos'))

    replace_tag(etree, '/fleurInput/atomGroups/atomGroup/filmPos', to_insert)

    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/filmPos') == []
    assert eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/cutoffs')[0] == to_insert


@pytest.mark.skip(reason='econfig extraction is not implemented')
def test_get_inpgen_para_from_xml(inpxml_etree):
    from aiida_fleur.tools.xml_util import get_inpgen_para_from_xml
    etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

    result = {
        'comp': {
            'jspins': 2.0,
            'frcor': False,
            'ctail': True,
            'kcrel': '0',
            'gmax': 10.0,
            'gmaxxc': 8.7,
            'kmax': 4.0
        },
        'atom0': {
            'z': 26,
            'rmt': 2.2,
            'dx': 0.016,
            'jri': 787,
            'lmax': 10,
            'lnonsph': 6,
            # 'econfig': <Element electronConfig at 0x1105d66e0>,
            'lo': '',
            'element': 'Fe'
        },
        'atom1': {
            'z': 78,
            'rmt': 2.2,
            'dx': 0.017,
            'jri': 787,
            'lmax': 10,
            'lnonsph': 6,
            # 'econfig': <Element electronConfig at 0x110516d20>,
            'lo': '',
            'element': 'Pt'
        },
        'title': 'A Fleur input generator calculation with aiida',
        'exco': {
            'xctyp': 'vwn'
        }
    }

    dict_result = get_inpgen_para_from_xml(etree, schema_dict)
    assert dict_result == result


class TestSetSpecies:
    """Tests for set_species"""

    paths = [
        'mtSphere/@radius', 'atomicCutoffs/@lmax', 'energyParameters/@s', 'electronConfig/coreConfig',
        'electronConfig/stateOccupation/@state', 'electronConfig/stateOccupation/@state', 'special/@socscale',
        'ldaU/@U', 'ldaU/@U', 'lo/@n', 'lo/@n'
    ]

    attdicts = [{
        'mtSphere': {
            'radius': 3.333
        }
    }, {
        'atomicCutoffs': {
            'lmax': 7.0
        }
    }, {
        'energyParameters': {
            's': 3.0
        }
    }, {
        'electronConfig': {
            'coreConfig': 'test'
        }
    }, {
        'electronConfig': {
            'stateOccupation': {
                'state': 'state'
            }
        }
    }, {
        'electronConfig': {
            'stateOccupation': [{
                'state': 'state'
            }, {
                'state': 'state2'
            }]
        }
    }, {
        'special': {
            'socscale': 1.0
        }
    }, {
        'ldaU': {
            'U': 2.0
        }
    }, {
        'ldaU': [{
            'U': 2.0
        }, {
            'U': 23.0
        }]
    }, {
        'lo': {
            'n': 2.0
        }
    }, {
        'lo': [{
            'n': 2.0
        }, {
            'n': 33.0
        }]
    }
                #  'nocoParams': {'test_att' : 2, 'qss' : '123 123 123'},
                ]

    results = [
        '3.333', '7.0', '3.0', 'test', 'state', ['state', 'state2'], '1.0', '2.0', ['2.0', '23.0'], '2.0',
        ['2.0', '33.0']
    ]

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results, paths))
    def test_set_species(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import set_species, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        set_species(etree, schema_dict, 'Fe-1', attributedict=attr_dict)

        result = eval_xpath2(etree, '/fleurInput/atomSpecies/species[@name="Fe-1"]/' + path)

        if isinstance(correct_result, str):
            if 'coreConfig' in path:
                assert result[0].text == correct_result
            else:
                assert result[0] == correct_result
        elif isinstance(correct_result, (float, int)):
            assert result[0] == correct_result
        else:
            assert correct_result == result

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results, paths))
    def test_set_species_label(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import set_species_label, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        set_species_label(etree, schema_dict, '                 222', attributedict=attr_dict)

        result = eval_xpath2(etree, '/fleurInput/atomSpecies/species[@name="Fe-1"]/' + path)

        if isinstance(correct_result, str):
            if 'coreConfig' in path:
                assert result[0].text == correct_result
            else:
                assert result[0] == correct_result
        elif isinstance(correct_result, (float, int)):
            assert result[0] == correct_result
        else:
            assert correct_result == result

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results, paths))
    def test_set_species_all_string(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import set_species, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        set_species(etree, schema_dict, 'all-Fe', attributedict=attr_dict)

        result = eval_xpath2(etree, '/fleurInput/atomSpecies/species[@name="Fe-1"]/' + path)

        if isinstance(correct_result, str):
            if 'coreConfig' in path:
                assert result[0].text == correct_result
            else:
                assert result[0] == correct_result
        elif isinstance(correct_result, (float, int)):
            assert result[0] == correct_result
        else:
            assert correct_result == result

    results_all = [[x, x] if not isinstance(x, list) else [x[0], x[1], x[0], x[1]] for x in results]

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results_all, paths))
    def test_set_species_all(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import set_species, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        set_species(etree, schema_dict, 'all', attributedict=attr_dict)

        result = eval_xpath2(etree, '/fleurInput/atomSpecies/species/' + path)

        import lxml
        print(lxml.etree.tostring(etree))

        if 'coreConfig' in path:
            assert [x.text for x in result] == correct_result
        else:
            assert result == correct_result

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results_all, paths))
    def test_set_species_label_all(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import set_species_label, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        set_species_label(etree, schema_dict, 'all', attributedict=attr_dict)

        result = eval_xpath2(etree, '/fleurInput/atomSpecies/species/' + path)

        if 'coreConfig' in path:
            assert [x.text for x in result] == correct_result
        else:
            assert result == correct_result


class TestChangeAtomgrAtt:
    """Tests for change_atomgr_att"""

    paths = ['force/@relaxXYZ', 'nocoParams/@beta']

    attdicts = [{'force': {'relaxXYZ': 'FFF'}}, {'nocoParams': {'beta': 7.0}}]

    results = ['FFF', '7.0']

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results, paths))
    def test_change_atomgr_att(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import change_atomgr_att, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        change_atomgr_att(etree, schema_dict, attributedict=attr_dict, species='Fe-1')

        result = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup[@species="Fe-1"]/' + path)

        assert result[0] == correct_result

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results, paths))
    def test_change_atomgr_att_position(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import change_atomgr_att, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        change_atomgr_att(etree, schema_dict, attributedict=attr_dict, position=1)

        result = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/' + path)

        assert result[0] == correct_result

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results, paths))
    def test_change_atomgr_att_label(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import change_atomgr_att_label, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        change_atomgr_att_label(etree, schema_dict, attributedict=attr_dict, at_label='                 222')

        result = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup[@species="Fe-1"]/' + path)

        assert result[0] == correct_result

    results_all = [[x, x] for x in results]

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results_all, paths))
    def test_change_atomgr_att_all(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import change_atomgr_att, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        change_atomgr_att(etree, schema_dict, attributedict=attr_dict, species='all')

        result = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/' + path)

        assert result == correct_result

    @staticmethod
    @pytest.mark.parametrize('attr_dict,correct_result,path', zip(attdicts, results_all, paths))
    def test_change_atomgr_att_label_all(inpxml_etree, attr_dict, correct_result, path):
        from aiida_fleur.tools.xml_util import change_atomgr_att_label, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        change_atomgr_att_label(etree, schema_dict, attributedict=attr_dict, at_label='all')

        result = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup/' + path)

        assert result == correct_result

    def test_change_atomgr_att_fail(self, inpxml_etree):
        from aiida_fleur.tools.xml_util import change_atomgr_att, eval_xpath2
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        change_atomgr_att(etree, schema_dict, attributedict=self.attdicts[0])

        result = eval_xpath2(etree, '/fleurInput/atomGroups/atomGroup[@species="Fe-1"]/' + self.paths[0])

        assert result[0] == 'TTT'


class TestSetInpchanges:
    """Tests group for set_inpchanges method"""
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

    schema_dict = InputSchemaDict.fromVersion('0.33')

    skip_paths = {
        'coreSpectrum', 'oneDParams', 'wannier', 'fields', 'xcParams', 'greensFunction', 'rdmft', 'ggaPrinting',
        'juPhon', 'spinSpiralQPointMesh', 'forceTheorem', 'bulkLattice', 'qsc'
    }

    @pytest.mark.parametrize('name,path', schema_dict['unique_attribs'].items())
    def test_set_inpchanges(self, inpxml_etree, name, path):
        from aiida_fleur.tools.xml_util import set_inpchanges, eval_xpath2
        etree = inpxml_etree(TEST_INP_XML_PATH)

        if any(x in path for x in self.skip_paths):
            pytest.skip('This attribute is not tested for FePt/inp.xml')

        if name == 'xcFunctional':
            name = 'name'

        text_attrib = False
        if name in self.schema_dict['attrib_types']:
            possible_types = self.schema_dict['attrib_types'][name]
        else:
            text_attrib = True

        if text_attrib:
            set_inpchanges(etree, self.schema_dict, change_dict={name: 'test'})
            result = eval_xpath2(etree, path)[0]
            assert result.text == 'test'
        else:
            if 'switch' in possible_types:
                set_inpchanges(etree, self.schema_dict, change_dict={name: 'T'})
                result = eval_xpath2(etree, path)
                assert result[0] == 'T'
            elif 'float' in possible_types or 'float_expression' in possible_types:
                set_inpchanges(etree, self.schema_dict, change_dict={name: 33.0})
                result = eval_xpath2(etree, path)
                assert float(result[0]) == 33
            elif 'int' in possible_types:
                set_inpchanges(etree, self.schema_dict, change_dict={name: 33})
                result = eval_xpath2(etree, path)
                assert int(result[0]) == 33
            else:
                set_inpchanges(etree, self.schema_dict, change_dict={name: 'test'})
                result = eval_xpath2(etree, path)
                assert result[0] == 'test'

    def test_set_inpchanges_fail(self, inpxml_etree):
        from aiida_fleur.tools.xml_util import set_inpchanges
        from aiida.common.exceptions import InputValidationError

        etree = inpxml_etree(TEST_INP_XML_PATH)
        with pytest.raises(InputValidationError):
            set_inpchanges(etree, self.schema_dict, change_dict={'not_existing': 'test'})

    def test_set_inpchanges_path_spec_under_specified(self, inpxml_etree):
        from aiida_fleur.tools.xml_util import set_inpchanges
        from aiida.common.exceptions import InputValidationError

        etree = inpxml_etree(TEST_INP_XML_PATH)
        with pytest.raises(InputValidationError):
            set_inpchanges(etree, self.schema_dict, change_dict={'spinf': 10.0, 'phi': 2.14})

    def test_set_inpchanges_path_spec(self, inpxml_etree):
        from aiida_fleur.tools.xml_util import set_inpchanges, eval_xpath2

        etree = inpxml_etree(TEST_INP_XML_PATH)
        set_inpchanges(etree,
                       self.schema_dict,
                       change_dict={
                           'spinf': 10.0,
                           'phi': 2.14
                       },
                       path_spec={
                           'spinf': {
                               'contains': 'scfLoop'
                           },
                           'phi': {
                               'not_contains': 'forceTheorem'
                           }
                       })

        result_spinf = eval_xpath2(etree, '/fleurInput/calculationSetup/scfLoop/@spinf')
        assert float(result_spinf[0]) == 10.0

        result_phi = eval_xpath2(etree, '/fleurInput/calculationSetup/soc/@phi')
        assert float(result_phi[0]) == 2.14

    def test_set_inpchanges_path_spec_over_specified(self, inpxml_etree):
        from aiida_fleur.tools.xml_util import set_inpchanges
        from aiida.common.exceptions import InputValidationError

        etree = inpxml_etree(TEST_INP_XML_PATH)
        with pytest.raises(InputValidationError):
            set_inpchanges(etree,
                           self.schema_dict,
                           change_dict={
                               'spinf': 10.0,
                               'phi': 2.14
                           },
                           path_spec={
                               'spinf': {
                                   'contains': 'scfLoop'
                               },
                               'phi': {
                                   'not_contains': 'forceTheorem',
                                   'contains': 'atom'
                               }
                           })


class TestShiftValue:
    """ Test group for test_shift value function """
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

    schema_dict = InputSchemaDict.fromVersion('0.33')

    skip_paths = {
        'coreSpectrum', 'oneDParams', 'wannier', 'fields', 'xcParams', 'greensFunction', 'rdmft', 'ggaPrinting',
        'juPhon', 'spinSpiralQPointMesh', 'forceTheorem', 'bulkLattice', 'qsc', 'geometryOptimization',
        'fermiSmearingTemp', 'fixed_moment', 'plotting', 'expertModes', 'maxTimeToStartIter', 'ldaHIA', 'numberPoints'
    }

    attr_dict = {}
    attr_dict_float = {}
    for key, path in schema_dict['unique_attribs'].items():
        if key in schema_dict['attrib_types']:
            if 'int' in schema_dict['attrib_types'][key]:
                attr_dict[key] = path
            if 'float' in schema_dict['attrib_types'][key] or \
               'float_expression'  in schema_dict['attrib_types'][key]:
                attr_dict[key] = path
                attr_dict_float[key] = path

    @pytest.mark.parametrize('attr_name, path', attr_dict.items())
    def test_shift_value(self, inpxml_etree, attr_name, path):
        from aiida_fleur.tools.xml_util import shift_value, eval_xpath2
        etree = inpxml_etree(TEST_INP_XML_PATH)

        if any(x in path for x in self.skip_paths):
            pytest.skip('This attribute is not tested for FePt/inp.xml')

        result_before = eval_xpath2(etree, path)

        if not result_before:
            raise BaseException('Can not find attribute that should exist in FePt/inp.xml')
        else:
            result_before = result_before[0]
            shift_value(etree, self.schema_dict, {attr_name: 333})
            result = eval_xpath2(etree, path)[0]

            assert float(result) - float(result_before) == 333

            shift_value(etree, self.schema_dict, {attr_name: 333})
            result = eval_xpath2(etree, path)[0]
            assert float(result) - float(result_before) == 666

    @pytest.mark.parametrize('attr_name, path', attr_dict_float.items())
    def test_shift_value_rel(self, inpxml_etree, attr_name, path):
        import math
        from aiida_fleur.tools.xml_util import shift_value, eval_xpath2
        etree = inpxml_etree(TEST_INP_XML_PATH)

        if any(x in path for x in self.skip_paths):
            pytest.skip('This attribute is not tested for FePt/inp.xml')

        result_before = eval_xpath2(etree, path)

        if not result_before:
            raise BaseException('Can not find attribute that should exist in FePt/inp.xml')
        else:
            result_before = result_before[0]
            shift_value(etree, self.schema_dict, {attr_name: 1.2442}, mode='rel')
            result = eval_xpath2(etree, path)[0]

            if float(result_before) != 0:
                assert math.isclose(float(result) / float(result_before), 1.2442, rel_tol=1e-6)
            else:
                assert float(result) == 0

    def test_shift_value_errors(self, inpxml_etree, capsys):
        from aiida_fleur.tools.xml_util import shift_value
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)

        with pytest.raises(ValueError, match="You try to shift the attribute:'does_not_exist'"):
            shift_value(etree, schema_dict, {'does_not_exist': 1.2442})

        with pytest.raises(ValueError, match='You are trying to write a float'):
            shift_value(etree, schema_dict, {'jspins': 3.3})

        with pytest.raises(ValueError, match='Given attribute name is not float or int'):
            shift_value(etree, schema_dict, {'l_noco': 33})

        with pytest.raises(ValueError, match="Mode should be 'res' "):
            shift_value(etree, schema_dict, {'jspins': 33}, mode='not_a_mode')

        with pytest.raises(ValueError, match='The attrib nz has no possible paths with the current specification'):
            shift_value(etree, schema_dict, {'nz': 333})


class TestShiftSpeciesLabel:
    """ Test group for test_shift species label function """
    attr_names = ['radius', 'gridPoints', 'logIncrement', 'lmax', 'lnonsphr', 's', 'p', 'd', 'f']
    tags = [
        'mtSphere', 'mtSphere', 'mtSphere', 'atomicCutoffs', 'atomicCutoffs', 'energyParameters', 'energyParameters',
        'energyParameters', 'energyParameters'
    ]

    path_spec = {'energyParameters': {'contains': 'energyParameters'}}

    @pytest.mark.parametrize('att_name,tag', zip(attr_names, tags))
    def test_shift_species_label(self, inpxml_etree, att_name, tag):
        from aiida_fleur.tools.xml_util import shift_value_species_label, eval_xpath2
        import math
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)
        path = '/fleurInput/atomSpecies/species[@name = "Fe-1"]/' + tag + '/@' + att_name
        old_result = eval_xpath2(etree, path)[0]

        path_spec = self.path_spec.get(tag, {})

        shift_value_species_label(etree, schema_dict, '                 222', att_name, 3, mode='abs', **path_spec)
        result = eval_xpath2(etree, path)[0]

        assert math.isclose(float(result) - float(old_result), 3)

    attr_names_float = ['radius', 'logIncrement']
    tags_float = ['mtSphere', 'mtSphere']

    @pytest.mark.parametrize('att_name,tag', zip(attr_names_float, tags_float))
    def test_shift_species_label_rel(self, inpxml_etree, att_name, tag):
        from aiida_fleur.tools.xml_util import shift_value_species_label, eval_xpath2
        import math
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)
        path = '/fleurInput/atomSpecies/species[@name = "Fe-1"]/' + tag + '/@' + att_name
        untouched = '/fleurInput/atomSpecies/species[@name = "Pt-1"]/' + tag + '/@' + att_name
        old_result = eval_xpath2(etree, path)[0]
        untouched_result = eval_xpath2(etree, untouched)[0]

        shift_value_species_label(etree, schema_dict, '                 222', att_name, 3.2, mode='rel')
        result = eval_xpath2(etree, path)[0]
        untouched_result_new = eval_xpath2(etree, untouched)[0]

        assert math.isclose(float(result) / float(old_result), 3.2)
        assert math.isclose(float(untouched_result_new) / float(untouched_result), 1.0)

    @pytest.mark.parametrize('att_name,tag', zip(attr_names, tags))
    def test_shift_species_label_all(self, inpxml_etree, att_name, tag):
        from aiida_fleur.tools.xml_util import shift_value_species_label, eval_xpath2
        import numpy as np
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)
        path = '/fleurInput/atomSpecies/species/' + tag + '/@' + att_name
        old_result = np.array(eval_xpath2(etree, path)).astype('float')

        path_spec = self.path_spec.get(tag, {})

        shift_value_species_label(etree, schema_dict, 'all', att_name, 3, mode='abs', **path_spec)
        result = np.array(eval_xpath2(etree, path)).astype('float')

        assert np.all(np.isclose(old_result + 3, result))

    @pytest.mark.parametrize('att_name,tag', zip(attr_names, tags))
    def test_shift_species_label_all_rel(self, inpxml_etree, att_name, tag):
        from aiida_fleur.tools.xml_util import shift_value_species_label, eval_xpath2
        import numpy as np
        etree, schema_dict = inpxml_etree(TEST_INP_XML_PATH, return_schema=True)
        path = '/fleurInput/atomSpecies/species/' + tag + '/@' + att_name
        old_result = np.array(eval_xpath2(etree, path)).astype('float')

        path_spec = self.path_spec.get(tag, {})

        shift_value_species_label(etree, schema_dict, 'all', att_name, 2, mode='rel', **path_spec)
        result = np.array(eval_xpath2(etree, path)).astype('float')

        assert np.all(np.isclose(old_result * 2, result))


class TestAddNumToAtt:
    """ Test group for add_num_to_att function """
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

    schema_dict = InputSchemaDict.fromVersion('0.33')

    skip_paths = {
        'coreSpectrum', 'oneDParams', 'wannier', 'fields', 'xcParams', 'greensFunction', 'rdmft', 'ggaPrinting',
        'juPhon', 'spinSpiralQPointMesh', 'forceTheorem', 'bulkLattice', 'qsc', 'geometryOptimization',
        'fermiSmearingTemp', 'fixed_moment', 'plotting', 'expertModes', 'maxTimeToStartIter', 'ldaHIA', 'numberPoints'
    }

    attr_dict = {}
    attr_dict_float = {}
    for key, path in schema_dict['unique_attribs'].items():
        if key in schema_dict['attrib_types']:
            if 'int' in schema_dict['attrib_types'][key]:
                attr_dict[key] = path
            if 'float' in schema_dict['attrib_types'][key] or \
               'float_expression'  in schema_dict['attrib_types'][key]:
                attr_dict[key] = path
                attr_dict_float[key] = path

    @pytest.mark.parametrize('attr_name, path', attr_dict.items())
    def test_add_num_to_att(self, inpxml_etree, attr_name, path):
        from aiida_fleur.tools.xml_util import add_num_to_att, eval_xpath2
        etree = inpxml_etree(TEST_INP_XML_PATH)

        if any(x in path for x in self.skip_paths):
            pytest.skip('This attribute is not tested for FePt/inp.xml')

        result_before = eval_xpath2(etree, path)

        if not result_before:
            raise BaseException('Can not find attribute that should exist in FePt/inp.xml')
        else:
            result_before = result_before[0]
            add_num_to_att(etree, path.split('/@')[0], path.split('/@')[1], 333)
            result = eval_xpath2(etree, path)[0]

            assert float(result) - float(result_before) == 333

    @pytest.mark.parametrize('attr_name, path', attr_dict_float.items())
    def test_add_num_to_att_rel(self, inpxml_etree, attr_name, path):
        import math
        from aiida_fleur.tools.xml_util import add_num_to_att, eval_xpath2
        etree = inpxml_etree(TEST_INP_XML_PATH)

        if any(x in path for x in self.skip_paths):
            pytest.skip('This attribute is not tested for FePt/inp.xml')

        result_before = eval_xpath2(etree, path)

        if not result_before:
            raise BaseException('Can not find attribute that should exist in FePt/inp.xml')
        else:
            result_before = result_before[0]
            add_num_to_att(etree, path.split('/@')[0], path.split('/@')[1], 1.2442, mode='rel')
            result = eval_xpath2(etree, path)[0]

            if float(result_before) != 0:
                assert math.isclose(float(result) / float(result_before), 1.2442, rel_tol=1e-6)
            else:
                assert float(result) == 0


# get_xml_attribute
@pytest.mark.skip(reason='Test not implemented')
def test_get_xml_attribute(inpxml_etree):
    from aiida_fleur.tools.xml_util import get_xml_attribute
    return False
