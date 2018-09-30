// This is a script to generate a Mario split pyramid as part of CS50 Problem Set 1
// Zach Sirera
// 5/13/18

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;

    // Prompt the user for a specified height of pyramid
    // Reject height if it is less than 0 or greater than 23
    do
    {
        n = get_int("Height:  ");
    }
    while (n < 0 || n > 23);

    // Print each row, top to bottom, line i at a time.
    for (int i = 0; i < n; i++)
    {
        // Print the spaces on the left side of the pyramid
        for (int k = (n - 1); k > i; k--)
        {
            printf(" ");
        }

        // Print the # chars on the left side of the pyramid
        for (int l = 0; l <= i; l++)
        {
            printf("#");
        }

        // Print the gap
        printf("  ");

        // Print # chars on the right side of the pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Print to next line
        printf("\n");
    }
}
