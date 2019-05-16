#!/bin/python

import argparse
import random


parser = argparse.ArgumentParser(description='Generate a r-arborescence problem.')
parser.add_argument('p', metavar='P', type=float, help='Edge probability')
parser.add_argument('--size', type=int, default=100)

args = parser.parse_args()

n = args.size
print(str(n) + "\n0")  # for simplification, the root is always 0
for n1 in range(n):
    for n2 in range(1, n):
        if random.random() < args.p:
            print(n1, n2)
