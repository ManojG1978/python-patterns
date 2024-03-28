import time
import random


class CircuitBreaker:
    """
    A simple circuit breaker class.
    """

    def __init__(self, failure_threshold, reset_time):
        """
        Initialize the circuit breaker.

        Args:
            failure_threshold: The number of failures before opening the circuit.
            reset_time: The time (in seconds) to wait before attempting to reset.
        """
        self.failure_threshold = failure_threshold
        self.reset_time = reset_time
        self._state = "CLOSED"  # Initial state
        self._failed_attempts = 0
        self._last_failure_time = None

    def call(self, func):
        """
        Executes the wrapped function while applying circuit breaker logic.

        Args:
            func: The function to be wrapped.

        Returns:
            The result of the wrapped function if successful, otherwise raises an exception.
        """

        if self._state == "OPEN":
            # Circuit is open, raise an exception
            raise CircuitBreakerOpen("Circuit is currently open")
        elif self._state == "HALF_OPEN":
            # Circuit is half-open, attempt to reset and call the function
            self._try_reset()
            try:
                return func()
            except Exception as inner_exc:
                self._handle_failure(inner_exc)
                raise  # Replicate the raised exception

        # Circuit is closed, proceed normally
        try:
            result = func()
            self._success()
            return result
        except Exception as inner_exc:
            self._handle_failure(inner_exc)
            raise  # Replicate the raised exception

    def _try_reset(self):
        """
        Attempts to reset the circuit breaker if enough time has passed.
        """
        current_time = time.time()
        if self._last_failure_time is None or (current_time - self._last_failure_time) >= self.reset_time:
            self._state = "CLOSED"
            self._failed_attempts = 0
            self._last_failure_time = None

    def _handle_failure(self, exc):
        """
        Handles a failure by incrementing the failure count and potentially opening the circuit.
        """
        self._failed_attempts += 1
        self._last_failure_time = time.time()
        if self._failed_attempts >= self.failure_threshold:
            self._state = "OPEN"

    def _success(self):
        """
        Resets the failure count upon a successful call.
        """
        self._failed_attempts = 0


class CircuitBreakerOpen(Exception):
    """
    Custom exception raised when the circuit breaker is open.
    """
    pass


# Example usage
def protected_function():
    # Simulate some operation that might fail
    if random.random() < 0.2:
        raise ValueError("Simulated failure")
    return "Success"


failure_threshold = 5
reset_time = 10  # 10 seconds

circuit_breaker = CircuitBreaker(failure_threshold, reset_time)

while True:
    try:
        result = circuit_breaker.call(protected_function)
        print(result)
    except CircuitBreakerOpen:
        print("Circuit breaker is open, waiting...")
        time.sleep(reset_time + 1)  # Wait for reset time plus some buffer
    except Exception as e:
        print(f"An error occurred: {e}")
