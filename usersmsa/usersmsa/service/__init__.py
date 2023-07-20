from . import transmitters


publisher_posts_list = transmitters.PostPublisher()
publisher_posts_author_list = transmitters.PostPublisher()
publisher_post_author = transmitters.PostPublisher()
publisher_posts_with_author_list = transmitters.PostPublisher()

kafka_producer_subscriber = transmitters.KafkaProducerSubscriber()

publisher_posts_list.attach(kafka_producer_subscriber)
publisher_posts_author_list.attach(kafka_producer_subscriber)
publisher_post_author.attach(kafka_producer_subscriber)
publisher_posts_with_author_list.attach(kafka_producer_subscriber)
