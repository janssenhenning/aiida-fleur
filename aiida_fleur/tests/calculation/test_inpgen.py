"""Tests for the `FleurinputgenCalculation` class."""

from __future__ import absolute_import
from aiida import orm
from aiida.common import datastructures
from aiida_fleur.calculation.fleur import FleurCalculation


def test_fleurinpgen_default(aiida_profile, fixture_sandbox, generate_calc_job,
                             fixture_code, generate_structure):  # file_regression
    """Test a default `FleurinputgenCalculation`."""
    entry_point_name = 'fleur.inpgen'

    parameters = {}

    inputs = {
        'code': fixture_code(entry_point_name),
        'structure': generate_structure(),
        # 'parameters': orm.Dict(dict=parameters),
        'metadata': {
            'options': {'resources': {'num_machines': 1},
                        'max_wallclock_seconds': int(100),
                        'withmpi': False}
        }
    }

    calc_info = generate_calc_job(fixture_sandbox, entry_point_name, inputs)

    cmdline_params = ['-explicit']
    local_copy_list = []
    retrieve_list = ['inp.xml', 'out', 'shell.out', 'out.error', 'struct.xsf', 'aiida.in']
    retrieve_temporary_list = []

    # Check the attributes of the returned `CalcInfo`
    assert isinstance(calc_info, datastructures.CalcInfo)
    codes_info = calc_info.codes_info
    assert sorted(codes_info[0].cmdline_params) == sorted(cmdline_params)
    assert sorted(calc_info.local_copy_list) == sorted(local_copy_list)
    assert sorted(calc_info.retrieve_list) == sorted(retrieve_list)
    #assert sorted(calc_info.retrieve_temporary_list) == sorted(retrieve_temporary_list)
    assert sorted(calc_info.remote_symlink_list) == sorted([])

    with fixture_sandbox.open('aiida.in') as handle:
        input_written = handle.read()

    aiida_in_text = """A Fleur input generator calculation with aiida\n&input  cartesian=F /
      5.1306064508       5.1306064508       0.0000000000
      5.1306064508       0.0000000000       5.1306064508
      0.0000000000       5.1306064508       5.1306064508
      1.0000000000
      1.0000000000       1.0000000000       1.0000000000

      2\n         14       0.0000000000       0.0000000000       0.0000000000
         14       0.2500000000       0.2500000000       0.2500000000\n"""
    # Checks on the files written to the sandbox folder as raw input
    assert sorted(fixture_sandbox.get_content_list()) == sorted(['aiida.in'])
    assert input_written == aiida_in_text
    #file_regression.check(input_written, encoding='utf-8', extension='.in')
