import logging
import time

import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger("Requester")
logger.setLevel(logging.INFO)


class Requester:
    RETRY_STATUSES = {408, 429, 500}
    BACKOFF_STATUS = 429

    def __init__(
        self, rate_limit: int = 60, max_retries: int = 5, timeout: float = 10.0, session: requests.Session | None = None
    ) -> None:
        """
        :param rate_limit: max requests per minute
        :param max_retries: how many times to retry on RETRY_STATUSES
        :param timeout: per-request network timeout (seconds)
        """
        self.max_retries = max_retries
        self.timeout = timeout

        self.rate_limit = rate_limit
        self.base_interval = 60.0 / self.rate_limit
        self.interval = self.base_interval
        self.next_allowed = time.monotonic()

        self.session = session or requests.Session()
        adapter = HTTPAdapter()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _time_to_wait(self) -> float:
        return max(0.0, self.next_allowed - time.monotonic())

    def _calculate_backoff(self) -> None:
        # simple exponential backoff with aggressive start
        if self.interval < 1.1:
            self.interval += 2.0
        else:
            self.interval **= 2

    def _update_next_allowed(self, status: int) -> None:
        now = time.monotonic()
        if status == self.BACKOFF_STATUS:
            self._calculate_backoff()
            logger.debug(f"429 received, backing off to {self.interval:.2f}s")
        else:
            self.interval = self.base_interval

        self.next_allowed = max(now, self.next_allowed) + self.interval

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        # respect rate limit
        wait = self._time_to_wait()
        if wait > 0:
            time.sleep(wait)

        # enforce timeout
        logger.debug(f"Requesting {method} {url} with timeout {self.timeout}")
        resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        self._update_next_allowed(resp.status_code)
        return resp

    def get(self, url: str, **kwargs) -> requests.Response | None:
        """
        Issue a GET, retrying on specified status codes.
        Returns the first non-retryable response, or the last response if
        all retries are exhausted.
        """
        last_resp = None

        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self._request("GET", url, **kwargs)
                last_resp = resp

                if resp.status_code in self.RETRY_STATUSES:
                    logger.debug(
                        f"Attempt {attempt}/{self.max_retries} for {url} returned {resp.status_code}, retrying..."
                    )
                    continue

                return resp

            except requests.RequestException as e:
                logger.error(f"Attempt {attempt}/{self.max_retries} error: {e}")
                last_resp = None

        logger.error(f"All {self.max_retries} attempts failed for {url}")
        return last_resp
