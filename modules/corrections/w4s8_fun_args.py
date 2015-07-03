# -*- coding: utf-8 -*-
from exercice_function import ExerciceFunction
from args import Args, ArgsKeywords

##############################
# @BEG@ week=4 sequence=8 name=distance
import math

def distance(*args):
    "la racine de la somme des carrés des arguments"
    # avec une compréhension on calcule la liste des carrés des arguments
    # on applique ensuite sum pour en faire la somme
    # vous pourrez d'ailleurs vérifier que sum ([]) = 0
    # enfin on extrait la racine avec math.sqrt
    return math.sqrt(sum([x**2 for x in args]))
# @END@

# ceci est testé mais je préfère ne pas l'exposer dans les corriges pour l'instant
def distance_bis(*args):
    "idem mais avec une expression génératrice"
    # on n'a pas encore vu cette forme - cf Semaine 6
    # mais pour vous donner un avant-goût d'une expression
    # génératrice:
    return math.sqrt(sum( (x**2 for x in args) ))

def distance_ko(*args):
    return sum([x**2 for x in args])

distance_inputs = [
    Args(),
    Args(1),
    Args(1, 1),
    Args(1, 1, 1),
    Args(1, 1, 1, 1),
    Args(*range(10)),
]

exo_distance = ExerciceFunction(
    distance, distance_inputs, exemple_how_many=3)

##############################
# @BEG@ week=4 sequence=8 name=doubler_premier
def doubler_premier(f, first, *args):
    """
    renvoie le résultat de la fonction f appliquée sur
    f(2 * first, *args)
    """
    # une fois qu'on a écrit la signature on a presque fini le travail
    # en effet on a isolé la fonction, son premier argument, et le reste
    # des arguments
    # il ne reste qu'à appeler f, après avoir doublé first
    return f(2*first, *args)
# @END@

# marche aussi mais moins élégant
def doubler_premier_bis(f, *args):
    first = args[0]
    remains = args[1:]
    return f(2*first, *remains)

doubler_premier_inputs = []
from operator import add
from operator import mul
import math

# pour l'exemple on choisit les 3 premiers avec des fonctions différentes
for i in [1, 3, 5]: 
    doubler_premier_inputs.append(Args(add, i, 4))
    doubler_premier_inputs.append(Args(mul, i, 4))
doubler_premier_inputs.insert(2, Args(distance, 1, 1, 1))
doubler_premier_inputs.insert(3, Args(distance, 2, 2, 2, 2))
doubler_premier_inputs.insert(4, Args(distance, 3, 3, 3, 3, 3))

exo_doubler_premier = ExerciceFunction(
    doubler_premier, doubler_premier_inputs, exemple_how_many=4,
    layout='truncate', render_name=False,
)

def doubler_premier_ko(f, first, *args):
    return f(3*first, *args)

##############################
# @BEG@ week=4 sequence=8 name=doubler_premier2
def doubler_premier2(f, first, *args, **keywords):
    """
    équivalent à doubler_premier 
    mais on peut aussi passer des arguments nommés
    """
    # c'est exactement la même chose
    return f(2*first, *args, **keywords)

# Complément - niveau avancé
# ----
# Il y a un cas qui ne fonctionne pas avec cette implémentation, 
# quand le premier argument de f a une valeur par défaut 
# *et* on veut pouvoir appeler doubler_premier
# en nommant ce premier argument 
#
# par exemple - avec f=muln telle que définie dans l'énoncé 
#def muln(x=1, y=1): return x*y

# alors ceci
#doubler_premier2(muln, x=1, y=2)
# ne marche pas car on n'a pas les deux arguments requis
# par doubler_premier2
# 
# et pour écrire, disons doubler_permier3, qui marcherait aussi comme cela
# il faudrait faire une hypothèse sur le nom du premier argument...
# @END@

def addn(x, y=0):
    return x+y

def muln(x=1, y=1):
    return x*y

doubler_premier2_inputs = []
dataset = ArgsKeywords((addn,1), dict(y=3));   doubler_premier2_inputs.append(dataset)
dataset = ArgsKeywords((muln,1), dict(y=3));   doubler_premier2_inputs.append(dataset)

# remettre les datasets de doubler_premier
doubler_premier2_inputs += doubler_premier_inputs

dataset = ArgsKeywords((addn, 1, 3), dict());  doubler_premier2_inputs.append(dataset)
dataset = ArgsKeywords((muln,1, 3), dict());   doubler_premier2_inputs.append(dataset)
dataset = ArgsKeywords((addn,1), dict());      doubler_premier2_inputs.append(dataset)
dataset = ArgsKeywords((muln,1), dict());      doubler_premier2_inputs.append(dataset)

exo_doubler_premier2 = ExerciceFunction(
    doubler_premier2, doubler_premier2_inputs,
    exemple_how_many=5,
    layout='truncate', render_name=False,
)

def doubler_premier2_ko(f, first, *args, **keywords):
    return f(3*first, *args, **keywords)

##############################
# @BEG@ week=4 sequence=8 name=validation2
def validation2(f, g, argument_tuples):
    """
    retourne une liste de booléens, un par entree dans entrees
    qui indique si f(*tuple) == g(*tuple)
    """
    # c'est presque exactement comme validation, sauf qu'on s'attend 
    # à recevoir une liste de tuples d'arguments, qu'on applique
    # aux deux fonctions avec la forme * au lieu de les passer directement
    return [f(*tuple) == g(*tuple) for tuple in argument_tuples]
# @END@

def validation2_ko(*args, **keywords):
    return [not x for x in validation2(*args, **keywords)]

#################### les jeux de données
validation2_inputs = []

########## dataset #1
from math import factorial
from operator import mul

# factoriel is still valid
fact_inputs = [(0,), (1,), (5,),]

def fact(n):
    "une version de factoriel à base de reduce"
    return reduce(mul, range(1, n+1), 1)

validation2_inputs.append(Args(fact, factorial, fact_inputs))

########## dataset #2
def broken_fact(n):
    return 0 if n <= 0 \
        else 1 if n == 1 \
             else n*fact(n-1)

validation2_inputs.append(Args(broken_fact, factorial, fact_inputs))

########## dataset #3
from operator import add

# addition can work too
add_inputs = [(2, 3), (0, 4), (4, 5)]

def plus(x1, x2): 
    return x1 + x2

validation2_inputs.append(Args(add, plus, add_inputs))

########## dataset #4
def plus_broken(x1, x2):
    if x1 != 0: 
        return x1 + x2
    else:
        return 1 + x2

validation2_inputs.append(Args(add, plus_broken, add_inputs))

#################### the exercice instance
for args_obj in validation2_inputs:
    args_obj.layout = 'truncate'

exo_validation2 = ExerciceFunction(
    validation2, validation2_inputs,
    correction_columns=(50, 8, 8),
    render_name=False,
)