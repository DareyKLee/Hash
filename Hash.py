import unittest

'''
Description: Dictionary implemented with nested lists
Author: DAREY LEE

Help received from: Stackoverflow.com (https://stackoverflow.com/questions/26660654/how-do-i-print-
                                the-key-value-pairs-of-a-dictionary-in-python)
'''

'''
    Implement a dictionary using chaining.
    You may assume every key has a hash() method, e.g.:
    >>> hash(1)
    1
    >>> hash('hello world')
    -2324238377118044897
'''


class dictionary:
    def __init__(self, init=None):
        self.__limit = 10
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0

        if init:
            for i in init:
                self.__setitem__(i[0], i[1])

    def __len__(self):
        return self.__count

    def flattened(self):
        return [item for inner in self.__items for item in inner]

    def __iter__(self):
        return (iter(self.flattened()))

    def __str__(self):
        return (str(self.flattened()))

    def __setitem__(self, key, value):
        if not self.__contains__(key):
            self.__items[self.page_number(key)].append([key, value])
            self.__count += 1

            if self.__count >= (.75 * self.__limit):
                self.doubling_rehash_up()

        else:
            for slot in self.__items[self.page_number(key)]:
                if slot[0] == key:
                    if slot[1] != value:
                        slot[1] = value

    def __getitem__(self, key):
        for slot in self.__items[self.page_number(key)]:
            if slot[0] == key:
                return slot[1]

        return "==KEY NOT FOUND=="

    def __contains__(self, key):
        for slot in self.__items[self.page_number(key)]:
            if slot[0] == key:
                return True

        return False

    def page_number(self, key):
        return hash(key) % self.__limit

    def doubling_rehash_up(self):
        self.__limit *= 2
        self.rehash()

    def halving_rehash_down(self):
        self.__limit //= 2
        self.rehash()

    def rehash(self):
        new_list = [[] for _ in range(self.__limit)]

        for item in self.flattened():
            new_list[hash(item[0]) % self.__limit].append(item)

        self.__items = new_list

    def number_of_pages(self):
        num_pages = 0

        for page in self.__items:
            num_pages += 1

        return num_pages

    def __delitem__(self, key):
        entry = 0

        for slot in self.__items[self.page_number(key)]:
            if slot and slot[0] == key:
                self.__items[self.page_number(key)].pop(entry)
                self.__count -= 1

                if self.__count <= (.25 * self.__limit) and self.__limit > 10:
                    self.halving_rehash_down()

            entry += 1

    def keys(self):
        list_of_keys = []

        for item in self.sort():
            list_of_keys.append(item[0])

        return list_of_keys

    def values(self):
        list_of_values = []

        for item in self.sort():
            list_of_values.append(item[1])

        return list_of_values

    def has_none_key(self):
        for item in self.flattened():
            if item[0] is None:
                return True

        return False

    def items(self):
        list_of_items = []

        for item in self.sort():
            list_of_items.append((item[0], item[1]))

        return list_of_items

    def sort(self):
        if self.has_none_key():
            index = 0
            item_list = self.flattened()

            for item in item_list:
                if item[0] is None:
                    temp = item_list.pop(index)
                    break

                index += 1

            item_list = sorted(item_list)
            item_list.insert(0, temp)

            return item_list

        else:
            return sorted(self.flattened())

    def __eq__(self, other_dictionary):
        return self.flattened() == other_dictionary.flattened()

''' C-level work '''

class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], "one")
        self.assertEqual(s[2], "two")

class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[1] = "one"
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], "one")

class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertFalse(s[1])

class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)

class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)

class test_False_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)

class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)

''' B-level work '''

class test_doubling_rehash(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[4] = "four"
        s[14] = "fourteen"
        self.assertEqual(s.number_of_pages(), 10)
        self.assertEqual(s.page_number(14), 4)

        for i in range(10):
            if s[i] == "==KEY NOT FOUND==":
            #if self.assertRaises(RuntimeError, lambda: s[i]):
                s[i] = "FILLED"

        self.assertEqual(s.number_of_pages(), 20)
        self.assertEqual(s.page_number(4), 4)
        self.assertEqual(s.page_number(14), 14)

        s[24] = "twenty four"
        s[34] = "thirty four"

        for i in range(20):
            if s[i] == "==KEY NOT FOUND==":
            #if self.assertRaises(RuntimeError, lambda: s[i]):
                s[i] = "FILLED"

        self.assertEqual(s.number_of_pages(), 40)
        self.assertEqual(s.page_number(24), 24)
        self.assertEqual(s.page_number(34), 34)

class test_delete_item(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = "zero"
        s[1] = "one"

        self.assertTrue(s.__contains__(None))
        self.assertTrue(s.__contains__(1))
        self.assertEqual(s.__len__(), 2)

        s.__delitem__(None)
        self.assertFalse(s.__contains__(None))
        self.assertEqual(s.__len__(), 1)

        s.__delitem__(1)
        self.assertFalse(s.__contains__(1))
        self.assertEqual(s.__len__(), 0)

''' A-level work '''

class test_halving_rehash(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[3] = "three"
        s[13] = "thirteen"
        s[23] = "twenty three"
        s[33] = "thirty three"
        s[43] = "forty three"

        for i in range(10):
            if s[i] == "==KEY NOT FOUND==":
                s[i] = "FILLED"

        self.assertEqual(s.number_of_pages(), 20)
        self.assertEqual(s.page_number(3), 3)
        self.assertEqual(s.page_number(13), 13)
        self.assertEqual(s.page_number(23), 3)
        self.assertEqual(s.page_number(33), 13)
        self.assertEqual(s.page_number(43), 3)

        for entry in s:
            if s[entry[0]] == "FILLED":
                s.__delitem__(entry[0])

        self.assertEqual(s.number_of_pages(), 10)
        self.assertEqual(s.page_number(3), 3)
        self.assertEqual(s.page_number(13), 3)
        self.assertEqual(s.page_number(23), 3)
        self.assertEqual(s.page_number(33), 3)
        self.assertEqual(s.page_number(43), 3)

class test_list_all_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[35] = "thirty five"
        s[555] = "five hundred fifty five"
        s[None] = "NONE"
        s[5] = "five"
        self.assertEqual(s.keys(), [None, 5, 35, 555])

class test_list_all_values(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[3] = "three"
        s[989] = "nine hundred eighty nine"
        s[25] = "twenty five"
        s[None] = "NONE"
        self.assertEqual(s.values(), ["NONE", "three", "twenty five", "nine hundred eighty nine"])

class test_key_not_found(unittest.TestCase):
    def test(self):
        s = dictionary()
        self.assertEqual(s[3], "==KEY NOT FOUND==")

''' Extra credit '''

class test_eq(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"

        x = dictionary()
        x[1] = "one"
        x[2] = "two"

        y = dictionary()
        y[None] = "NONE"
        y[25] = "twenty five"

        self.assertTrue(s.__eq__(x))
        self.assertFalse(s.__eq__(y))

class test_items(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[398] = "three hundred ninety eight"
        s[7] = "seven"
        s[None] = "NONE"
        s[1002] = "one thousand two"
        self.assertEqual(s.items(), [(None, "NONE"), (7, "seven"), (398, "three hundred ninety eight"),
                                     (1002, "one thousand two")])

if __name__ == '__main__':
    unittest.main()