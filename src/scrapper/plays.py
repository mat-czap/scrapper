import math
from typing import Dict, List, Tuple
from random import seed
from random import random




def get_list(given_text: str) -> List[str]:
    return [chr(ord(char) + 1) for sublist in given_text.split() for char in sublist]


# print((get_list(x)))


def get_words(init_word: str):
    return {word: len(word) for word in init_word.split()}


# print(get_words(x))
matrix = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flatten_matrix = [val for sublist in matrix for val in sublist]


# print(flatten_matrix)


def Cezar(given_text: str, mv_step: int) -> str:
    return "".join([chr(ord(char) + mv_step) for char in given_text])

    # changed_word = []
    # for char in given_text:
    #     num = ord(char) + mv_step
    #     changed_word.append(chr(num))
    # return "".join(changed_word)


# print(ord("a"))


# print(Cezar("aaaabbbbccc",1))

#
# dics = {"a": 1, "b": 2, "c": 3}
#
# def rev_k_v(dic: Dict[str,int]):
#     return {(v,k) for k, v in dic.items()}

# print(rev_k_v(dics))

low = 1
high = 12
nums = [2, 4, 5, 10]

# (1,1),(3,3),(6,11)

new_list = [x for x in range(low, high + 1) if x not in nums]
q = sorted(list(set(range(low, high + 1)) - set(nums)))
# [1, 3, 6, 7, 8, 9, 11, 12]
# print(q)

low = 1
high = 12
nums = [2, 4, 5, 10]

# (1,1),(3,3),(6,9),(11,12)


# def show_range(low:int, high:int, nums:List[int]) -> List[Tuple[int, int]]:
#
#     nl = [num for num in range(low, high + 1) if num not in nums]
#
#     s = []
#     t = []
#
#     len_nl: int = len(nl)
#
#     for i in range(len(nl)):
#         if i+1 >= len_nl:
#             import pdb;pdb.set_trace()
#             break
#         if nl[i + 1] - nl[i] > 1:
#             t.append(nl[i])
#             s.append((t[0], t[-1]))
#             t = []
#         else:
#             t.append(nl[i])

# t.append(nl[-1])
# s.append((t[0], t[-1]))

# return s

#  sdokdask  dsa

# def show_range(start:int, high:int, nums:List[int]) -> List[Tuple[int, int]]:
#     low = start
#     end = 0
#     result= list()
#
#     nl = [num for num in range(low, high + 1) if num not in nums]
#     len_nl: int = len(nl)
#
#     for i in range(start,high):
#         if i+1 >= len_nl:
#             break
#         import pdb;pdb.set_trace()
#         if nl[i-1] in nums:
#             result.append([low, end])
#             low = nl[i+1]
#             end = nl[i+1]
#         else:
#             end = nl[i]
#
#     return result
#
#

# from typing import Dict, List, Tuple
#
# def show_range(low: int, high: int, nums:List[int]):
#
#     nl = [num for num in range(low, high + 1) if num not in nums]
#
#     final = []
#     len_nl = len(nl)
#     temp_highest = 0
#     start_rng = low
#
#     for i in range(len(nl)):
#         if i + 1 == len_nl:
#             final.append((start_rng, nl[i]))
#             break
#         if nl[i + 1] - nl[i] > 1:
#             temp_highest = nl[i]
#             final.append((start_rng, temp_highest))
#             start_rng = nl[i + 1]  # po wrzuceniu do listy, start od kolejnego elementu
#         else:
#             temp_highest = nl[i]
#
#     return final


from typing import Dict, List, Tuple

def show_range(start: int, high: int, nums: List[int]):
    results = list()
    nl = [num for num in range(start, high + 1) if num not in nums]
    low = nl[0]
    end = nl[0]

    for index, number in enumerate(nl):
        if number < low:
            continue
        if index + 1 >= len(nl):
            results.append((low, end))
            break
        if nl[index + 1] == number + 1:
            end = nl[index + 1]
        else:
            results.append((low, end))
            low = nl[index + 1]
            end = nl[index + 1]

    return results


#

# #
#
print(*show_range(1, 12, [2, 4, 5, 10]))

#
# from collections import defaultdict
# dics = defaultdict(list)
# # #
# # dics=dict(list())
# # dics['Python']=[]
# dics['Python'].append("P")
# dics['Python'].append("YTHON")
# dics['JS'].append("javascript")
# # for el in dics.items():
# #     print(el)
# print(dics)

# class Auto:
#     def __init__(self, title):
#         self.title=title
#     #
#     # def show_title(self):
#     #     print(f"Nazwa tej instancji: {self.__title}")
#
#     def get_title(self):
#         return self._title
#
#
#
# Mazda = Auto("Mazda")
# # Mazda.title = "Romet"
# print(Mazda.get_title())


nums = [2,4,5,10]

c = list(set(range(1,12+1)) - set(nums))
print(c)