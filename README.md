# Kafka Order Event Pipeline

A small event-driven distributed system built using Apache Kafka, Python, Docker, Docker Compose, Pytest, and GitHub Actions.

## Project Overview

This project demonstrates a simple **event-driven order processing pipeline** using Apache Kafka.

The system consists of a Python Producer that generates mock order events and publishes them to a Kafka topic named `orders`. A Python Consumer subscribes to the topic, receives the events, processes the orders, and displays the processed order details.

The complete application runs using Docker Compose. Automated tests are executed using Pytest through GitHub Actions, and a GitHub branch ruleset ensures that the required CI check passes before changes can be merged.

---

## Architecture

```text
                    KAFKA ORDER EVENT PIPELINE
                    ==========================

                         DOCKER COMPOSE
              ┌───────────────────────────────────┐
              │                                   │
              │      ┌─────────────────────┐      │
              │      │      PRODUCER       │      │
              │      │    Python Service   │      │
              │      │                     │      │
              │      │  Creates Order      │      │
              │      │  Events             │      │
              │      └──────────┬──────────┘      │
              │                 │                 │
              │                 │ JSON Order      │
              │                 │ Event           │
              │                 ▼                 │
              │      ┌─────────────────────┐      │
              │      │    APACHE KAFKA     │      │
              │      │     Kafka Broker    │      │
              │      │                     │      │
              │      │   Topic: orders     │      │
              │      └──────────┬──────────┘      │
              │                 │                 │
              │                 │ Kafka Message   │
              │                 ▼                 │
              │      ┌─────────────────────┐      │
              │      │      CONSUMER       │      │
              │      │    Python Service   │      │
              │      │                     │      │
              │      │  Group:             │      │
              │      │  order-processors   │      │
              │      └──────────┬──────────┘      │
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                                │ Process Order
                                ▼
                     ┌─────────────────────┐
                     │   PROCESSED ORDER   │
                     │                     │
                     │   Status: PROCESSED │
                     │   Output / Logging  │
                     └─────────────────────┘


                 ─────── CI / CD PIPELINE ───────

                     ┌───────────────────┐
                     │  GitHub Repository│
                     └─────────┬─────────┘
                               │
                    Push / Pull Request
                               │
                               ▼
                     ┌───────────────────┐
                     │   GitHub Actions  │
                     │                   │
                     │   Python 3.11     │
                     │   + Pytest        │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │   4 Automated     │
                     │      Tests        │
                     └─────────┬─────────┘
                               │
                         ┌─────┴─────┐
                         │           │
                      PASS ✓       FAIL ✗
                         │           │
                         ▼           ▼
                 ┌────────────┐  ┌────────────┐
                 │  Branch    │  │   Merge    │
                 │  Ruleset   │  │   Blocked  │
                 │            │  │            │
                 │ Merge      │  │ Tests must │
                 │ Allowed    │  │ pass first │
                 └────────────┘  └────────────┘
```

---

## System Workflow

The system follows this workflow:

1. The Producer creates a mock order.
2. The Producer converts the order into a JSON event.
3. The event is published to the Kafka `orders` topic.
4. The Kafka broker stores and delivers the message.
5. The Consumer receives the order event.
6. The Consumer processes the order.
7. The processed order is displayed in the Consumer logs.
8. GitHub Actions automatically runs the automated tests whenever code is pushed or a pull request is created.
9. The branch ruleset requires the CI check to pass before changes can be merged.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Producer and Consumer applications |
| Apache Kafka 3.9.1 | Event/message broker |
| Docker | Containerization |
| Docker Compose | Running multiple services |
| Pytest | Automated testing |
| GitHub Actions | Continuous Integration |
| GitHub Branch Ruleset | Merge protection |

---

## Project Structure

```text
kafka-order-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── producer/
│   └── producer.py
│
├── consumer/
│   └── consumer.py
│
├── tests/
│   └── test_orders.py
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Producer

The Producer is a Python application that generates sample order events.

Example order:

```json
{
  "order_id": 101,
  "product": "Laptop",
  "amount": 55000
}
```

The Producer sends these events to the Kafka topic:

```text
orders
```

Example Producer output:

```text
Sent: {'order_id': 101, 'product': 'Laptop', 'amount': 55000}
Sent: {'order_id': 102, 'product': 'Mouse', 'amount': 1200}
Sent: {'order_id': 103, 'product': 'Keyboard', 'amount': 2500}

All orders sent successfully!
```

---

## Kafka

Apache Kafka acts as the **message broker** in the system.

The Producer publishes order events to the:

```text
orders
```

Kafka topic.

The Consumer subscribes to this topic and receives the published messages.

The Consumer uses the following consumer group:

```text
order-processors
```

This demonstrates asynchronous communication between independent services.

---

## Consumer

The Consumer is a Python application that listens to the Kafka `orders` topic.

When an order is received, it extracts the order information and processes it.

Example:

```text
Received Order:
Order ID: 101
Product: Laptop
Amount: ₹55000
Status: PROCESSED
```

---

## Docker Configuration

Docker Compose is used to run the system components together.

The project contains the following containers:

```text
Kafka Broker
     │
     ├── Producer Container
     │
     └── Consumer Container
```

Docker provides an isolated and reproducible environment for running the distributed application.

---

## How to Run

### Prerequisite

Install Docker Desktop and make sure Docker is running.

### 1. Start Kafka and Consumer

Open the project folder in the terminal and run:

```bash
docker compose up -d kafka consumer
```

This starts the Kafka broker and Consumer containers.

### 2. Run the Producer

In the same project directory, run:

```bash
docker compose run --rm producer
```

The Producer will generate and publish the sample orders.

### 3. View Consumer Output

Run:

```bash
docker compose logs -f consumer
```

You should see the Consumer receiving and processing the orders.

Example:

```text
Consumer started. Waiting for orders...

Received Order:
Order ID: 101
Product: Laptop
Amount: ₹55000
Status: PROCESSED
```

---

## Testing

The project contains **4 automated test cases** using Pytest.

### Test Cases

#### Test 1 — Required Order Fields

Checks that an order contains:

- `order_id`
- `product`
- `amount`

#### Test 2 — Order ID Type

Checks that the order ID is an integer.

#### Test 3 — Product Type

Checks that the product name is a string.

#### Test 4 — Positive Amount

Checks that the order amount is greater than zero.

### Run Tests

The tests can be executed using Docker:

```bash
docker run --rm -v "${PWD}:/app" -w /app python:3.11-slim sh -c "pip install -q pytest && python -m pytest tests"
```

Expected result:

```text
collected 4 items

tests/test_orders.py ....                                                [100%]

4 passed
```

---

## GitHub Actions CI/CD

The project uses GitHub Actions for automated testing.

The workflow is located at:

```text
.github/workflows/ci.yml
```

The workflow runs when:

- Code is pushed to the repository.
- A pull request is created or updated.

The workflow:

1. Checks out the repository.
2. Starts a Python 3.11 environment.
3. Installs Pytest.
4. Runs all automated tests.
5. Reports whether the tests passed or failed.

Example successful result:

```text
4 passed
```

---

## Branch Ruleset

A GitHub branch ruleset is configured for the main branch.

The ruleset requires:

- Pull requests before merging.
- The required `test` status check to pass.
- The branch to be up to date before merging.

If the required tests fail, the required CI check does not pass and the protected branch cannot be merged until the issue is fixed.

This provides a basic **quality gate** for the project.

---

## Distributed Systems Concepts Demonstrated

### 1. Event-Driven Architecture

The Producer and Consumer communicate through events sent through Kafka rather than directly communicating with each other.

### 2. Message Broker

Kafka acts as the intermediary message broker between the Producer and Consumer.

### 3. Asynchronous Communication

The Producer publishes an event without directly invoking the Consumer.

### 4. Topic-Based Messaging

Order events are published to the Kafka topic:

```text
orders
```

### 5. Consumer Groups

The Consumer uses the group:

```text
order-processors
```

This demonstrates Kafka's consumer-group mechanism.

### 6. Containerization

The Kafka broker and Python services are run using Docker containers managed by Docker Compose.

### 7. Continuous Integration

GitHub Actions automatically validates the project by running the automated test suite.

---

## Advantages

- Loose coupling between Producer and Consumer.
- Asynchronous event processing.
- Reliable message-based communication.
- Easy local deployment using Docker Compose.
- Automated testing.
- Continuous integration through GitHub Actions.
- Branch-level quality control.

---

## Demonstrated Result

The complete pipeline was successfully tested using Docker.

The Producer generated three sample orders:

```text
Order 101 → Laptop → ₹55000
Order 102 → Mouse → ₹1200
Order 103 → Keyboard → ₹2500
```

The Consumer successfully received and processed the order events.

The automated test suite also completed successfully:

```text
4 passed
```

---

## Learning Objectives

This project provides hands-on experience with:

- Distributed systems
- Event-driven architecture
- Apache Kafka
- Producer-Consumer communication
- Message brokers
- Kafka topics
- Consumer groups
- Docker containerization
- Docker Compose
- Automated testing
- GitHub Actions
- CI/CD concepts
- Branch protection and quality gates

---

## Conclusion

The Kafka Order Event Pipeline demonstrates how independent services can communicate through an event-driven architecture using Apache Kafka.

The project combines a Python Producer, Kafka Broker, and Python Consumer inside a Docker Compose environment. Automated Pytest cases and GitHub Actions provide continuous validation, while the GitHub branch ruleset adds an additional quality-control mechanism.

This project demonstrates the practical use of distributed-system concepts through a small, reproducible, and testable event-processing pipeline.

---

## Author

**Vaibhav Rawat**

B.Tech Computer Science & Engineering