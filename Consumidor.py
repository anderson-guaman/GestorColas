import os
import pika
import smtplib
from email.mime.text import MIMEText

def send_email(body):
    from_email = os.getenv('andersonguaman2002@gmail.com')
    to_email = 'anderson.guaman@udla.edu.ec'
    subject = 'Mensaje desde RabbitMQ'
    password = os.getenv('tu_contraseña')

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, [to_email], msg.as_string())
            print("Email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    send_email(body.decode())

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#channel.queue_declare(queue='cola_correos')

channel.basic_consume(queue='InformativeAlarms',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
