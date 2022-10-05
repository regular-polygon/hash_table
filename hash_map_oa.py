# Name: Wenhao Chen
# OSU Email: chenwenh@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/22
# Description: Hash map implementation with open addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Resizes the table if load factor is equal to or above 0.5
        Update a key/value pair in the hash map.
        For existing key, update value.
        For new key, add key/value pair.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            new_capacity = 2 * self.get_capacity()
            self.resize_table(new_capacity)

        # hashing the key to get dynamic array index
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        initial_index = index

        # quadratic probe until there's no collision
        hash_entry = self._buckets.get_at_index(index)
        quad_index = 1
        while hash_entry is not None and not hash_entry.is_tombstone:
            # check for duplicate key
            if hash_entry.key == key:
                hash_entry.value = value
                return
            # quadratic probing
            index = (initial_index + quad_index ** 2) % self.get_capacity()
            quad_index += 1
            hash_entry = self._buckets.get_at_index(index)

        # exit while loop once a space is available
        if hash_entry is None:
            new_hash_entry = HashEntry(key, value)
            self._buckets.set_at_index(index, new_hash_entry)
            self._size += 1
        elif hash_entry.is_tombstone:
            new_hash_entry = HashEntry(key, value)
            self._buckets.set_at_index(index, new_hash_entry)
            self._size += 1



    def table_load(self) -> float:
        """
        Returns the hash table load factor with open addressing.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_count = 0
        for idx in range(self._buckets.length()):
            hash_entry = self._buckets.get_at_index(idx)
            if hash_entry is None:
                empty_count += 1
            elif hash_entry.is_tombstone:
                empty_count += 1

        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hash table.
        Rehash all hash table links.
        """
        if new_capacity < self.get_size():
            return
        elif not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
            self._capacity = new_capacity
        else:
            self._capacity = new_capacity

        old_da = self._buckets
        self.clear()

        for idx in range(old_da.length()):
            hash_entry = old_da.get_at_index(idx)
            if hash_entry is not None and not hash_entry.is_tombstone:
                self.put(hash_entry.key, hash_entry.value)

    def get(self, key: str) -> object:
        """
        Returns the value corresponding with the given key.
        Return none if the key is not found.
        """
        if self.get_size() == 0:
            return None

        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        initial_index = index

        # quadratic probe until we hit None or a matching entry
        hash_entry = self._buckets.get_at_index(index)
        quad_index = 1
        while hash_entry is not None:
            if hash_entry.key == key and not hash_entry.is_tombstone:
                return hash_entry.value
            index = (initial_index + quad_index ** 2) % self.get_capacity()
            quad_index += 1
            hash_entry = self._buckets.get_at_index(index)

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the given key is in the hash map.
        Otherwise, returns false.
        """
        if self.get_size() == 0:
            return False

        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        initial_index = index

        # quadratic probe until we hit None or a matching entry
        hash_entry = self._buckets.get_at_index(index)
        quad_index = 1
        while hash_entry is not None:
            if hash_entry.key == key and not hash_entry.is_tombstone:
                return True
            elif hash_entry.key == key and hash_entry.is_tombstone:
                return False
            index = (initial_index + quad_index ** 2) % self.get_capacity()
            quad_index += 1
            hash_entry = self._buckets.get_at_index(index)

        return False

    def remove(self, key: str) -> None:
        """
        "removes" the key/value pair corresponding with the given key.
        Doesn't actually delete the pair, only sets is_tombstone to true.
        If key is not found, does nothing.
        """
        if self.get_size() == 0:
            return

        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        initial_index = index

        # quadratic probe until we hit None or a matching entry
        hash_entry = self._buckets.get_at_index(index)
        quad_index = 1
        while hash_entry is not None:
            if hash_entry.key == key and not hash_entry.is_tombstone:
                hash_entry.is_tombstone = True
                self._size -= 1
                return
            elif hash_entry.key == key and hash_entry.is_tombstone:
                return
            index = (initial_index + quad_index ** 2) % self.get_capacity()
            quad_index += 1
            hash_entry = self._buckets.get_at_index(index)

        return

    def clear(self) -> None:
        """
        Clear the content of the hash map.
        Does not change the hash table capacity.
        """
        self._size = 0
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of tuples (key, value)
        stored in the hash map
        """
        tuples_da = DynamicArray()

        for idx in range(self._buckets.length()):
            hash_entry = self._buckets.get_at_index(idx)
            if hash_entry is not None:
                if not hash_entry.is_tombstone:
                    tuples_da.append((hash_entry.key, hash_entry.value))

        return tuples_da


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        pass
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')
        pass

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
        pass

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
