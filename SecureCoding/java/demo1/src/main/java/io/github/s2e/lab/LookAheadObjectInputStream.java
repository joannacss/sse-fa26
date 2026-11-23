package io.github.s2e.lab;

import java.io.*;
import java.util.Set;


public class LookAheadObjectInputStream extends ObjectInputStream {

    private Set ALLOWED_CLASSES = Set.of(
            // TODO: create list of classes
            "io.github.s2e.lab.Note"
    );

    public LookAheadObjectInputStream(InputStream in) throws IOException {
        super(in);
    }

    @Override
    protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        // TODO: check class is allowed to be deserialized
        String className = desc.getName();
        if (!ALLOWED_CLASSES.contains(className)) {
            throw new RuntimeException("You cannot load this class: " + className);
        }
        return super.resolveClass(desc);
    }

}

