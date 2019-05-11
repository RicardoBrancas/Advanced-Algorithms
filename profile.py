#!/bin/python
import subprocess
from itertools import product
from collections import OrderedDict

iterations = 11
jobs = 11


def profile(generator, output, executable, parameters, option_names):
    parameters = OrderedDict(parameters)
    print("Starting!")

    result = open(output, "w+")
    result.write(" ".join(parameters.keys()) + " t mem\n")

    names = list(parameters.keys())
    options = [option_names[x] for x in names]
    grid = product(*list(parameters.values()))

    for param in grid:
        print("Running", executable, end=" ")
        for i in range(len(param)):
            print(names[i], "=", param[i], end=" ", sep="")
        print()

        N = 0
        total_time = 0
        total_mem = 0

        for i in range(0, iterations, jobs):
            processes = []
            for j in range(0, jobs):
                test_name = "/tmp/test_" + "-".join(map(str, param)) + "-" + str(i + j) + ".in"
                print("\tGenerating input", j + i, "...")
                f = open(test_name, "w+")

                com = [generator]
                for option, p in zip(options, param):
                    if option:
                        com.append(option)
                    com.append(str(p))

                subprocess.run(com, stdout=f)
                f.close()
                f = open(test_name, "r")

                processes.append(
                    subprocess.Popen(['/usr/bin/time -f "%e %M" ' + executable + ' > /dev/null'], stdin=f,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True,
                                     shell=True))

                f.close()

            for j in range(0, jobs):
                processes[j].wait()
                time_output = processes[j].stderr.read().split()

                N += 1
                total_time += float(time_output[0])
                total_mem += float(time_output[1])

        result.write(
            " ".join(map(str, param)) + " "
            + "{0:.5f}".format(total_time / N) + " "
            + "{0:.5f}".format(total_mem / N) + "\n")
        result.flush()

    result.close()


#profile("./bm_gen.py",
#        "bm.data",
#        "./bipartite_match.py",
#        {"p": [.1, .5, 1], "s": range(0, 501, 100)},
#        {"p": "", "s": "--size"})
#
#profile("./wbm_gen.py",
#        "wbm.data",
#        "./weighted_bipartite_match.py",
#        {"p": [.1, 0.5, 1], "s": range(0, 501, 100), "w": [100, 2000, 5000, 10000]},
#        {"p": "", "s": "--size", "w": "--weight"})

profile("./bm_gen.py",
        "mbm.data",
        "./matroid_bipartite_match.py",
        {"p": [.1, .5, 1], "s": range(0, 131, 20)},
        {"p": "", "s": "--size"})
