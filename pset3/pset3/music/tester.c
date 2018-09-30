#include <string.h>
#include <stdio.h>

#include "helpers.h"

    const string NOTES[] = {"C", "C#", "D", "D#", "E", "F",
                        "F#", "G", "G#", "A", "A#", "B"
                       };

int main(void)
{

    int f;
    char *note;

    for (int i = 0; i < 12; i++)
    {
        note = NOTES[i];
        f = frequency(note);
        printf("%d \n", f);
    }



}