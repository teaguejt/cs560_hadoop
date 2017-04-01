/*package edu.tj_hadoop;*/

import java.io.*;
import java.util.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

public class StopWords extends Configured implements Tool {

	public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, IntWritable> {
		static enum counters {INPUT};
		private final static IntWritable One = new IntWritable(1);
		private Text word = new Text();
		private long records = 0;
		int lineno = 0;
		private String inFile;
		
		public void configure(JobConf job) {
			inFile = job.get("map.input.file");
		}

		public void map(LongWritable key, Text val, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
			lineno++;
			String line = val.toString().toLowerCase();
			/* Strip punctuation from the string */
			String strippedline = line.replaceAll("[(\\[\\]){},.;:!?<>%]", "");
			
			System.out.printf("line %d: %s%n", lineno, strippedline);
		}
	}

	public static class Reduce extends MapReduceBase implements Reducer<Text, IntWritable, Text, IntWritable> {
		public void reduce(Text key, Iterator<IntWritable> values, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
		}
	}

	public int run(String [] args) throws Exception {
		JobConf conf = new JobConf(getConf(), StopWords.class);
		conf.setJobName("stopwords");
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(IntWritable.class);
		conf.setMapperClass(Map.class);
		conf.setCombinerClass(Reduce.class);
		conf.setReducerClass(Reduce.class);
		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);

		List<String> other_args = new ArrayList<String>();
		FileInputFormat.setInputPaths(conf, new Path("/test/works_of_william.txt"));
		FileOutputFormat.setOutputPath(conf, new Path("/test/stop_words.txt"));

		JobClient.runJob(conf);
		return 0;
	}

	public static void main(String [] args) throws Exception {
		int res = ToolRunner.run(new Configuration(), new StopWords(), args);
		System.exit(res);
	}
}
