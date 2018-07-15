import math
import Job

class Worker(object):
    """
    The representation of a Person with
    a job, hobbies and needs, and with a

    """
    def __init__(self, name):
        self.name = name
        self.rent = 0
        self.food = 80
        self.gym = 0
        self.otherExpenses = 0
        self.otherEarnings = 0
        self.job = Job.Job( 'Minijob', 9.46 )
    
    #Setter-Methodes for all
    def set_job(self, name, rate):
        self.job = Job.Job(name,rate)
    def set_expenses(self, rent, food, gym, others):
        self.rent = rent
        self.food = food
        self.gym = gym
        self.otherExpenses = others
    def set_othetEarnings(self, other):
        self.otherEarnings = other

    #Getter Methodes
    def get_expenses(self):
        return self.food + self.rent + self.gym + self.otherExpenses
    def get_budget(self):
        return self.get_income + self.otherEarnings
    def get_expectedBudget(self):
        return self.job.get_monthly + self.otherEarnings
    def get_income(self):
        return self.job.income
