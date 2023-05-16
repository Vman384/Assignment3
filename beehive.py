from dataclasses import dataclass
from heap import MaxHeap

@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

class BeehiveSelector:

    def __init__(self, max_beehives: int):
        raise NotImplementedError()

    def set_all_beehives(self, hive_list: list[Beehive]):
        raise NotImplementedError()
    
    def add_beehive(self, hive: Beehive):
        raise NotImplementedError()
    
    def harvest_best_beehive(self):
        raise NotImplementedError()
