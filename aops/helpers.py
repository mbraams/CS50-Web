# create the first possible solution, returns size
def create_letters(input, letters):
    stringlength = 0
    for lines in input:
        letters.append("l")
        stringlength += 1
    return stringlength

# changes the solution by flipping "r" and "l" logarithmically, so that eventually all solutions are covered.
def change_solution(input, counter):
    length = len(input) - 1
    
     #loop over every "l" or "r", starting on the final step, and going backwarts (so "l,l,l,l" would turn into "l,l,l,r")
    for x in range(length + 1):
        if (counter % 2**x == 0):
            if (input[length - x] == "l"):
                   input[length - x] = "r"
            else:
                input[length - x] = "l" 