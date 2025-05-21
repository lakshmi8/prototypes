package com.lakshmi8;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectionPool {

    private BoundedBlockingQueue<Connection> queue;

    // Attempts to create a new DB connection
    private Connection createNewConnection() {
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

    // Retry connection creation up to a fixed number of times
    private Connection tryCreateConnectionWithRetries(int retries) {
        Connection connection = null;
        while (retries-- > 0 && connection == null) {
            connection = createNewConnection();
            if (connection == null) {
                System.err.println("Could not establish a connection. Retrying...");
            }
        }
        return connection;
    }

    // Constructor initializes the queue and pre-fills it with connections
    public ConnectionPool(int capacity) {
        this.queue = new BoundedBlockingQueue<>(capacity);

        for (int i = 0; i < capacity; i++) {
            int retries = 3;
            Connection connection = tryCreateConnectionWithRetries(retries);
            if (connection != null) {
                this.queue.enqueue(connection);
            } else {
                System.err.println("Failed to initialize connection after retries. Skipping...");
            }
        }

        System.out.println("Successfully initialized " + queue.size() + " connections");
    }

    // Fetch a connection from the pool (blocking if none are available)
    public Connection getConnection() {
        return this.queue.dequeue();
    }

    // Return a connection back to the pool
    public void returnConnection(Connection connection) {
        this.queue.enqueue(connection);
    }

    // Shutdown the pool by closing all available connections in the queue
    public void shutdown() {
        System.out.println("Shutting down connection pool...");
        while (queue.size() > 0) {
            Connection connection = queue.dequeue();
            if (connection != null) {
                try {
                    connection.close();
                    System.out.println("Closed connection: " + connection);
                } catch (SQLException e) {
                    System.err.println("Failed to close connection: " + e.getMessage());
                }
            }
        }
        System.out.println("Connection pool shutdown complete.");
    }
}
