########################################################
#
# Implementation of the probabilistic data structure Bloom Filter (BF).
# We use k hash functions, where k depends on the size of the BF.
#
# Let U be the reference stream of elements. Let S ⊆ U be the set of "good" values in the stream.
# Given an element x ∈ U, we want to quickly determine, with high probability (specified as input),
# whether x ∈ S or x ∉ S.
# Let n = len(U) and m = len(S).
#
# Assumptions:
# - the elements of the stream are all strings
# - m << n
#
# Input:
# m: estimated value of len(S), i.e., the number of elements that will be inserted into the Bloom Filter
# p: admissible false positive rate (Failure Probability Rate)
#
# Output:
# A data structure that can be queried as follows: for each element, it quickly tells,
# with high probability, whether the element belongs to S or not.
#
# In this implementation, the k hash values associated with each element are computed as follows:
# we fix 2 hash values for each element, and from these two we derive the k hash values
# to be inserted into the array.
# This per-element complexity of O(2 * hash + k * additions) is significantly lower than O(k * hash),
# and, as shown by Kirsch and Mitzenmacher [1], it does not change the false positive rate
# of the Bloom Filter data structure.
#
########################################################



from bitarray import bitarray
import mmh3
import math
import random



class Bfilter:
    def __init__(self, m, p):
        self.n = math.ceil(-m * math.log(p) / (math.log(2) ** 2))  # Length that the Bloom Filter must have to satisfy the input false positive rate p
        self.array = bitarray(self.n)      # the actual Bloom Filter bit array
        self.array.setall(0)   # bit array initialization
        self.k = math.floor(self.n/m * math.log(2))   # number of hash functions used per inserted element
        if (self.k == 0):
            self.k = 1
    
    def insert(self, element):
        h1 = mmh3.hash(element, 1)
        h2 = mmh3.hash(element, 2)
        for i in range(self.k):
            self.array[(h1 + i * h2) % self.n] = 1  # Recommended formula to obtain k independent hash functions [1]

    # If even a single hash function returns "no", then the answer is "no".
    # Otherwise, the answer is "yes".
    def membership(self, element):
        for i in range(self.k):
            h1 = mmh3.hash(element, 1)
            h2 = mmh3.hash(element, 2)
            if (self.array[(h1 + i * h2) % self.n] == 0):
                return False
        return True




# Input stream (lorem ipsum...)

U = ['ferri', 'deorsum', 'suo', 'pondere', 'ad', 'lineam', 'hunc', 'naturalem', 'esse', 'omnium',
              'corporum', 'motum', 'Deinde', 'ibidem', 'homo', 'acutus', 'cum', 'illud', 'ocurreret', 'si',
              'omnia', 'deorsus', 'e', 'regione', 'ferrentur', 'et', 'ut', 'dixi', 'ad', 'lineam', 'numquam',
              'fore', 'ut', 'atomus', 'altera', 'alteram', 'posset', 'attingere', 'itaque', 'attulit', 'rem',
              'commenticiam', 'declinare', 'dixit', 'atomum', 'perpaulum', 'quo', 'nihil', 'posset', 'fieri',
              'minus', 'ita', 'effici', 'complexiones', 'et', 'copulationes', 'et', 'adhaesiones', 'atomorum',
              'inter', 'se', 'ex', 'quo', 'efficeretur', 'mundus', 'omnesque', 'partes', 'mundi', 'quaeque',
              'in', 'eo', 'essent', 'Quae', 'cum', 'tota', 'res', 'est', 'ficta', 'pueriliter', 'tum', 'ne',
              'efficit', 'quidem', 'quod', 'vult', 'nam', 'et', 'ipsa', 'declinatio', 'ad', 'libidinem', 'fingitur',
              'ait', 'enim', 'declinare', 'atomum', 'sine', 'causa', 'quo', 'nihil', 'turpius', 'physico', 'quam',
              'fieri', 'quicquam', 'sine', 'causa', 'dicere', 'et', 'illum', 'motum', 'naturalem', 'omnium',
              'ponderum', 'ut', 'ipse', 'constituit', 'e', 'regione', 'inferiorem', 'locum', 'petentium', 'sine',
              'causa', 'eripuit', 'atomis', 'nec', 'tamen', 'id', 'cuius', 'causa', 'haec', 'finxerat', 'assecutus',
              'est', 'Nam', 'si', 'omnes', 'atomi', 'declinabunt', 'nullae', 'umquam', 'cohaerescent', 'sive', 'aliae',
              'declinabunt', 'aliae', 'suo', 'nutu', 'recte', 'ferentur', 'primum', 'erit', 'hoc', 'quasi', 'provincias',
              'atomis', 'dare', 'quae', 'recte', 'quae', 'oblique', 'ferantur', 'deinde', 'eadem', 'illa', 'atomorum', 'in',
              'quo', 'etiam', 'Democritus', 'haeret', 'turbulenta', 'concursio', 'hunc', 'mundi', 'ornatum', 'efficere',
              'non', 'poterit', 'ne', 'illud', 'quidem', 'physici', 'credere', 'aliquid', 'esse', 'minimum', 'quod',
              'profecto', 'numquam', 'putavisset', 'si', 'a', 'Polyaeno', 'familiari', 'suo', 'geometrica', 'discere',
              'maluisset', 'quam', 'illum', 'etiam', 'ipsum', 'dedocere', 'Sol', 'Democrito', 'magnus', 'videtur',
              'quippe', 'homini', 'erudito', 'in', 'geometriaque', 'perfecto', 'huic', 'pedalis', 'fortasse', 'tantum',
              'enim', 'esse', 'censet', 'quantus', 'videtur', 'vel', 'paulo', 'aut', 'maiorem', 'aut', 'minorem', 'Ita',
              'quae', 'mutat', 'ea', 'corrumpit', 'quae', 'sequitur', 'sunt', 'tota', 'Democriti', 'atomi', 'inane',
              'imagines', 'quae', 'eidola', 'nominant', 'quorum', 'incursione', 'non', 'solum', 'videamus', 'sed',
              'etiam', 'cogitemus', 'infinitio', 'ipsa', 'quam', 'apeirian', 'vocant', 'tota', 'ab', 'illo', 'est',
              'tum', 'innumerabiles', 'mundi', 'qui', 'et', 'oriantur', 'et', 'intereant', 'cotidie', 'Quae', 'etsi',
              'mihi', 'nullo', 'modo', 'probantur', 'tamen', 'Democritum', 'laudatum', 'a', 'ceteris', 'ab', 'hoc',
              'qui', 'eum', 'unum', 'secutus', 'esset', 'nollem', 'vituperatum']



bf = Bfilter(100, 0.01)

print(f"Empty Bloom Filter: {bf.array}")

for i in range(100):
    bf.insert(U[i])


print(f"Bloom Filter after inserting m elements: {bf.array}")

"""
# Sanity check:
for x in U[:100]:
    print(bf.membership(x))
"""


sample = random.sample(range(50,200), 10)

for i in range(10):
    print(
        f"The element {U[sample[i]]} is probably in S"
        if bf.membership(U[sample[i]])
        else f"The element {U[sample[i]]} is certainly not in S"
    )


# [1] Adam Kirsch and Michael Mitzenmacher,
#     Less Hashing, Same Performance: Building a Better Bloom Filter,
#     LNCS 4168, pp. 456–467, 2006
