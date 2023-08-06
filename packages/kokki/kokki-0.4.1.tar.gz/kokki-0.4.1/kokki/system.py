
__all__ = ["System"]

import os
import sys
from functools import wraps
from subprocess import Popen, PIPE, STDOUT

def lazy_property(undecorated):
    name = '_' + undecorated.__name__
    @property
    @wraps(undecorated)
    def decorated(self):
        try:
            return getattr(self, name)
        except AttributeError:
            v = undecorated(self)
            setattr(self, name, v)
            return v
    return decorated

class System(object):
    @lazy_property
    def os(self):
        platform = sys.platform
        if platform.startswith('linux'):
            return "linux"
        elif platform == "darwin":
            return "darwin"
        else:
            return "unknown"

    def unquote(self, val):
        if val[0] == '"':
            val = val[1:-1]
        return val

    @lazy_property
    def arch(self):
        machine = self.machine
        if machine in ("i386", "i486", "i686"):
            return "x86_32"
        return machine

    @lazy_property
    def machine(self):
        p = Popen(["/bin/uname", "-m"], stdout=PIPE, stderr=PIPE)
        return p.communicate()[0].strip()

    @lazy_property
    def lsb(self):
        if os.path.exists("/etc/lsb-release"):
            with open("/etc/lsb-release", "rb") as fp:
                lsb = (x.split('=') for x in fp.read().strip().split('\n'))
            return dict((k.split('_', 1)[-1].lower(), self.unquote(v)) for k, v in lsb)
        elif os.path.exists("/usr/bin/lsb_release"):
            p = Popen(["/usr/bin/lsb_release","-a"], stdout=PIPE, stderr=PIPE)
            lsb = {}
            for l in p.communicate()[0].split('\n'):
                v = l.split(':', 1)
                if len(v) != 2:
                    continue
                lsb[v[0].strip().lower()] = self.unquote(v[1].strip().lower())
            lsb['id'] = lsb.pop('distributor id')
            return lsb

    @lazy_property
    def platform(self):
        operatingsystem = self.os
        if operatingsystem == "linux":
            lsb = self.lsb
            if not lsb:
                if os.path.exists("/etc/redhat-release"):
                    return "redhat"
                if os.path.exists("/etc/fedora-release"):
                    return "fedora"
                if os.path.exists("/etc/debian_version"):
                    return "debian"
                if os.path.exists("/etc/gentoo-release"):
                    return "gentoo"
                return "unknown"
            return lsb['id'].lower()
        elif operatingsystem == "darwin":
            out = Popen("/usr/bin/sw_vers", stdout=PIPE).communicate()[0]
            sw_vers = dict([y.strip() for y in x.split(':', 1)] for x in out.strip().split('\n'))
            # ProductName, ProductVersion, BuildVersion
            return sw_vers['ProductName'].lower().replace(' ', '_')
        else:
            return "unknown"

    @lazy_property
    def locales(self):
        p = Popen("locale -a", shell=True, stdout=PIPE)
        out = p.communicate()[0]
        return out.strip().split("\n")

    @lazy_property
    def ec2(self):
        if not os.path.exists("/proc/xen"):
            return False
        if os.path.exists("/etc/ec2_version"):
            return True
        return False

    @classmethod
    def get_instance(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = cls()
        return cls._instance
