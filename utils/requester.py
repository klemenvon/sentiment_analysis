from loguru import logger
import requests
import time

# --- Provides a rate limited request class ---
class Requester:
    RETRY_RESPONSES = [404, 408, 429, 500]
    def __init__(self, rate_limit=60, max_retries=5):
        """
        Rate limited request wrapper class.
        rate_limit (int): maximum requests this class will send out per minute
        max_retries (int): maximum number of retries on failed request
        """
        self.max_retries = max_retries
        self.base_interval = 60.0/float(rate_limit)
        self.interval = self.base_interval
        self.next_allowed_time = time.monotonic()

    def _calculate_backoff(self):
        """Do the backoff calculation for 429 responses."""
        # --- Exponential backoff ---
        if self.interval == self.base_interval:
            # Make sure that interval is > 1 to avoid shortening it
            self.interval = (1.0 + self.interval) ** 2
        else:
            self.interval **= 2
    
    def _time_to_next_request(self):
        """Calculates the time interval to the next allowed request window."""
        remainder = self.next_allowed_time - time.monotonic()
        return max(0.0, remainder)
    
    def _set_next_allowed_time(self, response_code):
        """Sets next allowed request timie based on the received response to the last request."""
        current_time = time.monotonic()

        # --- Adjust interval if necessary ---
        if response_code == 429:
            self._calculate_backoff()
            logger.debug(f"Backing off to interval of {self.interval}")
        else:
            self.interval = self.base_interval

        self.next_allowed_time = (
            max(current_time, self.next_allowed_time) + self.interval
        )
    
    def _make_request(self, *args, **kwargs):
        """Wrapper for requests.get() with a wait for rate limit and backoff seetup for 429 responses."""
        # --- Calculate the amount of time to next request window ---
        wait = self._time_to_next_request()
        if wait > 0.0:
            time.sleep(wait)
        
        # --- Send request ---
        response = requests.get(*args, **kwargs)

        # --- Set next allowed time based on response code ---
        self._set_next_allowed_time(response.status_code)

        return response
    
    def get(self, *args, **kwargs):
        """Wrapper for _make_requests with a retry condition."""
        retries = 0
        while retries < self.max_retries:
            try:
                response = self._make_request(*args, **kwargs)
                # --- Only retry if we hit a retriable response ---
                if response.status_code in self.RETRY_RESPONSES:
                    logger.debug(f"Request failed with response {response.status_code}. Retrying.")
                    continue
                # --- Otherwise return ---
                else:
                    return response
            except Exception as e:
                logger.error(f"Encountered exception: {e}")

            retries += 1
