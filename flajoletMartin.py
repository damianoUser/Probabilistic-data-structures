########################################################
#
# Implementation of the Flajolet–Martin probabilistic counter in its general form.
#
# Let U be the reference stream of elements. At each time step, we want to estimate how many distinct
# elements have appeared in the stream so far.
#
# The Flajolet–Martin algorithm provides a good approximation of this value without maintaining the full set of distinct
# elements (which could be too large to store in memory).
#
# Assumption:
# - the stream contains at most 2^64 distinct elements
#
# Input:
# s, t: number of hash functions used to improve the approximation
#
# Output:
# an approximation of the number of distinct elements seen so far in the stream, with high probability
#
# For better accuracy and lower variance, improved versions of Flajolet–Martin should be used, such as LogLog or HyperLogLog.
#
########################################################


import math
import mmh3
import numpy as np
import random



class FM_1:
    """
    Basic Flajolet-Martin sketch using a single hash function.
    """

    def __init__(self):
        self.mask = (1 << 64) - 1     # use only the last 64 bits of the hash
        self.R = 0                  # maximum number of trailing zeros observed
    
    def insert(self, element):
        seed = 0
        for char in element:
            seed += ord(char)

        val = mmh3.hash128(str(element), seed=seed, signed=False) & self.mask   # random 128-bit sequence, masked to 64 bits

        # count trailing zeros
        if val == 0:
            zeros = 64
        else:
            zeros = (val & -val).bit_length() - 1

        self.R = max(self.R, zeros)

    def query(self):
        # the FM estimate: a power of 2, unbiased after applying the correction factor
        return math.floor((2**self.R)/0.77351)


class FM_st:
    """
    Flajolet-Martin sketch with multiple hash functions and statistical aggregation.
    """

    def __init__(self, s, t):
        self.mask = (1 << 64) - 1    # assume |U| <= 2^64
        self.s = s
        self.t = t

        # We use s * t different hash functions.
        # For each of them, we run the FM algorithm and store the estimate.
        # The results are stored in a matrix of size t x s.
        #
        # Aggregation strategy:
        # - compute the mean for each row
        # - take the median of the means (median-of-means)
        #
        # Alternative:
        # - compute the median for each row
        # - take the mean of the medians (mean-of-medians)

        self.R_TABLE = np.zeros((self.t, self.s), dtype=int)

    def insert(self, element):

        seed = 0
        for i in range(self.t):
            for j in range(self.s):
                
                val = mmh3.hash128(str(element), seed, signed=False) & self.mask   # random 64-bit sequence
                
                if (val == 0):
                    zeros = 64
                else:
                    zeros = (val & -val).bit_length() - 1
                
                self.R_TABLE[i, j] = max(self.R_TABLE[i, j], zeros)

                seed = seed + 1 # Ensure a unique hash function per (i, j)

    
    def query_median_of_means(self):

        mean_array = np.mean((2.0 ** self.R_TABLE), axis=1)
        return math.floor(np.median((mean_array)))    # (mean_array)/0.77351
    
    def query_mean_of_medians(self):

        median_array = np.median((2.0 ** self.R_TABLE), axis=1)
        return math.floor(np.mean(median_array))


# Stream in input (lorem ipsum...)

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


true_distinct = len(set(U))


fm_1 = FM_1()                 # single hash function

fm_st = FM_st(1, 10000)       # median-of-means

fm_st_median = FM_st(100, 10000)  # mean-of-medians


sample = random.sample(len(U), 10)     # Random checkpoints in the stream
exact_distinct = [len(set(U[:i])) for i in sample]   # Exact number of distinct elements up to index i

k = 0
for i in range(len(U)):
    fm_1.insert(U[i])
    fm_st.insert(U[i])
    fm_st_median.insert(U[i])

    if i in sample:
        print(f"After {i} elements of the stream:")

        acc_fm1 = (1 - abs(fm_1.query() - exact_distinct[k]) / exact_distinct[k]) * 100
        acc_fmst = (1 - abs(fm_st.query_median_of_means() - exact_distinct[k]) / exact_distinct[k]) * 100
        acc_fmst_med = (1 - abs(fm_st_median.query_mean_of_medians() - exact_distinct[k]) / exact_distinct[k]) * 100

        print(f"Accuracy FM_1: {acc_fm1:.2f}%")
        print(f"Accuracy FM_st (median of means): {acc_fmst:.2f}%")
        print(f"Accuracy FM_st (mean of medians): {acc_fmst_med:.2f}%")
        k += 1


# Final estimates
est_fm1 = fm_1.query()
est_fmst = fm_st.query_median_of_means()
est_fmst_med = fm_st_median.query_mean_of_medians()

print("-" * 30)
print(f"True number of distinct elements: {true_distinct}")
print(f"FM_1 estimate: {est_fm1}")
print(f"FM_st estimate: {est_fmst}")
print(f"FM_st (mean of medians) estimate: {est_fmst_med}")




"""
Hash (57):   ... 0 0 1 1 1 0 0 1   (original 128-bit sequence: too long)
Mask (15):   ... 0 0 0 0 1 1 1 1   (64-bit mask defining the observation window)
---------------------------------
AND (&):     ... 0 0 0 0 1 0 0 1   (hashed value effectively used to count trailing zeros)
"""
