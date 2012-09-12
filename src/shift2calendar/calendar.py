#!/usr/bin/env python
#
#   Copyright (C) 2012 Lumir Jasiok
#   lumir.jasiok@alfawolf.eu
#   http://www.alfawolf.eu
#
#

import sys
import atom
import string
import atom.service
import gdata.service
import gdata.calendar
import gdata.calendar.service

from shift2calendar.config import config

class Google(object):
    """
    Connect to Google Calendar and create requested record in selected calendar

    """

    def __init__(self):
        self.url = ""

    def connect(self):
        """
        Connect to Google Calendar
    
        """
    
        calendar_service = gdata.calendar.service.CalendarService()
        calendar_service.email = config['calendar']['username']
        calendar_service.password = config['calendar']['password']
        calendar_service.source = 'shifts2calendar 0.1'
        calendar_service.ProgrammaticLogin()
    
        self.service = calendar_service
    
    
    def find_calendar_url(self, calendar):

        feed = self.service.GetAllCalendarsFeed()
        for i, a_calendar in enumerate(feed.entry):
            if (str(a_calendar.title.text) == calendar):
                l = a_calendar.GetAlternateLink()
                self.url = l.href
        # TODO - what in case that we didn't found calendar?
        #if not self.url:
        #    pass

    def add_shift(self, title='Tieto Shift', content='Tieto Shift',
                          where=config['Tieto']['office_address'],
                          start_time=None, end_time=None):

        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=content)
        event.where.append(gdata.calendar.Where(value_string=where))
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
    
        try:
            new_event = self.service.InsertEvent(event, self.url)
        except gdata.service.RequestError, e:
            print "Error adding event: %s" % (e[0]["reason"])
    

