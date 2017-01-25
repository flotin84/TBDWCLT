import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class TempTestDriver {

	public static void main(String args[])
	{
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
