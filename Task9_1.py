"""
Implement the [dining philosophers problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem).
Try synchronization primitives and fix deadlock
"""

from threading import Thread, Lock
import time
import random


class PhilosopherThread(Thread):
    status = True

    def __init__(self, number, fork_left: Lock, fork_right: Lock):
        super().__init__()
        self.number = number
        self.fork_left = fork_left
        self.fork_right = fork_right

    def run(self):
        while self.status:
            self.think()
            self.diner()

    def diner(self):
        while self.status:
            self.fork_left.acquire()
            locked = self.fork_right.acquire(False)
            if locked:
                break
            self.fork_left.release()
        else:
            return
        self.eat()
        self.fork_left.release()
        self.fork_right.release()

    def think(self):
        print(f'Philosopher {self.number} starts thinking...')
        thinking_sec = random.randint(3, 5)
        time.sleep(thinking_sec)
        print(f'Philosopher {self.number} thinks for {thinking_sec} seconds')

    def eat(self):
        print(f'Philosopher {self.number} starts eating...')
        eating_sec = random.randint(3, 10)
        time.sleep(eating_sec)
        print(f'Philosopher {self.number} eats for {eating_sec} seconds')


def main():
    forks = [Lock() for i in range(5)]
    philosophers = [PhilosopherThread(i, forks[i % 5], forks[(i + 1) % 5]) for i in range(1, 6)]
    PhilosopherThread.status = True
    for philosopher in philosophers:
        philosopher.start()
    time.sleep(100)
    PhilosopherThread.status = False


if __name__ == "__main__":
    main()
