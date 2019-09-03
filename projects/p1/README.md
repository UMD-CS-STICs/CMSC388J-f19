# Python practice 

**Assigned**: Week 1

**Due**: Week 2, September 6th, 2019, 11:59:59 PM

**Late Deadline**: One day after due date, for 10% off: September 7th, 2019, 11:59:59 PM

## Description

You will be implementing some basic functions in Python as practice, including using iterators and built-in functions.

## Setup

First activate your virtual environment, then run `pip install -r requirements.txt`. 
As a reminder, this command will install all python packages listed in requirements.txt.

## Project

In `practice.py`, implement the following functions:

1. `hello_world()`

   Return the string `Hello, World!`

2. `sum_without_dups(l)`

   Given a list of integers, return the sum of the integers, not counting duplicates, i.e. 
   if you have two or more copies of an integer, it should be added to the final sum once.

   Examples:
   ```python
   >>> sum_unique([])
   0
   >>> sum_unique([4, 4, 5])
   9
   >>> sum_unique([4, 2, 5])
   11
   >>> sum_unique([2, 2, 2, 2, 1])
   3
   ```

3. `palindrome(x)`

    Given an integer or a string *x*, determine if *x* has the same value as *x* reversed.

    Examples:
    ```python
    >>> palindrome(1331)
    True
    >>> palindrome('racecar')
    True
    >>> palindrome(1234)
    False
    >>> palindrome('python')
    False
    ```

4. `sum_multiples(num)`

    Given a positive integer `num`, find the sum of all multiples of 3 and 7 upto and not including `num`.

    Examples:
    ```python
    >>> sum_multiples(10) # Multiples: [3, 6, 7, 9]
    25
    >>> sum_multiples(3) # Multiples: []
    0
    >>> sum_multiples(7) # Multiples: [3, 6]
    9
    >>> sum_multiples(16) # Multiples: [3, 6, 7, 9, 12, 14, 15]
    66
    ```

5. `num_func_mapper(nums, funs)`

    Given a list of numbers `nums` and a list of functions `funs`, 
    apply each function to `nums` and store the result in a list.
    Return the list of results. 
    
    *Hint*: The list of results should be the same length as `funs`.

    Example:
    ```python
    >>> f_list = [sum_unique, sum]
    >>> num_list = [2, 2, 2, 4, 5]
    >>> all_the_sums(num_list, f_list)
    [11, 15]
    ```

6. `pythagorean_triples(n)`

    Given a positive integer `n`, find all pythagorean triples where all side lengths
    of the triangle are less than `n`. The function shouldn't return distinct tuples
    that represent identitical triangles. For example, (3, 4, 5) and (4, 3, 5)
    are distinct but represent the same triangle, flipped.

    Examples:
    ```python
    >>> pythagorean_triples(10)
    [(3, 4, 5)]
    >>> pythagorean_triples(11)
    [(3, 4, 5), (6, 8, 10)]
    >>> pythagorean_triples(20)
    [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
    ```

## Testing

Make sure you're in your virtual environment and have completed the [Setup](#setup). 
Navigate into the `p1/` directory and run `pytest -q test_practice.py`. 
The `-q` flag reduces the amount of space pytest takes in the terminal when it prints testing results.

## Submission & Grading

Make sure that you've run the testing file, as explained above, and that you've passed all
the tests. If you need help, come to office hours or contact us on Piazza for the quickest 
feedback. The submit server will not show test results, but just display "ACCEPTED".

Submit the `practice.py` file to the submit server. No other files are required. All your work
must be in the `practice.py` file.

There are 11 public tests, so each will be worth 10 points. There will also be 10 points for style. 
To get full points for style, make sure your code is readable and is using reasonable variable names.
