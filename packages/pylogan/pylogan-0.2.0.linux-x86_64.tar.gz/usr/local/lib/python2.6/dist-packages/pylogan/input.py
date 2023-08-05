#!/usr/bin/python
# -*- coding: utf-8 -*-


import string
import re
import time


class SyslogLine(object):
  """Structural class for every line
  
  It happend to be a struct to accomodate a line data after exploding the string
  """
  def __init__(self,line_timestamp,src_host,src_process,process_data):
    self.timestamp=line_timestamp
    self.host=src_host
    self.process=src_process
    self.data=process_data
    
  def IsTheProcess(self,the_process):
    """Check for source process
    
    Used to discard lines that not belongs to a specific process
    """
    return string.find(self.process,the_process)>-1


class Syslog(object):
  """Base class for syslog input
  
  Contains attributes and methods that belongs to syslog, it isolates the "process data" for later processing
  """
  def __init__(self,log_year=2010):
    self._year=log_year
    self.syslog_format=re.compile('^(\w*\s\d*\s\d*:\d*:\d*)\s(\w*)\s([\w\[\]]*):(.*)')
    self.start_timestamp=False
    self.end_timestamp=False
    self.lines=[]
   
  def SourceFile(self,logfile):
    """The syslog file to use
    
    Just open the file for reading
    """
    self.file = open(logfile)
    
  def ParseLine(self,the_line):
    """Build a SyslogLine object for the_line
    
    It explodes the line and builds a SyslogLine object that returns
    """
    line_result=re.match(self.syslog_format,the_line)
    if line_result:
      line_timestamp=time.mktime(time.strptime('%d %s' % (self._year, line_result.group(1)),'%Y %b %d %H:%M:%S'))
      line_obj=SyslogLine(line_timestamp,line_result.group(2),line_result.group(3),string.strip(line_result.group(4)))
      return line_obj
    else:
      return False

  def PopulateLines(self,the_process=False):
    """Reads and parses all the lines in the file
    
    It uses the already opened file to read every line and parses it into SyslogLines storing it in self.lines
    """
    line=self.file.readline()
    last_line=None
    while not line == '':
      line_result=self.ParseLine(line)
      if line_result:
	if not self.start_timestamp:
	  self.start_timestamp=line_result.timestamp
	if the_process:
	  if line_result.IsTheProcess(the_process):
	    self.lines.append(line_result)
	else:
	  self.lines.append(line_result)
	last_line=line_result
      line=self.file.readline()
    self.file.close()
    self.end_timestamp=last_line.timestamp
    return self.lines


class Squid(Syslog):
  """Input class for line processing
  
  It's the base class for manipulating the data related to squid stored in the syslog file
  """
  def __init__(self):
    super(Squid,self).__init__()
    self.squid_format=re.compile('[\d\.]*\s*\d*\s(\d*\.\d*\.\d*\.\d*)\s(\w*/\d{3})\s(\d*)\s(GET|POST|CONNECT|HEAD)\s(.*)\s(\w*)\s\w*/\d*\.\d*\.\d*\.\d*.*')
    
  def ExplodeData(self):
    """Parses all SyslogLines in self.lines
    
    Used to process the squid data after the use of PopulateLines
    """
    last_index=len(self.lines)
    for line_index in range(last_index-1,-1,-1):
      self.lines[line_index]=self.ParseSquid(self.lines[line_index])
      if not self.lines[line_index]:
	del(self.lines[line_index])
    return self.lines
    
  def ParseSquid(self,the_line):
    """Get squid related data from SyslogLine.data
    
    Using re module gets the traffic data from already built SyslogLines
    """
    result=re.match(self.squid_format,the_line.data)
    if result:
      the_line.sourceIp=result.group(1)
      the_line.squidEvent=result.group(2)
      the_line.size=result.group(3)
      the_line.method=result.group(4)
      the_line.url=result.group(5)
      the_line.user=result.group(6)
      del(the_line.data)
      return the_line
    else:
      return False
      
  def Lines(self):
    """'The' method to use
    
    This is the only method needed in the regular use, it calls the PopulateLines to parse de syslog file and later ExplodeData to get the squid info from that lines
    """
    self.PopulateLines('squid')
    self.ExplodeData()
    return self.lines
