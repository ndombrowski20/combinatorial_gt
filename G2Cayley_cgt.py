# generating g2 = < a, b | a^2, b^6, abAB>

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
abAB = Word([a, b, A, B])

g2 = Group([a, b], [aa, aA, bbbbbb, bB, abAB], 12)

g2_cayley = Cayley()

g2_cayley.read_newgraph(g2, 4, 12)

g2_cayley.for_saving('dicayley_g2_12', 'info_dicayley_g2_12')
