from . import observer


publisher_posts_list = observer.PostPublisher()
publisher_posts_author_list = observer.PostPublisher()
publisher_post_author = observer.PostPublisher()
publisher_posts_with_author_list = observer.PostPublisher()

kafka_producer_subscriber = observer.KafkaProducerSubscriber()

publisher_posts_list.attach(kafka_producer_subscriber)
publisher_posts_author_list.attach(kafka_producer_subscriber)
publisher_post_author.attach(kafka_producer_subscriber)
publisher_posts_with_author_list.attach(kafka_producer_subscriber)
