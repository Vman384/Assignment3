from __future__ import annotations
from threedeebeetree import Point
import random

from threedeebeetree import ThreeDeeBeeTree, BeeNode
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    def make_ordering_rec(order : list[Point]) -> tuple[float,float,float]:
        n = len(order)
        score = []
        number_of_points=3
        for i in range(number_of_points):
            left = max(0, i-1)  # Look at the neighbor on the left
            right = min(i+1, number_of_points-1)  # Look at the neighbor on the right
            left_score = left / (i + 1) if order[i] > order[left] else 0
            right_score = (n - right) / (n - i) if order[i] > order[right] else 0
            score.append(max(left_score, right_score))
        return tuple(score)

    my_coordinate_list.sort()  # Sort the list before processing

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



        










    
