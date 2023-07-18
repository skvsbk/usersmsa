import json
from abc import ABC, abstractmethod
from kafka import KafkaProducer

from .. import settings


class Publisher(ABC):
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
    @abstractmethod
    def update(self, publisher):
        pass


class KafkaProducerSubscriber(Subscriber):

    def update(self, publisher):
        producer = KafkaProducer(bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))

        producer.send(topic=settings.KAFKA_TOPIC_PRODUCER,
                      value=publisher.value,
                      key=publisher.key.encode())


class PostPublisher(Publisher):
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
