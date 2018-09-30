// Helper functions for music as part of CS50 Problem Set 3
// Zach Sirera
// 6/18/2018 to 6/24/2018


#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int dur;
    int dur_len = strlen(fraction);
    if (fraction[dur_len - 1] == '8')
    {
        dur = (fraction[0] - 48) * 1;
    }
    if (fraction[dur_len - 1] == '4')
    {
        dur = (fraction[0] - 48) * 2;
    }
    if (fraction[dur_len - 1] == '2')
    {
        dur = (fraction[0] - 48) * 4;
    }
    if (fraction[dur_len - 1] == '1')
    {
        dur = (fraction[0] - 48) * 8;
    }
    return dur;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int freq;
    int not_len = strlen(note);

    //Note - Calculate the frequency contribution the note makes
    float x;
    if (note[0] == 'A')
    {
        x = 0.0;
    }
    if (note[0] == 'B')
    {
        x = 2.0;
    }
    if (note[0] == 'C')
    {
        x = -9.0;
    }
    if (note[0] == 'D')
    {
        x = -7.0;
    }
    if (note[0] == 'E')
    {
        x = -5.0;
    }
    if (note[0] == 'F')
    {
        x = -4.0;
    }
    if (note[0] == 'G')
    {
        x = -2.0;
    }

    float note_f = 440 * pow(2, x / 12.0);


    //Accidental - Calculate the frequency contribution the accidental makes. Apply as needed.
    float acc;
    if (not_len == 3)
    {
        if (note[1] == '#')
        {
            acc = pow(2, 1.0 / 12.0);
        }
        if (note[1] == 'b')
        {
            acc = 1 / (pow(2, 1.0 / 12.0));
        }
    }
    else
    {
        acc = 1;
    }


    //Octave - Calculate the frequency calculation the octave makes. Apply as needed.
    float oct = 0;
    int octave = note[not_len - 1] - 48;
    if (octave > '4')
    {
        oct = pow(2, (octave - 4));
    }
    if (octave < '4')
    {
        oct = 1 / (pow(2, (4 - octave)));
    }
    else
    {
        oct = 1;
    }


    freq = round(note_f * acc * oct);
    return freq;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }
}
