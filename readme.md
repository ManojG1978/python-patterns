# Python API Client with Retry and Circuit Breaker

This project demonstrates the use of retry and circuit breaker patterns in a Python application that interacts with a web API. It's designed to handle transient failures and prevent overwhelming an already failing service, improving the robustness and reliability of the client application.

## Patterns Used

### Retry Pattern

The retry pattern is implemented using the `tenacity` library, which allows the client to automatically retry failed requests a configurable number of times, with a fixed wait interval between attempts. This pattern is useful for handling transient failures that are expected to resolve themselves after a short period.

### Circuit Breaker Pattern

The circuit breaker pattern is implemented with the `pybreaker` library. This pattern prevents the client from making requests to a service that's likely to fail, by "opening" the circuit breaker after a certain number of failures. Once open, further attempts to make requests are automatically blocked for a predefined timeout period, after which the circuit breaker allows a limited number of test requests to determine if the service has recovered.

## Getting Started

### Prerequisites

- Python 3.6+
- pip

### Installation and Running

1. Clone the repository:

```sh
   git clone https://your-repository-url-here
```

2. Navigate to the project directory:

```sh
   cd python-api-client-retry-circuit-breaker
```

3. Install the required Python packages (preferably in a virtual environment):

```sh
   pip install -r requirements.txt
```

4. Running the API

Start the Flask API server:

```sh
flask run
```

5. Running the Client
In a separate terminal window, run the client application:

```python
python client.py
```

#### Usage

The client application will continuously make requests to the Flask API every X seconds, automatically retrying upon failures and temporarily halting requests if the circuit breaker is triggered. The console will display messages in different colors based on the type of message: informational, warning, or error.

To stop the client, press *CTRL+C* in the terminal.
