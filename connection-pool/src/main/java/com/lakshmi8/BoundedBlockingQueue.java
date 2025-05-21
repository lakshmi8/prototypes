package com.lakshmi8;

import java.util.LinkedList;

public class BoundedBlockingQueue<T> {
    private final LinkedList<T> queue;
    private final int capacity;

    // Constructor initializes the queue with a given capacity
    public BoundedBlockingQueue(int capacity) {
        queue = new LinkedList<>();
        this.capacity = capacity;
    }

    // Adds an element to the queue, blocks if the queue is full
    public synchronized void enqueue(T element) {
        while (size() == capacity) {
            try {
                wait(); // wait for space to become available
            } catch(InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        queue.addLast(element);
        System.out.println("Enqueued " + element);
        notifyAll(); // notify waiting threads
    }

    // Removes and returns the head element, blocks if the queue is empty
    public synchronized T dequeue() {
        while (queue.isEmpty()) {
            try {
                wait(); // wait for an item to be available
            } catch(InterruptedException e) {
                Thread.currentThread().interrupt();
                return null;
            }
        }
        T element = queue.removeFirst();
        System.out.println("Dequeued " + element);
        notifyAll(); // notify waiting threads
        return element;
    }

    // Returns the current size of the queue
    public int size() {
        return queue.size();
    }

    // Main method for testing with String type
    public static void main(String[] args) {
        BoundedBlockingQueue<String> stringBoundedBlockingQueue = new BoundedBlockingQueue<>(10);

        // Spawn 20 producer threads
        for (int i = 0; i < 20; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    stringBoundedBlockingQueue.enqueue(Thread.currentThread().getName());
                    try {
                        Thread.sleep(100);
                    } catch(InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            }, "ProducingThread-" + (i + 1)).start();
        }

        // Spawn 20 consumer threads
        for (int i = 0; i < 20; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    String dequeuedElement = stringBoundedBlockingQueue.dequeue();
                    try {
                        Thread.sleep(100);
                    } catch(InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            }, "ConsumingThread-" + (i + 1)).start();
        }
    }
}