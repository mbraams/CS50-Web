# Pyramid.py is a program that finds the solution of the pyramid descent puzzle
# it gives the solution by printing the correct route to the target in sequence of "l" and "r"
# "l" means you go to the left, "r" to the right
# The program loops over the possible solutions, and test wether they are true, 
# at which point this solution is printed, and the program exits
# it takes a file pyramid_sample_input.txt as input from the same directory


from helpers import *
    #create variables
#solution string in "l" for left or "r" for right
letters = []
# numerical target we want to reach as solution
target = 0
# size of pyramid
size = 0
#counter starts at 1 for the first try
counter = 0

# open the file (in same directory)
with open("pyramid_sample_input.txt", "r") as file:
    # get the goal
    target = int(file.readline().split(" ")[1])    
    print("target: ", target)

    # "create_letters" creates solution string and return value is the size
    size = create_letters(file, letters)

    for x in range(32):
        
        counter += 1
        print("counter: ", counter)
        change_solution(letters, counter)        
        print("letter string: ", letters)
    print("pyramid size: " , size)




    #create empty array
    pyramid = []

    print("pyramid: ", pyramid)

    #fill in the pyramid array with the input file
    #for line in f.read().splitlines():



print(pyramid)





