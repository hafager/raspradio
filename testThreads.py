from threading import Thread
from queue import Queue
from time import sleep

class Producer(Thread):
    def __init__(self, queue):
        super(Producer, self).__init__()
        self.queue = queue

    def run(self):
        for i in range(10):
            self.queue.put(i)
            print("Added {} to the queue.".format(i))
            sleep(5)
        self.queue.put(None)

# Creates a class that inherits from Thread
class Consumer(Thread):
    def __init__(self, queue):
        super(Consumer, self).__init__()
        self.queue = queue

    # Overwrites the run() method in Thread
    def run(self):
        while True:
            item = self.queue.get()
            if item is None:
                break
            print("Found {} in the queue.".format(item))
            self.queue.task_done()

if __name__ == '__main__':
    queue = Queue()
    producer = Producer(queue)
    consumer = Consumer(queue)

    # Starts the thread and calls run()
    consumer.start()
    producer.start()
