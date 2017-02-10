import java.io.*;
import java.util.*;
import java.util.zip.*;

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
		String file = "target";
		String binaryfile = "Sinusoid.BIN";
		logs[0] = file;
		logs[1] = file;
		logs[2] = file;
		binary[0] = binaryfile;
		binary[1] = binaryfile;
		binary[2] = binaryfile;
		
		StringBuilder sb = new StringBuilder();
		
		try {
			//FileWriter writer = new FileWriter(experimentFileName);
			int i;
			for (i = 0; i < NumberOfNodes; i++) {
				sb.append(names[i] + ' ');
				//writer.write(names[i] + ' ');
			}
			
			for (i = 0; i < NumberOfNodes; i++) {
				sb.append('\n');
				//writer.write('\n');
				// log
				File log = new File(file);
				sb.append(names[i] + " log " + log.length() + '\n');
				//writer.write(names[i] + " log " + log.length() + '\n');
				Scanner temp = new Scanner(log);
				while (temp.hasNext()) {
					sb.append(temp.next());
					//writer.write(temp.next());
				}
				sb.append('\n');
				//writer.write('\n');
				
				// binary
				File binarytest = new File(binaryfile);
				sb.append(names[i] + " binary " + binarytest.length() + '\n');
				//writer.write(names[i] + " binary " + binarytest.length() + '\n');
				temp = new Scanner(binarytest);
				while (temp.hasNext()) {
					sb.append(temp.next());
					//writer.write(temp.next());
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		// Zip the file
		try {
			File f = new File("TestExperimentFile.zip");
			ZipOutputStream out = new ZipOutputStream(new FileOutputStream(f));
			ZipEntry e = new ZipEntry("TestExperimentFile.txt");
			out.putNextEntry(e);
	
			byte[] data = sb.toString().getBytes();
			out.write(data, 0, data.length);
				out.closeEntry();
	
			out.close();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
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