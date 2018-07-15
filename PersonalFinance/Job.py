class Job(object):
    """
    Represents a Job, which is either paid
    hourly or monthly
    """
    def __init__(self,name='A Job',hourly=9.49,holiday=9.49,night=9.49):
        self.name = name
        self.rate = hourly
        self.rate_holiday = holiday
        self.rate_night = night
        self.night_hours = 0
        self.holy_hours = 0
        self.month = [[],[]]
        self.income = 0

    def get_monthly(self):
        """
        Get an approximation of what one would have earned this month.
        It is just an approximation and it's also innaccurate, because
        it takes (if any) the first 2 days of the month as special (either as night shifts
        or as holiday shifts)
        """
        total = 0
        nights = self.night_hours
        holyday = self.holy_hours
        subtract = 0
        for i in len(self.month[1]):
            hours = int(self.month[1][i])
            #account for unpaid breaks
            if hours >= 10:
                hours -= 1
            elif hours >= 6:
                hours -= 0.5
            #account for special hours (inaccurate)
            if nights > 0:
                total += (nights*self.rate_night)
                hours -= nights
                nights = 0
            elif holyday > 0:
                total += (holyday*self.rate_holiday)
                hours -= holyday
                holyday = 0
            # We don't work negative hours, but we do need to account for the negative hours
            hours += subtract
            if hours >= 0:
                total += (hours*self.rate)
            else:
                subtract = hours
        return total
    def set__income(self, income):
        self.income = income
    def get_balance(self):
        return self.get_monthly - self.income
    def ideal_mini_hours(self):
        return 450/self.rate
    
    def add_workday(self, date, hours):
        self.month[0].append(date)
        self.month[1].append(hours)
    
    def set_holyPay(self, rate):
        self.rate_holiday = rate
    
    def set_nightPay(self, rate):
        self.rate_night = rate
    
    def reset_month(self):
        self.month = [[],[]]
        self.holy_hours = 0
        self.night_hours = 0

