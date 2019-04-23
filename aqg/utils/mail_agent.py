import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
class mail_agent:
    def mail_pdf(self,Email, name_of_file = "question_answer_output.pdf", flag=0) :
        fromaddr = "####<--Your_Email-->####"
        toaddr = Email

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        if flag == 0:
            msg['Subject'] = "PDF of Question Answer."
        elif flag == 1:
            msg['Subject'] = "PDF of Summarized Text. "

        body = "Please Check for Attachments."

        msg.attach(MIMEText(body, 'plain'))

        filename = name_of_file
        attachment = open(name_of_file, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "####<--Your_password-->####")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()


    def mail_txt(self,email_id, name_of_file = "one.txt") :
        fromaddr = "####<--Your_Email-->####"
        toaddr = email_id

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Question Answer of Txt "

        body = "Please Check for Attachments."

        msg.attach(MIMEText(body, 'plain'))

        filename = name_of_file
        attachment = open(name_of_file, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "####<--Your_password-->####")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
