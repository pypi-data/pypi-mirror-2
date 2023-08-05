import os
from Cheetah.Template import Template

def generate(services, settings, baseDir):
    
    template_path = os.path.dirname(__file__)
    
    serviceClassName = [s for s in dir(services) if s.endswith('ServiceLocator')][0]
    serviceName = serviceClassName[:-7]
    
    locator = getattr(services, serviceClassName)
    portName = [s for s in dir(locator) if s.endswith('_address')][0][:-8]
    
    arrayTypeNS = None
        
    nsdefs = [getattr(services,n) for n in dir(services) if n.startswith('ns')]
    for nsdef in nsdefs:
        nsname = nsdef.targetNamespace
        if not(nsname.startswith('urn:')): 
            if 'ArrayOf_xsd_anyType_Def' in [c for c in dir(nsdef)]:
                arrayTypeNS = nsdef
            continue
        
        p = nsname[4:].split('.') # remove "urn:" prefix
        p.reverse()
        name = '.'.join(p)
        
        if name not in settings.PACKAGE_MAPPING: 
            print "No package mapping for %r, skipping." % name
            continue

        # TODO: split these loops into two so that we can check for this type everwhere
        if not(arrayTypeNS):
            raise Exception('No namespace defines ArrayOf_xsd_anyType_Def.')
    
        ns = Namespace(name,nsdef.__name__) 
        for classdef in [getattr(nsdef,c) for c in dir(nsdef) if c.endswith('_Def')]:
            classname = classdef.type[1]
            clazz = Class(classname)
            ns.classes.append(clazz)
            for attrdef in classdef(None).ofwhat:
                if attrdef.__class__.__name__.endswith("Mirage"):
                    if attrdef.klass == arrayTypeNS.ArrayOf_xsd_anyType_Def:
                        a = Association(attrdef.pname, True) 
                    else:
                        a = Association(attrdef.pname, False)
                    clazz.associations.append(a)
                else:
                    clazz.attributes.append(Attribute(attrdef.pname))
        
        pkg = settings.PACKAGE_MAPPING[name].split('.')
        pkg[-1] += '.py'
        path = [baseDir] + pkg
        filepath = os.path.join(*path)
        
        tfile = os.path.join(template_path,'domain.tmpl')
        dict = {'serviceName' : serviceName,
                'prefix' : settings.ROOT_PACKAGE,
                'ns' : ns,
                'arrayTypeNS' : arrayTypeNS.__name__,
                }
        t = Template(file=tfile, searchList=[dict])
        file = open(filepath,"w")
        file.write(str(t));
        file.close()
    
    d = dir(services)
    reqdefs = [getattr(services,a) for a in d if "RequestTypecode" in a]
    resdefs = [getattr(services,a) for a in d if "ResponseTypecode" in a]
    functions = {}
    
    for req in reqdefs:
        function = Function(req.pname)
        functions[function.name] = function
        for what in req.ofwhat:
            param = Parameter(what.pname, what.type[1])
            function.params.append(param)
        
    for res in resdefs:
        name = res.pname[:res.pname.find("Response")]
        function = functions[name]
        function.type = res.ofwhat[0].type[1]
    
    tfile = os.path.join(template_path,'service.tmpl')
    dict = {'ZSI_serviceName' : serviceName,
            'ZSI_portName' : portName,
            'prefix' : settings.ROOT_PACKAGE,
            'serviceClassName' : settings.SERVICE_CLASS_NAME,
            'modules' : settings.PACKAGE_MAPPING.values(),
            'functions' : functions.values(),
            }
    t = Template(file=tfile, searchList=[dict])
    file = open(os.path.join(baseDir,"service.py"),"w")
    file.write(str(t));
    file.close()


class Function:
    def __init__(self, name):
        self.name = name
        self.uname = name[0].capitalize() + name[1:]
        self.params = []
        self.type = None
        
    def getParamList(self):
        plist = ['self']
        plist += list([p.name for p in self.params])
        return ', '.join(plist)
    
    def isObject(self):
        return "anyType" in self.type
    
    def isArray(self):
        return "Array" in self.type

class Parameter:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def isObject(self):
        return "anyType" in self.type
    
class Namespace:
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema
        self.classes = []
        
class Class:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.associations = []

class Association:
    def __init__(self, name, isCollection=False):
        self.name = name
        self.isCollection = isCollection
        self.uname = name[0].capitalize() + name[1:]

class Attribute:
    def __init__(self, name):
        self.name = name
        self.uname = name[0].capitalize() + name[1:]
        
        
if __name__ == '__main__':
    import CaBioWSQueryService_services as services
    t = generate(services)
    file = open("cabio.py","w")
    file.write(str(t));
    file.close()
    print "Code generated"

