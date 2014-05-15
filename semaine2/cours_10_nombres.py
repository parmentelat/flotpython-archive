
######################################## types de base de python

#################### les nombres

########## le plus simple : l'entier
1
# un entier negatif
-2

# nous verrons plus tard l'affectation, mais dans l'immediat
i=10
# rien ne s'affiche, mais
i

# pour affecter et voir le resultat en une fois (utile seulement si interactif)
i=20; i

########## flottants
f=3.14

# voir le type d'un nombre
type(i)
type(f)

# conversions
int(3.14)
float(3)

########## operateurs 
# addition et soustraction 
5+3-2

# attention : division entiere
5/3
# reste
5%3
# pour faire une division flottante il faut convertir
3/float(5)
float(3)/5

# a l'inverse, faire une division entiere sur un flottant
8.0//3

########## entiers avec plus de precision : long
type(1234567890)
type(12345678901234567890123456789012345678901234567890)

# si on veut forcer un entier a etre 'long' : prefixer avec 'L'
type(1234567890L)


########## complexes
1j
1j*1j

type(1j*1j)

c=(1+1j)*(1-1j)

# acceder aux parties reelle et imaginaire

c.real
c.imag

########## operateurs - suite

# puissance
2**32
pow(2,32)

### operateurs sur les champs de bits

# decalage multiplicatif (a gauche)
1<<2
# decalage diviseur (a droite)
512>>3

# operations logiques bit a bit
#                        12 = 1100
#                         7 = 0111
#----------------------------------------
# et logique (bitwise AND) -> 0100 -> 4
12 & 7 
# ou logique (bitwise OR)  -> 1111 -> 15
12 | 7

# une astuce : '_' represente le dernier resultat (en mode interactif seulement)
# _ * 2

########## le module 'math'
# on verra plus tard les importations, mais pour l'instant:
import math
dir(math)

math.tan(math.pi/4)
