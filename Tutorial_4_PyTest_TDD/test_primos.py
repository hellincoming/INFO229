import math
import pytest
def input_value():
   array = [13,23,11,4,5,7,9,2,3]
   return array

def is_prime(num):
    # Prime numbers must be greater than 1
    if num < 2:
        return False
    #Prime numbers mu
    for n in range(2, math.floor(math.sqrt(num) + 1)):
        if num % n == 0:
            return False
    return True

def sum_of_primes(input_value):
    su = 0
    for x in range (len(input_value)):
        if(is_prime(input_value[x])):
            su+=input_value[x]

    return su        

@pytest.mark.parametrize("array, output",[([8,4,5,1],5),([1,3,4,6,8],3),([999,61],61),([14,42,6,44],0)])
def test_sum_pr(array, output):
   assert sum_of_primes(array) == output
