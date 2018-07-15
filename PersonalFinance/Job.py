class Job(Object):
    """
    Represents a Job, which is either paid
    hourly or monthly
    """
    def __init__(self, name, hourly):
        self.name = name
        self.rate = hourly
        self.month = []
        self.income = 0

    def get_monthly(self):
        total = 0
        for i in len(1, self.month, 2):
            hours = int(self.month[i])
            #account for unpaid breaks
            if hours >= 10:
                hours -= 1
            elif hours >= 6:
                hours -= 0.5
            total += (hours*self.rate)
        return total
    def set__income(self, income):
        self.income = income
    def get_balance(self):
        return self.get_monthly - self.income
    def ideal_mini_hours(self):
        return 450/self.rate


