from datetime import date, timedelta, datetime
from .models import Expressions


def get_taken_expression_dates():
    """
    Gets all the dates that have are taken from the Expressions model.
    
    :return: Returns a list of all dates taken
    :rtype: list of date
    
    """
    date_list = set()
    expressions = Expressions.objects.all() 
    
    for e in expressions:

        sdate = e.suggested_start_date
        edate = e.suggested_end_date
        if sdate != None:  
            dates = date_between(sdate, edate)
            for date in dates:
                date_list.add(date)
    
    return list(date_list)
    
    
def binary_search_date(date, date_list):
    """
    Searches a date list for a date (using binary search).
    
    :param date: date we are searching for
    :type date: date
    :param date_list: list of dates we are searching for date in
    :type: list of date
    :return: Returns True if the date is within the date_list, else returns False
    :rtype: boolean
    """
    
    l = 0
    r = len(date_list)-1
    
    while l <= r:
        
        mid = l+(r-l)//2
  
        val = date_list[mid]

        
        if  val == date:
            return True
        
        elif val.year != date.year:
            if val.year < date.year:
                l = mid+1
            else:
                r = mid-1
        
        elif val.month != date.month:
            if val.month < date.month:
                l = mid+1
            else:
                r = mid-1
        
        else:
            if val.day < date.day:
                l = mid+1
            else:
                r = mid-1
        
def date_between(sdate, edate):
    """
    Get the dates between two dates.
    
    :param sdate: start date
    :type edate: end date
    :return: Returns a list of dates between the start and end date
    :rtype: list of date
    """
    delta = edate - sdate 
    dates = []

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.append(day)

    return dates

def binary_search_dates(dates, date_list):
    """
    Searches a list of dates in a list of dates.
    
    :param dates: the list of dates you are searching for
    :type date_list: the list of dates you are searching for in
    :return: Returns True if a date in dates is within date_list
    :rtype: boolean
    """
    if len(date_list) == 0:
        return False

    for i in dates:
        if binary_search_date(i, date_list):
            return True
    else:
        return False
