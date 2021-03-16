# Pyramid.py is a program that finds the solution of the pyramid descent puzzle
# it gives the solution by printing the correct route to the target in sequence of "l" and "r"
# "l" means you go to the left, "r" to the right
# The program loops over the possible solutions, and test wether they are true, 
# at which point this solution is printed, and the program exits
# it takes a file pyramid_sample_input.txt as input from the same directory


from helpers import *

#create variables
#list of the possible solution string with "l" for left or "r" for right
solution = []

# numerical target we want to reach as solution
target = 0

#counter starts at 1 for the first try
counter = 0

# Height and base width of pyramid
size = 0

# open the file (in same directory)
with open("pyramid_sample_input.txt", "r") as file:
    # get the goal
    target = int(file.readline().split(" ")[1])  

    #read the csv file into an array
    pyramid = []
    for line in file:
        pyramid.append(line.split(","))
        size += 1

    #amount of steps is one less than size because of starting number
    create_solution(size - 1, solution)

    #loop over possible solutions until the right solution has been found or we went over each solution without finding the answer
    while True:
        count = 0
        index = 0
        #loop over each letter in the solution   
        for x in range(size):
            if x == 0:
                #initiate base number, as there is 1 more number than "l"/"r" we don't look at the solution here
                count = int(pyramid[0][0])
            else:
            #if r, the next number is one to the right, so index changes, else it is the same (due to array representation of pyramid)
                if solution[x - 1] == "r":
                    index += 1
                #multiply count with the next number
                count = count * int(pyramid[x][index]) 

        #check if solution is correct, or move to next
        if count == target:
            for letter in solution:
                print(letter, end="")
            break
        else:
            counter +=1
            #change solution method updates to the next possible solution, see helpers.py
            change_solution(solution, counter)
            #amount of possible solutions is limited to 2^n where n is the size of the pyramid, so if we reach here, no solution exists.
            if counter == 2 ** size:
                print("no solution exists")
                break
        