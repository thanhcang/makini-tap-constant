import json
import os
import hashlib
from singer_sdk import Tap, Stream
from singer_sdk import typing as th
from singer_sdk.helpers._util import utc_now


class ConstantStream(Stream):
    """Stream class for constant data."""
    primary_keys = ["key"]  # Define 'key' as the primary key for deduplication

    def __init__(self, tap, name, data):
        super().__init__(tap, name=name)  # Set the stream name properly
        self.data = data
        self.logger = tap.logger

    @property
    def schema(self):
        """Define the schema for the stream."""
        return th.PropertiesList(
            th.Property("name", th.StringType, required=True, description="Name of the entity"),
            th.Property("code", th.StringType, required=True, description="Code of the entity"),
            th.Property("key", th.StringType, required=True, description="Unique key of the entity")
        ).to_dict()

    def get_records(self, context=None):
        """Yields records for the stream."""
        for status in self.data:
            if not isinstance(status, str) or not status.strip():
                self.logger.warning(f"Skipping invalid status: {status}")
                continue

            record = {
                "name": status,
                "code": status,
                "key": self.md5_hash('19', status)
            }
            self.logger.info(f"Yielding record for stream '{self.name}': {record}")
            yield record

    def md5_hash(self, collection_key: str, value: str) -> str:
        """Generate an MD5 hash of the given value."""
        hex_key = os.getenv("MAPPTER_MAKINI_HEXKEY", "default_key")  # Default to 'default_key' if not set
        if not value:
            return ""
        key_md5 = hashlib.md5(value.encode("utf-8")).hexdigest()
        return f"{collection_key}{hex_key}{key_md5}"


class TapConstant(Tap):
    """A tap to handle constant data."""
    name = "tap-makini-constant"

    # Define the constant data
    constant_data_json = os.getenv('MAKINI_TAP_ENTITIES_CONTANT', "[]")

    try:
        constant_data = json.loads(constant_data_json)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in environment variable 'MAKINI_TAP_ENTITIES_CONTANT': {constant_data_json}")

    if not isinstance(constant_data, list):
        raise ValueError(f"Expected a list in environment variable 'MAKINI_TAP_ENTITIES_CONTANT', but got: {type(constant_data).__name__}")


    def discover_streams(self):
        """Returns a list of streams that the tap can sync."""
        streams = []
        for stream in self.constant_data:
            stream_name = stream["name"]
            data = stream["data"]
            streams.append(ConstantStream(self, name=stream_name, data=data))
        return streams


if __name__ == "__main__":
    TapConstant.cli()