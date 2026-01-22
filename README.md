# Probabilistic Data Structures

This repository contains simple and educational Python implementations of two classic
**probabilistic data structures**:

- **Bloom Filter**
- **Flajolet–Martin distinct counter**

These data structures trade exactness for **space efficiency and speed**, and are widely
used in streaming algorithms and large-scale systems.

The goal of this repository is **didactic**: to provide clear, readable implementations
that highlight the core ideas behind these algorithms.

---

## Contents

- `bloomfilter.py`  
  Implementation of a Bloom Filter using *double hashing* (Kirsch–Mitzenmacher technique).

- `flajoletMartin.py`  
  Implementation of the Flajolet–Martin algorithm, including:
  - a basic single-hash version
  - a multi-hash version with statistical aggregation
  - median-of-means and mean-of-medians estimators

---

## Bloom Filter

A **Bloom Filter** is a probabilistic data structure for set membership queries.

Given an element `x`, it can tell:
- **“definitely not in the set”**
- **“probably in the set”**

False positives are possible, but **false negatives are not**.

### Features of this implementation

- Optimal computation of:
  - bit array size `n`
  - number of hash functions `k`
- Uses **double hashing**:
  
  <img src="https://latex.codecogs.com/svg.image?h_i(x)=h_1(x)&plus;i\cdot&space;h_2(x)" title="h_i(x)=h_1(x)+i\cdot h_2(x)" />
  

  as proposed by:
  > Adam Kirsch and Michael Mitzenmacher,  
  > *Less Hashing, Same Performance: Building a Better Bloom Filter*, 2006

- Uses `mmh3` for hashing and `bitarray` for space efficiency
- Includes a small demo on a sample input stream

---

## Flajolet–Martin Distinct Counter

The **Flajolet–Martin (FM)** algorithm estimates the number of **distinct elements**
in a data stream using very little memory.

Instead of storing all unique elements, it relies on the statistical properties of
hash functions and the number of **trailing zeros** in hashed values.

### Implemented variants

- **FM_1**  
  Basic Flajolet–Martin sketch using a single hash function

- **FM_st**  
  Generalized version using multiple hash functions with:
  - median-of-means aggregation
  - mean-of-medians aggregation

The implementation uses 128-bit MurmurHash (`mmh3.hash128`) to safely handle
large streams (up to \(2^{64}\) distinct elements).

> Note: the classical bias-correction factor (≈ 0.77351) is documented but not applied,
> to keep the implementation closer to the original algorithmic intuition.

---

## Limitations and Notes

- These implementations are **not production-ready**
- They are meant for:
  - learning
  - experimentation
  - understanding probabilistic algorithms
- For real-world applications, consider more advanced variants:
  - **Counting Bloom Filters**
  - **LogLog**
  - **HyperLogLog**

---

## Requirements

- Python 3.x
- `mmh3`
- `bitarray`
- `numpy`
- `math`
- `random`

You can install the dependencies with:

```bash
pip install mmh3 bitarray numpy math random
