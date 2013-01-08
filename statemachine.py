#!/usr/bin/python

import networkx as nx

class StateMachineError(Exception):
    pass

class State(object):
    """ a state in a finite state machine 
    
    A state has a name
    >>> s = State("start")
    >>> s.name
    'start'
    >>> s.name == "fart"
    False
    >>> t = State()
    Traceback (most recent call last):
       ...
    StateMachineError: a State needs a name given as parameter
    >>> t = State("")
    Traceback (most recent call last):
       ...
    StateMachineError: a State needs a name given as parameter

    """
    def __init__(self,name=None):
        if not name:
            raise StateMachineError("a State needs a name given as parameter")
        self.name = name

class StateMachine(nx.DiGraph):
    """ A basic, somewhat ad-hoc finite state machine 

    >>> sm = StateMachine()
    >>> welcomeState = State("welcome")
    >>> loginState = State("login")
    >>> annotateState = State("annotate")
    >>> endState = State("end")
    >>> sm.addTransition(welcomeState,loginState,
    ...   test=lambda x: True if x=="agree to participate" else False,
    ...   function=lambda x: "great, let's log you in")
    >>> sm.addTransition(loginState,annotateState,
    ...   test=lambda x: True if x=="correct login info"  else False,
    ...   function=lambda x: "great, let's start annotating")
    >>> sm.addTransition(annotateState,annotateState,
    ...   test=lambda x: True if x=="keep annotating"  else False,
    ...   function=lambda x: "great, keep going")
    >>> sm.addTransition(annotateState,endState,
    ...   test=lambda x: True if x=="done"  else False,
    ...   function=lambda x: "great, thanks")
    >>> sm("test")
    Traceback (most recent call last):
    ...
    AttributeError: 'StateMachine' object has no attribute 'state'

    oops, need to set the state
    >>> sm.setState(welcomeState)
    >>> sm("test")
    Traceback (most recent call last):
    ...
    StateMachineError: no valid transition using this input, given current state welcome

    OK, just checkikng...
    >>> sm("agree to participate")
    "great, let's log you in"
    >>> sm("correct login info")
    "great, let's start annotating"
    >>> sm("keep annotating")
    'great, keep going'
    >>> sm("keep annotating")
    'great, keep going'
    >>> sm("keep annotating")
    'great, keep going'

    and so on...
    >>> sm("done")
    'great, thanks'
    >>> sm("done")
    Traceback (most recent call last):
    ...
    StateMachineError: no valid transition using this input, given current state end

    no where left to go... except continue reading the code
    """

    def __call__(self,input):
        #catch special commands here
        self.processGlobalCommands(input)
        for n in self[self.state]:   #check neighbor states
            if self[self.state][n]['test'](input):
                output = self[self.state][n]['function'](input)
                self.setState(n)
                return output
        raise StateMachineError("no valid transition using this input, given current state %s"%self.state.name)
    
    def processGlobalCommands(self,input):
        pass
    def __init__(self):
        super(StateMachine,self).__init__()
    def addState(self,s):
        if not isinstance(s,State):
            raise StateMachineError("only State objects can be added to a StateMachine")
        self.add_node(s)
    def addTransition(self,s1,s2,
                       test=lambda *args:True,
                       function=lambda *args:"",
                       weight=1.0):
        if not isinstance(s1,State):
            raise StateMachineError("transitions must connect two State objects")
        if not isinstance(s2,State):
            raise StateMachineError("transitions must connect two State objects")
        self.add_edge(s1,s2,test=test,function=function)
    def setState(self,s):
        if s not in self.nodes():
            raise StateMachineError("no such state")
        self.state = s

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
