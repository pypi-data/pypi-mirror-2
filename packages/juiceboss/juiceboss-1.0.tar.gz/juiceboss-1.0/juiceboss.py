import urllib2
import re

class Juiceboss(object):
    """

    The Juiceboss class provides a simple way to monitor and control a
    juiceboss device on the local network.

    :param unit_id: unit id, e.g. "555-0001"
    :type unit_id: string
    :param ip: IP address of unit on network
    :type ip: string

    If ``ip`` is not specified, the Juiceboss object uses the central server to discover the IP address of the
    juiceboss device (see :ref:`finding`).
    """

    def __init__(self, unit_id, ip = None):
        self.unit_id = unit_id
        if ip:
            self.ip = ip
        else:
            self.ip = urllib2.urlopen('http://juiceboss.com/ip/' + unit_id).read()
        password = self.unit_id
        top_level_url =  "http://%s/" % self.ip
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, top_level_url, "admin", password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        self.request = lambda pg,data: opener.open(top_level_url + pg, data).read()

        self.update()

    def update(self):
        """ Connect to the device and update attributes """
        doc = self.request('', None)
        def extract(name):
            m = re.search(r"%s: ([0-9.]+)" % name, doc)
            return m.group(1)
        self._switch = int(extract('Switch'))
        self._voltage = float(extract('Voltage'))
        self._uptime = int(extract('Uptime'))
        self._version = int(extract('Firmware version'))

    @property
    def voltage(self):
        """Voltage of the device's DC supply, in volts;  float, read-only.

        ::

            >>> j = Juiceboss("555-0001")
            >>> print j.voltage
            7.8
        """
        return self._voltage

    @property
    def uptime(self):
        """Seconds since last restart of the device; int, read-only.

        ::

            >>> j = Juiceboss("555-0001")
            >>> print j.uptime
            79218
        """
        return self._uptime

    @property
    def version(self):
        """firmware version of the device; int, read-only."""
        return self._version

    @property
    def switch(self):
        """state of the device switch, integer 0 or 1.  This attribute is writable: assigning to it controls the device's switch::

            >>> j = Juiceboss("555-0001")
            >>> j.switch = 0    # turn it off
            >>> j.switch = 1    # turn it on
        """
        return self._switch

    @switch.setter
    def switch(self, value):
        assert value in [0,1]
        self.request(str(value), '')
        self.update()
