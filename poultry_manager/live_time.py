"""
This module defines the `NetworkTime` class, which is responsible for retrieving the current time
from an NTP (Network Time Protocol) server. If the NTP server request fails, it falls back to the
local system time. The primary use case is to ensure that the system gets accurate network time
when available, and otherwise defaults to the local system time in UTC.

Dependencies:
    - datetime: For managing time and date objects.
    - ntplib: For making requests to an NTP server to retrieve network time.
"""

from datetime import datetime, timezone

import ntplib


class NetworkTime:
    """
        A class that retrieves the current time from an NTP (Network Time Protocol) server.
        If the request fails, it falls back to the local system time.
    """
    @staticmethod
    def network_time() -> datetime:
        """
            Retrieve the current time from the 'time.windows.com' NTP server.
           If the request to the server fails, the local system time is returned instead.

           Returns:
               datetime: The current time as a timezone-aware UTC datetime object.
        """
        try:
            # Create an NTP client instance
            client = ntplib.NTPClient()

            # Send a request to the NTP server and get the response
            response = client.request('time.windows.com', version=3)

            # Convert the NTP time (response.tx_time) to a UTC datetime object
            network_time = datetime.fromtimestamp(
                response.tx_time, timezone.utc)
            return network_time

        except Exception:
            # If an error occurs, fall back to the local system time in UTC
            network_time = datetime.now(timezone.utc)
            return network_time
