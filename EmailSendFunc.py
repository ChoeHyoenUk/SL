import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders


def SendMail(image, text, title):
    me = 'mrbear6500@gmail.com'
    you = 'levy----@naver.com'
    contents = text

    msg = MIMEBase('multipart', 'mixed')
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = you
    main = MIMEText(contents)
    msg.attach(main)
    img = MIMEImage(image)
    msg.attach(img)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(me, 'qlalf!1234')
    s.sendmail(me, you, msg.as_string())
    s.close()
