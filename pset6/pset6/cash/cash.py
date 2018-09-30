# This is a program to implement cash as part of CS50 Problem Set 6
# Zach Sirera
# 8/13/2018 to 8/14/2018

import cs50

while True:
    print("Change owed: ", end="")
    s = cs50.get_float()
    if s > 0:
        break

i = 0
while True:
    if s >= 0.25:
        s = round(s - 0.25, 2)
        i = i + 1
    elif s >= 0.1:
        s = round(s - 0.1, 2)
        i = i + 1
    elif s >= 0.05:
        s = round(s - 0.05, 2)
        i = i + 1
    elif s >= 0.01:
        s = round(s - 0.01, 2)
        i = i + 1
    else:
        break
print(f"{i}")