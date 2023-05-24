from __future__ import annotations
from threedeebeetree import Point
import random

from threedeebeetree import ThreeDeeBeeTree, BeeNode
from ratio import Percentiles


# def merge_sort(arr, low, high, coord):
#     if low < high:
#         mid = (high + low) // 2
#         merge_sort(arr, low, mid, coord)
#         merge_sort(arr, mid+1, high, coord)
#         merge(arr, low, mid, high, coord)

# def merge(arr, low, mid, high, coord):
#     n1 = mid - low + 1
#     n2 = high - mid
#     L = [0] * (n1)
#     R = [0] * (n2)
#     for i in range(0 , n1):
#         L[i] = arr[low + i]
#     for j in range(0 , n2):
#         R[j] = arr[mid + 1 + j]
#     i = 0
#     j = 0
#     k = low
#     while i < n1 and j < n2 :
#         if L[i][coord] <= R[j][coord]:
#             arr[k] = L[i]
#             i += 1
#         else:
#             arr[k] = R[j]
#             j += 1
#         k += 1
#     while i < n1:
#         arr[k] = L[i]
#         i += 1
#         k += 1
#     while j < n2:
#         arr[k] = R[j]
#         j += 1
#         k += 1
   




   



def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
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
            for w in range(number_of_points):
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


        










    
