import java.io.*;
import java.util.*;


// Compile and run: javac *.java && java Main <filename>     
public class Main {

    public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException {
        FileInputStream fs = new FileInputStream(args[0] ="object2.txt");
        ObjectInputStream objIn = new ObjectInputStream(fs);
        Student obj = (Student) objIn.readObject();

        System.out.println("Read student " + obj.getName());
    }
}

