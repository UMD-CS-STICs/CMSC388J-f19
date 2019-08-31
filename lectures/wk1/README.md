# Week 1
### Starting with Python

**Variables**

Variables have dynamic types; you don't have to assign a specific type to a
variable, and you can change the type of value the variable stores later on.

```zsh
>>> data = 'This is a variable'
>>> type(data)
<class 'str'>
>>> data
'This is a variable'
>>> data = 67
>>> type(data)
<class 'int'>
>>> data
67
```

Here we can see that `int` and `str` have classes, so we can also check what
methods they have using `dir(int)` or `dir(str)`.

When we type in `dir(int)` and press enter, we can see methods listed like
`__add__`, `__mul__`, and `__gt__`, can you guess what they do?

If we want to check whether a certain class has a certain method, we do

```zsh
>>> hasattr(int, '__sub__')
True
```

You can use the `dir` and `hasattr` built-in methods to inspect any class.

**Iterators**

To use `for` loops, we use the built-in `range()` function.

```zsh
>>> for i in range(5):
...     i ** i
... 
1
1
4
27
256
>>> for i in range(10, 20, 2):
...     i
... 
10
12
14
16
18
```

If only supplied with one argument, `end`, `range()` returns integers in 
`[0, end)`. Supplied with two arguments, the new one being first, `start`, then
`range()` will return integers in `[start, end)`. If supplied with a third argument
`step`, `range()` skips over `step` integers each time.

`while` loops work similarly to other languages

```zsh
>>> i = 0
>>> while i < 4:
...     print(i)
...     i += 1
... 
0
1
2
3
```

**Working with sequences and collections**

To check if a certain value is in a list or array, you've probably used class 
methods of the list or array in other languages. In Python, 
lists, tuples, ranges, and strings are all sequences, so we can
use the `in` keyword to check membership. Sets and dictionaries are other 
collections, so we can also use the `in` keyword with them. To check the values
of a dictionary, we use `dict.values()`. 

```zsh
>>> d = {1 : 'one', 2 : 'two', 3 : 'three'}
>>> 1 in d
True
>>> 'two' in d
False
>>> 'two' in d.values()
True
>>> 1 in range(5)
True
>>> l = [2, 'python', ['panda', 'horse']]
>>> 'python' in l
True
>>> 'panda' in l
False
>>> 'K' in 'Kenton'
True
>>> t = (1, 'two', ([3, 'four'], ), 5)
>>> 1 in t
True
>>> 'four' in t
False
>>> 'four' in t[2][0]
True
```

And we can also iterate over the sequences in a loop

```zsh
>>> for char in 'Dog':
...     char
... 
'D'
'o'
'g'
>>> for item in [2, 'python', ['panda', 'horse'], {1 : 'one', 2 : 'two'}]:
...     print(str(item) + ' has type ' + str(type(item)))
... 
2 has type <class 'int'>
python has type <class 'str'>
['panda', 'horse'] has type <class 'list'>
{1: 'one', 2: 'two'} has type <class 'dict'>
```

To work with subsets of sequences or even reverse them, we use *slice notation*

```zsh
>>> s = 'Hello'
>>> s[::-1] # Reverses string by stepping backwards
'olleH'
>>> s = 'supercalifragilisticexpialidocious'
>>> s[9:20]
'fragilistic'
```

**Functions**

Python has many built-in functions for replacing common operations. We'll
look at some of them here, and the rest can be found in the
[official docs](https://docs.python.org/3/library/functions.html).

```zsh
>>> sum([1, 2, 3, 4])
10
>>> all(num % 2 == 0 for num in [2, 3, 4, 8, 10])
False
>>> all(num % 2 == 0 for num in [2, 4, 6, 8, 10])
True
>>> sum([1, 2, 3, 4])
10
>>> all(num % 2 == 0 for num in [2, 4, 6, 8, 10])
True
>>> list(map(lambda s: s[::-1], ['Yashas', 'Kenton', 'Gordon'])) # Reverses each string
['sahsaY', 'notneK', 'nodroG']
>>> list(filter(lambda s: s == s[::-1], ['geeg', 'racecar', 'hello'])) # Finds palindromes
['geeg', 'racecar']
>>> max(range(5))
4
>>> min([1, 2, 3, 9, 5, 2])
1
```

- `all()` checks if a given condition list is true for a given sequence
- `sum()` takes the sum of a sequence
- `map()` applies a function to every member of a given sequence
- `filter()` returns a sequence consisting of the members of the given sequence that satisfy the condition
- `max()` and `min()` return the maximum and minimum of sequences, respectively.
- There are more built-in functions, we talked about some of the others in previous sections

You may notice that we used a strange keyword `lambda` in `map()` and `filter()`. 
These are anonymous functions, so they aren't bound to any identifier keyword.
If we wanted, we could bind them:

```zsh
>>> average = lambda l: sum(l) / len(l)
>>> average(range(10))
4.5
```

We can also define our own functions

```zsh
>>> def average(l):
...     return sum(l) / len(l)
... 
>>> average(range(10))
4.5
>>> def multiples(start, end): # Finds multiples of 7 that are not multiples of 5
...     result = []
...     for n in range(start, end):
...         if n % 7 == 0 and n % 5 != 0:
...             result.append(n)
...     return result
... 
>>> multiples(0, 40)
[7, 14, 21, 28]
```

Let's break down what's happening here.

We define the function named `average` which takes a parameter `l` and
returns the average of the entries in `l`. Python has no idea if `l` is
actually a sequence of numbers. This can lead to runtime errors, which is why
testing is very important to python.

Finally, we can also pass functions as arguments to other functions. One
example where we've done this already is with the `map()` function.
We can also create our own function accepting another function to
get information about some data we're storing. Functions in python are first-class
objects, so we can pass them around.

``` zsh
>>> def apply(func):
...     l = list(range(10)) # Not visible outside the apply() function
...     return func(l)
... 
>>> apply(average)
4.5
```

Generators are a powerful concept in python. We can use generators when we 
want to use a sequence type, but don't want to generate all the members in the sequence
before using the sequence. For example, if you have a sequence of 10,000,000 objects,
creating a list with all of those objects and then iterating through would make our program
slower because all of the necessary memory had to be allocated in one go and then
accessed again. We'll show you a simple example for creating a generator by 
recreating the range function in python (it's implemented in C in the source code):

```zsh
>>> def new_range(stop):
...     i = -1
...     while i < stop:
...         i += 1
...         yield i
...
>>> new_range(10)
<generator object new_range at 0x10fc6ac50>
>>> for i in new_range(5):
...     print(i)
... 
0
1
2
3
4
5
>>> type(new_range)
<class 'function'>
```

Notice how the type of `new_range` is a function, and the type of object returned
when we call `new_range(10)` is a generator object. We can iterate over a generator object.

**List comprehensions**

A powerful tool in python is the list comprehension. It's a functional programming
tool, and it's used extensively by python developers.

If we want to create a list of integers:

```zsh
>>> ints = [i for i in range(5)]
>>> ints
[0, 1, 2, 3, 4]
```

If we want to create a list of squares of integers:

```zsh
>>> squ = [i**2 for i in range(5)]
>>> squ
[0, 1, 4, 9, 16]
```

The `**` operator is the exponent operator.

If we wanted to compute the Cartesian product of two sequences, that's 
straightforward with list comprehensions, too. For sets A and B, the Cartesian 
product is defined as all ordered pairs `(a, b)` for a in A and b in B.

```zsh
>>> l = [(i, j) for i in range(5) for j in range(5)]
>>> l
[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), 
(2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), 
(4, 4)]
```

Here we used chained `for` loops. Notice how `j` is increases from 0 to 4 and then `i`
starts increasing. This indicates that `for j in range(5)` is the inner loop. We can
create an identitical list with this code:

```zsh
>>> l = []
>>> for i in range(5):
...      for j in range(5):
...          l.append((i, j))
... 
>>> l
[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), 
(2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), 
(4, 4)]
```

So in a list comprehension, the outer loop comes first and inner loops come second. Any further
inner loops would come after these, but it's probably better to write out the loops explicity at
that point, i.e. not in a list comprehension, to improve readability.

We can also use conditionals in list comprehensions. If we want a list of even squared integers,
we can use an `if` statement.

```zsh
>>> l = [i ** 2 for i in range(10) if (i ** 2) % 2 == 0]
>>> l
[0, 4, 16, 36, 64]
```

One great use for list comprehensions comes from data science applications,
where you might want to flatten a matrix of inputs to input to a function.
We'll first create a randomized 10x10 matrix with the `random` module from the
python standard library, and then flatten it using our knowledge of chaining
loops. The underscore used in the loop means that we don't care about values returned
from the `range()` function, we just want to run the loop 10 times.

*Sidenote*: `random` [docs](https://docs.python.org/3.5/library/random.html)

```zsh
>>> import random as rand
>>> m = [[rand.random() for _ in range(10)] for _ in range(10)]
>>> f = [x for row in m for x in row]
```

If we want to only keep values that pass a certain threshold, but still maintain
the size of our data, we can use an `if-else` statement in our list comp.

```zsh
>>> import random as rand
>>> m = [[rand.random() for _ in range(10)] for _ in range(10)]
>>> threshold = 0.7
>>> f = [x if x > threshold else 0 for row in m for x in row]
```

The syntax if you're using an `if-else` is different than if you're just using `if`.
The syntax is `x if condition else y`.


**Modules**

Every Python file you create is a Python module. A module can be imported
into other modules by using `import {module_name}`, without the trailing `.py`.
For example, since you ran the `pip install -r requirements.txt` command, try
`import antigravity` in a shell.

**Usage**: If you made a module of constants named `constants.py`, you can import
it into your main working file by typing `import constants`. If you want to have
a different name for the constants module in your code, then do 
`import constants as c` and access constants or functions in the module using
dot notation. You can also choose to import only certain functions or variables
using `from constants import x`, where x is a function or variable.

For example:

```zsh
>>> import math
>>> math.factorial(50)
30414093201713378043612608166064768844377641568960512000000000000
>>> from collections import Counter
>>> Counter([1, 1, 2, 3, 3, 1, 1, 3, 9, 0, 4]) # Counts number of occurrences for each number
Counter({1: 4, 3: 3, 2: 1, 9: 1, 0: 1, 4: 1})
>>> import statistics as s
>>> s.median([4, 1, 2, 1, 4, 5, 2, 1])
2.0
```

**Best practices**

- Use two spaces or tabs for indented lines. Spaces are preferred, but whatever
you do, be consistent
- Don't use a one-liner with functions if it's not easily readable
- Follow the Zen of Python as best you can. You can see it using `import this`.
- Important note: don't name your python module the same as a dependency (!!!)

**Conclusion**

We went over a lot of Python syntax and other stuff today, feel free
to reach out to us if you have any questions. We ommited OO programming and
some other great things you can do with python to make this first week a little
easier to digest. We'll introduce more python language features as needed.

This week, you have a project assigned to implement some functions in Python.
We'll update the repo later today, and the project will be due next Friday, 
with a late penalty of 10% if you submit Saturday. Please get started sometime
this weekend so we can help you if you have questions.

[photo1]: ./landscape.png
