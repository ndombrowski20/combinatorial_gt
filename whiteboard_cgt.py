# this is what the name describes it to be: a place for me to think and scribble ideas

from Word_cgt import Word
from Letter_cgt import Letter
from Cayley_cgt import Cayley
from Group_cgt import Group
import time, os, pickle

a = Letter("a")
b = Letter("b")
A = Letter("A")
B = Letter("B")
c = Letter("c")
C = Letter("C")

identity = Word([])

aa = Word([a, a])
aA = Word([a, A])
bb = Word([b, b])
bB = Word([b, B])
cc = Word([c, c])
cC = Word([c, C])
abAB = Word([a, b, A, B])
bcBC = Word([b, c, B, C])
caCA = Word([c, a, C, A])

g2 = Group([a, b, c], [aa, aA, bb, bB, cc, cC, abAB, bcBC, abAB], 12)

g2_cayley = Cayley()

g2_cayley.read_newgraph(g2, 4, 6)

g2_cayley.for_saving('three_gens_6', 'info_three_gens_6')



