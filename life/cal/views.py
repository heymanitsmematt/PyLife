from django.shortcuts import render

import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from life.cal.models import *

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

@login_required
def main(request, year=None):
    if year:
	year = int(year)
    else:
	year - time.localtime()[:2]

    nowy, nowm = time.localtime()[:2]
    lst = []
    
    #create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year + 2]:
	mlst = []
	for n, month in enumerate(mnames):
	    entry = current = False #any entries for this month? current month?
	    entries = Entry.objects.filter(date__year=y, date__month=n+1)

	    if entries:
		entry = True
	    if y == nowy and n+1 = nowm:
		current = True
	    mlist.append(dict(n=n+1, name=month, entry=entry, current=current))
	list.append((y, mlst))

    return render_to_response("cal/main.html", dict(years=lst, user=request.user, year=year, reminders = reminders(request)))
