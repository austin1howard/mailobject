import mailobject

# Create an email object as below...MailObject(senderName,senderEmail,subject (optional)),
# and then keyword arguments from this list (defaults given):
#	smtp_host = 'localhost'
#	smtp_port = 0
#	smtp_ssl = False
#	smtp_tls = False
#	smtp_user = ''
#	smtp_pass = ''
# Note that senderEmail may be overwritten by the SMTP server,
# especially if it requires authentication (e.g., for gmail)

testmail = mailobject.MailObject('Adam George','adam@george.com','Demo Subject',
	smtp_host='smtp.gmail.com',smtp_user='me@gmail.com',smtp_pass='password',smtp_tls=True)

# Recipents can be added one at a time...
testmail.addRecipients('Bob Smith','bobsmith@gmail.com')

# Or in batches.
testmail.addRecipients(['Cecil Jones','David Smith'],['cecil@jones.com','david@smith.com'])

# Also text can be added one line at a time...
testmail.addText('You can put multiple lines')

# Or with \n characters.
testmail.addText('in separate commands, or\nin the string')

# Finally, add attachments one at a time...
testmail.addAttachments('/home/adam/firstfile')

# Or in batches.
testmail.addAttachments(['/home/adam/secondfile','/home/adam/thirdfile'])

# Finally, send everything with:
testmail.send()