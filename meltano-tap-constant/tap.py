import json
import os
from singer_sdk import Tap
from singer_sdk import typing as th
from singer_sdk.helpers._util import utc_now

class TapRestConstant(Tap):
    """A simple tap to return constant data for work orders statuses."""

    name = "tap-rest-constant"

    # Define the properties for the tap from environment variables
    stream_maps = [
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
    
    def discover(self):
        """Discover the streams. This is typically where metadata is discovered."""
        for stream in self.stream_maps:
            # Here we return the stream metadata in a way Singer expects
            yield {
                "stream": stream["name"],
                "schema": {
                    "properties": {property.name: property for property in self.stream_schemas},
                },
            }

    def sync(self):
        """Sync the streams and produce the records."""
        for stream in self.stream_maps:
            # Creating record per stream
            record = {
                "name": stream["name"],
                "data": [
                    {"code": status, "name": status} for status in stream["data"]
                ]
            }

            # Yield the record. You can add custom logic here for other fields.
            yield {
                "stream": stream["name"],
                "record": record,
                "version": utc_now(),
                "time_extracted": utc_now(),
            }

    # Helper method to load data from environment
    def load_data_from_env(self):
        stream_data = os.getenv("TAP_REST_API_MSDK_STREAMS", "[]")
        try:
            # Load stream data from the environment variable
            return json.loads(stream_data)
        except json.JSONDecodeError:
            return self.stream_maps