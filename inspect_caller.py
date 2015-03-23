import inspect
import sys

def afuncation():
    print inspect.stack()[1][3]

def caller(): afuncation()

#print <module> because this is the top level func call
afuncation()

#print the caller
caller()

