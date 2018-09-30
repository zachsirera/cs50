// This is a program to implement whodunit as part of CS50 Problem Set 4
// Zach Sirera
// 6/25/2018 to 7/2/2018


#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"


int main(int argc, char *argv[])
{
    // Ensure that the number of command line arguments is 2 and only 2.
    if (argc != 3)
    {
        printf("Usage: ./whodunit infile outfile\n");
        return 1;
    }

    // Remember filenames
    char *infile = argv[1];
    char *outfile = argv[2];

    // Open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s. \n", infile);
        return 2;
    }

    // Open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not write %s. \n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // Write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // Determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // Iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // Temporary storage
            RGBTRIPLE triple;

            // Read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);


            // Rewrite bytes in triple to "retain" only those components that are not pure red or white

            if (triple.rgbtRed != 0xff && triple.rgbtRed != 0x00)
            {
                triple.rgbtBlue = 0xff;
                triple.rgbtGreen = 0xff;
                triple.rgbtRed = 0xff;
            }
            else
            {
                triple.rgbtBlue = 0x00;
                triple.rgbtGreen = 0x00;
                triple.rgbtRed = 0x00;
            }


            // Write RGB triple to outfile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
        }

        // Skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

        // Then add it back (to demonstrate how)
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // Close infile
    fclose(inptr);

    // Close outfile
    fclose(outptr);

    // success
    return 0;
}