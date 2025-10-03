"""
Find the chances of randomonly choosing max value in an array. MONTY HALL PARADOX

An array of 3 random elements between 1-10 are generated. Choose a random index between 0-2.
Remove the smallest element between the elements which were not choosed at first as it is not the max value.
Change your choice to remaining element and check if you were right or wrong
"""
from random import randint

def monty_hall_paradox(iteration_cnt=1000, arr_length=3):

    crt_choice = 0
    
    for i in range(iteration_cnt):
        # Creating an array of 3 random elements without duplicates
        arr = []
        while len(arr)<arr_length:
            num = randint(1,10)
            if(num not in arr):
                arr.append(num)
        arr_original = arr.copy()

        # Guess an index for max value in the array
        indexes = list(range(arr_length))
        ind = randint(0, arr_length-1)

        # Find the minimum value between the remaining 2 options as it is not the max value
        starting_value = arr[ind]
        indexes.remove(ind)
        min_val = min(arr[indexes[0]], arr[indexes[1]])
        arr.remove(min_val)

        # Switch your choice to other option and see if it is the max value
        arr.remove(starting_value)
        if(max(arr_original) == arr[0]):
            crt_choice += 1
    
    print(f"Probablity of choosing the correct option after changing the first choice is {crt_choice/iteration_cnt} over {iteration_cnt} iteration")


monty_hall_paradox(1000, 5)

