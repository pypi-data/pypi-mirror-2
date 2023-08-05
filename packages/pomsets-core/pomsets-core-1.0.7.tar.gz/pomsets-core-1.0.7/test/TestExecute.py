from __future__ import with_statement

import os
import sys
import threadpool
import unittest
import logging
import shutil

import currypy
import pypatterns.command as CommandPatternModule

import cloudpool as CloudModule
import cloudpool.shell as ShellModule

import pypatterns.filter as FilterModule

import pomsets.automaton as AutomatonModule
import pomsets.builder as BuilderModule
import pomsets.command as TaskCommandModule
import pomsets.definition as DefinitionModule
import pomsets.error as ErrorModule
import pomsets.parameter as ParameterModule
import pomsets.task as TaskModule

import pomsets.test_utils as GeneratePomsetsModule




def createEchoDefinition():
    command = ['/bin/echo']
    executable = TaskCommandModule.Executable()
    executable.stageable(False)
    executable.path(command)
    executable.staticArgs([])
    
    definition = DefinitionModule.createShellProcessDefinition(
        inputParameters = {
            'item to echo':{ParameterModule.PORT_ATTRIBUTE_COMMANDLINE:True}
            },
        parameterOrderings = None,
        executable = executable
    )
    definition.name('echo')
    return definition

DEFINITION_ECHO = createEchoDefinition()

DEFINITION_WORDCOUNT = GeneratePomsetsModule.createWordCountDefinition()

DEFINITION_WORDCOUNT_REDUCE = GeneratePomsetsModule.createWordCountReduceDefinition()




class BaseTestClass(object):

    def setUp(self):
        automaton = AutomatonModule.Automaton()
        automaton.setThreadPool(
            None, 
            CloudModule.Pool(self.getNumWorkersToInstantiate()))
        automaton.commandManager(CommandPatternModule.CommandManager())
        self.automaton = automaton

        builder = BuilderModule.Builder()
        self.builder = builder

        return


    def tearDown(self):
        return

    def getNumWorkersToInstantiate(self):
        return 1

    def createCommandBuilderMap(self):
        commandBuilder = TaskCommandModule.CommandBuilder(
            TaskCommandModule.buildCommandFunction_commandlineArgs
        )
        commandBuilderMap = {
            'shell process':commandBuilder,
            'print task':commandBuilder
        }
        return commandBuilderMap

    def createExecuteEnvironmentMap(self):
        return {
            'shell process':ShellModule.LocalShell()
            }


    def getRequestContext(self, task=None, executeEnvironmentMap=None):
        
        automaton = self.automaton
        commandBuilderMap = self.createCommandBuilderMap()

        if executeEnvironmentMap is None:
            executeEnvironmentMap = self.createExecuteEnvironmentMap()

        requestContext = {
            'task':task,
            'command builder map':commandBuilderMap,
            'execute environment map':executeEnvironmentMap
        }
        
        return requestContext
    
    
    def executeTask(self, task, 
                    executeEnvironmentMap=None):
            
        automaton = self.automaton
        successCallback = automaton.getPostExecuteCallbackFor(task)
        errorCallback = automaton.getErrorCallbackFor(task)
        executeTaskFunction = automaton.getExecuteTaskFunction(task)
        
        requestContext = self.getRequestContext(
            task=task, executeEnvironmentMap=executeEnvironmentMap
        )

        request = threadpool.WorkRequest(
            executeTaskFunction,
            args = [],
            kwds = requestContext,
            callback = successCallback,
            exc_callback = errorCallback
        )

        threadPool = automaton.getThreadPoolUsingRequest(request)
        request.kwds['thread pool'] = threadPool
        
        task.workRequest(request)

        task.automaton(self.automaton)

        threadPool.putRequest(request)
        threadPool.wait()

        return request

    def assertPreExecute(self):
        return

    def assertPostExecute(self):
        task = self.request.kwds['task']
        if isinstance(task, TaskModule.CompositeTask):
            childTasks = [x for x in task.getErroredChildTasks()]
            assert not self.request.exception, childTasks[0].workRequest().kwds['exception stack trace']
        else:
            assert not self.request.exception

        return

    def createTask(self, reference):
        
        definitionToReference = reference.definitionToReference()
        if definitionToReference.isAtomic():
            task = TaskModule.AtomicTask()
            task.definition(reference)
            return task

        task = TaskModule.CompositeTask()
        task.definition(reference)
        taskGenerator = TaskModule.NestTaskGenerator()
        task.taskGenerator(taskGenerator)
        return task


    def bindTaskParameterValues(self, task):
        return

    def testExecute1(self):

        self.assertPreExecute()

        definition = self.createDefinition()

        reference = DefinitionModule.ReferenceDefinition()
        reference.definitionToReference(definition)
        reference.name(definition.name())

        task = self.createTask(reference)
        self.bindTaskParameterValues(task)

        request = self.executeTask(task)

        self.request = request

        self.assertPostExecute()

        return 


    def testExecute2(self):

        self.assertPreExecute()

        definition = self.createDefinition()
        reference = DefinitionModule.ReferenceDefinition()
        reference.definitionToReference(definition)
        reference.name(definition.name())

        reference = GeneratePomsetsModule.pickleAndReloadDefinition(
            '.'.join([self.getPicklePath(), 'pomset']),
            reference
        )

        task = self.createTask(reference)
        self.bindTaskParameterValues(task)

        request = self.executeTask(task)
        self.request = request

        self.assertPostExecute()
        return 


    def getPicklePath(self):
        return os.path.sep + os.path.join(
            'tmp', '.'.join([self.__class__.__module__,
                             self.__class__.__module__,
                             'pickle.pomset']))

    
    # END class BaseTestClass
    pass


class TestCase1(BaseTestClass, unittest.TestCase):
    """
    execute of atomic function
    """

    def createDefinition(self):
        return DEFINITION_ECHO

    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['foo'])
        return
    

    # END TestCase1
    pass


class TestCase2(BaseTestClass, unittest.TestCase):
    """
    execute of atomic function
    """

    def createDefinition(self):
        definition = DEFINITION_ECHO
        return definition

    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['"echoed testExecuteAtomicFunction2"'])
        return


    # END class TestCase2
    pass


class TestCase4(BaseTestClass, unittest.TestCase):
    """
    execute of composite function
    """

    def createDefinition(self):
        atomicDefinition = DEFINITION_ECHO

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        compositeDefinition.addParameter(parameter)
        
        node = compositeDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('echo')

        compositeDefinition._connectParameters(
            compositeDefinition, 'item to echo',
            node, 'item to echo'
        )
        return compositeDefinition

    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['foo'])
        return


    # END class TestCase4
    pass



    

class TestCase8(BaseTestClass, unittest.TestCase):
    """
    execute of composite function
    """

    def createDefinition(self):
        atomicDefinition = DEFINITION_ECHO

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        compositeDefinition.addParameter(parameter)
        
        for index in range(3):
            node = compositeDefinition.createNode(id='node%s' % index)
            node.definitionToReference(atomicDefinition)
            compositeDefinition._connectParameters(
                compositeDefinition, 'item to echo',
                node, 'item to echo'
            )
            node.name('echo %s' % index)

        return compositeDefinition


    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['foo'])
        return


    # END class TestCase8
    pass


class TestCase9(BaseTestClass, unittest.TestCase):
    """
    execute of composite function
    """

    def createDefinition(self):
        atomicDefinition = DEFINITION_ECHO

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        compositeDefinition.addParameter(parameter)

        nodes = []
        for index in range(3):
            node = compositeDefinition.createNode(id='node%s' % index)
            node.definitionToReference(atomicDefinition)
            compositeDefinition._connectParameters(
                compositeDefinition, 'item to echo',
                node, 'item to echo'
            )
            node.name('echo %s' % index)
            nodes.append(node)
            pass

        for sourceNode, targetNode in zip(nodes[:-1], nodes[1:]):
            compositeDefinition.connectNodes(
                sourceNode, 'temporal output',
                targetNode, 'temporal input'
            )
            pass
        return compositeDefinition

    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['foo'])
        return


    # END class TestCase9
    pass

    
class TestCase10(BaseTestClass, unittest.TestCase):
    """
    execution fails due to incomplete parameter binding 
    """

    def createDefinition(self):
        atomicDefinition = DEFINITION_ECHO

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        compositeDefinition.addParameter(parameter)
        
        node = compositeDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('echo')

        return compositeDefinition


    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['foo'])
        return


    def assertPostExecute(self):
        request = self.request
        assert request.exception
        return

    # END class TestCase10
    pass


class TestCase11(TestCase1):
    """
    execute of atomic function
    """

    def getNumWorkersToInstantiate(self):
        return 0

    
    def executeTask(self, task, 
                    executeEnvironmentMap=None):

        automaton = self.automaton
        successCallback = automaton.getPostExecuteCallbackFor(task)
        errorCallback = automaton.getErrorCallbackFor(task)
        executeTaskFunction = automaton.getExecuteTaskFunction(task)
        
        requestContext = self.getRequestContext(
            task=task, executeEnvironmentMap=executeEnvironmentMap
        )
        request = threadpool.WorkRequest(
            executeTaskFunction,
            args = [],
            kwds = requestContext,
            callback = successCallback,
            exc_callback = errorCallback
        )

        try:
            automaton.enqueueRequest(request)
            assert False
        except ErrorModule.ExecutionError, e:
            self.assertEquals('need to start thread before execution',
                              str(e))

        return request



    # END TestCase11
    pass


class TestCase12(BaseTestClass, unittest.TestCase):

    def createDefinition(self):
        atomicDefinition = DEFINITION_ECHO
        nestDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        nestDefinition.addParameter(parameter)
        
        node = nestDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('echo')

        nestDefinition._connectParameters(
            nestDefinition, 'item to echo',
            node, 'item to echo'
        )

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        node = compositeDefinition.createNode(id='nest')
        node.definitionToReference(nestDefinition)

        node.setParameterBinding('item to echo', ['foo'])

        return compositeDefinition


    # END class TestCase12
    pass


class TestCase13(BaseTestClass, unittest.TestCase):

    def createDefinition(self):
        atomicDefinition = DEFINITION_ECHO
        nestDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        nestDefinition.addParameter(parameter)
        
        node = nestDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('echo')

        nestDefinition._connectParameters(
            nestDefinition, 'item to echo',
            node, 'item to echo'
        )

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        compositeDefinition.addParameter(parameter)

        node = compositeDefinition.createNode(id='nest')
        node.definitionToReference(nestDefinition)

        compositeDefinition._connectParameters(
            compositeDefinition, 'item to echo',
            node, 'item to echo'
        )

        return compositeDefinition


    def bindTaskParameterValues(self, task):
        task.setParameterBinding('item to echo', ['foo'])
        return


    # END class TestCase13
    pass
    

class TestParameterSweep1(BaseTestClass, unittest.TestCase):
    

    def createDefinition(self):

        atomicDefinition = DEFINITION_ECHO

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        node = compositeDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('echo')
        
        parameter = ParameterModule.DataParameter(
            id='item to echo', 
            portDirection=ParameterModule.PORT_DIRECTION_INPUT)
        parameter.setAttribute(ParameterModule.PORT_ATTRIBUTE_PARAMETERSWEEP, True)
        compositeDefinition.addParameter(parameter)
        node.isParameterSweep('item to echo', True)
        
        compositeDefinition._connectParameters(
            compositeDefinition, 'item to echo',
            node, 'item to echo'
        )

        return compositeDefinition

    def bindTaskParameterValues(self, task):
        task.setParameterBinding(
            'item to echo', 
            ['"echoed %s : 1"' % self.__class__.__name__,
             '"echoed %s : 2"' % self.__class__.__name__])
        return


    # END class TestParameterSweep1
    pass

    
class TestParameterSweep2(BaseTestClass, unittest.TestCase):

    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestExecute')
    OUTPUT_DIR = os.path.sep + 'tmp'
    
    INPUT_FILES = ['text1', 'text2']
    OUTPUT_FILES = ['count1', 'count2']
    
    def removeFile(self, file):
        try:
            os.remove(file)
        except OSError:
            pass
        return
    
    def fileExists(self, file):
        return os.path.exists(file)
    
    def setUp(self):
        BaseTestClass.setUp(self)

        # ensure that the script and the text files exist
        # remove the $BASE_DIR/count* files
        self.inputFiles = [
            os.path.join(x, y)
            for x,y in zip([TestParameterSweep2.BASE_DIR]*len(TestParameterSweep2.INPUT_FILES), 
                           TestParameterSweep2.INPUT_FILES)
        ]
        self.outputFiles = [
            os.path.join(x, y)
            for x,y in zip([TestParameterSweep2.OUTPUT_DIR]*len(TestParameterSweep2.OUTPUT_FILES), 
                           TestParameterSweep2.OUTPUT_FILES)
        ]
        
        for outputFile in self.outputFiles:
            self.removeFile(outputFile)
            pass
        
        return
    

    def tearDown(self):

        BaseTestClass.tearDown(self)
        
        self.removeFiles()
        return

    
    def removeFiles(self):
        
        # remove the $BASE_DIR/count* files
        for outputFile in self.outputFiles:
            self.removeFile(outputFile)
            pass
        return

    

    def createDefinition(self):
        atomicDefinition = DEFINITION_WORDCOUNT

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        node = compositeDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('mapper')

        # TODO:
        # the info to expose the parameters on the composite definition
        # should be retrieved from the definition itself
        parameterGroup = {
            'input file':{ParameterModule.PORT_ATTRIBUTE_PARAMETERSWEEP:True}, 
            'output file':{
                ParameterModule.PORT_ATTRIBUTE_PARAMETERSWEEP:True,
                ParameterModule.PORT_ATTRIBUTE_ISSIDEEFFECT:True
            }
        }
        for parameterId, attributes in parameterGroup.iteritems():
            parameter = ParameterModule.DataParameter(
                id=parameterId, 
                portDirection=ParameterModule.PORT_DIRECTION_INPUT)
            for attributeKey, attributeValue in attributes.iteritems():
                parameter.setAttribute(attributeKey, attributeValue)
                pass
            
            compositeDefinition.addParameter(parameter)
            node.isParameterSweep(parameterId, True)
        
            compositeDefinition._connectParameters(
                compositeDefinition, parameterId,
                node, parameterId
            )
            pass
        node.addParameterSweepGroup(parameterGroup.keys())

        return compositeDefinition

    def bindTaskParameterValues(self, task):
        task.setParameterBinding(
            'input file',
            self.inputFiles
        )
        task.setParameterBinding(
            'output file',
            self.outputFiles
        )
        return

        
    def assertPreExecute(self):
        BaseTestClass.assertPreExecute(self)
        
        # assert that the files do not exist
        for inputFile in self.inputFiles:
            assert self.fileExists(inputFile), \
                'expected inputFile %s to exist' % inputFile
            pass
        
        for outputFile in self.outputFiles:
            assert not self.fileExists(outputFile), \
                'expected outputFile %s to not exist' % outputFile
        
        pass


    def assertPostExecute(self):
        BaseTestClass.assertPostExecute(self)

        # assert that the files exist
        for outputFile in self.outputFiles:
            assert self.fileExists(outputFile), \
                'expected output file %s to exist' % outputFile
            pass
        
        return 

    
    # END class TestParameterSweep2
    pass


class TestParameterSweep3(BaseTestClass, unittest.TestCase):
    
    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestExecute')
    OUTPUT_DIR = os.path.sep + 'tmp'
    
    INPUT_FILES = ['count1', 'count2']
    OUTPUT_FILES = ['count_reduce']
    
    def removeFile(self, file):
        try:
            os.remove(file)
        except OSError:
            pass
        return
    
    def fileExists(self, file):
        return os.path.exists(file)
    
    
    def setUp(self):
        BaseTestClass.setUp(self)

        # ensure that the script and the text files exist
        # remove the $BASE_DIR/count* files
        self.inputFiles = [
            os.path.join(x, y) 
            for x,y in zip([TestParameterSweep3.BASE_DIR]*len(TestParameterSweep3.INPUT_FILES), 
                           TestParameterSweep3.INPUT_FILES)
        ]
        self.outputFiles = [
            os.path.join(x, y)
            for x,y in zip([TestParameterSweep3.OUTPUT_DIR]*len(TestParameterSweep3.OUTPUT_FILES), 
                           TestParameterSweep3.OUTPUT_FILES)
        ]
        
        for outputFile in self.outputFiles:
            self.removeFile(outputFile)
            pass
        
        return
    
    def tearDown(self):
        
        BaseTestClass.tearDown(self)
        self.removeFiles()
        return
    
    def removeFiles(self):
        # remove the $BASE_DIR/count* files
        for outputFile in self.outputFiles:
            self.removeFile(outputFile)
            pass
        
        return
    


    def createDefinition(self):
            
        atomicDefinition = DEFINITION_WORDCOUNT_REDUCE

        compositeDefinition = DefinitionModule.getNewNestDefinition()
        node = compositeDefinition.createNode(id='node')
        node.definitionToReference(atomicDefinition)
        node.name('reducer')

        parameterIds = ['input files', 'output file']
        for parameterId  in parameterIds:
            parameter = ParameterModule.DataParameter(
                id=parameterId, 
                portDirection=ParameterModule.PORT_DIRECTION_INPUT)
            compositeDefinition.addParameter(parameter)
        
            compositeDefinition._connectParameters(
                compositeDefinition, parameterId,
                node, parameterId
            )
            pass

        return compositeDefinition

    def bindTaskParameterValues(self, task):
        task.setParameterBinding(
            'input files',
            self.inputFiles
        )
        task.setParameterBinding(
            'output file',
            self.outputFiles
        )
        return

    def assertPreExecute(self):

        BaseTestClass.assertPreExecute(self)

        for inputFile in self.inputFiles:
            assert self.fileExists(inputFile), 'expected inputFile %s to exist' % inputFile
            pass
        
        
        for outputFile in self.outputFiles:
            assert not self.fileExists(outputFile), 'expected outputFile %s to not exist' % outputFile
            
            
        return


    def assertPostExecute(self):
        BaseTestClass.assertPostExecute(self)

        # assert that the files exist
        for outputFile in self.outputFiles:
            assert self.fileExists(outputFile), 'expected output file %s to exist' % outputFile
            pass
        
        return 

    # END class TestParameterSweep3
    pass


class TestParameterSweep4(BaseTestClass, unittest.TestCase):
    """
    tests combining a mapper with a reducer
    """
    
    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestExecute')
    TEST_DIR = os.path.sep + 'tmp'
    
    INPUT_FILES = ['text1', 'text2']
    INTERMEDIATE_FILES = ['count1', 'count2']
    OUTPUT_FILES = ['count_reduce']

    def removeFile(self, file):
        try:
            os.remove(file)
        except OSError:
            pass
        return
    
    def fileExists(self, file):
        return os.path.exists(file)
    
    
    def setUp(self):

        BaseTestClass.setUp(self)

        # ensure that the script and the text files exist
        # remove the $BASE_DIR/count* files
        self.inputFiles = [
            os.path.join(x, y)
            for x,y in zip([TestParameterSweep4.BASE_DIR]*len(TestParameterSweep4.INPUT_FILES), 
                           TestParameterSweep4.INPUT_FILES)
        ]
        self.intermediateFiles = [
            os.path.join(x, y)
            for x,y in zip([TestParameterSweep4.TEST_DIR]*len(TestParameterSweep4.INTERMEDIATE_FILES), 
                           TestParameterSweep4.INTERMEDIATE_FILES)
        ]
        self.outputFiles = [
            os.path.join(x, y)
            for x,y in zip([TestParameterSweep4.TEST_DIR]*len(TestParameterSweep4.OUTPUT_FILES), 
                           TestParameterSweep4.OUTPUT_FILES)
        ]
        
        for outputFile in self.outputFiles+self.intermediateFiles:
            self.removeFile(outputFile)
            pass
        
        return
    
    def tearDown(self):

        BaseTestClass.tearDown(self)
        self.removeFiles()
        return
    
    def removeFiles(self):
        # remove the $BASE_DIR/count* files
        for outputFile in self.outputFiles+self.intermediateFiles:
            self.removeFile(outputFile)
            pass
        
        return
    

    def createDefinition(self):
    
        compositeDefinition = DefinitionModule.getNewNestDefinition()

        # setup the reference definition for parameter sweep
        mapperNode = compositeDefinition.createNode(id='mapper')
        mapperNode.definitionToReference(DEFINITION_WORDCOUNT)
        mapperNode.isParameterSweep('input file', True)
        mapperNode.isParameterSweep('output file', True)
        mapperNode.addParameterSweepGroup(['input file', 'output file'])
        mapperNode.name('mapper')

        reducerNode = compositeDefinition.createNode(id='reducer')
        reducerNode.definitionToReference(DEFINITION_WORDCOUNT_REDUCE)
        reducerNode.name('reducer')

        self.builder.exposeNodeParameter(
            compositeDefinition, 'input file',
            mapperNode, 'input file',
            shouldCreate=True)

        self.builder.exposeNodeParameter(
            compositeDefinition, 'output file',
            reducerNode, 'output file',
            shouldCreate=True)

        self.builder.exposeNodeParameter(
            compositeDefinition, 'intermediate file',
            mapperNode, 'output file',
            shouldCreate=True)

        edge = self.builder.connect(
            compositeDefinition,
            mapperNode, 'output file',
            reducerNode, 'input files',
        )

        return compositeDefinition


    def bindTaskParameterValues(self, task):
        task.setParameterBinding(
            'input file',
            self.inputFiles
        )
        task.setParameterBinding(
            'output file',
            self.outputFiles
        )
        task.setParameterBinding(
            'intermediate file',
            self.intermediateFiles
        )

        return

    def assertPostExecute(self):
        BaseTestClass.assertPostExecute(self)
        
        # assert that the files exist
        for outputFile in self.outputFiles+self.intermediateFiles:
            assert self.fileExists(outputFile), 'expected output file %s to exist' % outputFile
            pass
        
        return
        
    # END class TestParameterSweep4
    pass


class BaseNestTestClass(object):

    ATOMIC_DEFINITION = DEFINITION_ECHO

    def createDefinitionWithEmptyNest(self):

        nestContext = self.builder.createNewNestPomset('nest')
        nestDefinition = nestContext.pomset()

        parentContext = self.builder.createNewNestPomset('parent')
        parentDefinition = parentContext.pomset()

        atomicNode1 = self.builder.createNewNode(
            parentDefinition,
            name='atomic node 1',
            definitionToReference=BaseNestTestClass.ATOMIC_DEFINITION)
        atomicNode2 = self.builder.createNewNode(
            parentDefinition,
            name='atomic node 2',
            definitionToReference=BaseNestTestClass.ATOMIC_DEFINITION)
        nestNode = self.builder.createNewNode(
            parentDefinition,
            name='nest node',
            definitionToReference=nestDefinition)

        self.builder.bindParameterValue(atomicNode1, 'item to echo', ['foo 1'])
        self.builder.bindParameterValue(atomicNode2, 'item to echo', ['foo 2'])

        return parentDefinition

    
    def createDefinitionWithNonEmptyNest(self):
        parentDefinition = self.createDefinitionWithEmptyNest()

        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]
        nestDefinition = nestNode.definitionToReference()

        atomicNode3 = self.builder.createNewNode(
            nestDefinition,
            name='atomic node 3',
            definitionToReference=BaseNestTestClass.ATOMIC_DEFINITION)

        self.builder.bindParameterValue(atomicNode3, 'item to echo', ['foo 3'])

        return parentDefinition

    # END BaseNestTestClass
    pass


class TestNest1(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            nestNode, 'temporal input')
        self.builder.connect(
            parentDefinition,
            nestNode, 'temporal output',
            atomicNode2, 'temporal input')

        return parentDefinition


    # END class TestNest1
    pass


class TestNest2(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            nestNode, 'temporal input')
        self.builder.connect(
            parentDefinition,
            nestNode, 'temporal output',
            atomicNode2, 'temporal input')

        return parentDefinition

    # END class TestNest2
    pass


class TestNest3(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            atomicNode2, 'temporal input')
        self.builder.connect(
            parentDefinition,
            nestNode, 'temporal output',
            atomicNode2, 'temporal input')

        return parentDefinition

    # END class TestNest3
    pass


class TestNest4(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            nestNode, 'temporal input')
        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output',
            atomicNode2, 'temporal input')

        return parentDefinition

    # END class TestNest4
    pass


class TestNest5(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            nestNode, 'temporal input')
        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output',
            atomicNode2, 'temporal input')
        self.builder.connect(
            parentDefinition,
            nestNode, 'temporal output',
            atomicNode2, 'temporal input')

        return parentDefinition

    # END class TestNest5
    pass

class TestNest6(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            nestNode, 'temporal input')
        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output',
            atomicNode2, 'temporal input')
        self.builder.connect(
            parentDefinition,
            atomicNode2, 'temporal output',
            nestNode, 'temporal input')

        return parentDefinition

    # END class TestNest6
    pass

class TestNest7(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            atomicNode1, 'temporal output', 
            nestNode, 'temporal input')
        self.builder.connect(
            parentDefinition,
            atomicNode2, 'temporal output',
            nestNode, 'temporal input')

        return parentDefinition

    # END class TestNest7
    pass


class TestNest8(BaseTestClass, BaseNestTestClass, unittest.TestCase):

    def createDefinition(self):
        parentDefinition = BaseNestTestClass.createDefinitionWithNonEmptyNest(self)
        
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 1']
        atomicNode1 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'atomic node 2']
        atomicNode2 = nodes[0]
        nodes = [x for x in parentDefinition.nodes() if x.name() == 'nest node']
        nestNode = nodes[0]

        self.builder.connect(
            parentDefinition,
            nestNode, 'temporal output', 
            atomicNode1, 'temporal input')
        self.builder.connect(
            parentDefinition,
            nestNode, 'temporal output',
            atomicNode2, 'temporal input')

        return parentDefinition

    # END class TestNest8
    pass



class TestLoop1(BaseTestClass, unittest.TestCase):
    
    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestExecute')

    FILE_PREFIX = os.path.sep + os.path.join('tmp', 'loop')
    INDEX_INITIAL = 0
    INDEX_FINAL = 5
    FILE_INITIAL = '%s%s' % (FILE_PREFIX, INDEX_INITIAL)
    FILE_FINAL = '%s%s' % (FILE_PREFIX, INDEX_FINAL)
    
    def fileExists(self, file):
        return os.path.exists(file)
    
    def removeFile(self, file):
        try:
            os.remove(file)
        except OSError:
            pass
        return
    
    def setUp(self):

        BaseTestClass.setUp(self)
        
        # ensure that INITIAL_FILE exists
        shutil.copyfile(os.path.join(TestLoop1.BASE_DIR, 'text1'), 
                        TestLoop1.FILE_INITIAL)
        
        return

    
    def tearDown(self):

        self.removeFiles()
        BaseTestClass.tearDown(self)
        return
      
    def removeFiles(self):
        # ensure that INITIAL_FILE no longer exists
        # ensure that created files no longer exist
        for index in range(TestLoop1.INDEX_INITIAL, TestLoop1.INDEX_FINAL+1):
            self.removeFile('%s%s' % (TestLoop1.FILE_PREFIX, index))
            pass
        return
    
    def createDefinition(self):
        definition = GeneratePomsetsModule.createPomsetContainingLoopDefinition()
        
        # GeneratePomsetsModule.bindLoopDefinitionParameters(definition)
        nodes = [x for x in definition.nodes() if x.id() == 'loop']
        loopNode = nodes[0]
    
        # set the parameter bindings on loopNode
        loopNode.setParameterBinding(
            DefinitionModule.LoopDefinition.PARAMETER_INITIAL_STATE, 
            TestLoop1.INDEX_INITIAL)
        loopNode.setParameterBinding(
            DefinitionModule.LoopDefinition.PARAMETER_CONTINUE_CONDITION,
            "lambda x: x<%s" % TestLoop1.INDEX_FINAL)
        loopNode.setParameterBinding(
            DefinitionModule.LoopDefinition.PARAMETER_STATE_TRANSITION,
            "lambda x: x+1")
        loopNode.setParameterBinding(
            DefinitionModule.LoopDefinition.PARAMETER_STATE_CONFIGURATION,
            # set the value of input file
            # set the value of output file
            [
                # for some reason
                # exec is missing
                # we we need to do this using multiple strings
                "childTask.setParameterBinding('input file', ['/tmp/loop' + str(parentTask.getParameterBinding(DefinitionModule.LoopDefinition.PARAMETER_STATE))])",
                "childTask.setParameterBinding('output file', ['/tmp/loop' + str(parentTask.getParameterBinding(DefinitionModule.LoopDefinition.PARAMETER_STATE)+1)])"
            ]
        )
        
        return definition

    
    def assertPostExecute(self):
        BaseTestClass.assertPostExecute(self)
        
        for index in range(TestLoop1.INDEX_INITIAL+1,
                           TestLoop1.INDEX_FINAL+1):
            assert self.fileExists('%s%s' % (TestLoop1.FILE_PREFIX, index))
        
        return
    
    
    # END class TestLoop1
    pass


class TestBranch1(BaseTestClass, unittest.TestCase):
    
    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestExecute')
    
    FILE_PREFIX = os.path.sep + os.path.join('tmp', 'branch')
    INDEX_INITIAL = 0
    INDEX_FINAL = 1
    FILE_INITIAL = '%s%s' % (FILE_PREFIX, INDEX_INITIAL)
    FILE_FINAL = '%s%s' % (FILE_PREFIX, INDEX_FINAL)
    
    def fileExists(self, file):
        return os.path.exists(file)
    
    def removeFile(self, file):
        try:
            os.remove(file)
        except OSError:
            pass
        return
    
    def setUp(self):

        BaseTestClass.setUp(self)
        
        # ensure that INITIAL_FILE exists
        shutil.copyfile(os.path.join(TestBranch1.BASE_DIR, 'text1'), 
                        TestBranch1.FILE_INITIAL)
        
        self.assertTrue(self.fileExists(TestBranch1.FILE_INITIAL))
        return

    
    def tearDown(self):

        self.removeFiles()
        BaseTestClass.tearDown(self)
        return

    def removeFiles(self):
        # ensure that INITIAL_FILE no longer exists
        # ensure that created files no longer exist
        for index in range(TestLoop1.INDEX_INITIAL, TestBranch1.INDEX_FINAL+1):
            self.removeFile('%s%s' % (TestBranch1.FILE_PREFIX, index))
            pass
        return
    
    def createDefinition(self):
        definition = GeneratePomsetsModule.createPomsetContainingBranchDefinition()
        
        nodes = [x for x in definition.nodes() if x.id() == 'branch']
        branchNode = nodes[0]
    
        # set the parameter bindings on branchNode
        branchNode.setParameterBinding(
            DefinitionModule.BranchDefinition.PARAMETER_CONDITION_STATE, 
            0)

        branchNode.setParameterBinding(
            DefinitionModule.BranchDefinition.PARAMETER_CONDITION_FUNCTION, 
            "lambda x: x"
        )
        
        branchNode.setParameterBinding(
            DefinitionModule.BranchDefinition.PARAMETER_CONDITION_MAP, 
            "[(0, 'wordcount'), (1,'reduce')]"
        )

        
        # now bind the definitions in the branches
        wcNode = [x for x in branchNode.definitionToReference().nodes() 
                  if x.id()=='wordcount'][0]
        wcNode.setParameterBinding(
            'input file', [TestBranch1.FILE_INITIAL])
        wcNode.setParameterBinding(
            'output file', [TestBranch1.FILE_FINAL])
        
        reduceNode = [x for x in branchNode.definitionToReference().nodes() 
                      if x.id()=='reduce'][0]
        reduceNode.setParameterBinding(
            'input files', [TestBranch1.FILE_INITIAL])
        reduceNode.setParameterBinding(
            'output file', [TestBranch1.FILE_FINAL])
        
        return definition


    
    def assertPostExecute(self):
        BaseTestClass.assertPostExecute(self)
        
        
        return
    
    
    # END class TestBranch1
    pass


if __name__=="__main__":
    main()

