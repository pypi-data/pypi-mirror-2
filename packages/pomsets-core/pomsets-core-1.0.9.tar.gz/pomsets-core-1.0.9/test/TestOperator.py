import os
import unittest

import pypatterns.command as CommandPatternModule
import pypatterns.filter as FilterModule
import pypatterns.relational as RelationalModule

import cloudpool as CloudModule

import pomsets.automaton as AutomatonModule
import pomsets.builder as BuilderModule
import pomsets.library as LibraryModule
import pomsets.parameter as ParameterModule
import pomsets.python as PythonModule
import pomsets.task as TaskModule
import pomsets.test_utils as TestUtilsModule


import test.TestExecute as BaseModule


class TestPythonFunction(unittest.TestCase):

    def setUp(self):
        self.builder = BuilderModule.Builder()
        return

    def tearDown(self):
        return
    
    def testGetFunctionName(self):

        functionName = 'testFunction'


        executable = self.builder.createExecutableObject(
            ['', functionName],
            executableClass=PythonModule.Function)

        self.assertEquals(functionName, executable.name())

        return

    # END class TestPythonFunction
    pass


class TestPythonCommandBuilder(unittest.TestCase):


    def setUp(self):
        self.builder = BuilderModule.Builder()

        self.functionName = 'testFunction'
        self.executableObject = self.builder.createExecutableObject(
            [None, self.functionName],
            executableClass=PythonModule.Function)

        parentContext = self.builder.createNewNestPomset(name='root')
        parentDefinition = parentContext.pomset()
        
        pythonEvalContext = self.builder.createNewAtomicPomset(
            name='testPython',
            executableObject = self.executableObject,
            commandBuilderType = 'python eval')
        pythonEvalDefinition = pythonEvalContext.pomset()
        self.definitionToReference = pythonEvalDefinition

        self.definition = self.builder.createNewNode(
            parentDefinition, name='node', 
            definitionToReference=pythonEvalDefinition)

        self.commandBuilder = PythonModule.CommandBuilder()

        parentTask = TaskModule.CompositeTask()
        parentTask.definition(parentDefinition)
        taskGenerator = TaskModule.NestTaskGenerator()
        parentTask.taskGenerator(taskGenerator)
        self.parentTask = parentTask

        return


    def tearDown(self):
        return


    def assertBuiltCommand(self, expected):
        task = TaskModule.createTaskForDefinition(
            self.parentTask, self.definition)

        command = self.commandBuilder.buildCommand(task)

        self.assertEquals(expected,
                          command)

        return


    def testBuildCommand1(self):
        """
        this ensures that building succeeds
        when there are no arguments
        """

        self.assertBuiltCommand('%s()' % self.functionName)
        return


    def testBuildCommandArgOnly1(self):
        # this ensures that building succeeds
        # when there is only a single non-keyword arg

        parameterId = 'arg1'

        # add parameters to definition
        self.builder.addPomsetParameter(
            self.definitionToReference, parameterId,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT})

        arg1 = 'arg1'
        self.builder.bindParameterValue(self.definition,
                                        parameterId,
                                        arg1)


        self.assertBuiltCommand('%s("%s")' % (self.functionName, arg1))
        return


    def testBuildCommandArgOnly2(self):
        # this ensures that building succeeds
        # when there are only non-keyword args

        parameter1Id = 'arg1'
        parameter2Id = 'arg2'

        # add parameters to definition
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter1Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT})
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter2Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT})

        # order parameters
        self.builder.addParameterOrdering(
            self.definitionToReference, 
            parameter1Id, parameter2Id)


        # bind values on task
        arg1 = 'arg1'
        arg2 = 5

        self.builder.bindParameterValue(self.definition,
                                        parameter1Id,
                                        arg1)
        self.builder.bindParameterValue(self.definition,
                                        parameter2Id,
                                        arg2)


        self.assertBuiltCommand('%s("%s", %s)' % 
                                (self.functionName, arg1, arg2))
        return


    def testBuildCommandKeywordOnly1(self):
        # this ensures that building succeeds
        # when there are only a single keyword arg

        parameterId = 'arg1'
        arg1Key = 'arg1key'
 
        # add parameters to definition
        self.builder.addPomsetParameter(
            self.definitionToReference, parameterId,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT,
             'is keyword':True,
             'keyword to pass':arg1Key})

        arg1 = 'arg1value'
        self.builder.bindParameterValue(self.definition,
                                        parameterId,
                                        arg1)


        self.assertBuiltCommand('%s(%s="%s")' % 
                                (self.functionName, arg1Key, arg1))
        return


    def testBuildCommandKeywordOnly2(self):
        # this ensures that building succeeds
        # when there are only keyword args

        parameter1Id = 'arg1'
        parameter2Id = 'arg2'
        parameter3Id = 'arg3'

        arg1Key = 'arg1key'
        arg2Key = 'arg2key'
        arg3Key = 'arg3key'
 
        # add parameters to definition
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter1Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT,
             'is keyword':True,
             'keyword to pass':arg1Key})
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter2Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT,
             'is keyword':True,
             'keyword to pass':arg2Key})
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter3Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT,
             'is keyword':True,
             'keyword to pass':arg3Key})

        # order parameters
        self.builder.addParameterOrdering(
            self.definitionToReference, 
            parameter2Id, parameter1Id)
        self.builder.addParameterOrdering(
            self.definitionToReference, 
            parameter1Id, parameter3Id)

        arg1 = 'arg1value'
        arg2 = 8
        arg3 = None

        self.builder.bindParameterValue(self.definition,
                                        parameter1Id,
                                        arg1)
        self.builder.bindParameterValue(self.definition,
                                        parameter2Id,
                                        arg2)
        self.builder.bindParameterValue(self.definition,
                                        parameter3Id,
                                        arg3)


        self.assertBuiltCommand('%s(%s=%s, %s="%s", %s=%s)' % 
                                (self.functionName, 
                                 arg2Key, arg2,
                                 arg1Key, arg1,
                                 arg3Key, arg3))
        return


    def testBuildCommand6(self):
        # this ensures that building succeeds
        # when there are both keyword and non-keyword args

        parameter1Id = 'arg1'
        parameter2Id = 'arg2'
        parameter3Id = 'arg3'

        arg1Key = 'arg1key'
        arg3Key = 'arg3key'
 
        # add parameters to definition
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter1Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT,
             'is keyword':True,
             'keyword to pass':arg1Key})
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter2Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT})
        self.builder.addPomsetParameter(
            self.definitionToReference, parameter3Id,
            {'direction':ParameterModule.PORT_DIRECTION_INPUT,
             'is keyword':True,
             'keyword to pass':arg3Key})

        # order parameters
        self.builder.addParameterOrdering(
            self.definitionToReference, 
            parameter2Id, parameter1Id)
        self.builder.addParameterOrdering(
            self.definitionToReference, 
            parameter1Id, parameter3Id)

        arg1 = 'arg1value'
        arg2 = 8
        arg3 = None

        self.builder.bindParameterValue(self.definition,
                                        parameter1Id,
                                        arg1)
        self.builder.bindParameterValue(self.definition,
                                        parameter2Id,
                                        arg2)
        self.builder.bindParameterValue(self.definition,
                                        parameter3Id,
                                        arg3)


        self.assertBuiltCommand('%s(%s, %s="%s", %s=%s)' % 
                                (self.functionName, 
                                 arg2,
                                 arg1Key, arg1,
                                 arg3Key, arg3))

        return


    # END class 
    pass





class TestLoadListValues1(BaseModule.BaseTestClass, unittest.TestCase):


    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestOperator')
    INPUT_FILE = 'listValues1'


    def setUp(self):
        BaseModule.BaseTestClass.setUp(self)
        self.builder = BuilderModule.Builder()
        return


    def getPythonEvalDefinition(self):
        pythonEvalDefinition = \
            TestUtilsModule.createLoadListValuesFromFilesDefinition()
        return pythonEvalDefinition


    def createDefinition(self):
        pythonEvalDefinition = self.getPythonEvalDefinition()

        parentContext = self.builder.createNewNestPomset(name='root')
        parentDefinition = parentContext.pomset()
        

        self.definition = self.builder.createNewNode(
            parentDefinition, name='node', 
            definitionToReference=pythonEvalDefinition)


        self.builder.bindParameterValue(
            self.definition,
            'file to read',
            [os.path.sep.join([TestLoadListValues1.BASE_DIR, 
                               TestLoadListValues1.INPUT_FILE])]
            )

        return parentDefinition


    def createCommandBuilderMap(self):
        commandBuilderMap = BaseModule.BaseTestClass.createCommandBuilderMap(self)
        commandBuilderMap['python eval'] = PythonModule.CommandBuilder()
        return commandBuilderMap


    def createExecuteEnvironmentMap(self):
        return {
            'python eval':PythonModule.PythonEval()
            }


    def createTask(self, definition):

        parentTask = TaskModule.CompositeTask()
        parentTask.definition(definition)
        taskGenerator = TaskModule.NestTaskGenerator()
        parentTask.taskGenerator(taskGenerator)

        # TODO:
        # bind the parameters
        #task = TaskModule.createTaskForDefinition(
        #    parentTask, self.definition)
        # return task

        self.parentTask = parentTask

        return parentTask


    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)

        childTasks = self.parentTask.getChildTasks()
        childTask = childTasks[0]

        values = childTask.getParameterBinding('eval result')

        self.assertEquals(['/tmp/foo', '/user/home/me/bar.txt', './baz.ext'],
                          values)
        
        return 


    # END class TestLoadListValues1
    pass


class TestLoadListValues2(TestLoadListValues1):


    def getLibraryDir(self):
        return os.path.join(os.getcwd(), 'resources', 'testdata', 'TestLibrary', 'library')

    def initializeLibrary(self):
        library = LibraryModule.Library()
        library.shouldMarkAsLibraryDefinition(True)
        libraryDir = self.getLibraryDir()
        library.bootstrapLoaderDefinitionsDir(libraryDir)

        library.loadBootstrapLoaderDefinitions()
        return library

    def setUp(self):
        TestLoadListValues1.setUp(self)

        automaton = AutomatonModule.Automaton()
        automaton.setThreadPool(None, CloudModule.Pool(1))
        automaton.commandManager(CommandPatternModule.CommandManager())
        self.automaton = automaton

        self.library = self.initializeLibrary()
        automaton.runBootstrapLoader(self.library)
        return


    def getPythonEvalDefinition(self):
            
        filter = RelationalModule.ColumnValueFilter(
            'definition',
            FilterModule.IdFilter(LibraryModule.ID_LOADLISTVALUESFROMFILES))
        
        return self.library.getDefinition(filter)

        
    # END class TestLoadListValues2
    pass


class TestRange1(BaseModule.BaseTestClass, unittest.TestCase):


    def setUp(self):
        BaseModule.BaseTestClass.setUp(self)
        self.builder = BuilderModule.Builder()
        return


    def getPythonEvalDefinition(self):
        pythonEvalDefinition = \
            TestUtilsModule.createRangeDefinition()
        return pythonEvalDefinition


    def createDefinition(self):
        pythonEvalDefinition = self.getPythonEvalDefinition()

        parentContext = self.builder.createNewNestPomset(name='root')
        parentDefinition = parentContext.pomset()
        

        self.definition = self.builder.createNewNode(
            parentDefinition, name='node', 
            definitionToReference=pythonEvalDefinition)


        self.bindParameterValues()

        return parentDefinition


    def bindParameterValues(self):
        self.builder.bindParameterValue(
            self.definition,
            'end', 3)

        return


    def createCommandBuilderMap(self):
        commandBuilderMap = BaseModule.BaseTestClass.createCommandBuilderMap(self)
        commandBuilderMap['python eval'] = PythonModule.CommandBuilder()
        return commandBuilderMap


    def createExecuteEnvironmentMap(self):
        return {
            'python eval':PythonModule.PythonEval()
            }


    def createTask(self, definition):

        parentTask = TaskModule.CompositeTask()
        parentTask.definition(definition)
        taskGenerator = TaskModule.NestTaskGenerator()
        parentTask.taskGenerator(taskGenerator)

        # TODO:
        # bind the parameters
        #task = TaskModule.createTaskForDefinition(
        #    parentTask, self.definition)
        # return task

        self.parentTask = parentTask

        return parentTask


    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)

        childTasks = self.parentTask.getChildTasks()
        childTask = childTasks[0]

        values = childTask.getParameterBinding('eval result')

        self.assertEquals(range(3),
                          values)
        
        return 


    # END class TestRange1
    pass


class TestRange2(TestRange1):

    def bindParameterValues(self):
        self.builder.bindParameterValue(
            self.definition,
            'start', 2)

        self.builder.bindParameterValue(
            self.definition,
            'end', 10)

        self.definition.parameterIsActive('start', True)

        return

    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)

        childTasks = self.parentTask.getChildTasks()
        childTask = childTasks[0]

        values = childTask.getParameterBinding('eval result')

        self.assertEquals(range(2,10),
                          values)
        
        return 


    # END class TestRange2
    pass


class TestRange3(TestRange1):
    """
    This tests the default value
    """

    def getPythonEvalDefinition(self):
        pythonEvalDefinition = TestRange1.getPythonEvalDefinition(self)

        parameter = pythonEvalDefinition.getParameter('start')
        parameter.defaultValue(5)

        return pythonEvalDefinition


    def bindParameterValues(self):

        self.builder.bindParameterValue(
            self.definition,
            'end', 10)

        self.definition.parameterIsActive('start', True)

        return


    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)

        childTasks = self.parentTask.getChildTasks()
        childTask = childTasks[0]

        values = childTask.getParameterBinding('eval result')

        self.assertEquals(range(5,10),
                          values)
        
        return 


    # END class TestRange3
    pass


class TestRange4(TestRange1):

    def bindParameterValues(self):
        self.builder.bindParameterValue(
            self.definition,
            'start', 2)

        self.builder.bindParameterValue(
            self.definition,
            'end', 10)

        self.builder.bindParameterValue(
            self.definition,
            'step', 3)

        self.definition.parameterIsActive('start', True)
        self.definition.parameterIsActive('step', True)

        return

    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)

        childTasks = self.parentTask.getChildTasks()
        childTask = childTasks[0]

        values = childTask.getParameterBinding('eval result')

        self.assertEquals(range(2,10,3),
                          values)
        
        return 


    # END class TestRange4
    pass



class TestMakeDirs1(BaseModule.BaseTestClass, unittest.TestCase):

    PATH_TO_CREATE = os.path.sep.join(['', 'tmp', 'TestMakeDirs1'])

    def setUp(self):
        BaseModule.BaseTestClass.setUp(self)
        self.builder = BuilderModule.Builder()

        if os.path.exists(TestMakeDirs1.PATH_TO_CREATE):
            import shutil
            shutil.rmtree(TestMakeDirs1.PATH_TO_CREATE)
        return

    def tearDown(self):
        if os.path.exists(TestMakeDirs1.PATH_TO_CREATE):
            import shutil
            shutil.rmtree(TestMakeDirs1.PATH_TO_CREATE)
        return

    def getPythonEvalDefinition(self):
        pythonEvalDefinition = \
            TestUtilsModule.createMakeDirsDefinition()
        return pythonEvalDefinition


    def createDefinition(self):
        pythonEvalDefinition = self.getPythonEvalDefinition()

        parentContext = self.builder.createNewNestPomset(name='root')
        parentDefinition = parentContext.pomset()
        

        self.definition = self.builder.createNewNode(
            parentDefinition, name='node', 
            definitionToReference=pythonEvalDefinition)

        self.bindParameterValues()

        return parentDefinition


    def bindParameterValues(self):
        self.builder.bindParameterValue(
            self.definition,
            'path', TestMakeDirs1.PATH_TO_CREATE)

        return


    def createCommandBuilderMap(self):
        commandBuilderMap = BaseModule.BaseTestClass.createCommandBuilderMap(self)
        commandBuilderMap['python eval'] = PythonModule.CommandBuilder()
        return commandBuilderMap


    def createExecuteEnvironmentMap(self):
        return {
            'python eval':PythonModule.PythonEval()
            }


    def createTask(self, definition):

        parentTask = TaskModule.CompositeTask()
        parentTask.definition(definition)
        taskGenerator = TaskModule.NestTaskGenerator()
        parentTask.taskGenerator(taskGenerator)

        self.parentTask = parentTask

        return parentTask


    def assertPreExecute(self):
        BaseModule.BaseTestClass.assertPreExecute(self)
        self.assertFalse(os.path.exists(TestMakeDirs1.PATH_TO_CREATE))
        return

    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)
        self.assertTrue(os.path.exists(TestMakeDirs1.PATH_TO_CREATE))
        return 


    # END class TestMakeDirs1
    pass


class TestMakeDirs2(TestMakeDirs1):

    PATH_PARENT = os.path.sep.join(['', 'tmp', 'TestMakeDirs2'])
    PATH_TO_CREATE = os.path.sep.join([PATH_PARENT, 'level2'])

    def setUp(self):
        BaseModule.BaseTestClass.setUp(self)
        self.builder = BuilderModule.Builder()

        if os.path.exists(TestMakeDirs2.PATH_PARENT):
            import shutil
            shutil.rmtree(TestMakeDirs2.PATH_PARENT)
        return

    def tearDown(self):
        if os.path.exists(TestMakeDirs2.PATH_PARENT):
            import shutil
            shutil.rmtree(TestMakeDirs2.PATH_PARENT)
        return

    def bindParameterValues(self):
        self.builder.bindParameterValue(
            self.definition,
            'path', TestMakeDirs2.PATH_TO_CREATE)

        return

    def assertPreExecute(self):
        BaseModule.BaseTestClass.assertPreExecute(self)
        self.assertFalse(os.path.exists(TestMakeDirs2.PATH_PARENT))
        return

    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)
        self.assertTrue(os.path.exists(TestMakeDirs2.PATH_TO_CREATE))
        return 

    # END TestMakeDirs2
    pass



class TestStringReplace1(BaseModule.BaseTestClass, unittest.TestCase):

    PATH_TO_CREATE = os.path.sep.join(['', 'tmp', 'TestMakeDirs1'])

    def setUp(self):
        BaseModule.BaseTestClass.setUp(self)
        self.builder = BuilderModule.Builder()
        return

    def getPythonEvalDefinition(self):
        pythonEvalDefinition = \
            TestUtilsModule.createStringReplaceDefinition()
        return pythonEvalDefinition


    def createDefinition(self):
        pythonEvalDefinition = self.getPythonEvalDefinition()

        parentContext = self.builder.createNewNestPomset(name='root')
        parentDefinition = parentContext.pomset()
        
        self.definition = self.builder.createNewNode(
            parentDefinition, name='node', 
            definitionToReference=pythonEvalDefinition)

        self.bindParameterValues()

        return parentDefinition


    def bindParameterValues(self):
        self.builder.bindParameterValue(
            self.definition,
            'string to modify', ['this is a test'])
        self.builder.bindParameterValue(
            self.definition,
            'original substring', ' is a ')
        self.builder.bindParameterValue(
            self.definition,
            'new substring', ' is a successful ')
        return


    def createCommandBuilderMap(self):
        commandBuilderMap = BaseModule.BaseTestClass.createCommandBuilderMap(self)
        commandBuilderMap['python eval'] = PythonModule.CommandBuilder()
        return commandBuilderMap


    def createExecuteEnvironmentMap(self):
        return {
            'python eval':PythonModule.PythonEval()
            }


    def createTask(self, definition):

        parentTask = TaskModule.CompositeTask()
        parentTask.definition(definition)
        taskGenerator = TaskModule.NestTaskGenerator()
        parentTask.taskGenerator(taskGenerator)

        self.parentTask = parentTask

        return parentTask


    def assertPostExecute(self):
        BaseModule.BaseTestClass.assertPostExecute(self)

        childTasks = self.parentTask.getChildTasks()
        childTask = childTasks[0]

        values = childTask.getParameterBinding('eval result')

        self.assertEquals(['this is a successful test'], values)
        return 


    # END class TestStringReplace1
    pass
