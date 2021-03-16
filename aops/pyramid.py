# Pyramid.py is a program that finds the solution of the pyramid descent puzzle
# it gives the solution by printing the correct route to the target in sequence of "l" and "r"
# "l" means you go to the left, "r" to the right
# The program loops over the possible solutions, and test wether they are true, 
# at which point this solution is printed, and the program exits
# it takes a file pyramid_sample_input.txt as input from the same directory


from helpers import *

#create variables
#list of the solution string with "l" for left or "r" for right
letters = []
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
    create_solution(size - 1, letters)

    #test the solution methods
    #for x in range(31):
        
        #counter += 1
        #print("counter: ", counter)
        #change_solution(letters, counter)        
        #print("letter string: ", letters)
    while True:
        #start with base number
        count = 0
        index = 0        
        for x in range(size):
            if x == 0:
                count = int(pyramid[0][0])
            else:
            #if r, the next number is one to the right, else it is the same (due to array representation of pyramid)
                print("x is :", x)
                print("letters[x] is ", letters[x - 1])
                if letters[x - 1] == "r":
                    index += 1
                count = count * int(pyramid[x][index]) 
                print("pyramid[x][index]: ", int(pyramid[x][index]))
                print("count is: ", count)
            if x == 4:
                print("x is 4")

        #check if solution is correct, or move to next
        if count == target:
            print("target found:")
            for letter in letters:
                print(letter)
                break
        else:
            counter +=1
            change_solution(letters, counter)
            if counter == 32:
                break
        