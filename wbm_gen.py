#!/bin/python

import argparse
import random

parser = argparse.ArgumentParser(description='Generate a random weighted bipartite matching problem.')
parser.add_argument('p', metavar='P', type=float, help='Edge probability')
parser.add_argument('--size', type=int, default=100)
parser.add_argument('--weight', type=int, default=100)

args = parser.parse_args()

jobs = args.size - int(random.random() * args.size / 10)
people = args.size - int(random.random() * args.size / 10)

print(people, jobs)

for p in range(people):
    for j in range(jobs):
        if random.random() < args.p:
            print(p+1, j+1, int(random.random() * (args.weight - 1)) + 1)
