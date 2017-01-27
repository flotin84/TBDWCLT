import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class TempTestDriver {

	public static void main(String args[])
	{
		String filePath = "C:\\Users\\JRC\\TestExperimentFiles\\file_example.txt";
		String[] wrongFiles = {"C:\\Users\\JRC\\TestExperimentFiles\\file_example2.txt","C:\\Users\\JRC\\TestExperimentFiles\\file_example3.txt","C:\\Users\\JRC\\TestExperimentFiles\\file_example4.txt"};
		try {			
			BufferedReader in = new BufferedReader(new FileReader(filePath));
			ExperimentFileReader.findNodeFile(in,1,false);
			System.out.println( in.readLine() );
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
	}
}
