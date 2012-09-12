#!/usr/bin/env python
#
#   Copyright (C) 2012 Lumir Jasiok
#   lumir.jasiok@alfawolf.eu
#   http://www.alfawolf.eu
#
#
import os
from configobj import ConfigObj

package_dir = os.path.dirname(__file__)
filename = os.path.join(package_dir, "shift2calendar.conf")
config = ConfigObj(filename, encoding="UTF8")
