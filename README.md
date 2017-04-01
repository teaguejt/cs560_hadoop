# cs560_hadoop

## A MapReduce and Hadoop proof-of-concept by Joseph Teague and Clarence Jackson

## Stop words:
This program assumes that large text files are being processed and removes any word that occurs more than 1800 times. This value was determined by examining a complete word count of the Works of William Shakespeare. Over 5MB text, words that occur over 1800 times are typically words that do not be analyzed like "the," "a," and "and." Words that are important typically do not occur more than 300 times, meaning 1800 is a safe cutoff even for larger file analysis.

Due to the fact that this is a streaming algorithm, it is difficult to obtain on-the-fly values for total file size, total wordcount, etc. While in theory it may seem better to cull any words that exceed a percentage of total words, this is not feasible in a streaming program without increasing execution complexity and requiring the somewhat cumbersom MapReduce framework be invoked multiple times.

Words are counted as the same word without respect to case or following or preceeding punctuation (e.g. "Hello," "HELLO," "hello," and "::;HeLlO!!..,," are treated as the same word). The program does not take tense into consideration (e.g. "ran" and "run" are treated as different words).

## Implementation:
The mapper and reducer are written in Python due to its simplicity and powerful string processing features. As can probably be inferred, mapper.py contains code for the mapper and reducer.py contains code for the reducer. These programs are streaming algorithms, i.e. they operate on lines received over stdin instead of files. Files are passed to the mapper by the Hadoop framework on standard input, which "prints" them to standard output for receipt by the reducer, which stores them in the specified output directory per the standard Hadoop MapReduce naming scheme.

One design quirk results in these programs (specifically the mapper) **NOT WORKING OUTSIDE HADOOP**. Because files are sent as lines on stdin, the program reads a Hadoop environment variable (MAPREDUCE_MAP_INPUT_FILE) to get the current file for the document ID. Otherwise, there would be no way to map a line to a particular document ID for the index.

The mapper emits each word in a line in the format `word \t docID \t 1 \t line number \t position` where:  
`word` is the word being processed  
`docID` is the document ID which, for readability in query results, is the filename with its full path and extension stripped (e.g. /users/hduser/input.txt would have docID "input").  
`1` is the minimal count of the word  
`line number` is the line number within the current file at which the word is found. When `MAPREDUCE_MAP_INPUT_FILE` changes, the line count is reset to 0 as the document being processed has changed.  
`position` is the position of the word on the line. This is used by the web portal query.  

These lines are received and processed by the reducer. The reducer maintains a current count of each word and a list of occurences. Because mapper output is sorted alphabetically, we can guarantee that the reducer does not switch words before processing the last instance of its current word. Therefore, the reducer can make some assumptions. As it encounteres words, it increments the count and adds the occurence to its occurences list. When the word changes, it outputs a line in the format `word \t count \t occurences` where:  
`word` is the last processed word  
`count` is the total count of occurences in the word  
`occurences` is the list of occurences in the format `docID-line number-line position`, with each occurence separated by a tab.  
The reducer then resets the count and empties the occurences list so it can process the next word. There is an exception to this process: if the total count for a word is greater than the pre-determined stop word count, it is not emitted to the reducer's output file.
