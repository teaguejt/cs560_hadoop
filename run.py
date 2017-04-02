#!/usr/bin/env python

import sys
import os

original_files = []
input_files = []
hdfs_files = []

# Preprocess
for arg in sys.argv:
	if arg == sys.argv[0]:
		continue

	infilename = arg
	outfilename = "pre_" + arg
	infile = open(infilename, 'r')
	outfile = open(outfilename, 'w')
	original_files.append(infilename)
	input_files.append(outfilename)
	linenum = 1

	for line in infile:
		outfile.write(str(linenum) + " " + line)
		linenum += 1

	infile.close()
	outfile.close()

# Copy files to hdfs
if len(original_files) != len(input_files):
	printf("preprocessing error: unequal number of files")
	sys.exit(1)

for i in range(len(original_files)):
	hdfs_file = "/test/" + original_files[i]
	hdfs_files.append(hdfs_file)
	# Delete any files with the same name that already exist,
	# Then copy the new ones
	cmd = "hadoop fs -rm -r -f " + hdfs_files[i]
	print("executing: " + cmd)
	os.system(cmd)
	cmd = "hadoop fs -put " + input_files[i] + " " + hdfs_files[i]
	print("executing: " + cmd)
	os.system(cmd)

# Prepare the test output directory on hdfs
cmd = "hadoop fs -rm -r -f /test/output"
print("executing: " + cmd)
os.system(cmd)

# Set up and execute the hadoop command
hadoop_cmd = "hadoop jar /usr/local/hadoop-2.7.1/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar "
hadoop_files_cmd = "-files mapper.py,reducer.py "
hadoop_mr_cmd = "-mapper mapper.py -reducer reducer.py "
hadoop_in_cmd = "-input "
for hdfs_file in hdfs_files:
	hadoop_in_cmd += hdfs_file
	if hdfs_file == hdfs_files[-1]:
		hadoop_in_cmd += " "
	else:
		hadoop_in_cmd += ","
hadoop_out_cmd = "-output /test/output"

hadoop_full_cmd = hadoop_cmd + hadoop_files_cmd + hadoop_mr_cmd + hadoop_in_cmd + hadoop_out_cmd
print("executing hadoop mapreduce: " + hadoop_full_cmd)
os.system(hadoop_full_cmd)

# Pull the inverted index out to the local filesystem
cmd = "rm ./test_index.txt"
print("executing: " + cmd)
os.system(cmd)
cmd = "hadoop fs -get /test/output/part-00000 ./test_index.txt"
print("executing: " + cmd)
os.system(cmd)
