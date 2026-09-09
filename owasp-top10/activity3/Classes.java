package vulnerable;

import java.io.*;
import java.util.*;


class Config implements Serializable {
    private String page;
    public void readObject(ObjectInputStream ois) throws IOException, ClassNotFoundException {
        Runtime.getRuntime().exec("open http://localhost:/" + page);
    }
}
class CacheManager implements Serializable {

    private Runnable task;
    private Runnable[] taskArray;
    private List<Runnable> taskList;
    private Set<Runnable> taskSet;
    private Map<String, Runnable> taskMap;
    private String os;
    private long timestamp;

    public void readObject(ObjectInputStream ois) throws IOException, ClassNotFoundException {
        ois.defaultReadObject();
        Runnable r;
        if (os.equals("windows") && task instanceof CommandTask) {
            r = getInitHook(); r.run();
        }else {
            r = getFromArray(); r.run();
            r = getFromList(); r.run();
            r = getFromSet(); r.run();
            r = getFromMap(); r.run();
        }
    }

    Runnable getInitHook(){ return task; }

    Runnable getFromArray() { return taskArray[0]; }

    Runnable getFromList() { return taskList.get(0); }

    Runnable getFromSet() { return taskSet.iterator().next(); }

    Runnable getFromMap() { return taskMap.get("xyz"); }
}

class CommandTask implements Runnable, Serializable {

    private String command;
    private TaskExecutor taskExecutor;

    public CommandTask(String command, TaskExecutor taskExecutor) {
        this.command = command;
        this.taskExecutor = taskExecutor;
    }

    private CommandTask() {

    }


    @Override 
    public void run() {
        if (!command.isEmpty() && taskExecutor != null) {
            taskExecutor.executeCmd(command);
        }
    }
}

class TaskExecutor implements Serializable {

    public void executeCmd(String cmd) {
        try { Runtime.getRuntime().exec(cmd); }
        catch (IOException e) { }
    }
}