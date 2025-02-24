import math
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, fpr, num_ob):
        """
        Initialization of bloom filter
        :param fpr: Desired false positivity rate
        :type fpr: float
        :param num_ob: Number of objects to be inserted into the bloom filter
        :type num_ob: int
        """
        self.false_positivity_rate = fpr
        self.num_objects = num_ob
        self.bit_array_size =  self.get_bit_array_size(self.false_positivity_rate, self.num_objects)
        self.num_hash_fns = self.get_num_hash_fns(self.num_objects, self.bit_array_size)
        self.bit_array = bitarray(self.bit_array_size)
        self.bit_array.setall(0)

    def get_bit_array_size(self, false_positivity_rate, num_objects):
        """
        Determining the bloom filter size based on false positivity rate and the number of objects to be inserted
        :param false_positivity_rate: Desired false positivity  rate
        :type false_positivity_rate: float
        :param num_objects: Number of objects to be inserted into the bloom filter
        :type num_objects: int
        :return: Bit array size
        :rtype: int
        """
        bit_array_size = -(num_objects * math.log(false_positivity_rate)) / (math.log(2) ** 2)
        return int(bit_array_size)

    def get_num_hash_fns(self, num_objects, bit_array_size):
        """
        Determing the number of hash functions based on bit array size and the number of objects to be inserted
        :param num_objects: Number of objects to be inserted  into the bloom filter
        :type num_objects: int
        :param bit_array_size: Bit array size
        :type bit_array_size: int
        :return: Number of hash functions
        :rtype: int
        """
        num_hash_fns = (bit_array_size / num_objects) * math.log(2)
        return int(num_hash_fns)

    def insert(self, x):
        """
        Inserting an element into the bloom filter
        :param x: Element to insert into the bloom filter
        :type x: string
        :return: None
        :rtype: None
        """
        for i in range(self.num_hash_fns):
            hash_index = mmh3.hash(x, i) % self.bit_array_size
            self.bit_array[hash_index] = True

    def lookup(self, x):
        """
        Checking for existence in the bloom filter
        :param x: Element to check for existence
        :type x: string
        :return: Existence of the element
        :rtype: bool
        """
        for i in range(self.num_hash_fns):
            hash_index = mmh3.hash(x, i) % self.bit_array_size
            if self.bit_array[hash_index] == False:
                return False
        return True

if __name__ == '__main__':
    # Create a bloom filter for 1000 items and 1% false positivity rate
    bloom_filter = BloomFilter(0.01, 1000)

    # Insert elements into the bloom filter
    bloom_filter.insert("Lakshmi")

    # Lookup for elements in a bloom filter
    print(bloom_filter.lookup("Lakshmi")) # Checking for existent item, should return True
    print(bloom_filter.lookup("Velan")) # Checking a non-existent item, should return False  (with 1% probability
    # of returning true)
    print(bloom_filter.lookup("Abhishek")) # Checking a non-existent item, should return False  (with 1% probability
    # of returning true)

    # Print the parameters values
    print("Size of bloom filter = ", bloom_filter.bit_array_size)
    print("Number of hash functions = ", bloom_filter.num_hash_fns)

