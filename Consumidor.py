import pika
import smtplib
from email.mime.text import MIMEText

def send_email(body):
    from_email = 'andersonguaman2002@gmail.com'
    to_email = 'anderson.guaman@udla.edu.ec'
    subject = 'Mensaje desde RabbitMQ'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail(from_email, [to_email], msg.as_string())
        print("Email sent!")

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    send_email(body.decode())

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
