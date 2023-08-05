"""
Classes and functions for recording machine friendly data
about the overall distribution about what happened to
installations.  This is a strict superset of :mod:`wizard.seen`
functionality, as it records seen autoinstallers in finer
granularity.

.. warning::

    This code relies on indexes not being changed while using
    the same directory.  We should probably add some sanity
    checks for this.
"""

import os
import errno

class ReportSet(object):
    #: Dictionary of names to reports
    reports = None
    def __init__(self, reports):
        self.reports = reports
    def write(self, name, i, *entry):
        self.reports[name].write(i, *entry)

class Report(object):
    #: File object to this report
    file = None
    #: Set of indexes
    values = None
    def __init__(self, file, values=None):
        self.file = file
        self.values = set() if values is None else values
    def write(self, i, *entry):
        self.file.write("%04d %s\n" % (i, ' '.join(entry)))
        self.values.add(i)
        self.file.flush()

def make(log_dir, *names):
    reports = {}
    for name in names:
        filename = os.path.join(log_dir, "%s.txt" % name)
        values = set()
        try:
            for line in open(filename):
                if not line: continue
                values.add(int(line.partition(' ')[0]))
        except IOError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise
        file = open(filename, "a")
        reports[name] = Report(file, values)
    return ReportSet(reports)

def make_fresh(log_dir, *names):
    reports = {}
    for name in names:
        file = open(os.path.join(log_dir, "%s.txt" % name), "w")
        reports[name] = Report(file)
    return ReportSet(reports)
