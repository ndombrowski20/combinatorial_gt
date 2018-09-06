# generating g4 = < a, b | a^2, b^3, ababab>

from Word_cgt import Word
from Letter_cgt import Letter
from Cayley_cgt import Cayley
from Group_cgt import Group
import time, os, pickle
start_time = time.time()

a = Letter("a")
b = Letter("b")
A = Letter("A")
B = Letter("B")

identity = Word([])

aa = Word([a, a])
aA = Word([a, A])
bB = Word([b, B])
bbb = Word([b, b, b])
ababab = Word([a, b, a, b, a, b])

g4 = Group([a, b], [aa, aA, bbb, bB, ababab], 14)

g4_cayley = Cayley()

g4_cayley.read_newgraph(g4, 4, 14)

g4_cayley.for_saving('dicayley_g4_14', 'info_dicayley_g4_14')
