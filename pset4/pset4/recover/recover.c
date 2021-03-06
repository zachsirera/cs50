// This is a program to implement recover as part of CS50 Problem Set 4
// Zach Sirera
// 7/13/18 to

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

// struct to store bytes blocks
typedef struct
{
    uint8_t block[512];
} BUFFER;


int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "usage: ./recover file.raw");
        return 1;
    }

    // Create file based on raw data from memory card
    FILE *file = fopen(argv[1], "r");

    // Create image file for outputs
    FILE *image;

    // Ensure that the file can be opened
    if (file == NULL)
    {
        fclose(file);
        fprintf(stderr, "Could not open raw file. \n");
        return 2;
    }

    // Create variables needed
    BUFFER buffer;
    bool jpeg_found = false;
    bool close_jpeg = false;
    int image_title = 0;
    char temp[8] = {0};

    // Begin loop looking for images
    while (fread(&buffer, sizeof(buffer), 1, file))
    {
        // Check that the first 3 bytes are consitent with JPEG formatting
        if (buffer.block[0] == 0xff && buffer.block[1] == 0xd8 && buffer.block[2] == 0xff)
        {
            // Check to make sure byte 4 is consistent with JPEG formatting
            if (buffer.block[3] == 0xe0 || buffer.block[3] == 0xe1 || buffer.block[3] == 0xe2 || buffer.block[3] == 0xe3 ||
                buffer.block[3] == 0xe4 || buffer.block[3] == 0xe5 || buffer.block[3] == 0xe6 || buffer.block[3] == 0xe7 ||
                buffer.block[3] == 0xe8 || buffer.block[3] == 0xe9 || buffer.block[3] == 0xea || buffer.block[3] == 0xeb ||
                buffer.block[3] == 0xec || buffer.block[3] == 0xed || buffer.block[3] == 0xee || buffer.block[3] == 0xef)
            {

                // If the beginning of a jpeg has been found, the previous image must be closed before writing to a new one.
                if (jpeg_found)
                {
                    close_jpeg = true;
                }

                // Beginning of a jpeg has been found
                jpeg_found = true;

                // Close old image
                if (close_jpeg)
                {
                    fclose(image);
                }

                // Create title for old image
                sprintf(temp, "%03i.jpg", image_title);

                // Update image title for new image
                image_title = image_title + 1;

                // Open new image file
                image = fopen(temp, "a");

                // Write bytes to new file
                fwrite(&buffer, sizeof(buffer), 1, image);
            }
        }
        else if (jpeg_found)
        {
            fwrite(&buffer, sizeof(BUFFER), 1, image);
        }
    }
    // Close files
    fclose(image);
    fclose(file);
}
