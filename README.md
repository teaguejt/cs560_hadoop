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

The query operates outside of HDFS and works thusly **INSERT HOW THE QUERY WORKS HERE**

The web portal operates outside of HDFS and works thusly **IF WE FINISH THE PORTAL, HOW IT WORKS GOES HERE**

## Invocation
These invocation instructions assume that all environment variables are pre-configured.

To use the mapper and reducer, first the input files need to be copied to HDFS by invoking `hadoop fs -put local_file remote_file` for each input file.

Once this copy is performed, the mapper and reducer can be run. From the path containing mapper.py and reducer.py, call `hadoop jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-steaming-2.7.1.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input HDFS_INPUT_FILE_PATHS -output HDFS_OUTPUT_DIR`, where `HDFS_INPUT_FILE_PATHS` is a comma-separated list of input files as fully-qualified HDFS paths (which is why the copy step above must be performed).

The program will now run. When it is finished, bring the generated index to the local filesystem with `hadoop -fs -text HDFS_OUTPUT_DIR/part-00000 > index.txt`. This will create a file in the working directory called `index.txt` that contains the full inverted index and can be processed using the query or the web portal.

## Test Results
Included with this assignment are two test text files and a sample inverted index file. They are, respectively, test.txt, test1.txt, and test_index.txt. These files are mostly nonsensical but demonstrate the operation of the program.

test.txt contains:  
I want to believe  
in the existence of Aliens  
Much like Mulder  
I really want to believe  
  
There is no such thing as a free lunch  
There is such a thing as free air.  

test1.txt contains:  
Mulder likes extraterrestrials

test_index.txt contains:  
a	2 	test-1-4 	test-6-7   
aliens	1 	test-2-5   
as	2 	test-6-6 	test-1-6   
believe	2 	test-4-5 	test-1-4   
existence	1 	test-2-3   
extraterrestrials	1 	test1-1-3   
free	1 	test-6-8   
i	2 	test-1-1 	test-4-1   
in	1 	test-2-1   
is	2 	test-6-2 	test-1-2   
like	1 	test-3-2   
likes	1 	test1-1-2   
lunch	1 	test-6-9   
mom	1 	test-1-8   
much	1 	test-3-1   
mulder	2 	test-3-3 	test1-1-1   
no	1 	test-6-3   
of	1 	test-2-4   
really	1 	test-4-2   
such	2 	test-6-4 	test-1-3   
the	1 	test-2-2   
there	2 	test-6-1 	test-1-1   
thing	2 	test-1-5 	test-6-5   
to	2 	test-4-4 	test-1-3   
want	2 	test-4-3 	test-1-2   
your	1 	test-1-7   

This output demonstrates that the mapper and reducer succesfully counts words, records line number and position (taking blank lines into account), and emits results in an easily-processable format.

The complete Shakespeare inverted index is also included with this submission in index.txt, but due to its extreme length it is not included in this readme.
