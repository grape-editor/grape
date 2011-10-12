from threading import Thread
from threading import Semaphore
from time import sleep
from sys import settrace

from lib.vertex import Vertex
from lib.edge import Edge

class Algorithm(Thread):

    def __init__(self, graph_ui):
        Thread.__init__(self)
        
        self.__semaphore = Semaphore()
        self.__graph_ui = graph_ui
        self.__graph = graph_ui.graph
        self.__checks = {}

        # To UNDO and REDO actions
        self.__states= []
        self.__state_index = 0
        self.__add_state()

        # To kill thread
        self.__stopped = False
        
#        self.graph = graph.graph_to_networkx()

        self.vertex_list = self.__graph.vertices
        self.edge_list = self.__graph.edges

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
        if self.__stopped:
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
        print "next"
        if self.__playing:
            self.__playing = False
        elif not self.__redo():
            self.__signal()
        
    def prev(self):
        """Jump to the previous state"""
        print "prev"
        if self.__playing:
            self.__playing = False
        else:
            self.__undo()

    def play(self):
        """Start alorithm execution"""
        self.__playing = True
        self.__run_backup = self.run
        self.run = self.__run # Force the Thread to install our trace.
        Thread.start(self)

    def stop(self):
        """Kill thread that execute algorithm"""
        self.__semaphore.release()
        self.__stopped = True
        for param in self.__checks:
            self.__uncheck(param)

    def show(self):
        """Used to show current algorithm state"""
        self.__wait()
        if self.__playing:
            self.__graph_ui.queue_draw()
            sleep(0.5)
            if self.__playing:
                self.__signal()
        self.__add_state()

    def __wait(self):
        """Stop thread until receive release signal"""
        self.__semaphore.acquire()

    def __signal(self):
        """Sets free the thread to continue"""
        self.__semaphore.release()
        
