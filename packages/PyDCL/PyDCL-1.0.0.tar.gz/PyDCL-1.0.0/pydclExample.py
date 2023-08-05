from __future__ import with_statement
from pydcl import require, ensure, invariant, requireLayer, ensureLayer, invariantLayer, requireTypes, ensureTypes
import contextPy as cop

firstnameLayer = cop.layer("First name contracts")

class Person(object):
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
   
    @requireTypes(lastNameOnly = [bool])
    @require("self.firstname is not None", __layer__ = (firstnameLayer,))
    @ensureTypes(str)
    def getName(self, lastNameOnly):
        if lastNameOnly:
            return self.lastname
        else:
            return self.firstname + self.lastname
    
    @invariant()
    def typeInvariant(self):
        assert isinstance(self.firstname, (str)), "Firstname must be a string"
        assert isinstance(self.lastname, (str)), "Lastname must be a string"

print "-=-=-=-=-=-=-=-=-=-=-=-=-="
print "Person Example - Proper Usage"
person = Person("Michael", "Perscheid")
print person.getName(True)
print person.getName(False)
    
#print "-=-=-=-=-=-=-=-=-=-=-=-=-="
#print "Design by Contract with Dynamic Contract Layers"
#try:
#    person = Person(1, 2)
#    #with (cop.activelayers(ensureLayer, requireLayer, invariantLayer)):
#    #with (cop.activelayers(ensureLayer, requireLayer)):
#    #with (cop.activelayers(ensureLayer)):
#    print person.getName("arrr!")
#except AssertionError as error:
#    print error

#print "-=-=-=-=-=-=-=-=-=-=-=-=-="
#print "Contract Grouping"
#try:
#    with (cop.activelayers(firstnameLayer)):
#        print person.getName("arrr!")
#        person.firstname = None
#        print person.getName("arrr!")
#except AssertionError as error:
#    print error
    