from general_matroid import *
from algos import *


class PartitionMatroid(Matroid):

    def __init__(self, vertices: List, partition: List, edges: List, both=True):
        self.vertices = vertices
        self.partition = partition
        self.both = both
        super().__init__(set(edges))

    def reset(self):
        super().reset()
        if self.both:
            self.counters_from = {e: 0 for e in self.vertices}
        self.counters_to = {e: 0 for e in self.vertices}

    def remove(self, elem) -> None:
        super().remove(elem)
        if self.both:
            self.counters_from[elem[0]] -= 1
        self.counters_to[elem[1]] -= 1

    def add(self, elem) -> None:
        super().add(elem)
        if self.both:
            self.counters_from[elem[0]] += 1
        self.counters_to[elem[1]] += 1

    def is_independent_except_with(self, excp, elem) -> bool:
        if self.both and excp[0] != elem[0] and elem[0] in self.partition and self.counters_from[elem[0]] + 1 >= 2:
            return False
        if excp[1] != elem[1] and elem[1] in self.partition and self.counters_to[elem[1]] + 1 >= 2:
            return False
        return True

    def is_independent_with(self, elem) -> bool:
        if self.both and elem[0] in self.partition and self.counters_from[elem[0]] + 1 >= 2:
            return False
        if elem[1] in self.partition and self.counters_to[elem[1]] + 1 >= 2:
            return False
        return True


class GraphicMatroid(Matroid):

    def __init__(self, vertices: List, edges: List):
        self.vertices = vertices
        super().__init__(set(edges))

    def remove(self, elem) -> None:
        self.I.remove(elem)

    def add(self, elem) -> None:
        self.I.add(elem)

    def is_independent(self, set) -> bool:
        return is_acyclic(mk_graph(self.vertices, set))

    def is_independent_except_with(self, excp, elem) -> bool:
        return self.is_independent(self.I - {excp} | {elem})

    def is_independent_with(self, elem) -> bool:
        return self.is_independent(self.I | {elem})

