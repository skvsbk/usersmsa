import json
from abc import ABC, abstractmethod
from kafka import KafkaProducer

from .. import settings


class Publisher(ABC):
    """Interface for concrete publishers"""
    @abstractmethod
    def attach(self, subscriber):
        pass

    @abstractmethod
    def detach(self, subscriber):
        pass

    @abstractmethod
    def notify(self):
        pass


class Subscriber(ABC):
    """Interface for concrete subscribers"""
    @abstractmethod
    def update(self, publisher):
        pass


class KafkaProducerSubscriber(Subscriber):
    """Subscriber for sending message by Kafka"""
    def update(self, publisher):
        try:
            producer = KafkaProducer(bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                     value_serializer=lambda m: json.dumps(m).encode('ascii'))
            producer.send(topic=settings.KAFKA_TOPIC_PRODUCER,
                          value=publisher.value,
                          key=publisher.key.encode())
            KafkaError().set_error(publisher.key, False)
        except Exception as e:
            # Write some log record
            KafkaError().set_error(publisher.key, True)

class PostPublisher(Publisher):
    """Publisher for notify concrete subscribers"""
    def __init__(self):
        self._observers = []
        self.key = None
        self.value = None

    def attach(self, subscriber):
        self._observers.append(subscriber)

    def detach(self, subscriber):
        self._observers.remove(subscriber)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def change_state(self, key, value):
        self.key = key
        self.value = value
        self.notify()


class KafkaError:

    _error = {}


    def get_error(self, key):
        return self._error.get(key)

    def set_error(self, key, value):
        self._error.update({key: value})
