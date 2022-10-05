# Name: Wenhao Chen
# Course: CS261 - Data Structures
# Description: Hash table implementation with separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates key/value pairs in the hash map.
        If key exists, replace its value with the new value.
        If key does not exist, add the new key/value pair.
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()

        # if bucket already contains a node with matching key, modify node instead of inserting node
        linked_list = self._buckets.get_at_index(index)
        matching_node = linked_list.contains(key)
        if matching_node is not None:
            matching_node.value = value
        else:
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        """
        empty_count = 0
        for idx in range(self.get_capacity()):
            linked_list = self._buckets.get_at_index(idx)
            if linked_list.length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """
        Return the hash table load factor.
        load factor = n elements / m buckets
        """
        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        Clear the content of the hash map.
        """
        self._size = 0
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())


    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the has table.
        Move all existing key/value pairs. Rehash the links.
        """
        if new_capacity < 1:
            return
        elif not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # preserve data
        old_da = self._buckets

        # update capacity and clear da
        self._capacity = new_capacity
        self.clear()

        # rehash existing key, value pairs
        for idx in range(old_da.length()):
            linked_list = old_da.get_at_index(idx)
            for node in linked_list:
                self.put(node.key, node.value)


    def get(self, key: str) -> object:
        """
        Receives a key.
        Returns the value associated with the key.
        If the key is not in the hash map, return None.
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()

        linked_list = self._buckets.get_at_index(index)
        for node in linked_list:
            if node.key == key:
                return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Receives a key.
        Returns true if the key is in the hash map.
        Otherwise, returns false.
        """
        if self.get_size() == 0:
            return False

        hash = self._hash_function(key)
        index = hash % self.get_capacity()

        linked_list = self._buckets.get_at_index(index)
        for node in linked_list:
            if node.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Receives a key.
        Remove that key and the corresponding value from the hash map.
        Does nothing if it doesn't find the key.
        """
        if self.get_size() == 0:
            return

        hash = self._hash_function(key)
        index = hash % self.get_capacity()

        linked_list = self._buckets.get_at_index(index)
        if linked_list.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing a tuple of (key, value)
        for each key/value pair in the hash map.
        """
        tuple_array = DynamicArray()
        for idx in range(self._buckets.length()):
            linked_list = self._buckets.get_at_index(idx)
            for node in linked_list:
                tuple_array.append((node.key, node.value))

        return tuple_array

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives an unsorted dynamic array.
    Return a tuple containing a dynamic array and an integer.
    The dynamic array should contain the mode value(s). Ties are allowed.
    The integer should be the count of occurrences of one of the mode values.
    O(N) required.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(capacity=da.length())

    # use the input dynamic array values as the key
    # use the value in the key/value pair to track occurrence count
    # because of determinism, the same value will always result in the same bucket index
    mode_da = DynamicArray()
    mode_count = 0
    for idx in range(da.length()):
        key = da.get_at_index(idx)
        # encounter a value for the second time or more
        if map.contains_key(key):
            current_count = map.get(key)
            new_count = current_count + 1
            map.put(key, new_count)
        # encountering a value for the first time
        else:
            map.put(key, 1)

        # check if we need to update mode values and candidates
        # this is the current count after put/update
        current_count = map.get(key)
        if current_count == mode_count:
            mode_da.append(key)
        elif current_count > mode_count:
            mode_count = current_count
            # clear the array because there's a new unique mode value
            mode_da = DynamicArray()
            mode_da.append(key)

    return mode_da, mode_count

