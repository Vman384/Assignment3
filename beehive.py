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

    
    def product(self):
        if (self.volume or self.capacity or self.nutrient_factor) == 0:
            return 0
        elif self.volume >= self.capacity:
            return self.nutrient_factor * self.capacity
        elif self.volume < self.capacity:
            return self.nutrient_factor * self.volume

    def __eq__(self, other):
        if not isinstance(other, Beehive):
            return NotImplemented
        return self.product() == other.product()

    def __ne__(self, other):
        if not isinstance(other, Beehive):
            return NotImplemented
        return self.product() != other.product()

    def __lt__(self, other):
        if not isinstance(other, Beehive):
            return NotImplemented
        return self.product() < other.product()

    def __gt__(self, other):
        if not isinstance(other, Beehive):
            return NotImplemented
        return self.product() > other.product()

    def __le__(self, other):
        if not isinstance(other, Beehive):
            return NotImplemented
        return self.product() <= other.product()

    def __ge__(self, other):
        if not isinstance(other, Beehive):
            return NotImplemented
        return self.product() >= other.product()

class BeehiveSelector:

    def __init__(self, max_beehives: int):
        self.beehives = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]):
        """
        Complexity :

        Best case  = Worst case : O(n log n) - This is when the add operation always results in a rise to the root of the MaxHeap 
                    (thus maximizing the number of operations).
        
        """

        self.beehives = MaxHeap(len(self.beehives.the_array)) #python will clear the memory of the old one later
        for i in len(hive_list):
            self.beehives.add(i)
    
    def add_beehive(self, hive: Beehive):
        """
        Complexity :

        Best case  =  Worst case : O(log n) - This is when the add operation results in a rise to the root of the MaxHeap 
                                    (thus maximizing the number of operations).
        
        """
        self.beehives.add(hive)
    
    def harvest_best_beehive(self) -> int:   
        """
        Complexity :

        Best case : O(log n) - This is when the get_max and add operations execute as efficiently as possible, 
                    meaning they don't have to perform the maximum number of possible comparisons and swaps. This 
                    happens when the heap property is maintained with minimal adjustments.
        
        Worst case : O(log n) - This is when the get_max and add operations have to perform the maximum number of comparisons 
                     and swaps. This happens when the heap property requires the most adjustments, such as when the element that 
                     is removed is the root and when the element that is added rises all the way to the root.
        
        """     
        current_max = self.beehives.get_max()
        if current_max.volume >=  current_max.capacity:
            emeralds = current_max.nutrient_factor * current_max.capacity
            current_max.volume = current_max.volume - current_max.capacity
        else:
            emeralds = current_max.nutrient_factor * current_max.volume
            current_max.volume = 0
        self.beehives.add(current_max)
        return emeralds