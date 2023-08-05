#
# Importing this module fixes ZSI to work with an caCORE SDK-based web service.
# 
import sys

from ZSI import ParsedSoap
from xml.dom import minidom

#from ZSI.wstools import logging
#logging.setLevel(logging.DEBUG)

debug = False

ns = 'http://webservice.system.nci.nih.gov'
nsa = 'ws'

class AxisReader:
    """ A drop-in replacement SOAP reader for ZSI which deals with some Axis 
        idiosyncrasies (meaning bugs!).
        
        Besides the XML mangling done here on the SOAP responses, the WSDL also 
        had to be modified in the following ways:
        
        1) Change extension base of HashMap to "anyType"
        2) Change namespace on all wsdl:output bodies to match the wsdl:input.
        3) Add namespace ws = http://webservice.system.nci.nih.gov
        4) Change namespace of schema containing ArrayOf_xsd_anyType to ws
        5) Change all instances of impl:ArrayOf_xsd_anyType to ws:ArrayOf_xsd_anyType
    """

    def fromString(self, input):
        dom = minidom.parseString(input, None)
        env = dom.childNodes[0]
        body = env.childNodes[0]
        
        if body.childNodes[0].nodeName == 'soapenv:Fault':
            return dom
        
        # functionResponse and functionReturn 
        response = body.childNodes[0]
        result = response.childNodes[0]
                
        # returning void
        if not(result.childNodes):
            return dom
        
        # returning a single scalar 
        if result.childNodes[0].nodeType == result.TEXT_NODE:
            return dom
        
        # Add namespace for ArrayOf_xsd_anyType
        a = dom.createAttributeNS('http://www.w3.org/2000/xmlns/','xmlns:'+nsa)
        a.value = ns
        env.setAttributeNodeNS(a)
        
        # returning a single anyType object
        if result.childNodes[0].nodeName != result.nodeName:
            result.namespaceURI = None
            fix_member_types(result, dom)
            return dom
        
        # If we got this far, it means we have an array on our hands, which
        # we need to fix, if it's going to get parsed correctly.
        fix_array(result, dom)
        
        if debug: print dom.toprettyxml()
        return dom
        
    def __call__(self, args):
        """ If this happens, we will need to implement whatever method is 
            needed. Until then... 
        """
        from exceptions import NotImplementedError
        raise NotImplementedError


def fix_array(node, dom):
    """ Fix bug in Axis which causes item nodes to be incorrectly named
        with the parent node name.
    """
    for item in node.childNodes:
        if item.nodeType == item.ELEMENT_NODE:
            dom.renameNode(item, None, 'item')
            item.localName = 'item'
            fix_member_types(item, dom)


def fix_member_types(item, dom):
    """ For associations, replace soapenc:Array with generated List type
    """
    for member in item.childNodes:
        if not(member): continue
        if member.childNodes and member.childNodes[0].localName == member.localName: 
            # Careful, this is a 2 step recursion
            fix_array(member, dom)
        if member.attributes:
            attr = member.attributes['xsi:type']
            if attr.value == 'soapenc:Array':
                attr.value = nsa+':ArrayOf_xsd_anyType'
    
    
class ZSIDebugStreamReader:

    def write(self, c):
        if not(c[0] == '<'): return
        dom = minidom.parseString(c, None)
        xml = dom.toprettyxml()
        sys.stderr.write(xml.encode('UTF-8'))


# Stealth fix for a bug in ZSI, reported as SF2006855:
# http://sourceforge.net/tracker/index.php?func=detail&aid=2006855&group_id=26590&atid=387667
# Remove all of this when the above bug is fixed in ZSI.
def parse(self, elt, ps):
    self.checkname(elt, ps)
    # Bug fix: check for nilled BEFORE looking for href
    if self.nilled(elt, ps): return None
    elt = self.SimpleHREF(elt, ps, 'boolean')
    if not elt: return None
    v = self.simple_value(elt, ps).lower()
    return self.text_to_data(v, elt, ps)

from ZSI.TC import Boolean
Boolean.parse = parse

