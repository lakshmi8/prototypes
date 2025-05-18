package com.lakshmi8;

import java.util.LinkedList;

public class BoundedBlockingQueue<T> {
    private final LinkedList<T> queue;
    private final int capacity;

    public synchronized void enqueue(T element) {
        while (size() == capacity) {
            try {
                wait();
            } catch(InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        queue.addLast(element);
        System.out.println("Enqueued " + element);
        notifyAll();
    }

    public synchronized T dequeue() {
        while (queue.isEmpty()) {
            try {
                wait();
            } catch(InterruptedException e) {
                Thread.currentThread().interrupt();
                return null;
            }
        }
        T element = queue.removeFirst();
        System.out.println("Dequeued " + element);
        notifyAll();
        return element;
    }

    public int size() {
        return queue.size();
    }

    public BoundedBlockingQueue(int capacity) {
        queue = new LinkedList<>();
        this.capacity = capacity;
    }

    public static void main(String[] args) {
        BoundedBlockingQueue<String> stringBoundedBlockingQueue = new BoundedBlockingQueue<>(10);

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
