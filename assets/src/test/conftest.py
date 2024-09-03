import os


def pytest_configure(config):
    # Set environment variables here
    os.environ["SHA"] = "1234567"
