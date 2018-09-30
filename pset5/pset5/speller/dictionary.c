// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Defining a node, the building block of the linked list.
typedef struct node
{
    char value[LENGTH + 1];
    struct node *next;
}
node;

// Creating the hash function global so that it can be used in load as well as check.
unsigned long zhash(char *str)
{
  unsigned long hash = 5381;
  int c;

  while ((c = *str++))
      hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

  return hash;
}

// Create global variables needed outside of individual functions.
node *table[SIZE];

int dict_length = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    int leng = strlen(word);
    char word_copy[leng];

    // Conver word to lowercase and store in word_copy
    for (int i = 0; i < leng; i++)
    {
        word_copy[i] = tolower(word[i]);
    }

    // Add a null termination to word_copy
    //word_copy[leng] = '\0';

    // Pass word through zhash to return the bucket into which it belongs.
    int z_index = zhash(word_copy);

    // Create a cursor to traverse our linked list looking for words.
    node *cursor = table[z_index];

    // Iterate over all words in linked list of length z_index
    while (cursor != NULL)
    {
        // Compare word in text file to word in dictionary
        if (strcasecmp(cursor->value, word_copy) == 0)
        {
            return true;
        }
        else
        {
            // If comparison fails, move to next word in dictionary
            cursor = cursor->next;
        }
    }

    // If comparison fails and we reach the end of the linked list, return false to signify a misspelled word
    return false;
}

bool loaded;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary.
    FILE *file = fopen(dictionary, "r");

    // Create needed variables.

    char *dict_word = malloc(LENGTH + 1);
    node *head = NULL;

    // Iterate through entire dictionary.
    while (fscanf(file, "%s", dict_word) != EOF)
    {
        // Create memory for the words and their pointers.
        node *new_node = malloc(sizeof(node));

        // Test and ensure there is enough memory for every word in the dictionary.
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy the dictionary word to the value member of the node.
        strcpy(new_node->value, dict_word);

        // Pass the dictionary word through the hash function to return the index of the bucket where it should be stored.
        int len = zhash(new_node->value);

        // Amend linked list with dictionary word.
        new_node->next = head;
        head = new_node;
        table[len] = head;
        //free(new_node);

        // Add count to dict_length for the purpose of the size() function.
        dict_length++;
    }
    free(dict_word);
    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return dict_length;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // iterate over the buckets in the array
    for (int i = 1; i < SIZE; i++)
    {
        // clear all linked lists stemming from each bucket
        node *cursor = table[i];
        while (cursor != NULL)
        {
            // traverse linked list and clear it, node by node until reaching the end.
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    loaded = false;
    return true;
}
