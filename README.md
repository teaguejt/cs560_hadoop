# cs560_hadoop

## A MapReduce and Hadoop proof-of-concept by Joseph Teague and Clarence Jackson

## tl;dr
Make sure your environment is set up and that a directory called "test" exists on the HDFS, then run `./run.py file1 file2 ...` to process your desired files (e.g. `./run.py works_of_william.txt`). When the command finishes, the generated list of stop words will be in gen_stop_words.txt and the inverted index will be in index.txt.

## Stop words:
This program assumes that large text files are being processed and removes any word that occurs more than 1800 times. This value was determined by examining a complete word count of the Works of William Shakespeare. Over 5MB text, words that occur over 1800 times are typically words that do not be analyzed like "the," "a," and "and." Words that are important typically do not occur more than 300 times, meaning 1800 is a safe cutoff even for larger file analysis.

Due to the fact that this is a streaming algorithm, it is difficult to obtain on-the-fly values for total file size, total wordcount, etc. While in theory it may seem better to cull any words that exceed a percentage of total words, this is not feasible in a streaming program without increasing execution complexity and requiring the somewhat cumbersom MapReduce framework be invoked multiple times, with additional processing outside of HDFS.

Words are counted as the same word without respect to case or following or preceeding punctuation (e.g. "Hello," "HELLO," "hello," and "::;HeLlO!!..,," are treated as the same word). The program does not take tense into consideration (e.g. "ran" and "run" are treated as different words).

To accomplish the goal of identifying stop words, a mapper and recuder, written in Python, generate a list of words exceeding the 1800-instance count and emit them. These words are then passed to the reducer as command line arguments. If the run script is not used, it is the responsibility of the user to ensure that any desired words are passed as command line arguments to the reducer. This decision was made to avoid file operations on files stored in the HDFS, which can be tricky to implement and unpredicatable (in our experience, at least).

## Implementation:
The mapper and reducer for both stop word generation and the main program are written in Python due to its simplicity and powerful string processing features. As can probably be inferred, mapper.py contains code for the mapper and reducer.py contains code for the reducer. stop_mapper.py and stop_reducer.py are the files for the stop word generator. These programs are streaming algorithms, i.e. they operate on lines received over stdin instead of files. Files are passed to the mapper by the Hadoop framework on standard input, which "prints" them to standard output for receipt by the reducer, which stores them in the specified output directory per the standard Hadoop MapReduce naming scheme.

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
The reducer then resets the count and empties the occurences list so it can process the next word. 

The reducer accepts stop words as command line arguments and stores them in a list when it starts. If the word it is processing is in the list of stop words, the reducer ignores it, performs no processing, and emits nothing.

Because map job splits can make line number calculations unpredictable, we have also included a run script. This run script performs preprocessing and invokes the mapper and reducer, executing all needed HDFS commands to ensure the desired output is obtained. More on this will be discussed in the "invocation" section, however the preprocessor needs to be mentioned here. Because line number calculations within MapReduce are unreliable, the preprocessor opens each file the user wants to process and adds the line number to the beginning of each line. This allows the mapper to obtain an accurate line number at each stage of its operation, without regard to how many map jobs are actually running.

The query operates outside of HDFS and works thusly **INSERT HOW THE QUERY WORKS HERE**

The web portal operates outside of HDFS and works thusly **IF WE FINISH THE PORTAL, HOW IT WORKS GOES HERE**

## Invocation
These invocation instructions assume that all environment variables are pre-configured.

We have included a run script that should be used to make life a lot easier for whoever grades this. However, the run script assumes the environment (e.g. HADOOP_HOME and JAVA_HOME variables) is set up correctly and that a directory called "test" exists in the root of the HDFS.

The run script can be invoked using `./run.py file1 file2...` where file1 file2 ... is a list of files for which the user would like to obtain a word count.

The run script performs the following functions:  
1. Delete the test directory on the HDFS and any input files matching the names of its command line arguments.  
2. Run the preprocessor to obtain copies of the user's files that have line numbers included. This is non-destructive and does not modify the original files.  
3. Copy the pre-processed files to HDFS.  
4. Run the stop word generator to obtain a list of stop words.  
5. Pull the stop words file from HDFS to the local file system, open it, and read in a list of the generated stop words.  
6. Delete the test directory again.  
7. Run the main mapper and reducer, using the list of stop words generated in step 5 as command line arguments to the reducer.  
8. Pull the inverted index from HDFS to the local file system.  
9. Clean up by deleting the preprocessed files.  

When invoked using the run script, the stop words will be stored in the working directory as "gen_stop_words.txt" and the inverted index is stored in the working directory as "index.txt".

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
a	2 	test-7-4 	test-6-7   
air	1 	test-7-8   
aliens	1 	test-2-5   
as	2 	test-6-6 	test-7-6   
believe	2 	test-4-5 	test-1-4   
existence	1 	test-2-3   
extraterrestrials	1 	test1-1-3   
free	2 	test-6-8 	test-7-7   
i	2 	test-1-1 	test-4-1   
in	1 	test-2-1   
is	2 	test-6-2 	test-7-2   
like	1 	test-3-2   
likes	1 	test1-1-2   
lunch	1 	test-6-9   
much	1 	test-3-1   
mulder	2 	test-3-3 	test1-1-1   
no	1 	test-6-3   
of	1 	test-2-4   
really	1 	test-4-2   
such	2 	test-6-4 	test-7-3   
the	1 	test-2-2   
there	2 	test-6-1 	test-7-1   
thing	2 	test-7-5 	test-6-5   
to	2 	test-4-4 	test-1-3   
want	2 	test-4-3 	test-1-2   

Please note that for this example, due to the low word count and to demonstrate full functionality, there are no stop words sent to the reducer. This output demonstrates that the mapper and reducer succesfully counts words, records line number and position (taking blank lines into account), and emits results in an easily-processable format.

The complete Shakespeare inverted index is also included with this submission in index.txt, but due to its extreme length it is not included in this readme.

## Submission
The assignment is submitted as a tarball that contains the following files:  
`README.md`: this file  
`stop_mapper.py`: the mapper for stop word generation  
`stop_reducer.py`: the reducer for stop word generation  
`mapper.py`: the main mapper  
`reducer.py`: the main reducer  
`run.py`: the run script that should be used for the execution of the program  
`gen_stop_words.txt` and `shakespeare_stop_words.txt`: the stop words generated from the works of William Shakespeare   
`index.txt` and `shakespeare_index.txt`: the inverted index generated from the works of William Shakespeare  
`test.txt` and `test1.txt`: test text files used as we developed the program  
`test_index.txt`: the index generated using the above text files  
`works_of_william.txt`: the complete works of William Shakespeare  
