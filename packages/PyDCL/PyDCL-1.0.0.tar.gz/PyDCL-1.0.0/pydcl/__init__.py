from __future__ import with_statement
import contextPy as cop
import copy
import sys
import types

#REQUIREMENTS (NICHT LOESCHEN SONDERN ABHAKEN)
#DONE: parameter hat im Moment keine Bedeutung!!! Ebenso kann man im String auf ALLE Variabeln zugreifen! Ist das gut oder schlecht???
#DONE: RequireTypes implementieren Bsp. @requireTypes(self = [__main__.A, __main__.B], number = [int, float]) (Redundanten Code verhindern, __common mit Parametern Trick)
#DONE: Eigenes Modul/Package bauen
#DONE: Mehrere Layer pro Bedingung, um sie z.B. nach Feature/Use-cases zu ordnen??? Aktivieren von Conditions fuer einen Use-case, Kontrollfluss und dynamisch zur Laufzeit anschalten. Anscheinend in UseCasePy implementiert! D.h. COP hier wieder anpassen an meine Beduerfnisse --- hat funktioniert ohne grosse Probleme
#DONE: nicht nur bloecke angeben fuer Typen sondern vl auch String mit Code z.B. "number < 10 or number > 100"
#DONE: Probleme mit Static and Class Methods --- Besteht das noch? Ja unwrappen mal wieder um an die wichtigen Parameter zu kommen! Ggf. erzeugtes Function Object auch zu einer class method casten...
#OK(REMOVED): Bei einer Verletzung der Assertion gibt es nur eine bedingt schoene Ausgabe --> besseren Source Code erzeugen, der ein Statement ausgibt! Ebenso assert ganz entfernen, da es durch Interpreter Flags disabled werden kann...
#REMOVED: Eigene Exception fuer bessere Lesbarkeit einfuehren! Und anzeigen was genau schief gegangen ist!
#DONE: Require = Pre Conditions und Ensure = Post Conditions!!!
#DONE: Ensure (Postconditions) implementieren also Standardtext (Code) der ausgefuehrt wird analog zu require
#DONE: old Zustand in ensure erlaube, welcher vorher gespeichert wird und auf den dann zugegriffen werden kann... Bsp. @ensure("self.value == old(self.value) + 1") --> speichern des alten Wertes und dann hinterlegen in der Postcondition
#DONE: Ensure Type implementieren
#OK: Pruefen was mit Super calls und Subklassen ist. Geht alles wie erwartet???
#OK: Verstaerken und Abschwaechen von Bedingungen --- Bedingungen koennen PRO Methode angegeben werden und somit werden die anderen Werte ueberschrieben, wenn man so will verfeinert...
#REMOVED (Nur bedingt entscheidbar, welcher Wert angezeigt werden sollen): Im Falle einer Verletzung auch den aktuellen Wert anzeigen! Objekt/Parameterwerte spaeter return Wert printen!
#DONE: Bei Types entsprechend den Typ printen!!!
#DONE: @ensureTypes muessen noch im after den eigentlichen Wert zurueckgeben!!!

#DONE: Invarianten werden fuer die gesamte Klasse definiert und werden bei jedem Methoden Aufruf geprueft!!! Invarianten werden fuer jeden Methodencall davor und danach geprueft!
#DONE: Dabei verhindern, dass bei weiteren Methodencalls in einer Invarianten keine endlose Rekursion triggert (Guards in PyDCL genutzt)

#TODO: #!!! Bedingungen pro USE-CASE!!! Anwendung fuer dynamische Vertraege und Use-case Meta-objects!!! Automatische Generierung anpassen und vl auch schon mit use-cases meta-objects/layers zur logischen decomposition nutzen?
#TODO: Wenn eine Use-case Annotation gefunden wurde, dann soll diese genutzt werden um die Vertraege direkt and die Layer/Use-case zu binden!
#DONE: Automatische Generierung anpassen 

#DONE: Ordentliche Tests schreiben!

#FIXME: Bug bei Default Werten in Methodensignaturen. Diese werden in THEFUNCTION nicht mit uebernommen, was zu Fehlern fuehrt da ggf. mehr Werte beim proceed erwartet werden als die Funktion bekommt... man kann darauf zugreien mittels functionObject.func_defaults. Jedoch muss die Beschraenkung der partiellen Methode aufgehoben werden, damit auch andere Objektdefaultwerte entsprechend gefunden werden koennen. Der Scope muss dem der base Methode entsprechen
#DONE: Invarianten werden nur richtig in descriptoren gewrapped, wenn die bestehende Methode bereits partiell ist, d.h. bei normalen instanzmethoden ohne andere Dekorator passiert garnichts (fehlschlagener Test bereites hinzugefuegt)
#DONE: Partielle Methoden sollen auch als Vertraege moeglich sein - analog zur Original Implementierung PyDCL

# From ContextPy: Overwrite cacheMethods adapting a tuple of layers for a method
class _contractMethodDescriptor(cop._layeredmethoddescriptor):
    
    def cacheMethods(self, activelayers):
        layers = list(activelayers)
        for layer_ in activelayers:
            if layer_ is not None:
                layers = layer_.getEffectiveLayers(layers)
        layers = list(reversed(layers))

        # For each active layer, get all methods and the when advice class related to this layer
        # if currentLayer in tuple of layers for a particular method then add to methods
        methods = sum([
            list(reversed(
                [(lmwgm[1], lmwgm[2]) for lmwgm in self._methods if currentlayer in self.getLayers(lmwgm[0]) and lmwgm[3](activelayers)]
            )) for currentlayer in layers], [])

        self._cache[activelayers] = result = cop._advice.createchain(methods)
        return result
    
    # Converts the None layer argument from base methods to a tuple
    def getLayers(self, layers):
        if layers == None:
            return (None, )
        return layers

# From ContextPy: Change the class constructor to contractMethodDescriptor 
def createlayeredmethod(base, partial):
    if base:
        return _contractMethodDescriptor([(None, base, cop._around, cop._true)] + partial)
    else:
        return _contractMethodDescriptor(partial)

requireLayer = cop.layer("requireLayer")
ensureLayer = cop.layer("ensureLayer")
invariantLayer = cop.layer("invariantLayer")

LAYER_KEYWORD = "__layer__"

# The list of symbols that are included by default in the generated
# function's environment
SAFE_SYMBOLS = ["list", "dict", "tuple", "set", "long", "float", "object",
                "bool", "callable", "True", "False", "dir",
                "frozenset", "getattr", "hasattr", "abs", "cmp", "complex",
                "divmod", "id", "pow", "round", "slice", "vars",
                "hash", "hex", "int", "isinstance", "issubclass", "len",
                "map", "filter", "max", "min", "oct", "chr", "ord", "range",
                "reduce", "repr", "str", "type", "zip", "xrange", "None",
                "Exception", "KeyboardInterrupt"]
# Also add the standard exceptions
__bi = __builtins__
if type(__bi) is not dict:
    __bi = __bi.__dict__
for k in __bi:
    if k.endswith("Error") or k.endswith("Warning"):
        SAFE_SYMBOLS.append(k)
del __bi


def createFunction(sourceCode, args="", additional_symbols=dict()):
    """
    Create a python function from the given source code
    
    \param sourceCode A python string containing the core of the
    function. Might include the return statement (or not), definition of
    local functions, classes, etc. Indentation matters !
    
    \param args The string representing the arguments to put in the function's
    prototype, such as "a, b", or "a=12, b",
    or "a=12, b=dict(akey=42, another=5)"
  
    \param additional_symbols A dictionary variable name =>
    variable/funcion/object to include in the generated function's
    closure
  
    The sourceCode will be executed in a restricted environment,
    containing only the python builtins that are harmless (such as map,
    hasattr, etc.). To allow the function to access other modules or
    functions or objects, use the additional_symbols parameter. For
    example, to allow the source code to access the re and sys modules,
    as well as a global function F named afunction in the sourceCode and
    an object OoO named ooo in the sourceCode, specify:
    additional_symbols = dict(re=re, sys=sys, afunction=F, ooo=OoO)
  
    \return A python function implementing the source code. It can be
    recursive: the (internal) name of the function being defined is:
    __TheFunction__. Its docstring is the initial sourceCode string.

    Tests show that the resulting function does not have any calling
    time overhead (-3% to +3%, probably due to system preemption aleas)
    compared to normal python function calls.
    """
    # Include the sourcecode as the code of a function __TheFunction__:
    s = "def __TheFunction__(%s):\n" % args
    s += "\t" + "\n\t".join(sourceCode.split('\n')) + "\n"

    # Byte-compilation (optional)
    byteCode = compile(s, "<string>", 'exec')  

    # Setup the local and global dictionaries of the execution
    # environment for __TheFunction__
    bis   = dict() # builtins
    globs = dict()
    locs  = dict()

    # Setup a standard-compatible python environment
    bis["locals"]  = lambda: locs
    bis["globals"] = lambda: globs
    globs["__builtins__"] = bis
    globs["__name__"] = "SUBENV"
    globs["__doc__"] = sourceCode
  
    # Determine how the __builtins__ dictionary should be accessed
    if type(__builtins__) is dict:
        bi_dict = __builtins__
    else:
        bi_dict = __builtins__.__dict__
    
    # Include the safe symbols
    for k in SAFE_SYMBOLS:
        # try from current locals
        try:
            locs[k] = locals()[k]
            continue
        except KeyError:
            pass
        # Try from globals
        try:
            globs[k] = globals()[k]
            continue
        except KeyError:
            pass
        # Try from builtins
        try:
            bis[k] = bi_dict[k]
        except KeyError:
            # Symbol not available anywhere: silently ignored
            pass

    # Include the symbols added by the caller, in the globals dictionary
    globs.update(additional_symbols)

    # Finally execute the def __TheFunction__ statement:
    eval(byteCode, globs, locs)
    # As a result, the function is defined as the item __TheFunction__
    # in the locals dictionary
    fct = locs["__TheFunction__"]
    # Attach the function to the globals so that it can be recursive
    del locs["__TheFunction__"]
    globs["__TheFunction__"] = fct
    # Attach the actual source code to the docstring
    fct.__doc__ = sourceCode
    
    return fct

# Look up parameter of method
def getParametersFromMethod(method):
    parameters = ""
    if (issubclass(type(method), cop._layeredmethoddescriptor)):
        baseMethod = method.methods[0][1]
        if (type(baseMethod) in (classmethod, staticmethod)):
            baseMethod = baseMethod.__get__(None, cop._dummyClass)
        parameters = ", ".join(baseMethod.func_code.co_varnames[:baseMethod.func_code.co_argcount])
    elif (type(method) in (classmethod, staticmethod)):
        # Bound the method to a dummy class to retrieve the original name
        boundedMethod = method.__get__(None, cop._dummyClass)
        parameters = ", ".join(boundedMethod.func_code.co_varnames[:boundedMethod.func_code.co_argcount]) 
    else:    
        parameters = ", ".join(method.func_code.co_varnames[:method.func_code.co_argcount])
            
    parameters += ", *args, **kwargs"
    
    return parameters
    
def lookUpLayerEntries(standardLayer, **kwargs):
    # Choose corresponding layer
    usedLayers = [standardLayer,]
    if kwargs.has_key(LAYER_KEYWORD):
        if isinstance(kwargs[LAYER_KEYWORD], (list, tuple)):
            usedLayers += list(kwargs[LAYER_KEYWORD])
        else:
            usedLayers.append(kwargs[LAYER_KEYWORD])
    return usedLayers
       
def createSourceCodeFromStrings(parameters, *args, **kwargs):
    # Create contract source code
    sourcecode = ""
    if len(args) == 0:
        sourcecode = "pass"
    else:
        for condition in args:           
            assertionMessage = condition
            sourcecode += "assert " + condition + ", \"" + assertionMessage + "\"\n"
    return sourcecode

def createEnsureSourceCodeFromStrings(parameters, *args, **kwargs):
    # Create contract source code for post conditions
    sourcecode = ""
    #remove self or cls from parameters
    proceedParameters = parameters
    if proceedParameters.startswith("self"):
        proceedParameters = proceedParameters[4:].strip(", ")
    if proceedParameters.startswith("cls"):
        proceedParameters = proceedParameters[4:].strip(", ")        
    if len(args) == 0:
        sourcecode += "return proceed(" + proceedParameters +")\n"   
    else:
        #Store old values for later use in post condition assertions
        sourcecode += "oldValues = dict()\n"
        for condition in args:
            startIndex = -1
            while not condition.find("old(", startIndex + 1) == -1:
                startIndex = condition.find("old(", startIndex + 1) + 4
                endIndex = condition.find(")", startIndex)
                oldIdentifier = condition[startIndex:endIndex]
                sourcecode += "oldValues['" + oldIdentifier + "'] = deepcopy(" + oldIdentifier +")\n"
                
        #Call proceed
        sourcecode += "__result__ = proceed(" + proceedParameters +")\n"

        #Check assertions
        for condition in args:           
            rewrittenCondition = condition
            while not rewrittenCondition.find("old(") == -1:
                #replace old(...) -> oldValues['...']
                indexStartOld = rewrittenCondition.find("old(")
                indexEndOld = rewrittenCondition.find(")", indexStartOld)
                rewrittenCondition = rewrittenCondition[:indexStartOld] + "oldValues['" + rewrittenCondition[indexStartOld + 4:indexEndOld] + "']" + rewrittenCondition[indexEndOld + 1:]                
            
            assertionMessage = condition
            sourcecode += "assert " + rewrittenCondition + ", \"" + assertionMessage + "\"\n"

        #Return proper result    
        sourcecode += "return __result__\n"
    
    return sourcecode    
    
def createSourceCodeFromTypes(parameters, *args, **kwargs):
    #Create source code for type checking
     
    sourcecode = ""
    numberOfTypeDescriptions = len(kwargs) - kwargs.has_key(LAYER_KEYWORD) - kwargs.has_key("__result__")
    if numberOfTypeDescriptions == 0 and len(args) == 0:
        sourcecode = "pass"
    else:    
        for entry in kwargs: 
            if entry == LAYER_KEYWORD:
                continue       
            sourcecode += "assert "
            assertionSourceCode = ""
            expectedTypes = ""
            
            for _typ in kwargs[entry]:           
                
                variableIdentifier = entry
                if entry == "__result__":
                    variableIdentifier = "kwargs['__result__']"
                
                #Class OR Type OR Class OR Type
                if type(_typ) == str:
                    # String Type Comparison (Otherwise it requires the import of the related Classes)                 
                    assertionSourceCode += "str(type(" +  variableIdentifier + ")) == \"" + _typ + "\""
                    expectedTypes += _typ
                elif type(_typ) == type:
                    typ = str(_typ)
                    typeStr = typ[typ.find("'")+1:typ.find("'", typ.find("'") + 1)]
                    assertionSourceCode += "isinstance(" + variableIdentifier + ", " + typeStr + ")"
                    expectedTypes += typeStr
                else:
                    #TODO: ERROR
                    pass
                assertionSourceCode += " or "
                expectedTypes += ", "
                
            #Remove last OR
            assertionSourceCode = assertionSourceCode[:-4]
            assertionMessage = "Wrong type of parameter " + entry + " (current type: \" + str(type(" + variableIdentifier + ")) + \") expected " + expectedTypes[:-2]
            
            sourcecode += assertionSourceCode + ", \"" + assertionMessage + "\"\n"
        
        if kwargs.has_key("__result__"):
            sourcecode += "return kwargs['__result__']\n"
        
    return sourcecode
                
# Common Decorator
def __common(sourceCodeFunction, standardLayer, when, *args, **kwargs):
 
    def decorator(method):   
                      
        symbolDict = {"proceed": cop.proceed, "deepcopy": copy.deepcopy, "NoneType": types.NoneType}
        parameters = getParametersFromMethod(method)

        func = createFunction(sourceCodeFunction(parameters, *args, **kwargs), parameters, symbolDict)

        #Class and static partial methods must be bound to their classes        
        if (type(method) in (classmethod, )):
            func = classmethod(func)
        elif (type(method) in (staticmethod, )):
            func = staticmethod(func)
        elif (issubclass(type(method), cop._layeredmethoddescriptor)):
            baseMethod = method.methods[0][1]
            if (type(baseMethod) in (classmethod, )):
                func = classmethod(func)
            elif (type(baseMethod) in (staticmethod, )):
                func = staticmethod(func)
        
        if (issubclass(type(method), cop._layeredmethoddescriptor)):
            method.registerMethod(func, 
                                  when, 
                                  lookUpLayerEntries(standardLayer, **kwargs), 
                                  cop._true, 
                                  cop.getMethodName(method))
            returnMethod = method
        else:
            returnMethod = createlayeredmethod(method, 
                                               [(lookUpLayerEntries(standardLayer, **kwargs), 
                                               func, 
                                               when, 
                                               cop._true, 
                                               cop.getMethodName(method))])
        return returnMethod
       
    return decorator

def require(*args, **kwargs):
    return __common(createSourceCodeFromStrings, requireLayer, cop._before, *args, **kwargs)

def ensure(*args, **kwargs):
    return __common(createEnsureSourceCodeFromStrings, ensureLayer, cop._around, *args, **kwargs)

def requireTypes(*args, **kwargs):
    return __common(createSourceCodeFromTypes, requireLayer, cop._before, *args, **kwargs)

def ensureTypes(*args, **kwargs):
    #Map types condition to return value
    if len(args) == 1:
        if isinstance(args[0], (list, tuple)):
            kwargs["__result__"] = args[0]
        else:
            kwargs["__result__"] = (args[0],)
    else:
        kwargs["__result__"] = args         
    return __common(createSourceCodeFromTypes, ensureLayer, cop._after, *args, **kwargs)

def __commonPartial(standardLayer, when, *args, **kwargs):

    vars = sys._getframe(2).f_locals

    def decorator(method):

        methodName = cop.getMethodName(method)
        currentMethod = vars.get(methodName)        

        if (issubclass(type(currentMethod), cop._layeredmethoddescriptor)):
            currentMethod.registerMethod(method, 
                                  when, 
                                  lookUpLayerEntries(standardLayer, **kwargs), 
                                  cop._true, 
                                  cop.getMethodName(method))
            returnMethod = currentMethod
        else:
            returnMethod = createlayeredmethod(currentMethod, 
                                               [(lookUpLayerEntries(standardLayer, **kwargs), 
                                               method, 
                                               when, 
                                               cop._true, 
                                               cop.getMethodName(method))])
        return returnMethod

    return decorator

def requireContract(*args, **kwargs):
    return __commonPartial(requireLayer, cop._before, *args, **kwargs)

def ensureContract(*args, **kwargs):
    return __commonPartial(ensureLayer, cop._around, *args, **kwargs)

class LayerDeactivationProxy(object):
    def __init__(self, inst, cls, layers, method):
        self.inst = inst
        self.cls = cls
        self.layers = layers
        self.method = method
        
    def __call__(self, *args, **kwargs):
        with (cop.disableAllLayer()):
            # Ensure AER for Design by Contract (no endless recursion)
            # Ignore all parameters so that only the self parameter is delivered
            self.method.__get__(self.inst, self.cls)()
            if kwargs.has_key("__result__"):
                return kwargs["__result__"]

class LayerDeactivationWrapper(object):
    def __init__(self, layers, method):
        self.layers = layers
        self.method = method
        
    def __get__(self, inst, cls = None):
        return LayerDeactivationProxy(inst, cls, self.layers, self.method)

class contracts(type):
        
    def __init__(self, name, base, members):
        super(contracts, self).__init__(name, base, members)
        if members.has_key("__invariants__"):
            for layers, method in members["__invariants__"]:
                invariantName = cop.getMethodName(method)
                wrappedMethod = LayerDeactivationWrapper(layers, method)
                
                for each in members:
                    if callable(members[each]) and not (each == invariantName or each == "__metaclass__"):
                        #Add invariant to each instance method in that class
                        if (issubclass(type(members[each]), cop._layeredmethoddescriptor)):  
                            if isinstance(members[each].methods[0][1], (classmethod, staticmethod)):
                                continue
                            members[each].registerMethod(wrappedMethod, cop._before, layers, cop._true, each)
                            members[each].registerMethod(wrappedMethod, cop._after, layers, cop._true, each)
                        else:
                            if isinstance(members[each], (classmethod, staticmethod)):
                                continue
                            partialMethod = createlayeredmethod(members[each], [(layers, wrappedMethod, cop._before, cop._true, each)])
                            partialMethod.registerMethod(wrappedMethod, cop._after, layers, cop._true, each)
                            setattr(self, each, partialMethod)                            
                               

def invariant(*args, **kwargs):
          
    vars = sys._getframe(1).f_locals
    # Evil hack that insert the metaclass through the backdoor
    if vars.has_key("__metaclass__"):
        raise Exception, "Cannot insert contracts metaclass since another metaclass still exists"
    vars.setdefault("__metaclass__", contracts)
    
    def decorator(method):
        layers = [invariantLayer]
        for layer in args:
            if isinstance(layer, cop.layer):
                layers.append(layer)
        
        vars.setdefault("__invariants__", []).append((layers, method))
        return method       

    return decorator
        




## Invariant Decorator
#def invariant(*args, **kwargs):
## Angabe des Layers
## ablegen der Invariante 
# 
# 
#    def decorator(method):   
#        
#        symbolDict = {"proceed": cop.proceed, "deepcopy": copy.deepcopy, "NoneType": types.NoneType}
#        parameters = getParametersFromMethod(method)
#              
#        func = createFunction(sourceCodeFunction(parameters, *args, **kwargs), parameters, symbolDict)
#
#        #Class and static partial methods must be bound to their classes        
#        if (type(method) in (classmethod, )):
#            func = classmethod(func)
#        elif (type(method) in (staticmethod, )):
#            func = staticmethod(func)
#        elif (issubclass(type(method), cop._layeredmethoddescriptor)):
#            baseMethod = method.methods[0][1]
#            if (type(baseMethod) in (classmethod, )):
#                func = classmethod(func)
#            elif (type(baseMethod) in (staticmethod, )):
#                func = staticmethod(func)
#        
#        if (issubclass(type(method), cop._layeredmethoddescriptor)):
#            method.registerMethod(func, 
#                                  when, 
#                                  lookUpLayerEntries(standardLayer, **kwargs), 
#                                  cop._true, 
#                                  cop.getMethodName(method))
#            returnMethod = method
#        else:
#            returnMethod = createlayeredmethod(method, 
#                                               [(lookUpLayerEntries(standardLayer, **kwargs), 
#                                               func, 
#                                               when, 
#                                               cop._true, 
#                                               cop.getMethodName(method))])
#        return returnMethod
#       
#    return decorator
