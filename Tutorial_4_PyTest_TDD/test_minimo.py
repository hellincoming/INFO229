import pytest
def input_value():
   array = [13,23,11,4,5,7,9]
   return array

def minimo(input_value):
   mini=input_value[0]
   for i in range (len(input_value)):
      if(mini>=input_value[i]):	      
         mini=input_value[i]
   return mini

@pytest.mark.parametrize("array, output",[([8,4,5,1],1),([1,3,4,6,8],1),([999,619],619),([14,42,6,44],6)])
def test_min(array, output):
   assert minimo(array) == output