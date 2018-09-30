// This is a program to implement the Vigenere cipher as part of CS50 Problem Set 2
// Zach Sirera
// 6/14/2018 (resubmitted 8/10/2018)

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
        printf("Usage: ./vigenere k\n");
        return 1;
    }

    // Get key from user input in the command line.
    string key = argv[1];

    // Check that key is alphabetical
    int kleng = strlen(key);
    for (int y = 0; y < kleng; y++)
    {
        if (!isalpha(key[y]))
        {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
        else if (isupper(key[y]))
        {
            key[y] = tolower(key[y]);
        }
        else
        {
            key[y] = key[y];
        }
    }

    // Prompt user for input to be passed through the Vigenere cipher.
    string s = get_string("plaintext:  ");
    printf("ciphertext: ");
    int n = strlen(s);
    int c;  //c is the cypertext character in each iteration of the loop
    int p;  //p is the plaintext character in each iteration of the loop
    int k;  //k is the cypher value in each iteration of the loop
    int q;  //q is the offset depending on the case of each character for use in k
    int j = 0;  //j is the counter for the key iterations

    for (int i = 0; i < n; i++)
    {
        p = tolower(s[i]);
        if (isupper(p))
        {
            q = 65;
        }
        else
        {
            q = 97;
        }
        k = key[j % kleng] - q;
        if (!isalpha(p))
        {
            c = p;
        }
        else
        {
            c = p + k;
            if (c > 122)
            {
                c = c - 26;
            }
            if (isupper(s[i]))
            {
                c = toupper(c);
            }
            j++;
        }
        printf("%c", (char) c);
    }
    printf("\n");
    return 0;
}
