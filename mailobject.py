### Library to easily send emails through smtp server
import smtplib
import base64
from os.path import basename

class MailObject:
	smtp_host = 'localhost'
	smtp_port = 0
	smtp_ssl = False
	smtp_tls = False
	smtp_user = ''
	smtp_pass = ''
	recipAddressList = []
	recipNameList = []
	senderAddress = ''
	senderName = ''
	subject = ''
	bodyText = ''
	isAttachment = False
	attachmentFilenames = [] # List of strings for the files
	attachmentData = [] # List of base64 encoded data
	uniqueMarker = '4aEa22517196fCCb6247B8483f05eFaf'
	
	def applyOnlyIfExists(self,kwargs):
		for key, value in kwargs.iteritems():
			# Check to make sure that the var is already in your class:
			try:
				getattr(self,key)
				# If here, it exists, so set the new value
				setattr(self,key,value)
			except:
				# It wasn't there, so do nothing
				pass
	
	def __init__(self,sendername,senderaddress,subject = '',**kwargs):
		self.senderName = sendername
		self.senderAddress = senderaddress
		self.subject = subject
		self.applyOnlyIfExists(kwargs)

	def _addSingleRecip(self,recipname,recipaddress):
		self.recipNameList.append(recipname)
		self.recipAddressList.append(recipaddress)	

	def addRecipients(self,recipname,recipaddress):
		"""recipname and recipaddress can be either lists or a single string"""
		if type(recipname) == type([]):
			for i,n in enumerate(recipname):
				self._addSingleRecip(n,recipaddress[i])
		else:
			self._addSingleRecip(recipname,recipaddress)

	def addRecipient(self,recipname,recipaddress):
		"""simply removes plural from function name"""
		self.addRecipients(recipname,recipaddress)
	
	def addText(self,text):
		self.bodyText = '%s\n%s' % (self.bodyText, text)
	
	def _addSingleAttachment(self,filename):
		# Read a file and encode it into base64 format
		self.isAttachment = True
		file = open(filename, "rb")
		filecontent = file.read()
		encodedcontent = base64.b64encode(filecontent)  # base64
		self.attachmentFilenames.append(filename)
		self.attachmentData.append(encodedcontent)
	
	def addAttachments(self,filename):
		if type(filename) == type([]):
			for i,f in enumerate(filename):
				self._addSingleAttachment(f)
		else:
			self._addSingleAttachment(filename)

	def addAttachment(self,filename):
		"""simply removes plural from function name"""
		self.addAttachments(filename)
	
	def send(self):
		# Header section
		formattedRecips=''
		for i,n in enumerate(self.recipNameList):
			formattedRecips='%s %s <%s>,' % (formattedRecips,n,self.recipAddressList[i])
		header  = 'From: %s <%s>\n' % (self.senderName,self.senderAddress)
		header += 'To: %s\n' % formattedRecips
		header += 'Subject: %s\n' % self.subject
		header += 'MIME-Version: 1.0\n'
		header += 'Content-Type: multipart/mixed; boundary=\"%s\"\n' % self.uniqueMarker
		header += '\n\nThis is a multi-part message in MIME format.\n'
		header += '--%s\n' % self.uniqueMarker
		
		# Message section
		message  = 'Content-Type: text/plain; charset=iso-8859-1\n'
		message += 'Content-Transfer-Encoding: 8bit\n'
		message += '%s' % self.bodyText
		
		# Attachment section
		# First, are there any attachments?
		if self.isAttachment:
			# Now loop through the attachments
			attachments = '\n\n--%s' % self.uniqueMarker
			for i,n in enumerate(self.attachmentFilenames):
				attachments += '\nContent-Type: application/octet-stream; name=\"%s\"\n' % basename(n)
				attachments += 'Content-Transfer-Encoding: base64\n'
				attachments += 'Content-Disposition: attachment; filename=\"%s\"\n\n' % basename(n)
				attachments += '%s\n\n' % self.attachmentData[i]
				attachments += '--%s' % self.uniqueMarker
			attachments += '--\n'
		else:
			attachments = '\n\n--%s--\n' % self.uniqueMarker
		
		# Make the entire email:
		email = header + message + attachments
		
		# Send it!
		if self.smtp_ssl:
			# Port 465 most likely, unless otherwise specified at __init__
			if self.smtp_port == 0:
				self.smtp_port = 465
			smtpObj = smtplib.SMTP_SSL(self.smtp_host,self.smtp_port)
		elif self.smtp_tls:
			# Port 587 most likely, unless otherwise specified at __init__
			if self.smtp_port == 0:
				self.smtp_port = 587
			smtpObj = smtplib.SMTP(self.smtp_host,self.smtp_port)
			smtpObj.ehlo()
			smtpObj.starttls()
			smtpObj.ehlo()
		else:
			# Port 25 most likely, unless otherwise specified at __init__
			if self.smtp_port == 0:
				self.smtp_port = 25
			smtpObj = smtplib.SMTP(self.smtp_host,self.smtp_port)
		
		if self.smtp_user != '':
			smtpObj.login(self.smtp_user, self.smtp_pass)
		
		smtpObj.sendmail(self.senderAddress, self.recipAddressList, email)