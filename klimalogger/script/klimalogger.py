#!/usr/bin/env python3

import argparse
import logging
from importlib.metadata import metadata

import klimalogger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="verbose output"
    )
    parser.add_argument(
        "-d", "--debug", dest="debug", action="store_true", help="debug output"
    )
    parser.add_argument("--version", help="print package version", action="store_true")
    parser.add_argument(
        "--check", help="measure once and print the results", action="store_true"
    )
    parser.add_argument(
        "--service",
        help="run as service performing periodic measurements",
        action="store_true",
    )
    args = parser.parse_args()

    klimalogger.add_log_handler(klimalogger.logger.create_console_handler())
    klimalogger.set_log_level(logging.WARN)
    if args.debug:
        klimalogger.set_log_level(logging.DEBUG)
    elif args.verbose:
        klimalogger.set_log_level(logging.INFO)

    try:
        if args.version:

            print(f"Version {metadata('klimalogger')['Version']}")
        else:
            client = klimalogger.client()
            if args.check:
                print(client.measure())
            else:
                if args.service:
                    client.measure_and_store_periodically()
                else:
                    client.measure_and_store()
    except Exception as e:
        print("Error", e)
        return 10
    return 0


if __name__ == "__main__":
    main()
