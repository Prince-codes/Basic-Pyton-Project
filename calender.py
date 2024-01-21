import calendar as c
from datetime import datetime

now = datetime.now()
y, m = now.year, now.month

print(c.month(theyear=y, themonth=m))

