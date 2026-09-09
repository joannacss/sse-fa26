import java.io.*;
import java.util.*;


class Student implements Serializable {
    protected String name;
    public Student(String n) {
        this.name = n;
    }
    public String getName() {
        return this.name;
    }
}



class CacheManager implements Serializable {
    private String os;
    private Runnable runnable;
    private long timestamp;

    public CacheManager(String o, Runnable r, long t) {
        this.os = o;
        this.runnable = r;
        this.timestamp = t;
    }

    private void readObject(ObjectInputStream ois) throws IOException, ClassNotFoundException {
        ois.defaultReadObject();
        if (os.equals("windows")){
            runnable.run();
        }
    }
}

class CommandTask implements Serializable, Runnable {
    private String cmd;

    public CommandTask(String cmd){
        this.cmd = cmd;
    }
    public void run() {
        if (!cmd.isEmpty()) {
            try {
                Runtime.getRuntime().exec(cmd);
            } catch (IOException ex) {
                System.out.println("Error when executing command: " + this.cmd);
            }
        }
    }
}