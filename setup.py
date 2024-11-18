from setuptools import setup, find_packages

setup(
    name="meltano-tap-constant",  # Plugin name
    version="0.1.0",  # Initial version of your plugin
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[
        "singer-sdk>=0.6.0"  # Singer SDK is required for Meltano taps
        # Add any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "meltano-tap-constant = meltano-tap-constant:main",  # Entry point for the Tap
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    zip_safe=False,
)