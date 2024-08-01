// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

int number_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
   int hash_value = hash(word);
   node *cursor = table[hash_value];
   while(cursor != NULL)
   {
    if(strcasecmp(cursor->word, word)==0)
    {
        return true;
    }
    else
    {
        cursor = cursor->next;
    }
   }
return false;

    // TODO
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    for(int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    FILE *dict_file = fopen( dictionary , "r");
    if(dict_file == NULL)
    {
        printf("couldn't open dictionary\n");
        return false;


    }
    char buffer[45];

    while(fscanf(dict_file, "%s", buffer) != EOF)
    {
        node *new_word = malloc(sizeof(node));
        int hash_value = hash(buffer);
        strcpy(new_word -> word, buffer);
        new_word->next = table[hash_value];
        table[hash_value] = new_word;
        number_words++;
    };
    fclose(dict_file);
    return true;
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return number_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for(int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = table[i];
     while (cursor != NULL)
    {
        cursor = cursor->next;
        free(tmp);
        tmp = cursor;
    }

    }
    // TODO
    return true;
}
