# This is a program to implement Caesear as part of CS50 Problem Set 6
# Zach Sirera
# 8/10/2018 to 8/13/2018

import cs50
import sys
import string

if len(sys.argv) != 2:
    print("Usage: python caesar.py k")
    sys.exit(1)
else:
    # Prompt the user for a string to encipher
    print("plaintext: ", end="")
    s = cs50.get_string()
    print("ciphertext: ", end="")
    key = int(sys.argv[1]) % 26

    for char in s:
        if char.isalpha():
            c = ord(char) + key
            if char.islower():
                if c > 122:
                    c = c - 26
            else:
                if c > 90:
                    c = c - 26
            c = chr(c)
        else:
            c = char
        print(f"{c}", end="")
    print()
    sys.exit(0)