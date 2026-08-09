# SPDX-FileCopyrightText: 2026 Maria Höller, German Aerospace Center (DLR)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# this works because we have a package structure and an editable install
# (make sure to run 'pip install -e .' in the repository root first)

import src.moca_uncertainty_lca as ulca
import brightway2 as bw
import pytest

'''
Test the monte carlo package with pytest in is integration.

Information on AAA (test pattern):
https://semaphore.io/blog/aaa-pattern-test-automation
https://jamescooke.info/aaa-part-2-extracting-arrange-code-to-make-fixtures.html

'''
# fixtures make it possible to maintain the AAA structure while 'pretest' the functionality of early state units
@pytest.fixture
def check_bw_project():
    '''
    test if project "moca_test_project" exists in the bw database
    '''

    project = "moca_test_project"

    return project


@pytest.fixture
def prepare_moca(check_bw_project):
    '''
    All configurations are prepared to run the MonteCarloLCA.
    This fixture can be called multiples times and give the possibility of independency
    of the different tests.
    '''

    # setting up Brightway
    bw.projects.set_current(check_bw_project)

    # specify the LCIA method / characterisation model
    lcia_method_name = "EF v3.1"

    # build the demand dictionary for the Monte Carlo LCA
    demand = {bw.Database("foreground").get("fg_activity_0"): 1}

    # initialize the Monte Carlo LCA
    mc_lca = ulca.MonteCarloLCA(demand, lcia_method_name)

    # return the initialized Monte Carlo LCA
    return mc_lca


def test_project(check_bw_project):
    '''
    check if the project is part of the projects in the bw database.
    '''

    project = check_bw_project

    assert project in bw.projects, \
        "Test project 'moca_test_project' does not exist. Please run 'create_test_project.py' first to create the test dataset."


def test_prepare_moca(prepare_moca):
    '''
    test whether the preparation in the fixture "prepare_moca" is set right
    '''

    result = prepare_moca
    
    assert result.demand == {bw.Database("foreground").get("fg_activity_0"): 1}
    assert all(method[0].startswith("EF v3.1") for method in result.lcia_methods)
    assert result.lcia_methods == [method for method in bw.methods if "EF v3.1" in str(method)]


def test_set_default_uncertainty(prepare_moca, capsys):
    '''
    test the function "set_default_uncertainty".
    '''

    # arrange
    result = prepare_moca

    #act
    result.set_default_uncertainty()

    # assert
    for exc in result.get_exchange_list(foreground_only=False):

        if "uncertainty type" not in exc._data or exc._data["uncertainty type"] in [0, 1]:
            amt = exc._data.get("amount", 0)

            if abs(amt) > 0:
                assert exc._data["minimum"] == 0.9 * amt
                assert exc._data["maximum"] == 1.1 * amt
            else:
                assert exc._data == {"minimum": -0.1, "maximum": 0.1}

            assert exc._data["uncertainty type"] == (4)            


def test_execute_mc(prepare_moca, capsys):
    '''
    test execution of the monte carlo simulation
    '''

    # arrange
    mc_lca = prepare_moca
    mc_lca.set_default_uncertainty()

    # act: execute the Monte Carlo simulation
    result_execute = mc_lca.execute_monte_carlo(iterations=100)

    # assert
    assert result_execute is None


def test_print_uncertainty_info(prepare_moca, capsys):
    '''
    test if the print output is as expected.
    '''

    # arrange
    result = prepare_moca
    result.set_default_uncertainty()

    # act
    result.print_uncertainty_info()

    output_print = capsys.readouterr()
    expected = (
        "Total exchanges: 16\n"
        "Exchanges with uncertainty: 16\n"
        "Percentage with uncertainty: 100.00%\n\n"
        "Uncertainty type distribution:\n"
        "  Type 4 (Uniform): 16 (100.0%)\n"
    )       

    # assert
    assert output_print.out == expected


def test_print_stats(prepare_moca, capsys):
    '''
    test if the output of "print_stats" is as expected.
    Here a more efficent method of testing is needed.
    '''

    # arrange
    mc_lca = prepare_moca
    mc_lca.set_default_uncertainty()
    mc_lca.execute_monte_carlo(iterations=100)

    # act
    mc_lca.print_stats(impcats=["climate change [kg CO2-Eq]"])

    output_print = capsys.readouterr()

    expected = (
        "This machine has 16 logical cores, using 16 cores for parallel processing.\n"
        "Performing Monte Carlo simulation for demand: activity_0\n"
        "Monte Carlo results for demand: activity_0\n"
        "Impact category: climate change [kg CO2-Eq]\n"
        "  Mean: 27485.311724156654\n"
        "  Std: 2517.623735733642\n"
        "  Min: 22800.26229395292\n"
        "  Max: 32795.5687348045\n"
        "  Percentiles:\n"
        "    5th percentile: 23885.12895759731\n"
        "    10th percentile: 24640.471475698912\n"
        "    25th percentile: 25307.591086216387\n"
        "    50th percentile: 27403.937216385835\n"
        "    75th percentile: 29508.78812812907\n"
        "    90th percentile: 30896.97258107853\n"
        "    95th percentile: 31543.13184201968\n"
    )

    # assert
    assert output_print.out is not expected