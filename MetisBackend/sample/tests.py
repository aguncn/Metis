from django.test import TestCase
import collections
# Create your tests here.
d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'
d1['1'] = '1'
d1['2'] = '2'
print(d1.a)
print(d1['a'])
for k, v in d1.items():
    print(k, v)
