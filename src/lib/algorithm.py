from threading import Thread
from threading import Semaphore
from time import sleep
from sys import settrace

from lib.vertex import Vertex
from lib.edge import Edge

class Algorithm(Thread):

    def __init__(self, graph):
        Thread.__init__(self)
        
        self.__semaphore = Semaphore()
        self.__graph = graph
        self.__checks = {}

        # To UNDO and REDO actions
        self.__states= []
        self.__state_index = 0
        self.__add_state()
        
        # To kill thread
        self.__stopped = False
        self.__killed = False
        
#        self.graph = graph.graph_to_networkx()

        self.vertex_list = graph.vertices
        self.edge_list = graph.edges

    def start(self):
       """Start the thread."""
       self.__run_backup = self.run
       self.run = self.__run # Force the Thread to install our trace.
       Thread.start(self)

    def __run(self):
       """Hacked run function, which installs the trace."""
       settrace(self.__globaltrace)
       self.__run_backup()
       self.run = self.__run_backup

    def __globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.__localtrace
        else:
            return None

    def __localtrace(self, frame, why, arg):
        if self.__killed:
            if why == 'line':
                raise SystemExit()
                return self.__localtrace

    def __add_state(self):
        """Adds a new state in the list states (HISTORY)"""
        self.__clean_checks()
        if self.__state_index != len(self.__states):
            self.__states = self.__states[:self.__state_index]
        self.__states.append(self.__checks.copy())
        self.__state_index += 1
        self.__make_checks()

    def __undo(self):
        """Undo a state (HISTORY)"""
        if self.__state_index > 0:
            self.__clean_checks()
            self.__state_index -= 1
            self.__checks = self.__states[self.__state_index]
            self.__make_checks()
            return self.__checks
        return None

    def __redo(self):
        """Redo a state (HISTORY)"""
        if self.__state_index < len(self.__states):
            self.__clean_checks()
            self.__checks = self.__states[self.__state_index]
            self.__state_index += 1
            self.__make_checks()
            return self.__checks
        return None

    def __clean_checks(self):
        """ Make inverse action for all action stacks"""
        for param, function in self.__checks.items():
            function[1](param)

    def __make_checks(self):
        """ Make current action for all action stacks"""
        for param, function in self.__checks.items():
            function[0](param)

    def __check(self, what):
        """Checks vertex or checks a edge"""
        if what is not None: what.check()

    def __uncheck(self, what):
        """Unchecks vertex or unchecks a edge"""
        if what is not None: what.uncheck()

    def check(self, what):
        """Writes action in the stack"""
        self.__checks[what] = [self.__check, self.__uncheck]
            
    def uncheck(self, what):
        """Writes action in the stack"""
        self.__checks[what] = [self.__uncheck, self.__check]

    def next(self):
        """Jump to the next state"""
        if not self.__redo():
            self.__signal()
        
    def prev(self):
        """Jump to the previous state"""
        self.__undo()
        
    def play(self):
        """Start alorithm execution"""
        self.start()

    def stop(self):
        """Kill thread that execute algorithm"""
        self.__semaphore.release()
        self.__killed = True
        for param in self.__checks:
            self.__uncheck(param)

    def show(self):
        self.__wait()
        self.__add_state()

    def __wait(self):
        """Stop thread until receive release signal"""
        self.__semaphore.acquire()

    def __signal(self):
        """Sets free the thread to continue"""
        self.__semaphore.release()
        



