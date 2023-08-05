# Sample_builder_phish_cheap.py:
#
# pcain@antiphishing.org -  March 32 2010
#
# This file generates an IODEF-Document from a bunch of command
# line arguments. The resultant document is only an IODEF-Document,
# no other lbnraries (e.g., phish) were used.
#
# Some (cheap) people who don't want to fill out a whole PhraudReport
# can use this script to generate (cheap) phishing reports.
#

import sys, getopt
from datetime import datetime, tzinfo, timedelta
import StringIO
import iodef.base
from iodef.phish import phish


'''
  This routine builds an IODEf Incident structure.
  Default values are used for required feilds if not
  supplied. In heory, one could call this with a lot
  of arguments and be done. :)

  Running this script with these arguments will create a valid
  IODEF-Docuent:
  
    python -i sample_builder_phish_cheap.py --incident cain:002
    --ce 'paatt@home.org' --ct 'person' -e "A description" -l 'la-pig'
    --url 'http://www.example.us' --uc 67 -V --impact Silly:low:failed:extortion

  Running this script with these arguments will create a valid
  PhraudReport within an IODEF-Docuent:
  
    python -i sample_builder_phish_cheap.py --incident cain:002
    --ce 'paat@at.home' --ct 'person' -e "A description" -l 'la-pig'
    --uc 67 --url 'http://www.example.con' -V --impact Silly:low:failed:extortion
    -P  --crime phishing --lure I:192.168.1.13

  Note: As the intent is to provide a means to finidh your code, some
        liberties are taken in the content of some elements and attributes.

'''


if __name__ == '__main__':

  def usage():
    print "python sample_builder_phish_cheap.py "
    print "output XML to file:        [-o out.xml]"
    print ""
    print "Base IODEF-Document elements:"
    print ""
    print "  ReportTime:         -r reportTime"
    print "  Assessment/Impact:  [ --impact value:severity:completion:type]"
    print "  Incident purpose:   [-p purpose]"
    print "  IncidentID:         --incidentID name:identifier"
    print "  Contact Type:       --ct (person,organization,ext-value)"
    print "  Contact Name:       --cn contactName"
    print "  Contact EMail:      --ce contactEmail"
    print "  Contact Type:       --cr {creator,admin,tech,irt,cc,ext-value)"
    print "  Language            -l language tag"
    print "         [-4 ipv4-addr]"
    print "         [-6 ipv6-addr]"
    print "         [-d dnsName]"
    print ""
    print "PhraudReport elements:"
    print "  FraudType:           --crime fraudType"
    print "  SiteURL & conf:      [--uc number --url url ]"
    print "  Lure Source:         --lure  type:IP or DNS"
    print "    type is I or D for IP or DNS"

    print "Important flags:"
    print "  Generate PhraudReport:         [-P ]"
    print "  validate XML:     [-V ]"
    print "  craft bad doc:    [-F]"
    print ""

    print "A proper IODEF-Document requires:"
    print " (a) a crime time, (b) a reporter-unique identifer,"
    print " (c) a contact type and name, (d) miscreant address info"
    print " (e) other stuff like dnsName or IPAddress"
    print " The other fields get defaults. :p"
    print " "
    print " A PhraudReport REQUIRES a crime type,a URL, and a confidence"
    print " value."
    print " "
    
  opts, args = getopt.getopt( sys.argv[1:],
        "Do:r:4:6:d:p:e:l:VFP",
        ['debug','crime=','reportTime=','incidentID=', 'lang=', 'impact=',
         'ctype=', 'contact=', 'v4=', 'v6=', 'dnsName=', 'url=', 'lure=',
         'uc=', 'purpose=', 'ce=', 'cn=', 'ct=', 'cr=', 'origsen=',
         'description' ])
  # This is called a debugging line....
  #import pdb; pdb.set_trace()

  class GMT0(tzinfo):
    def utcoffset(self, dt):
      return timedelta(hours=0)
  class EST(tzinfo):
    def utcoffset(self, dt):
      return timedelta(hours=-5)

  ''' Default values '''
  lang = 'en-US'
  crime = ''
  restriction = 'private'
  reportTime = datetime.utcnow().replace(microsecond=0, tzinfo=GMT0()).isoformat()
  incidentID = { 'unknown':0 }
  contactName = iodef.base.MLStringType.factory()
  contact = iodef.base.Contact.factory( type_='person', role='creator')
  assessment = iodef.base.Assessment.factory()
  lureSource = phish.LureSource_type.factory()
  # DateFirstSeen is the same time as ReportTime but different tz
  origsensor = phish.OriginatingSensor_type.factory(
    DateFirstSeen=datetime.now().replace(microsecond=0, tzinfo=EST()).isoformat())
  urlConfidence = '67'
  doPhraudReport = False
  validate = False
  outfile = None
  fail = False

  ''' Do some sub-incident building first... '''
#  import pdb; pdb.set_trace()           # DEBUG

  osDNS = iodef.base.MLStringType.factory()
  osDNS.valueOf_ = 'unknown'
  osNode = iodef.base.Node()
  osNode.NodeName.append(osDNS)
  osSystem = iodef.base.System()
  osSystem.set_Node(osNode)
  origsensor.add_System( osSystem)
  origsensor.set_OriginatingSensorType('human')

  ''' Let's build an incident: '''
  incident = iodef.base.Incident(
      restriction=restriction,
      purpose='other',
      IncidentID=None,
      AlternativeID=None,
      RelatedActivity=None,
      DetectTime=None,
      StartTime=None,
      EndTime=None,
      ReportTime=reportTime,
      Description=None,
      Assessment=[],
      Method=None,
      Contact=None,
      EventData=None,
      History=None,
      AdditionalData=None)

  
  phraudReport = iodef.phish.phish.PhraudReport.factory(
      ext_value=None, Version='1.0',
      FraudType=None,
      PhishNameRef=None, 
      PhishNameLocalRef=None,
      FraudParameter=None,
      FraudedBrandName=None,
      LureSource=None,
      OriginatingSensor=None,
      EmailRecord=None,
      DCSite=None,
      TakeDownInfo=None,
      ArchivedData=None,
      RelatedData=None,
      CorrelationData=None,
      PRComments=None)

  ''' Now add whatever we got called with. '''
  
  debug = False
  for o, a in opts:
    if o == "-D":
      debug = True
    elif o == "-V":
      validate = True
    elif o == "-F":
      fail = True
    elif o in ("-l", "--lang"):
      lang = a
      ''' Language actually set when we craft the IODEF-Document '''
    elif o in ("-r", "--reportTime"):
      incident.ReportTime = a
    elif o in ("--incidentID"):
      incidentId = iodef.base.IncidentIDType()
      incidentId.name, incidentId.valueOf_ = a.split(':')
      incident.IncidentID = incidentId
    elif o in ("--impact"):
      impact = iodef.base.Impact.factory()
      impact.valueOf_, impact.severity, impact.completion, impact.type = a.split(':')
      assessment.add_Impact( impact)
    elif o in ("-4", "--v4"):
      v4addr = a
    elif o in ("-6", "--v6"):
      v6addr = a
    elif o in ("-d", "--dnsName"):
      dnsName = a
    elif o in ("-u", "--url"):
      dcSite = phish.DCSite_type.factory()
      dcSite.DCType = 'web'
      surl = phish.SiteURL.factory()
      surl.lang=lang
      surl.valueOf_ = a
      surl.confidence = urlConfidence
      dcSite.set_SiteURL(surl)
      phraudReport.add_DCSite(dcSite)
    elif o in ("--uc"):
      urlConfidence = a
    elif o in ("-p", "--purpose"):
      incident.purpose = a
    elif o == "-o":
      outfile = open(a,'w')
    elif o in ("--crime"):
      phraudReport.FraudType = a
    elif o in ("-P"):
      doPhraudReport = True
    elif o in ("--ct"):
      contact.type_ = a
    elif o in ("--cn"):
      contact.add_ContactName(a)
    elif o in ("--cr"):
      contact.role = a
    elif o in ("--ce"):
      contactEmail = iodef.base.ContactMeansType.factory()
      contactEmail.valueOf_ = a
      contact.add_Email(contactEmail)
    elif o in ("--lure"):
      # A LureSource is either a DNSName or IPAddress
      lureSystem = iodef.base.System.factory()
      lureNode = iodef.base.Node.factory()
      lureType, lureValue = a.split(':')
      if lureType is 'I':
        nodeAd = iodef.base.Address.factory()
        nodeAd.valueOf_ = lureValue
        nodeAd.category = 'ipv4-addr'
        lureNode.add_Address(nodeAd)
      elif lureType is 'D':
        lureDNS = iodef.base.MLStringType.factory()
        lureDNS.valueOf_ = lureValue
        lureNode.NodeName.append(lureDNS)
      else:
        print "Bad LureSource Type"
        exit (0)
      lureSystem.set_Node( lureNode)
      lureSystem.set_spoofed( 'yes')
      lureSource.add_System( lureSystem)
      phraudReport.LureSource.append(lureSource)
    elif o in ("--origsen"):
      import pdb; pdb.set_trace()           # DEBUG
      osType, osValue = a.split(':')
      osAd = iodef.base.Address.factory()
      osAd.valueOf_ = osValue
      osAd.category = 'ipv4-addr'
      osSystem = iodef.base.System.factory()
      osNode = iodef.base.Node.factory( Address=nodeAd)
      osSystem.set_Node( osNode)
      origsensor.set_System(osSystem)
      origsensor.set_OriginatingSensorType('unknown')
    elif o in ("-e", "--description"):
      desc = iodef.base.MLStringType.factory()
      desc.valueOf_ = a
      incident.add_Description( desc)
 
    else:
      usage()
      sys.exit()
  
 
  incident.add_Contact(contact)
  if not fail:
    incident.add_Assessment(assessment)
  phraudReport.OriginatingSensor.append(origsensor)
    
  
  ''' Build the PhraudReport, if asked '''
  if doPhraudReport:
    et = iodef.base.ExtensionType.factory(dtype='xml')
    et.setValueOf_( phraudReport)
    ad = iodef.base.EventData.factory()
    ad.add_AdditionalData(et)
    incident.add_EventData(ad)  

  ''' Now buld the IODEF-Document: '''
  doc = iodef.base.IODEF_Document.factory()
  doc.add_Incident(incident)
  doc.lang=lang
  import pdb; pdb.set_trace()    
  if outfile:
    doc.export(outfile,0)
    outfile.close()

  outString = StringIO.StringIO()
  doc.export(outString, 0)
  bob = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n" + outString.getvalue()
  outString.close()
  
  ''' Should we validate it? '''

  if validate:
    from lxml import etree
    ''' First load the schema '''
    if doPhraudReport:
      if sys.platform in ['win32', 'cygwin']:
        schdoc = etree.parse('iodef-phish-1.0-win.xsd')
      else:
        schdoc = etree.parse('iodef-phish-1.0.xsd')        
    else:
      schdoc = etree.parse('iodef-1.0.xsd')
    schema = etree.XMLSchema(schdoc)
    ''' Parse and validate the examlpe doc.
        Validate will reutrn  'true' is validation suceeds.
    '''
    xmldoc=etree.fromstring(bob)
    if  not schema.validate(xmldoc):
      ''' This will print out the errors. '''
      schema.assertValid(xmldoc)
    else:
      print "WooHoo!!\n"
  
  pass



