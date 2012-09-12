#!/usr/bin/env python
#
#   Copyright (C) 2012 Lumir Jasiok
#   lumir.jasiok@alfawolf.eu
#   http://www.alfawolf.eu
#
#

import re

class Html(object):
    """
    Parse input text stream and return dictionary with dates and associated shifts

    """

    def __init__(self):
        """Basic initialization"""

        self.html = ""
        self.name = ""
        self.shifts = []

    def parse_file(self, html_file, name):
        try:
            html_fd = open(html_file, 'r')
        except Exception, e:
            raise e
        pattern = re.compile('<td class="person">(.*?)%s</td>(.*)</tr>' % (name.encode('utf8'),))
        for line in html_fd.readlines():
            r = pattern.search(line)
            if r:
                self.html = r.groups()[1]
        html_fd.close()

    def get_shifts(self):
        """
        Parse self.html and return list with string representation of shift

        """

        pattern = re.compile('<td(.*?)>(.*?)</td>', re.I | re.S)
        list_td = []
        for each in pattern.findall(self.html):
            list_td.append(each)
        for item in list_td:
            shift_type = self.__parse_shift_type(item[1])
            self.shifts.append(shift_type)
        return self.shifts

    def __parse_shift_type(self, text):
        """
        Get string, parse and return appropriate shift type. Supported types are:
            D - day shift, 7.5 hours
            D8 - day sfift, 8 hours
            D12 - day shift, 12 hours
            D-ShiftSupervisor - day shift, 7.5 hours, Shift Supervisor
            E - Afternoon shift, 7.5 hours
            N12 - night shift, 12 hours
            F - day free
        """

        if not text:
            return "F"
        else:
            pattern = re.compile('<div(.*?)><div(.*?)>(.*?)</div></div>', re.I | re.S)
            for each in pattern.findall(text):
                return each[2]
        
