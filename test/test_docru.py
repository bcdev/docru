import pint

from docru.docru import Resources


def test_parse_line():
    line = (
        '{"BlockIO":"16.2GB / 0B","CPUPerc":"100.47%",'
        '"Container":"9839ab6be2d5","ID":"9839ab6be2d5","MemPerc":"0.96%",'
        '"MemUsage":"288.2MiB / 29.29GiB","Name":"angry_hugle",'
        '"NetIO":"15.4kB / 1.81kB","PIDs":"8"}'
    )
    ur = pint.UnitRegistry()
    r = Resources.parse_line(line)
    assert r.cpu == 100.47 * ur.percent
    assert r.mem == ur("288.2 MiB")
