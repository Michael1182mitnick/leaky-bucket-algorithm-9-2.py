# Leaky_Bucket_Algorithm
# Implement a rate limiter that limits the number of API requests a user can make within a specified time window. Use different algorithms like the Token Bucket or Leaky Bucket.
# Requests are processed at a fixed rate (like water leaking from a bucket).
# If requests come faster than the rate, excess requests are denied.
# This ensures a steady flow of requests without allowing bursts.

import time
from threading import Lock


class LeakyBucket:
    def __init__(self, rate, capacity):
        """
        Initialize the leaky bucket.

        :param rate: The rate at which requests are processed (requests per second).
        :param capacity: The maximum number of requests the bucket can hold.
        """
        self.rate = rate  # Rate at which requests are processed
        self.capacity = capacity  # Maximum requests in the bucket
        self.current_level = 0  # Current number of requests in the bucket
        self.last_checked = time.time()  # Last time requests were processed
        self.lock = Lock()  # To handle concurrency

    def allow_request(self):
        """
        Returns True if the request is allowed, otherwise False.
        """
        with self.lock:
            current_time = time.time()
            elapsed_time = current_time - self.last_checked

            # Process requests at the given rate
            leaked_requests = elapsed_time * self.rate
            self.current_level = max(0, self.current_level - leaked_requests)
            self.last_checked = current_time

            if self.current_level < self.capacity:
                self.current_level += 1
                return True
            else:
                return False


# Example Usage
if __name__ == "__main__":
    # 1 request/sec, max 5 requests
    rate_limiter = LeakyBucket(rate=1, capacity=5)

    for _ in range(10):
        if rate_limiter.allow_request():
            print("Request allowed")
        else:
            print("Request denied")
        time.sleep(0.5)
