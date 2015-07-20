'''
Created on Mar 17, 2014

@author: pablob
'''
import random
import string

def incrementor(seed):
    # Return a function that when it is call the first time returns the seed 
    # given. Subsequents calls return 1 + the las value returned. So first, 
    # would be seed. Then seed +1, then seed +2 and you can imagine the other
    # calls.
    def _infinit_incr(value):
        i = value
        while True:
            yield i
            i = i + 1
    inc = _infinit_incr(seed)
    return lambda : inc.next()

def random_id():
    def _random():
        while True:
            yield random.randint(1000000, 999999999)
    ran = _random()
    return lambda : ran.next()

def __random_letters(m):
    buf = []
    for i in range(m):
        buf.append(random.choice(string.letters))
    return ''.join(buf)

def random_letters(amount):
    def _random():
        while True:
            yield __random_letters(amount)
    ran = _random()
    return lambda : ran.next()
