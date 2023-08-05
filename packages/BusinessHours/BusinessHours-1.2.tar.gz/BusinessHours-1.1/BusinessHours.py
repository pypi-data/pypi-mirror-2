"""
Class:  BusinessHours(datetime1,datetime2,worktiming=[9 ,18],weekends=[6,7],holidayfile=None)

Synopsis: Provides three date functions.
getdays()       - Returns the number of working days betweeen the two datetime object.
gethours()      - Returns the number of working hours between the two datetime objects.
dateinbetween() - Checks whether a given datetime lies between two datetime objects , used by the internal functions.

Class Parameters:
datetime1   - The datetime object with the starting date.
datetime2   - The datetime object with the ending date.
worktiming  - The working office hours . A list containing two values start time and end time
weekends    - The days in a week which have to be considered as weekends sent as a list, 1 for monday ...  7 for sunday.
holidayfile - A file consisting of the predetermined office holidays.Each date starts in a new line and currently must only be in the format dd-mm-yyyy

Example:
from BusinessHours import BusinessHours
from datetime import   datetime 

testing = BusinessHours(datetime(2007,10,15),datetime.now())
print testing.getdays()
print testing.gethours()
 

"""
class BusinessHours:
 
    def __init__(self,datetime1,datetime2,worktiming=[9 ,18],weekends=[6,7],holidayfile=None):
        self.holidayfile = holidayfile
        self.weekends = weekends
        self.worktiming = worktiming
        self.datetime1 = datetime1
        self.datetime2 = datetime2

    def getdays(self):
        days = (self.datetime2-self.datetime1).days 
        #exclude any day in the week marked as holiday (ex: saturday , sunday)
        noofweeks = days / 7 
        extradays = days % 7
        startday = self.datetime1.isoweekday();
        days = days - (noofweeks * self.weekends.__len__())
        # this is for the extra days that dont make up 7 days , to remove holidays from them
        for weekend in self.weekends:
            if(startday==weekend):
                days = days - 1;
            else:
                if(weekend >= startday):
                    if(startday+extradays >= weekend):
                        days = days - 1 ;
                else:
                    if(7-startday+extraday>=weekend):
                        days = days - 1 ;
        # Read company holiday's from the file 
        if(self.holidayfile is not None):                 
            f=open(self.holidayfile);
            fdata = f.read();
            definedholidays=fdata.split();
            f.close();
        #exclude any holidays that have been marked in the companies academic year
            for definedholiday in definedholidays:
                flag=0;
                day , month , year = definedholiday.split('-')
                holidate = date(int(year) , int(month) , int(day))
                for weekend in self.weekends:
                     #check if mentioned holiday lies in defined weekend , shouldnt deduct twice
                    if(holidate.isoweekday==weekend): 
                        flag=1;
                        break; 
                if(flag==1):
                    continue;
                if(self.dateinbetween(holidate)):
                    days = days - 1
        return days;        

    def gethours(self):
        days = self.getdays()
        #calculate hours 
        days = days - 2 # (-2)To remove the start day and the last day
        hoursinaday = self.worktiming[1]-self.worktiming[0]
        hours = days * hoursinaday
        # To calculate working hours in the first day.
        if(self.datetime1.hour < self.worktiming[0] ):
            hoursinfirstday = hoursinaday;
        elif(self.datetime1.hour > self.worktiming[1]):
            hoursinfirstday = 0;
        else:
            hoursinfirstday = worktiming[1]-self.datetime1.hour
        # To calculate working hours in the last day
        if(self.datetime2.hour > self.worktiming[1] ):
            hoursinlastday = hoursinaday;
        elif(self.datetime2.hour < self.worktiming[0]):
            hoursinlastday = 0;
        else:
            hoursinlastday = self.datetime2.hour-self.worktiming[0]
        hours = hours + hoursinfirstday + hoursinlastday
        return hours

    def dateinbetween(self,holidate):
        if(holidate.year > self.datetime1.year and holidate.year <= self.datetime2.year):
            return True
        if(holidate.year >= self.datetime1.year and holidate.year < self.datetime2.year):
            return True
        if(holidate.year == self.datetime1.year and holidate.year == self.datetime2.year):
            if(holidate.month > self.datetime1.month and holidate.month <= self.datetime2.month):
                return True
            if(holidate.month >= self.datetime1.month and holidate.month < self.datetime2.month):
                return True
            if(holidate.month == self.datetime1.month and holidate.month == self.datetime2.month):
                if(holidate.day >= self.datetime1.day and holidate.day <= self.datetime2.day):
                    return True
        return False;
                        
'''
* Sponsored by Ma Foi
#
* Written by Antano Solar John "solar_ant"  <solar345@gmail.com>
#
* (C)2006-2007 All Rights Reserved,
#
*
#
* This library is free software; you can redistribute it and/or
#
* modify it under the terms of the GNU Lesser General Public
#
* License as published by the Free Software Foundation; either
#
* version 2.1 of the License, or (at your option) any later version.
#
*
#
* This library is distributed in the hope that it will be useful,
#
* but WITHOUT ANY WARRANTY; without even the implied warranty of
#
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#
* Lesser General Public License for more details.
#
*
#
* You should have received a copy of the GNU Lesser General Public
#
* License along with this library; if not, write to the Free Software
#
* Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
*
#
*
'''

