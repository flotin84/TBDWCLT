/*
 * Store information about node
 */

public class Node {
	private String binPath;
	private String logPath;
	private String name;

	
	/**
	 * 
	 * @param name string name valid chars 0-9a-zA-Z_
	 * @param logPath path to log file
	 * @param binPath path to bin file
	 */
	Node(String name, String logPath, String binPath)
	{
		this.name = name;//TODO:validity check
		this.binPath = binPath;
		this.logPath = logPath;
	}

	public String getBinPath() {
		return binPath;
	}

	public String getLogPath() {
		return logPath;
	}

	public String getName() {
		return name;
	}
	
}
