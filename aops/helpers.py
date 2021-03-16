# create the first possible solution, returns size (size input is already adjusted for having 1 less letter than rows in pyramid)
def create_solution(size, array):
    for i in range(size):
        array.append("l")

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

