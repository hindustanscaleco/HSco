import threading
from django.core.mail import EmailMessage, send_mail
from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
 
from django.http import HttpResponse
from django.template.loader import get_template
 
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
 
from xhtml2pdf import pisa  
#difine render_to_pdf() function

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content,sender, recipient_list,cc_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        self.cc_list = cc_list if cc_list else []

        threading.Thread.__init__(self)

    def run(self):
        try:
            msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list,cc=self.cc_list)
            msg.content_subtype = 'html'
            msg.send()
            print('email sent')
        except Exception as e:
            print(e)
            print('exception occured email not sent')
            pass


def send_html_mail(subject, html_content,sender, recipient_list,cc_list ):
    EmailThread(subject, html_content,sender, recipient_list,cc_list).start()

class Email_text_Thread(threading.Thread):
    def __init__(self, subject, message, sender,recipient,cc_list):
        self.subject = subject
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.cc_list = cc_list if cc_list else []
        threading.Thread.__init__(self)

    def run(self):
        try:
            msg = EmailMessage(self.subject, self.message, self.sender, self.recipient,cc=self.cc_list)
            msg.content_subtype = 'text'
            msg.send()

            print('email sent')
        except Exception as e:
            print(e)
            print('exception occured email not sent')
            pass


def send_text_mail(subject, message, sender, recipient,cc_list):
    Email_text_Thread(subject, message, sender, recipient,cc_list).start()


 
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
 
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None