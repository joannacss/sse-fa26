import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.*;
import com.ibm.wala.ipa.callgraph.cha.CHACallGraph;
import com.ibm.wala.ipa.callgraph.impl.Util;
import com.ibm.wala.ipa.callgraph.propagation.InstanceKey;
import com.ibm.wala.ipa.callgraph.propagation.SSAPropagationCallGraphBuilder;
import com.ibm.wala.ipa.cha.ClassHierarchy;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.config.FileOfClasses;

import java.io.File;
import java.io.FileInputStream;
import java.util.Collection;
import java.util.jar.JarFile;
import java.util.jar.JarOutputStream;

/**
 * Example coded in class - Lecture 14.
 * Walked through WALA's main data structures and how to create call graphs.
 *
 * @author Joanna C. S. Santos
 */
public class LiveExample1 {

    private static boolean isApplicationNode(CGNode node) {
        return node.getMethod().getDeclaringClass().getClassLoader().getReference().equals(ClassLoaderReference.Application);
    }
    public static void printCallGraph(CallGraph cg, String callgraphName) {
        System.out.println("================ " + callgraphName + " call graph ===================");
        System.out.println(CallGraphStats.getStats(cg));
        System.out.println("Call Graph (application scope only): ");
        for (CGNode n : cg) {

            if (!isApplicationNode(n)) continue;
            cg.getSuccNodes(n).forEachRemaining(next -> {
                System.out.print("\"" + n.getMethod().getSignature() + "\"");
                System.out.println(" -> \"" + next.getMethod().getSignature() + "\"");
            });
            System.out.println("");

        }
        System.out.println("===================================================");
    }


    public static void main(String[] args) throws Exception {
        // TODO: create the analysis scope to analyze the Example1.jar (print at the end)
        AnalysisScope scope = AnalysisScope.createJavaAnalysisScope();
        String appPath = LiveExample1.class.getResource("Example1.jar").getPath();
        scope.addToScope(ClassLoaderReference.Application, new JarFile(appPath));
        String jrePath = LiveExample1.class.getResource("jdk-17.0.1/rt.jar").getPath();
        scope.addToScope(ClassLoaderReference.Primordial, new JarFile(jrePath));
        String exclusionsPath = LiveExample1.class.getResource("Java60RegressionExclusions.txt").getPath();
        scope.setExclusions(new FileOfClasses(new FileInputStream(exclusionsPath)));
        System.out.println(scope);

        // TODO: create the class hierarchy
        IClassHierarchy ch = ClassHierarchyFactory.make(scope);




        // TODO: print the number of classes in the class hierarchy
        System.out.println(ch.getNumberOfClasses());



        // TODO: iterate over the class hierarchy and print the classes in the application scope
        for (IClass c: ch){
            if(c.getClassLoader().getReference().equals(ClassLoaderReference.Application)){
                System.out.println(c.getName());
            }
        }

        // TODO: compute entrypoint methods
        Iterable<Entrypoint> entrypoints = Util.makeMainEntrypoints(scope, ch);

        // TODO: create the CHA call graph
        CHACallGraph chaCallGraph = new CHACallGraph(ch, true);
//        chaCallGraph.init(entrypoints);
//        printCallGraph(chaCallGraph, "CHA");


        // TODO: create the RTA call graph
        AnalysisCacheImpl cache = new AnalysisCacheImpl();
        AnalysisOptions options = new AnalysisOptions();
        options.setEntrypoints(entrypoints);
        options.setAnalysisScope(scope);
        CallGraphBuilder<InstanceKey> rtaBuilder = Util.makeRTABuilder(options, cache, ch, scope);
//        CallGraph rtaCg = rtaBuilder.makeCallGraph(options, null);
//        System.out.println(rtaCg.getNumberOfNodes());
//        printCallGraph(rtaCg, "RTA");

        // TODO: create the 1-CFA call graph
        SSAPropagationCallGraphBuilder nCfaBuilder = Util.makeNCFABuilder(1, options, cache, ch, scope);
        CallGraph oneCfaCg = nCfaBuilder.makeCallGraph(options, null);
        System.out.println(oneCfaCg.getNumberOfNodes());

        // TODO: print the IR of the main method
        CGNode mainNode = oneCfaCg.getEntrypointNodes().iterator().next();
        IMethod method = mainNode.getMethod();
        IR ir = mainNode.getIR();
        Context context = mainNode.getContext();
        System.out.println(ir);


        // TODO: getting the CFG of a CG node

    }
}
