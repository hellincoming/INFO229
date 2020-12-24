import pytest
def input_value():
   st='hola'
   return st

def invertir(input_value):
   inv=''
   n=len(input_value)
   for x in range (len(input_value)):
      inv+=input_value[n-1]
      n-=1
   return inv

@pytest.mark.parametrize("input_value, output", [('buyaka','akayub'),('wena','anew'),('holi','iloh')])
def test_inversa(input_value, output):
   assert invertir(input_value) == output