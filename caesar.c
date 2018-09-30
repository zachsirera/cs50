// This is a program to implement the Caesar cipher as part of CS50 Problem Set 2.
// Zach Sirera
// 5/18/18 to 5/20/2018

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Ensure that the number of command line arguments is 2 and only 2.
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    // Get key from user input in the command line.
    int k = atoi(argv[1]) % 26;

    // Prompt user for input to be passed through the Caesar cipher.
    string s = get_string("plaintext:  ");
    int n = strlen(s);

    // Implement the Caesar cipher.
    printf("ciphertext: ");

    int c;

    for (int i = 0; i < n; i++)
    {
        // Encypher only those characters that are alphabetical.
        if (isalpha(s[i]))
        {
            // Preserve case of character.
            if (isupper(s[i]))
            {
                c = (int) s[i] + k;
                if (c > 90)
                {
                    c = c - 26;
                }
            }
            else
            {
                c = (int) s[i] + k;
                if (c > 122)
                {
                    c = c - 26;
                }
            }
        }
        else
        {
            c = s[i];
        }
        printf("%c", (char) c);
    }
    printf("\n");
    return 0;
}
