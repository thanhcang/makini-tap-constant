import json
import os
from singer_sdk import Mapper
from singer_sdk import typing as th
from singer_sdk.helpers._util import utc_now

class TapRestConstant(Mapper):
    """A simple mapper to transform constant data for work orders statuses."""

    name = "tap-rest-constant"

    def __init__(self):
        super().__init__()
        self.logger.info("Loading constang mapper instance")
        self.stream_maps = self.load_data_from_env()

    # Define the stream schema for mapping
    @property
    def stream_schemas(self):
        """Return stream schemas based on the properties."""
        return [
            th.Property(
                "name", 
                th.StringType, 
                required=False, 
                description="Name of the entity"
            ),
            th.Property(
                "data", 
                th.ArrayType(th.ObjectType({
                    "code": th.StringType,
                    "name": th.StringType
                })), 
                required=False, 
                description="List of data"
            ),
        ]
    
    def map(self, record: dict, stream_id: str) -> dict:
        """Map a record for a given stream."""
        self.logger.info(f"Mapping stream: {stream_id}")
        
        stream = next(filter(lambda x: x['name'] == stream_id, self.stream_maps), None)
        
        if stream is None:
            raise ValueError(f"Stream {stream_id} not found.")
        
        # Map the 'data' field into objects with 'code' and 'name'
        mapped_data = [
            {"code": status, "name": status} for status in stream['data']
        ]

        # Return the mapped record
        return {
            "stream": stream["name"],
            "record": {
                "name": stream["name"],
                "data": mapped_data,
            },
            "version": utc_now(),
            "time_extracted": utc_now(),
        }

    def load_data_from_env(self):
        """Load stream data from the environment variable TAP_REST_API_CONSTANT_STREAMS."""
        stream_data = os.getenv("TAP_REST_API_CONSTANT_STREAMS", "[]")
        try:
            # Load stream data from the environment variable
            self.logger.info("Loading stream data from environment variable.")
            return json.loads(stream_data)
        except json.JSONDecodeError as e:
            # Log error if there's an issue with parsing the JSON
            self.logger.error(f"Failed to load stream data from environment. Error: {e}")
            # If there's an error loading, return default stream maps
            return [
                {
                    "name": "work_orders_statuses",
                    "data": ["new", "open", "onhold"]
                },
                {
                    "name": "work_orders_statuses-2",
                    "data": ["new", "open", "onhold"]
                },
            ]