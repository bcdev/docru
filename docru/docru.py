import datetime
import json
import pathlib
import subprocess
import time
from typing import Self

import click
import pint


@click.group()
def cli():
    pass


@cli.command()
def log():
    while True:
        # print(datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ"))
        subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "json"],
        )
        time.sleep(1)


@cli.command()
@click.argument(
    "logfile",
    type=click.Path(
        path_type=pathlib.Path, dir_okay=False, file_okay=True, exists=True
    ),
)
@click.option(
    "-c",
    "--container",
    help="Filter by this container name",
)
def parse(logfile: pathlib.Path, container: str):
    with open(logfile) as fh:
        res = [
            r
            for line in fh.readlines()
            if (r := Resources.parse_line(line)).name == container
        ]

    print(f"Maximum memory: {max(r.mem for r in res):~P}")
    print(f"Maximum CPU: {max(r.cpu for r in res):~P}")


class Resources:
    ur = pint.UnitRegistry()

    def __init__(self, name, mem, cpu):
        self.name = name
        self.mem = mem
        self.cpu = cpu

    @classmethod
    def parse_line(cls, line: str) -> Self:
        data = json.loads(line)
        cpu_quantity = cls.ur(data["CPUPerc"])
        assert cpu_quantity.u == cls.ur.percent
        mem_quantity = cls.ur(data["MemUsage"].split(" / ")[0])
        mem_bytes = mem_quantity.to(pint.Unit("byte")).m
        return Resources(name=data["Name"], cpu=cpu_quantity, mem=mem_quantity)
