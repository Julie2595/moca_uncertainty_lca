'''
NEXT STEPS:
   - How can I run a test, without having this whole code?
   - Which mock-object I need to replace the method-item
      and which configurations it must have?
'''

import pytest
# import method to test
from src.moca_uncertainty_lca.monte_carlo import MonteCarloLCA as mc
# import MagicMock
from unittest.mock import MagicMock

# implement mock object
mock_mc_lca = MagicMock()
mock_mc_lca.mc_results = {
   "quantity [unit]": [1,2,3,4,5], 
   "quantity2 [unit2]": [6,7,8,9,10]
}
mock_mc_lca.lcia_methods = [
   ('database','method','quantity [unit]'),
   ('database2','method2','quantity2 [unit2]')
]
mock_mc_lca.key_list = [
   'quantity [unit]',
   'quantity2 [unit2]'
]

# implement mock method
mock_method = (
   ('database','method','quantity [unit]'),
   ('database2','method2','quantity2 [unit2]'),
   ('database3','method3','quantity3 [unit3]')   
)

# implement a second mock object
mock_mc_lca_2 = MagicMock()
mock_mc_lca_2.mc_results = {
   "quantity [unit]": [1,2,3,4,5], 
   "quantity2 [unit2]": [6,7,8,9,10],
   'quantity3 [unit3]': [11,12,13,14,15]
}
mock_mc_lca_2.lcia_methods = [
   ('database','method','quantity [unit]'),
   ('database2','method2','quantity2 [unit2]'),
   ('database3','method3','quantity3 [unit3]')
]
mock_mc_lca_2.key_list = [
   'quantity [unit]',
   'quantity2 [unit2]',
   'quantity3 [unit3]'
]

# test method get_results_dataframe
def test_get_one_method():
   result = mc.get_results_dataframe(self = mock_mc_lca, method = mock_method[1])
   print("\n") 
   print(result)

def test_get_two_methods():
   result_two = mc.get_results_dataframe(self = mock_mc_lca, method = mock_method[:2])
   print("\n")
   print(result_two)

def test_get_three_methods():
   with pytest.raises(ValueError):
      result_three = mc.get_results_dataframe(self = mock_mc_lca, method = mock_method)
      print("\n")
      print(result_three)

def test_get_three_methods_2():
   # with pytest.raises(ValueError):
      result_three_2 = mc.get_results_dataframe(self = mock_mc_lca_2, method = mock_method)
      print("\n")
      print(result_three_2)