// This is program to implement resize (less) as part of CS50 Problem Set 4
// Zach Sirera
// 7/13/2018

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // ensure the scale factor 'n' is between 1 and 100
    int n = atoi(argv[1]);
    if (n < 1 || n > 100)
    {
        fprintf(stderr, "n must be greater than or equal to 1 and less than or equal to 100. \n");
        return 2;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, new_bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, new_bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }

    // Update size parameters of new file
    new_bf = bf;
    new_bi = bi;
    new_bi.biWidth = bi.biWidth * n;
    new_bi.biHeight = bi.biHeight * n;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int new_padding = (4 - (new_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // write new image size
    new_bi.biSizeImage = (new_bi.biWidth * sizeof(RGBTRIPLE) + new_padding) * abs(new_bi.biHeight);

    // write new file size
    new_bf.bfSize = new_bi.biSizeImage + 0x36;

    // write outfile's BITMAPFILEHEADER
    fwrite(&new_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&new_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over each of the infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // temporary storage
        RGBTRIPLE triple[bi.biWidth];

        // read RGB triple from infile
        for (int l = 0; l < bi.biWidth; l++)
        {
            fread(&triple[l], sizeof(RGBTRIPLE), 1, inptr);
        }

        for (int k = 0; k < n; k++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                for (int m = 0; m < n; m++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple[j], sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            // padding
            for (int o = 0; o < new_padding; o++)
            {
                fputc(0x00, outptr);
            }
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;

}