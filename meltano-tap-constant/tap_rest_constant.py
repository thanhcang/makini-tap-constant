from singer_sdk import Tap
from singer_sdk import typing as th
from singer_sdk.helpers._util import utc_now
import json
import os

class TapRestConstant(Tap):
    """A tap to handle constant data."""
    name = "tap-rest-constant"

    # Define the constant data
    constant_data = [
        {
            "name": "work_orders_statuses",
            "data": ["new", "open", "onhold"]
        },
        {
            "name": "work_orders_statuses-2",
            "data": ["new", "open", "onhold"]
        },
    ]

    # Define the stream schema
    @property
    def stream_schemas(self):
        """Return stream schemas based on the properties."""
        return [
            th.Property(
                "name", 
                th.StringType, 
                required=True, 
                description="Name of the entity"
            ),
            th.Property(
                "data", 
                th.ArrayType(th.StringType), 
                required=True, 
                description="List of data"
            ),
        ]

    def sync(self):
        """Sync the streams and store constant data."""
        for stream in self.constant_data:
            # Creating record per stream
            record = {
                "name": stream["name"],
                "data": [{"code": status, "name": status} for status in stream["data"]]
            }

            # Yield the record, and insert it into the database or any other action
            yield {
                "stream": stream["name"],
                "record": record,
                "version": utc_now(),
                "time_extracted": utc_now(),
            }

    def load_data_from_env(self):
        """Load stream data from the environment variable TAP_REST_API_CONSTANT_STREAMS."""
        stream_data = os.getenv("TAP_REST_API_CONSTANT_STREAMS", "[]")
        try:
            return json.loads(stream_data)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to load stream data from environment. Error: {e}")
            return self.constant_data