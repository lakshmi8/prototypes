import uuid
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, num_hash_fns):
        self.bit_array_size = size
        self.bit_array = bitarray(self.bit_array_size)
        self.bit_array.setall(0)
        self.num_hash_fns = num_hash_fns

    def insert(self, x):
        for i in range(self.num_hash_fns):
            hash_index = mmh3.hash(x, i) % self.bit_array_size
            self.bit_array[hash_index] = True

    def lookup(self, x):
        for i in range(self.num_hash_fns):
            hash_index = mmh3.hash(x, i) % self.bit_array_size
            if self.bit_array[hash_index] == False:
                return False
        return True

def generate_uuid():
    return uuid.uuid4()

if __name__ == '__main__':
    num_hash_fns = 100
    bit_array_size = 10000

    dataset = []
    dataset_exists = []
    dataset_not_exists = []

    for i in range(500):
        x = str(generate_uuid())
        dataset.append(x)
        dataset_exists.append(x)

    for i in range(500):
        x = str(generate_uuid())
        dataset.append(x)
        dataset_not_exists.append(x)

    for i in range(1, num_hash_fns):
        bloom_filter = BloomFilter(bit_array_size, i)

        for x in dataset_exists:
            bloom_filter.insert(x)

        false_positive_cnt = 0
        for x in dataset:
            is_present = bloom_filter.lookup(x)
            if is_present and x in dataset_not_exists:
                false_positive_cnt += 1

        false_positive_pct = false_positive_cnt/1000
        print("False positive percentage = ", round(false_positive_pct * 100, 2))
