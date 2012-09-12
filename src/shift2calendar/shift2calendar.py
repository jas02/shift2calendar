#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright (C) 2012 Lumir Jasiok
#   lumir.jasiok@alfawolf.eu
#   http://www.alfawolf.eu
#
#
#
import sys
import time
import getopt
import datetime

from shift2calendar.config import config
from shift2calendar.parser import Html
from shift2calendar.calendar import Google

def usage():
    """
    Print a program usage and exit the application

    """
    
    print "\n"
    print "Usage: \n\t" + str(sys.argv[0]) + \
          "-f <HTML file with shifts table> [-h <help>]\n" + \
          "-d <year and month you want to parse YYYY-MM format>\n" + \
    sys.exit(0)


def opts():
    """
    Get options from command line and return it as dictionary

    """

    opt = {}
    (options, arguments) = getopt.getopt(sys.argv[1:],'f:d:h')
    if len(options) == 0:
            usage()
    for o,a in options:
        if o == '-h':
            usage()
        elif o == '-f':
            opt['file'] = a
        elif o == '-d':
            opt['date'] = a
        else:
            # In case of zero arguments
            pass
    return opt



def get_times(date_begin, shift):
    """
    Return tuple with string of begin and end of shift

    """

    time_table = {'D': {'begin': '07:00:00',
                        'end': '15:00:00'},
                  'D8': {'begin': '08:00:00',
                         'end': '16:30:00'},
                  'D12': {'begin': '08:00:00',
                          'end': '20:00:00'},
                  'D-ShiftSupervisor': {'begin': '07:00:00',
                                        'end': '15:00:00'},
                  'E': {'begin': '13:00:00',
                        'end': '21:00:00'},
                  'N12': {'begin': '20:00:00',
                          'end': '08:00:00'}
    }
    
    # In case of night shift we need to move end of event to next day
    time_begin = datetime.datetime(*time.strptime(date_begin, "%Y-%m-%d")[0:5])
    if (shift == "N12"):
        plus_day = datetime.timedelta(days=1)
        time_end = time_begin + plus_day
    else:
        time_end = time_begin

    begin_day = time_begin.day
    begin_month = time_begin.month
    end_day = time_end.day
    end_month = time_end.month

    # In case that day or month is just one number long (1..9)
    if ((len(str(time_begin.day)) == 1)):
        begin_day = "0%s" % (time_begin.day)
    if ((len(str(time_begin.month)) == 1)):
        begin_month = "0%s" % (time_begin.month)
    if ((len(str(time_end.day)) == 1)):
        end_day = "0%s" % (time_end.day)
    if ((len(str(time_end.month)) == 1)):
        end_month = "0%s" % (time_end.month)

    # Night Shift, ending next day
    begin = "%s-%s-%sT%s" % (time_begin.year, begin_month, begin_day, time_table[shift]['begin'])
    end = "%s-%s-%sT%s" % (time_end.year, end_month, end_day, time_table[shift]['end'])

    return (begin, end)

def main():
    """
    Main function

    """

    opt = opts()
    arg_file = opt['file']
    arg_date = opt['date']
    html = Html()
    name = "%s" % (config['ShiftMaster']['full_name'],)
    html.parse_file(arg_file, name)
    shifts = html.get_shifts()
    calendar = Google()
    calendar.connect()
    cal_name = config['calendar']['shift_calendar']
    calendar.find_calendar_url(cal_name)

    day = 1
    for shift in shifts:
        if shift == "F":
            day += 1
            continue
        date_begin = "%s-%s" % (arg_date, day)
        times = get_times(date_begin, shift)
        day += 1
        event_title = "Shift %s" % (shift,)
        print "Adding Shift for date %s (Begin %s End %s)" % (date_begin, times[0], times[1])
        calendar.add_shift(title=event_title, start_time=str(times[0]), end_time=str(times[1]))

if __name__ == "__main__":
    main()
