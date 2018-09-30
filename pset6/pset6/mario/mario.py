# This is a program to implement Mario (more) as part of CS50 Problem Set 6
# Zach Sirera
# 8/2/2018 to 8/10/2018

import cs50

# Ask the user for the height of the Mario Pyramid
print("Height: ", end="")
height = cs50.get_int()

# Validate the height input
if height < 0 or height > 23:
    print("Height: ", end="")
    height = cs50.get_int()

# Carry out the printing iteration line by line
for i in range(height):
    # Print the initial spaces
    for j in range(height - i - 1):
        print(" ", end="")
    # Print the # characters for the left pyramid on each row
    for k in range(i + 1):
        print("#", end="")
    # Print the space between each pyramid
    print("  ", end="")
    # print the # characters for the right pyramid on each row
    for l in range(i + 1):
        print("#", end="")
    print("")