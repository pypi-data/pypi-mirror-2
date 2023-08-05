from __future__ import with_statement
from contextPy import layer, proceed, activelayer, around, base

employerLayer = layer("EmployerLayer")

class Person(object):
    def __init__(self):
        self.name = "Michael Perscheid"
        self.employer = "Hasso-Plattner-Institute"

    @base
    def getDetails(self):
        return self.name
    
    @around(employerLayer)
    def getDetails(self):
        return proceed() + "\n" + self.employer

person = Person()
print person.getDetails()
with activelayer(employerLayer):
    print person.getDetails()