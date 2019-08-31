import practice as p
import random
import collections
import operator

class TestPractice(object):
    def test_hello_world(self):
        assert 'Hello, World!' == p.hello_world()

    def test_empty_sum_without_dups(self):
        l = []
        assert 0 == p.sum_without_dups(l)
    
    def test_sum_without_dups(self):
        copies = random.randint(2, 10)

        assert 9 == p.sum_without_dups(([5] * copies) + [4])

        copies = random.randint(2, 10)
        l1 = [1, 2, 4, 5] * copies
        random.shuffle(l1)

        assert 12 == p.sum_without_dups(l1)

        copies = random.randint(2, 10)

        assert 4 == p.sum_without_dups([4] * copies)

    def test_single_element_palindrome(self):
        assert True == p.palindrome('')
        assert True == p.palindrome('f')
        assert True == p.palindrome(7)

    def test_longer_palindromes(self):
        assert True == p.palindrome('aa')
        assert True == p.palindrome(33)
        assert False == p.palindrome('ab')
        assert False == p.palindrome(48)

        assert True == p.palindrome('racecar')
        assert True == p.palindrome(1337331)
        assert False == p.palindrome('python')
        assert False == p.palindrome(1234567)

    def test_small_sum_multiples(self):
        assert 0 == p.sum_multiples(2)
        assert 0 == p.sum_multiples(3)
        
        assert 3 == p.sum_multiples(6)
        assert 9 == p.sum_multiples(7)

    def test_large_sum_multiples(self):
        assert 66 == p.sum_multiples(16)
        assert 129 == p.sum_multiples(25)
        assert 327099 == p.sum_multiples(1234)

    def test_empty_lists_num_func_mapper(self):
        nums = []
        funs = [p.sum_without_dups, sum]
        assert [0, 0] == p.num_func_mapper(nums, funs)

        nums = [2, 2, 2, 4, 5]
        funs = []
        assert [] == p.num_func_mapper(nums, funs)

    def test_num_func_mapper_1(self):
        nums = [2, 2, 2, 4, 5]
        funs = [p.sum_without_dups, sum]
        assert [11, 15] == p.num_func_mapper(nums, funs)

    def test_num_func_mapper_2(self):
        def most_occurring(nums):
            c = collections.Counter(nums)
            # Returns key in dict with highest value
            return max(c.items(), key=operator.itemgetter(1))[0]

        nums = [2, 2, 2, 4, 5, 8, 9]
        funs = [sum, max, most_occurring]
        assert [32, 9, 2] == p.num_func_mapper(nums, funs)
    
    def test_pythagorean_triples(self):
        assert [(3, 4, 5)] == p.pythagorean_triples(10)
        assert [(3, 4, 5), (6, 8, 10)] == p.pythagorean_triples(11)
        assert [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)] == p.pythagorean_triples(20)