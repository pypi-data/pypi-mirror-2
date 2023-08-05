import copy
import os
import sys
import unittest
import logging

import StringIO

import threadpool

import pypatterns.command as CommandPatternModule

import pomsets.automaton as AutomatonModule
import pypatterns.filter as FilterModule

import cloudpool as CloudModule

import pomsets.command as TaskCommandModule
import pomsets.task as TaskModule

import pomsets.test_utils as GeneratePomsetsModule



class PrintObject(object):
    
    def __init__(self):
        automaton = AutomatonModule.Automaton()
        automaton.setThreadPool(0, CloudModule.Pool(1))
        automaton.commandManager(CommandPatternModule.CommandManager())
        self.automaton = automaton
        return

    def createCommandBuilderMap(self):
        commandBuilder = TaskCommandModule.CommandBuilder(
            TaskCommandModule.buildCommandFunction_commandlineArgs
        )
        return {
            'shell process':commandBuilder
            }

    def createTask(self, definition):

        compositeTask = TaskModule.CompositeTask()
        compositeTask.definition(definition)
        taskGenerator = TaskModule.NestTaskGenerator()
        compositeTask.taskGenerator(taskGenerator)
        return compositeTask
    
    
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

    
    def createExecuteEnvironmentMap(self):
        io = StringIO.StringIO()
        env = TaskCommandModule.PrintTaskCommand()
        env.outputStream(io)
        self.env = env

        return {
            'shell process':env
            }

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
        task.workRequest(request)
        
        pool = self.automaton.getThreadPoolUsingRequest(request)
        requestContext['thread pool'] = pool

        task.automaton(self.automaton)

        pool.putRequest(request)
        pool.wait()

        return request
    
    # END class PrintObject
    pass


class TestCompositeDefinition(unittest.TestCase):
    
    def setUp(self):
        definition = GeneratePomsetsModule.createPomsetContainingParameterSweep()
        GeneratePomsetsModule.bindParameterSweepDefinitionParameters(definition)
        
        self.definitionToCopy = definition
        return

    def testEq(self):

        newDefinition = copy.copy(self.definitionToCopy)
        
        assert newDefinition == self.definitionToCopy
        
        return

    def testCommands(self):
        """
        This tests for functional performance
        """
        
        # here we have to execute a task for both definitions
        # and assert that output of the task for the copy
        # is the same as the output of the task for the original
        
        newDefinition = copy.copy(self.definitionToCopy)
        
        commands = self.buildCommandsToExecute(self.definitionToCopy)
        commandsForCopiedNode = self.buildCommandsToExecute(newDefinition)
        
        assert commands == commandsForCopiedNode
        
        return
 
    
    def createTask(self, definition):

        compositeTask = TaskModule.CompositeTask()
        compositeTask.definition(definition)
        taskGenerator = TaskModule.NestTaskGenerator()
        compositeTask.taskGenerator(taskGenerator)
        compositeTask.setParameterBinding(
            'input file',
            self.inputFiles
        )
        compositeTask.setParameterBinding(
            'output file',
            self.outputFiles
        )
        compositeTask.setParameterBinding(
            'intermediate file',
            self.intermediateFiles
        )
        return compositeTask
    
    def buildCommandsToExecute(self, definition):
        
        testObj = PrintObject()
        
        task = testObj.createTask(definition)
        request = testObj.executeTask(task)

        commands = testObj.env.outputStream().getvalue()
        
        return commands
    
    # END class TestCompositeDefinition
    pass


class TestReferenceDefinition(unittest.TestCase):
    
    def setUp(self):
        definition = GeneratePomsetsModule.createPomsetContainingParameterSweep()
        GeneratePomsetsModule.bindParameterSweepDefinitionParameters(definition)
        
        self.definitionToCopy = definition
        return


    def testCopyMapper(self):
        
        nodeToCopy = [x for x in self.definitionToCopy.nodes()
                      if x.id() == 'mapper'][0]
        
        copiedNode = copy.copy(nodeToCopy)

        self.assertTrue(copiedNode.graph() is None)
        copiedNode.graph(nodeToCopy.graph())

        # assert nodeToCopy == copiedNode
        differences = [x for x in nodeToCopy.getDifferencesWith(copiedNode)]
        self.assertEquals(['self has 1 outgoing edges, other has 0'], 
                          differences)
        
        return


    def testCopyReducer(self):
        nodeToCopy = [x for x in self.definitionToCopy.nodes()
                      if x.id() == 'reducer'][0]
        
        copiedNode = copy.copy(nodeToCopy)

        self.assertTrue(copiedNode.graph() is None)
        copiedNode.graph(nodeToCopy.graph())

        # assert nodeToCopy == copiedNode
        differences = [x for x in nodeToCopy.getDifferencesWith(copiedNode)]
        self.assertEquals(['self has 1 incoming edges, other has 0'], 
                          differences)

        
        return
        
    # END class TestReferenceDefinition
    pass

