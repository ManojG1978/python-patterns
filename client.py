import requests
import pybreaker
from tenacity import retry, stop_after_attempt, wait_fixed
import time

TIMEOUT = 10   # Timeout in seconds
FAIL_MAX = 2    # Maximum number of failures before the circuit opens
REQUEST_TIMEOUT = 1  # Timeout for the HTTP request

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_info(message):
    print(f"{Colors.OKCYAN}{message}{Colors.ENDC}")


def print_warning(message):
    print(f"{Colors.WARNING}{message}{Colors.ENDC}")


def print_error(message):
    print(f"{Colors.FAIL}{message}{Colors.ENDC}")


def print_event(message):
    print(f"{Colors.OKCYAN}{message}{Colors.OKCYAN}")


def print_success(message):
    print(f"{Colors.OKGREEN}{message}{Colors.OKGREEN}")


# Custom listener for circuit breaker state changes with open duration tracking
class CircuitBreakerStateChangeListener(pybreaker.CircuitBreakerListener):
    def __init__(self):
        self.opened_at = None

    def state_change(self, cb, old_state, new_state):
        if new_state.name == "open":
            self.opened_at = time.time()
            print_event(
                f"Circuit breaker state changed from {old_state.name} to {new_state.name}")
        elif new_state.name in ["closed", "half_open"] and self.opened_at:
            duration_open = time.time() - self.opened_at
            print_event(
                f"Circuit breaker state changed from {old_state.name} to {new_state.name}. It was open for {duration_open:.2f} seconds.")
            self.opened_at = None


# Circuit breaker setup with the custom listener
circuit_breaker = pybreaker.CircuitBreaker(fail_max=FAIL_MAX,
                                           reset_timeout=TIMEOUT,
                                           listeners=[
                                               CircuitBreakerStateChangeListener()],
                                           name="HTTP GET Circuit Breaker")

# Decorator for wrapping functions with the circuit breaker


def circuit_breaker_decorator(func):
    def wrapper(*args, **kwargs):
        return circuit_breaker.call(func, *args, **kwargs)
    return wrapper


def after_retry(retry_state):
    print_warning(f"Attempt {retry_state.attempt_number} failed.")


def before_sleep(retry_state):
    print_warning(
        f"Retry {retry_state.attempt_number} failed. Waiting {retry_state.next_action.sleep} seconds before next attempt...")


# @retry(stop=stop_after_attempt(2),
#        wait=wait_fixed(3),
#        after=after_retry,
#        before_sleep=before_sleep)
# @circuit_breaker_decorator
def make_request_with_retry():
    response = requests.get("http://127.0.0.1:5000/", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def main():
    try:
        while True:
            try:
                response = make_request_with_retry()
                print_info(f"Success: {response}")
            except pybreaker.CircuitBreakerError:
                print_error(
                    "Circuit breaker is open. Halting calls to prevent failure.")
            except Exception as e:
                print_error(f"Failed to process request: {e}")
            time.sleep(2)  # Wait for 2 seconds before the next call
    except KeyboardInterrupt:
        print_error("Program terminated by user.")


if __name__ == "__main__":
    main()
