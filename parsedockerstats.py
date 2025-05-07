#!/usr/bin/env python3

import argparse
from collections import namedtuple
import json
import sys

import pint

Resources = namedtuple(
    "Resources",
    ["name", "cpu", "mem"]
)

def main():
    parser = argparser.ArgumentParser()
    parser.add_argument(
        "--name", "-n", type=str, help="filter by this container name"
    )
    parser.add_argument("logfile", type=str)
    args = parser.parse_args()
    
    with open(args.logfile) as fh:
        res = [Resources.parse_line(line) for line in fh.readlines()]

    if args.name:
        res = [r for r in res if r.name == args.name]

    print(set(r.name for r in res))
    print(max(r.cpu for r in res))
    print(max(r.cpu for r in res))
    
    

class Resources:

    ur = pint.UnitRegistry()
    
    def __init__(self, name, mem, cpu):
        self.name = name
        self.mem = mem
        self.cpu = cpu

    @classmethod
    def parse_line(cls, line: str) -> Resources:
        data = json.loads(line)
        cpu_quantity = cls.ur(data["CPUPerc"])
        assert cpu_quantity.u == cls.ur.percent
        mem_quantity = cls.ur(data["MemUsage"].split(" / ")[0])
        mem_bytes = mem_quantity.to(pint.Unit("byte")).m
        return Resources(
            name=data["Name"],
            cpu=cpu_quantity.m,
            mem=mem_bytes
        )


def test_parse_line():
    line = (
        '{"BlockIO":"16.2GB / 0B","CPUPerc":"100.47%",'
        '"Container":"9839ab6be2d5","ID":"9839ab6be2d5","MemPerc":"0.96%",'
        '"MemUsage":"288.2MiB / 29.29GiB","Name":"angry_hugle",'
        '"NetIO":"15.4kB / 1.81kB","PIDs":"8"}'
    )
    r = Resources.parse_line(line)
    assert 100.46 < r.cpu < 100.48
    assert abs(r.mem - 288.2 * 2**20) < 1

        
if __name__ == "__main__":
    main()
