import pytest
def input_value():
   n = 6
   return n

def fibonacci(input_value):
   p=0
   s=1
   for x in range(input_value):
      c=p+s
      p=s
      s=c
   return p

@pytest.mark.parametrize("input_value, output", [(5,5),(7,13),(9,34),(11,89)])
def test_min(input_value, output):
   assert fibonacci(input_value) == output