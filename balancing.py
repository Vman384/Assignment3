from __future__ import annotations
from threedeebeetree import Point
import random

from threedeebeetree import ThreeDeeBeeTree, BeeNode
from ratio import Percentiles

def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """

    Complexity :

    Best case = Worst case : The nested loops in make_ordering_rec are executed for each point in the input list. 
                             This operation leads to a cubic time complexity of O(n^3). Adding points to the Percentiles 
                             object contributes a complexity of O(n log n) since each insertion into a Binary Search Tree is 
                             O(log n) and this operation is repeated n times. The ratio calculation function traverses through 
                             all nodes of the binary tree, giving a time complexity of O(n). Therefore, adding up all these 
                             operations, the total time complexity of the make_ordering function is O(n^3) + O(n log n) + O(n). 
                             However, as n grows large, the terms O(n log n) and O(n) become insignificant relative to the cubic 
                             term. So, it is common to represent the overall time complexity using the term with the highest order 
                             of magnitude, which in this case is O(n^3).

                             ( yes yes i know O(n^3) is insane )


    """
    def make_ordering_rec(order : list[Point]) -> tuple[float,float,float]:
        n = len(order)
        score = []
        number_of_points=3
        for i in range(number_of_points):
            left = [0] * number_of_points
            right = [0] * number_of_points
            for j in range(number_of_points):
                if i==j:
                    continue
                if order[j] < order[i]:
                    left[i]+=1
                else:
                    right[i]+=1
            final_score = []
            for _ in range(number_of_points):
                if min(left[i] , right[i]) > 17:
                    final_score.append(min(left[i] , right[i]) / max(left[i] , right[i]))
                if not final_score:
                    score.append(1.0)
                else:
                    score.append(min(final_score))
            return tuple(score)
    best = (float('inf') , float('inf') , float('inf'))
    for compute in my_coordinate_list:
        new_score = make_ordering_rec(compute)
        if new_score < best:
            best = new_score
    
    ratio = Percentiles()
    for p in my_coordinate_list:
        ratio.add_point(p)

    my_coordinate_list = ratio.ratio(0,0)

    return my_coordinate_list[0:7]


        










    
