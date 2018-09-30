// This is a script to validate credit card numbers as part of CS50 Problem Set 1
// Zach Sirera
// 5/14/18 to 5/18/18

#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    // Get credit card number from user input, assign to variable 'number'.

    long long number = get_long_long("Number:  ");

    // Determine length of number

    long long j = number;
    int length;
    for (length = 0 ; j != 0 ; length++)
    {
        j = j / 10;
    }

    int halflength = length / 2;


    // Check if length fits at least one of the companies' criteria
    // Amex         15 digits
    // MasterCard   16 digits
    // Visa         13 or 16 digits

    bool AmLenCheck = false;
    bool MCLenCheck = false;
    bool ViLenCheck = false;
    if (length == 15)
    {
        AmLenCheck = true;
    }
    else if (length == 13)
    {
        ViLenCheck = true;
    }
    else if (length == 16)
    {
        MCLenCheck = true;
        ViLenCheck = true;
    }
    else
    {
        printf("INVALID \n");
        exit(EXIT_SUCCESS);
    }

    // Iplement Luhn's algorithm to determine validity

    bool LuhnCheck = false;
    long long a;
    int dig;
    int dig2;
    int digsum = 0;
    int digsum2 = 0;

    // Find the set of digits not being multiplied by 2

    for (int i = 0; i <= halflength; i++)
    {
        a = pow(10, 2 * i) ;
        dig = (number / a) % 10;
        digsum = digsum + dig;

    }

    // Find the set of digits being multiplied by 2

    for (int k = 0; k <= halflength - 1; k++)
    {
        a = pow(10, 2 * (k + 1) - 1);
        dig2 = 2 * ((number / a) % 10);
        if (dig2 > 9)
        {
            dig2 = (dig2 % 10) + (dig2 / 10);
        }

        digsum2 = digsum2 + dig2;
    }

    if (((digsum + digsum2) % 10) == 0)
    {
        LuhnCheck = true;
    }


    // Check if the first digit(s) meet at least one of the companies' criteria
    // Amex         34 or 37
    // MasterCard   51 to 55
    // Visa         4

    bool AmDigCheck = false;
    bool MCDigCheck = false;
    bool ViDigCheck = false;

    long long b = pow(10, (length - 2));
    long long c = pow(10, (length - 3));
    int d = (number / b) / 10;
    int e = (number / c) / 10;

    if (e == 34 || e == 37)
    {
        AmDigCheck = true;
    }
    else if (e == 51 || e == 52 || e == 53 || e == 54 || e == 55)
    {
        MCDigCheck = true;
    }
    else if (d == 4)
    {
        ViDigCheck = true;
    }
    else
    {
        printf("INVALID \n");
        exit(EXIT_SUCCESS);
    }

    // Combine all criteria. If number meets all criteria for one company, program will output that companies name.
    // Otherwise, the program will return INVALID.

    if (LuhnCheck && AmLenCheck && AmDigCheck)
    {
        printf("AMEX \n");
    }
    else if (LuhnCheck && MCLenCheck && MCDigCheck)
    {
        printf("MASTERCARD \n");
    }
    else if (LuhnCheck && ViLenCheck && ViDigCheck)
    {
        printf("VISA \n");
    }
    else
    {
        printf("INVALID \n");
        exit(EXIT_SUCCESS);
    }
}
