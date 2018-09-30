# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

The longest word in the dictionary, also it is a pneumoconiosis caused by the inhalation of fine volcanic dust.

## According to its man page, what does `getrusage` do?

returns the resource usage measures for a program, specifically for functions that are called.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Because each instance of calculate is a separate operation within a greater sum that eventually determines the entire time spent in
each operation. Passing these variables as references allows them to be calculated dynamically.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

main calls fgetc() to return each character in the text file. If the character is alphabetical or is an appostrophe it is appended onto the variable 'word'. If the word has
numerical characters it is ignored. It does this as long as the length of the word is less than the length of the longest word in the dictionary. Otherwise, it
is deemed an alphabetical string too long to be a word. If the speller runs into a character that is neither alphabetical, numberical, or an appostrophe, it assumes
it has completed an entire word. As no words contain characters different than those listed above. Once the word is read from the file
it is passed through check to determine if it is a valid word or not.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

fscanf works well for the dictionary file because all words are strings that follow consistent rules. The words in our text file are
not so consistent. fgetc moves character by character, allowing us to impose our own rules on the logical selection process, as listed
above, so that we may determine if it is a valid word or not.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So that these parameters cannot be modified by the program. As they are dependent on information coming to them from another program
and consistency between the two programs is critical in determining whether a word is a valid word.
