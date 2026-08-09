'''
Instead of using a MagicMock-Object here a Stub-Object is used to test the function. 
Using the package "dataclasses".
'''

from src.moca_uncertainty_lca.monte_carlo import MonteCarloLCA as mc
import pytest
from dataclasses import dataclass

@dataclass
class mcLCAStub:
	mc_results: dict
	lcia_methods: list
	key_list: list

mcLCA_1 = mcLCAStub(
	{
		"quantity [unit]": [1,2,3,4,5], 
		"quantity2 [unit2]": [6,7,8,9,10]},
	[
		('database','method','quantity [unit]'),
		('database2','method2','quantity2 [unit2]')], 
	[
		'quantity [unit]',
		'quantity2 [unit2]']
)

mcLCA_2 = mcLCAStub(
	{
		"quantity [unit]": [1,2,3,4,5], 
		"quantity2 [unit2]": [6,7,8,9,10],
		'quantity3 [unit3]': [11,12,13,14,15]},
	[
		('database','method','quantity [unit]'),
		('database2','method2','quantity2 [unit2]'),
		('database3','method3','quantity3 [unit3]')],
	[
		'quantity [unit]',
		'quantity2 [unit2]',
		'quantity3 [unit3]']
)

# implement mock method
mock_method = (
	('database','method','quantity [unit]'),
	('database2','method2','quantity2 [unit2]'),
	('database3','method3','quantity3 [unit3]')   
)

# test method get_results_dataframe
def test_get_one_method():
	result = mc.get_results_dataframe(self = mcLCA_1, method = mock_method[1])
	print("\n") 
	print(result)

def test_get_two_methods():
	result_two = mc.get_results_dataframe(self = mcLCA_1, method = mock_method[:2])
	print("\n")
	print(result_two)

def test_get_three_methods():
	with pytest.raises(ValueError):
		result_three = mc.get_results_dataframe(self = mcLCA_1, method = mock_method)
		print("\n")
		print(result_three)

def test_get_three_methods_2():
	# with pytest.raises(ValueError):
		result_three_2 = mc.get_results_dataframe(self = mcLCA_2, method = mock_method)
		print("\n")
		print(result_three_2)