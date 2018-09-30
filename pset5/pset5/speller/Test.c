#include <string.h>
#include <stdio.h>

int main(void)
{
    char *string1 = "hello";
    int len = strlen(string1);
    char string2[len];

    for(int i = 0; i < len; i++)
    {
        string2[i] = string1[i];
    }
    string2[len] = '\0';
    if(strcmp(string1, string2) == 0)
    {
        printf("succes");
    }
    else
    {
        return 0;
    }
    return 1;
}