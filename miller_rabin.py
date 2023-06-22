import math, random, sys

class ModularExponentiation:
    def __init__(self, base: int, exponent: int, mod: int) -> None:
        """
        A class to perform modular exponentiation
        """

        # base, exponent and mod
        self.base = base
        self.exponent = exponent
        self.mod = mod

        # to store the final answer
        self.ans = 1

        # to perform the modular exponentiation
        self.mod_exp()

    def mod_exp(self) -> None:
        """
        Modular exponenentiation with repeated squaring for 
        efficiency.

        :Complexity:
        :Time          : O(log N), where N is the exponent
        :Aux Space     : O(log N), where N is the exponent
        """

        # bit length of the exponent
        bit_length = self.exponent.bit_length()

        # to store the results of the repeated squaring
        result_list = [0] * bit_length
        
        # start with the base to apply the repeated squaring
        result_list[0] = self.base % self.mod

        # check if the last bit of the exponent is 1
        self.check_bit(result_list[0])

        # for repeated squaring
        for i in range(1, bit_length):

            # repeated squaring
            result_list[i] = (result_list[i-1] * result_list[i-1]) % self.mod

            # check if the current bit is 1
            # starts chceking the bit from behind
            self.check_bit(result_list[i])
            
        return 
    def check_bit(self, value: int) -> None:
        """
        To check if the current bit of the exponent is 1 so
        that it could contribute to the final answer.
        """
            
        # check if the current bit of the exponent is 1
        if (self.exponent & 1 ) == 1:      

            # if yes, contribute to final answer                           
            self.ans = (self.ans * value) % self.mod     

        # move to next bit of exponent  
        self.exponent >>= 1

    def get_ans(self) -> int:
        return self.ans
    
class MillerRabin:
    def __init__(self, value: int) -> None:
        """
        A class to perform Miller-Rabin primality test.
        """
        # value to be tested
        self.value = value
        self.k = self.optimal_k()

        # to store the result
        # True if prime, False if composite
        self.is_prime = self.run()

    def optimal_k(self) -> int:
        """
        To calculate the optimal k value for the Miller-Rabin based
        on the value to be tested.
        """
        return int(math.log(self.value) + 1)

    def run(self) -> bool: 
        """
        To run the Miller-Rabin primality test. Will return true if
        self.value is a prime, false if composite. 

        :Complexity:
        :Time          : O(k log^3 N), where k is the optimal k value and N is the value to be tested
        :Aux Space     : O(1)

        Citation: FIT3155 Week 6 Lecture Notes
        """

        # check if the value is 2 or 3 (special prime cases)
        if self.value == 2 or self.value == 3:
            return True
        
        # if it is even, it is composite
        if self.value % 2 == 0:
            return False
        
        counter = 0

        t = self.value - 1

        # divide t by 2 until it is odd
        while t % 2 == 0:

            # tracks it with the counter
            counter += 1
            t //= 2

        # run k times. k is based on n
        for _ in range(self.k):
            
            # get a random number between 2 and n-2 inclusive
            random_number = random.randint(2, self.value - 2)

            # calculate the modular exponentiation of random_number^t mod n
            previous = ModularExponentiation(random_number, t, self.value).get_ans()

            # to run the sequence test
            for _ in range(1, counter + 1):

                # based on repeated squaring
                current = (previous * previous) % self.value

                if current == 1 and (previous != 1 and previous != self.value - 1):
                    return False
                
                previous = current
            
            # check if the self.value satisifies Fermat's Little Theorem
            if ModularExponentiation(random_number, self.value - 1, self.value).get_ans() != 1:
                return False

        # probably is prime     
        return True
        
    def get_result(self) -> bool:
        """
        To return the result of the Miller-Rabin test in
        a form of a boolean.
        """
        return self.is_prime
