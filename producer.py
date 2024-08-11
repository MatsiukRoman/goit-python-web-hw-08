import json
import pika
from faker import Faker
from models import connect, Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

queue_name = 'web_16_queue'
exchange_name = 'web16_exchange'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name)

fake = Faker()

def generate_contacts(n):
    for _ in range(n):
        fullname = fake.name()
        email = fake.email()
        contact = Contact(fullname=fullname, email=email)
        contact.save()

        contact_id = str(contact.id)
        message = json.dumps({'contact_id': contact_id})
        channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=message)
        print(f'Contact {contact_id} - generated and sent to queue.')

        contact.sent = True
        contact.save()
        print(f'Contact {contact_id} marked as sent.')

if __name__ == '__main__':
    # Set the required number of contacts to generate
    number_of_contacts = 5  
    generate_contacts(number_of_contacts)
    connection.close()