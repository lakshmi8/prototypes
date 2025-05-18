package com.lakshmi8;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Main {

    private static Connection createNewConnection() {
        String jdbcUrl =  "jdbc:mysql://localhost:3306/prototype_db";
        String username = System.getenv("DB_USER");
        String password = System.getenv("DB_PASSWORD");

        if (username == null || password == null) {
            System.err.println("Database credentials are not set in the environment");
            return null;
        }

        try {
            Connection connection = DriverManager.getConnection(jdbcUrl, username, password);
            System.out.println("Returning a connection object");
            return connection;
        } catch (SQLException sqlException) {
            System.err.println("Connection could not be established");
            return null;
        }
    }

    public static void main(String[] args) {

        int queueCapacity = 10;
        BoundedBlockingQueue<Connection> queue = new BoundedBlockingQueue<>(queueCapacity);

        for (int i = 0; i < queueCapacity; i++) {
            Connection connection = createNewConnection();
            if (connection == null) {
                System.err.println("Could not establish a connection.");
            }
            queue.enqueue(connection);
        }
        int numThreads = 200;
        for (int i = 0; i < numThreads; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Connection connection = queue.dequeue();
                    try {
                        Thread.sleep(100);
                    } catch(InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    queue.enqueue(connection);
                }
            }, "Thread-" + (i + 1)).start();
        }

        /*
        // The following solution won't scale beyond 151 threads as MySQL doesnt support creating more than 151 DB connections (atleast in my system).
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