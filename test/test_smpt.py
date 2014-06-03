import json
import smtplib

# Constants
marker = "AUNIQUEMARKER"
sender = 'ami@amilab.com'
receivers = ['diana.tatu@gmail.com']
body ="""This is a test email to send an attachement."""

# Attachment data
filename = '/home/diana/ami/amilab-basis/test/measurements_sample.json'
fo = open(filename, "rb")
image64 = json.loads(fo.read()).get('image_rgb', {}).get('image', '')

# Define the main headers.
part1 = """From: From Person <ami@amilab.com>
To: Diana Tatu <diana.tatu@gmail.com>
Subject: [IMPORTANT] Tracked person may be in danger!
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, image64, marker)
message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"
