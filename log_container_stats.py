#!/usr/bin/env python3

import datetime
import time
import subprocess


def main():
    while True:
        print(datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ"))
        subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "json"],
        )
        time.sleep(1)
    

if __name__ == "__main__":
    main()
