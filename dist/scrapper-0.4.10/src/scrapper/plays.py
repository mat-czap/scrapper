
print([ set(input().split()) for _ in range(4)])

a,b, *args = [i for i in range(8)][::2]

print(a,b,args)






# import string
# from itertools import permutations, combinations
# from pprint import pprint
#
#
# def DNA_strand(dna):
#     x = string.maketrans("ATCG","TAGC")
#     return dna.translate(x)
#
# DNA_strand("TTT")




# def minion_game(s):
#     # s=[char.lower() for char in s]
#     vowels = 'AEIOU'
#     Kevin=0
#     Stuart=0
#
#     for i in range(len(s)):
#
#         if s[i] in vowels:
#             print(s[i],(len(s) - i))
#
#             Kevin += (len(s) - i)
#         else:
#             Stuart += (len(s) - i)
#     print(Kevin)
    #
    # for i in range(0,len(s)):
    #     for el in s[:i+1]:
    #         # print(i)
    #         if el in ("a","e","o","u","i"):
    #             Kevin += 1
    #         else:
    #             Stuart += 1

    # if Stuart > Kevin:
    #     print(f"Stuart {Stuart}")
    # elif Kevin > Stuart:
    #     print(f"Kevin {Kevin}")
    # else:
    #     print("draw")
#
# minion_game("BANANA")

