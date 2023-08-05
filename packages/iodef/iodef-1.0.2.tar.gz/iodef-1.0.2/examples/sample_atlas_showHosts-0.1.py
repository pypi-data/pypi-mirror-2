# A program to pull data from an 'ARBOR-ATLAS' XML file
# pcain@antiphishing.org - March 2010
#
# This is a python script to decode an arbor atlas report
# iodef-encoded file and return the host data. If called
# directly, the decoded data is printed on stdout.
#
# For each event record, we pull;
#   - impact type
#   - host address
#   - system category

import sys, getopt
from xml.dom import minidom

from iodef import common as iodef


def decode_node(nod):
  event = {}
  for add in nod.get_Address():
    evt = {}
    evt['Address'] = add.getValueOf_()
    evt['Role'] = syt.get_category()
    event['Flow'].append(evt)
  for cnt in nod.get_Counter():
    event['Flow']['Counter'].append(cnt.get_Counter()[0].getValueOf_()) 
    event['Flow']['Units'].append(cnt.get_Counter()[0].get_type()) 
  return event

def process_Assessment(node):
  for ind in node:
    if ind.has_key('iodef:Impact'):
      ine = ind['iodef:Impact']
      return #ine['type']
  return False

def decode_EventData_dos(ev):
  event = {}
  if ev.get_DetectTime(): event['DetectTime'] = ev.get_DetectTime()
  if ev.get_StartTime(): event['StartTime'] = ev.get_StartTime()
  if ev.get_EndTime(): event['EndTime'] = ev.get_EndTime()
  exp = ev.get_Expectation()
  event['Expectation']= exp[0].get_action()
  event['Description'] = exp[0].get_Description()[0].getValueOf_()
  event['Flow'] = []
  # An EventData may have multiple Flow elements
  for flo in ev.get_Flow():
    # A Flow may have multiple System elements
    for syt in flo.get_System():
      # A System may only have one Node element
      nod = syt.get_Node()
      # Nodes can has 0ne Name or many Addresses and other stuff
      event['Flow'].append(decode_node(nod))
  return event

def decode_EventData_recon(ev):
  event = {}
  exp = ev.get_Expectation()
  event['Expectation']= exp[0].get_action()
  event['Description'] = exp[0].get_Description()[0].getValueOf_()
  event['Flow'] = []
  # An EventData may have multiple Flow elements
  for flo in ev.get_Flow():
    # A Flow may have multiple System elements
    for syt in flo.get_System():
      # A System may only have one Node element
      nod = syt.get_Node()
      # Nodes can has 0ne Name or many Addresses
 
  
  return event


if __name__ == '__main__':

  def usage():
    print "python sample_atlas.py [-o output-file] input-file.xml"


  opts, args = getopt.getopt(sys.argv[1:], "o:", ["output"])
  # This is called a debugging line....
#  import pdb; pdb.set_trace()
  output = ''
  for o, a in opts:
    if o == "-o":
      output = open(a)
    else:
      usage()
#  incident = printDict.xmltodict(args[0])     
#  if output:
#    output.write( incident)
  # Some example things: (they may not work in all docs)
  
  # Note that we need to do a 'build' if we want to use the
  # iodef get_* routines. Kind of like this:


  # we redo the parse just to show the whole thing....
  doc = minidom.parse(args[0]) 
  rootNode = doc.documentElement
  rootObj = iodef.IODEF_Document.factory()
  rootObj.build(rootNode)

  stuff = []
  iIndex = 0
  evIndex = 0
  for inc in rootObj.get_Incident():
    iIndex+=1

    # This is the return structure. 
    istuff = {}
    # Get the Assessment
    assm = inc.get_Assessment()
    # Although one can have multiple Assessments, we only do one.
    if assm:
      assmt = assm[0].get_Impact()
      # True for Impact, too. 
      istuff['ImpactType'] = ImpactType = assmt[0].get_type()   

    for ent in inc.get_EventData():
      evIndex+=1
      for flow in ent.get_Flow():
        for syt in flow.get_System():
          istuff['category'] = syt.get_category()
          node = syt.get_Node()
          istuff['Address'] = []
          for addr in node.get_Address():
            istuff['Address'].append( addr.getValueOf_())
          if node.get_Location():
            istuff['Location'] = []
            loc = node.get_Location()
            istuff['Location'].append(dict(lang=loc.lang))
            istuff['Location'].append(loc.valueOf_)
          if node.get_Counter():
            counter = node.get_Counter()
            istuff['Counter'] = []
            istuff['Counter'].append(dict(type=counter[0].type_))
            istuff['Counter'].append(counter[0].valueOf_)
      stuff.append(istuff)

  print "we found %d events in %d incidents."%(evIndex,iIndex)
  print "The stuff we found:"
  for goo in stuff:
    print goo
        
      
