import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class TempTestDriver {

	public static void main(String args[])
	{
		ArrayList<Node> nodes = new ArrayList();
	
		Node test = new Node("bob","path","path2");
		nodes.add(test);
		
		System.out.println(test.getBinPath());
		System.out.println(test.getLogPath());
		System.out.println(test.getName());

		
		String filePath = "C:\\Users\\JRC\\TestExperimentFiles\\file_example.txt";
		String[] wrongFiles = {"C:\\Users\\JRC\\TestExperimentFiles\\file_example2.txt","C:\\Users\\JRC\\TestExperimentFiles\\file_example3.txt","C:\\Users\\JRC\\TestExperimentFiles\\file_example4.txt"};
		try {
			ExperimentFile testFile = new ExperimentFile(filePath);
			System.out.println(testFile.getNodeNames());
			System.out.println(testFile.getNumberOfNodes());
			testFile = new ExperimentFile(wrongFiles[2]);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
	}
}
