package com.lakshmi8;

import java.sql.Connection;

public class Main {

    public static void main(String[] args) {

        int poolCapacity = 10;
        ConnectionPool connectionPool = new ConnectionPool(poolCapacity);

        int numThreads = 200;
        for (int i = 0; i < numThreads; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    // Acquire a connection from the pool
                    Connection connection = connectionPool.getConnection();
                    try {
                        // Simulate work using the connection
                        Thread.sleep(100);
                    } catch(InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    // Return the connection to the pool
                    connectionPool.returnConnection(connection);
                }
            }, "Thread-" + (i + 1)).start();
        }

        // Delay to allow threads to complete before shutting down the pool
        try {
            Thread.sleep(5000); // adjust if needed
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Shut down the connection pool and release all resources
        connectionPool.shutdown();

        /*
        // The following solution won't scale beyond 151 threads as MySQL doesn't support creating more than 151 DB connections (in my system).
        int numThreads = 152;
        for (int i = 0; i < numThreads; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Connection connection = null;
                    try {
                        connection = createNewConnection();
                        if (connection == null) {
                            System.err.println(Thread.currentThread().getName() + " could not establish a connection.");
                            return;
                        }
                        Thread.sleep(10000);
                        System.out.println(Thread.currentThread().getName() + " has finished its task");

                    } catch (InterruptedException interruptedException) {
                        System.err.println(Thread.currentThread().getName() + " was interrupted.");
                        interruptedException.printStackTrace();
                    } finally {
                        if (connection != null) {
                            try {
                                connection.close();
                                System.out.println(Thread.currentThread().getName() + " closed the connection.");
                            } catch (SQLException sqlException) {
                                sqlException.printStackTrace();
                            }
                        }
                    }
                }
            }, "Thread-" + (i + 1)).start();
        }*/
    }
}
