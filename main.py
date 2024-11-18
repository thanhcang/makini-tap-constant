from meltano_tap_constant.tap import TapRestConstant  # Adjust the import path to your script

def main():
    tap = TapRestConstant()
    tap.cli()  # Correct method to run the tap

if __name__ == "__main__":
    main()