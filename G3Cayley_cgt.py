# generating g3 = < a, b | a^2, b^6, abab>

from Word_cgt import Word
from Letter_cgt import Letter
from Cayley_cgt import Cayley
from Group_cgt import Group
import time, os, pickle

a = Letter("a")
b = Letter("b")
A = Letter("A")
B = Letter("B")

identity = Word([])

aa = Word([a, a])
aA = Word([a, A])
bB = Word([b, B])
bbbbbb = Word([b, b, b, b, b, b])
abab = Word([a, b, a, b])

g3 = Group([a, b], [aa, aA, bbbbbb, bB, abab], 10)

g3_cayley = Cayley()

g3_cayley.read_newgraph(g3, 4, 10)

g3_cayley.for_saving('dicayley_g3_10', 'info_dicayley_g3_10')
