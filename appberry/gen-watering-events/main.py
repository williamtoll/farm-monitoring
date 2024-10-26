from dateutil.rrule import *
from dateutil.parser import *
from datetime import *


print(list(rrule(DAILY, count=10, dtstart=parse("19970902T090000"))))

list(rrule(DAILY,dtstart=parse("19970902T090000"),until=parse("19971224T000000")))