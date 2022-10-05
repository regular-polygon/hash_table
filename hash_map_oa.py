# Name: Wenhao Chen
# Course: CS261 - Data Structures
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


