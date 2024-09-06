"""
live_time.py

This module provides a class `NetworkTime` that includes a static method
for fetching the current time from an NTP server. If the NTP server request
fails, it falls back to the local system time.

Keyword arguments:
- None

Return:
- datetime: The current network time if available, otherwise local time.
"""

from datetime import datetime, timezone

import ntplib


class NetworkTime:
    @staticmethod
    def network_time() -> datetime:
        """Fetches the current time from an NTP server.

            Attempts to connect to an NTP server and return the current time in UTC.
            If the connection fails, returns the local system time instead.

            Returns:
                datetime: The current network time if available, otherwise local time.
        """
        try:
            client = ntplib.NTPClient()
            response = client.request('time.windows.com', version=3)
            network_time = datetime.fromtimestamp(
                response.tx_time, timezone.utc)
            return network_time
        except Exception:
            network_time = datetime.now(timezone.utc)
            return network_time
