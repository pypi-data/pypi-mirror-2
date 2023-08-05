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
from datetime import datetime
import iodef as iodef
import iodef.phish as phish

'''
  This routine builds an IODEf Incident structure.
  Default values are used for required feilds if not
  supplied. In heory, one could call this with a lot
  of arguments and be done. :)

  Running this script with these arguments will create a valid
  IODEF-Docuent:
  
    python -i sample_builder_phish_cheap.py --incident cain:002
    --ce 'paatt.ru' --ct 'person' -e "A description" -l 'la-pig'
    -u 'http://www.cn' --uc 67 -V --impact Silly:low:failed:extortion

  Running this script with these arguments will create a valid
  PhraudReport within an IODEF-Docuent:
  
    python -i sample_builder_phish_cheap.py --incident cain:002
    --ce 'paatt.ru' --ct 'person' -e "A description" -l 'la-pig'
    --uc 67 -u 'http://www.cn' -V --impact Silly:low:failed:extortion
    -P 


'''


if __name__ == '__main__':

  def usage():
    print "python sample_builder_phish_cheap.py "
    print "output XML to file:        [-o out.xml]"
    print "         --crime fraudType"
    print "ReportTime:         -r reportTime"
    print "Assessment/Impact:    [ --impact value:severity:completion:type]"
    print "IncidentID:         --incidentID name:identifier"
    print "Contact Type:         --ct (person,organization,ext-value)"
    print "Contact Name:         --cn contactName"
    print "Contact EMail:         --ce contactEmail"
    print "Contact Type:         --cr {creator,admin,tech,irt,cc,ext-value)"
    print "Language         -l language tag"
    print "         [-4 ipv4-addr]"
    print "         [-6 ipv6-addr]"
    print "         [-d dnsName]"
    print "SiteURL & conf:         [-u url --uc number]"
    print "Incident purpose:         [-p purpose]"
    print "Generate PhraudReport:         [-P ]"
    print "validate XML:     [-V ]"
    print "craft bad doc:    [-F]"
    

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
        "Do:r:4:6:d:u:p:e:l:VFP",
        ['debug','crime=','reportTime=','incidentID=', 'lang=', 'impact=',
         'ctype=', 'contact=', 'v4=', 'v6=', 'dnsName=', 'url=',
         'uc=', 'purpose=', 'ce=', 'cn=', 'ct=', 'cr=', 'description' ])
  # This is called a debugging line....
  #import pdb; pdb.set_trace()

  ''' Default values '''
  lang = 'en-US'
  crime = ''
  restriction = 'private'
  reportTime = datetime.utcnow().replace(microsecond=0).isoformat()
  incidentID = { 'unknown':0 }
  contactName = iodef.MLStringType.factory()
  contact = iodef.Contact.factory( type_='person', role='creator')
  urlConfidence = '67'
  doPhraudReport = False
  validate = False
  outfile = None
  fail = False

  ''' Do some sub-incident building first... '''


  ''' Let's build an incident: '''
  incident = iodef.Incident(
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

  
  phraudReport = phish.PhraudReport.factory(
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

  assessment = iodef.Assessment.factory()

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
      incidentId = iodef.IncidentIDType()
      incidentId.name, incidentId.valueOf_ = a.split(':')
      incident.IncidentID = incidentId
    elif o in ("--impact"):
      impact = iodef.Impact.factory()
      impact.valueOf_, impact.severity, impact.completion, impact.type = a.split(':')
      assessment.add_Impact( impact)
      assessment.exportS(0)
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
      fraudType = a
    elif o in ("-P"):
      doPhraudReport = True
    elif o in ("--ct"):
      contact.type_ = a
    elif o in ("--cn"):
      contact.add_ContactName(a)
    elif o in ("--cr"):
      contact.role = a
    elif o in ("--ce"):
      contactEmail = iodef.ContactMeansType.factory()
      contactEmail.valueOf_ = a
      contact.add_Email(contactEmail)
    elif o in ("-e", "--description"):
      desc = iodef.MLStringType.factory()
      desc.valueOf_ = a
      incident.add_Description( desc)
    else:
      usage()
      sys.exit()
  
 
  incident.add_Contact(contact)
  incident.add_Assessment(assessment) 
  
  ''' Build the PhraudReport, if asked '''
  if doPhraudReport:
    ad = iodef.ExtensionType.factory(dtype='xml')
    ad.setValueOf_( phraudReport)
    incident.add_EventData(ad)  

  ''' Now buld the IODEF-Document: '''
  doc = iodef.IODEF_Document.factory()
  doc.add_Incident(incident)
  doc.lang=lang
  if outfile:
    doc.export(outfile,0)
    outfile.close()
  import pdb; pdb.set_trace()    
  bob = doc.exportS(0)

  ''' Should we validate it? '''

  if validate:
    from lxml import etree
    ''' First load the schema '''
    if doPhraudReport:
      if sys.platform in ['win32', 'cygwin']:
        schdoc = etree.parse('draft-cain-post-inch-phishingextns-07-win.xsd')
      else:
        schdoc = etree.parse('draft-cain-post-inch-phishingextns-07.xsd')        
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



