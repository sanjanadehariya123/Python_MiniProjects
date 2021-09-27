import os
import sys
import mimetypes
import email
from email import policy
from email.parser import BytesParser
from fpdf import FPDF

pdf = FPDF()

output_count = 0

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

od=__location__+'attach'

oPdf=__location__+'/pdf'

os.path.exists(od) or os.makedirs(od)

os.path.exists(oPdf) or os.makedirs(oPdf)

with open(__location__+'/mail.eml', 'rb') as fp:
    msg = BytesParser(policy=policy.default).parse(fp)
    
with open(os.path.join(oPdf, 'mail.txt'), "w") as txtOut:
    txtOut.write('To: {}\n'.format(msg['to']))
    txtOut.write('From: {}\n'.format(msg['from']))
    txtOut.write('Subject: {}\n'.format(msg['subject']))
    simpleBody = msg.get_body(preferencelist=('plain', 'html'))
    txtOut.write('\n')
    txtOut.write(''.join(simpleBody.get_content().splitlines(keepends=True)))
    txtOut.write('Attachments:\n')
    
    for attachment in msg.iter_attachments():
        output_filename = attachment.get_filename()
        
        if output_filename:
            output_count += 1
            txtOut.write('Attachment {}: {}\n'.format(output_count,output_filename))
            
            with open(os.path.join(od, output_filename), "wb") as of:
                of.write(attachment.get_payload(decode=True))
        
        if output_count == 0:
            txtOut.write("No attachment found")
            
pdf = FPDF()

pdf.add_page()

pdf.set_font("Courier", size = 11)

file = open(os.path.join(oPdf, 'mail.txt'))

for g in file:
    pdf.cell(200, 10, txt = g, ln = 1, align = 'L')
    
pdf.output(os.path.join(oPdf,'PDF.pdf'))
