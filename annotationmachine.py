#!/usr/bin/python

from statemachine import StateMachine, State

class AnnotationMachine(StateMachine):
    welcomeState = State("welcome")
    loginState = State("login")
    annotateState = State("annotate")
    endState = State("end")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
