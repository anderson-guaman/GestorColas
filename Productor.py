import pika


def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='cola_correos')

    channel.basic_publish(exchange='',
                          routing_key='cola_correos',
                          body=message)
    print(" [x] Sent %r" % message)

    connection.close()


# Enviar un mensaje
send_message('Hola, este es el primer mensaje')
