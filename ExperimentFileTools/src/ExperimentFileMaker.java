import java.io.*;
import java.util.*;

public class ExperimentFileMaker {
	public static void main(String[] args) {
		// Inputs
		int NumberOfNodes = 3;
		String experimentFileName = "TestExperimentFile";
		String[] names = new String[NumberOfNodes];
		String[] logs = new String[NumberOfNodes];
		String[] binary = new String[NumberOfNodes];
		
		// Hardcoded test values
		names[0] = "node1";
		names[1] = "node2";
		names[2] = "node3";
		String file = "TestFile.txt";
		String binaryfile = "TestFileBinary.txt";
		logs[0] = file;
		logs[1] = file;
		logs[2] = file;
		binary[0] = binaryfile;
		binary[1] = binaryfile;
		binary[2] = binaryfile;
		
		try {
			FileWriter writer = new FileWriter(experimentFileName, true);
			//PrintWriter writer = new PrintWriter(new FileWriter("TestExperimentFile", true));
			int i;
			for (i = 0; i < NumberOfNodes; i++) {
				writer.write(names[i] + ' ');
			}
			
			for (i = 0; i < NumberOfNodes; i++) {
				writer.write('\n');
				// log
				File log = new File(file);
				writer.write(names[i] + " log " + log.length() + '\n');
				Scanner temp = new Scanner(log);
				while (temp.hasNext()) {
					writer.write(temp.next());
				}
				
				writer.write('\n');
				
				// binary
				File binarytest = new File(binaryfile);
				writer.write(names[i] + " binary " + binarytest.length() + '\n');
				temp = new Scanner(binarytest);
				while (temp.hasNext()) {
					writer.write(temp.next());
				}
			}
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}


/*
name1 name2 name3
name1 log length
-logfile-
name1 binary length
-binaryfile-
name2 log length
-logfile-
name2 binary length
-binaryfile-
name3 log length
-logfile-
name3 binary length
-binaryfile-
*/