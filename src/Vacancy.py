class Vacancy:
    """
    Класс для работы с вакансиями
    """
    __slots__ = ('id', 'name', 'url', 'salary', 'currency', 'area', 'employer', 'requirement', 'schedule')

    def __init__(self, id, name, url, salary, currency, area, employer, requirement, schedule):
        self.id = id
        self.name = name
        self.url = url
        self.salary = self.__validation(salary)
        self.area = area
        self.employer = employer
        self.requirement = requirement
        self.schedule = schedule
        self.currency = currency

    @staticmethod
    def __validation(salary):
        if salary is None:
            return 0
        else:
            return salary

    def __dict__(self):
        return {"id": self.id,
                "name": self.name,
                "url": self.url,
                "salary": self.salary,
                "currency": self.currency,
                "area": self.area,
                "employer": self.employer,
                "requirement": self.requirement,
                "schedule": self.schedule,
                }

    def __ge__(self, other):
        return self.salary >= other.salary
