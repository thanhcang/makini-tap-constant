from meltano_tap_constant.tap_rest_constant import  TapRestConstant # Adjust the import path to your script
from singer_sdk import SingerSink

def main():
    tap = TapRestConstant()
    tap.sync()  # Run the sync method to generate the output

if __name__ == "__main__":
    main()