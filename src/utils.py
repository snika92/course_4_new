import os

from src.API import HeadHunterAPI
from src.FileManager import JSONInteraction
from src.Vacancy import Vacancy


def get_vacancy_from_hh_data(vacancies, city):
    """
    Получает вакансии в json формате
    Возвращает список объектов класса Vacancy
    """
    list_of_vacancy_instances = []
    for vacancy in vacancies:
        if vacancy['area']['name'] == city:
            id = vacancy['id']
            name = vacancy['name']
            url = vacancy['alternate_url']
            try:
                salary = vacancy['salary']['from']
            except TypeError:
                salary = vacancy['salary']
            try:
                currency = vacancy['salary']['currency']
            except TypeError:
                currency = vacancy['salary']
            # if vacancy['salary']:
            #     if vacancy['salary']['from']:
            #         salary = vacancy['salary']['from']
            #     else:
            #         salary = 0
            # else:
            #     salary = 0
            area = vacancy['area']['name']
            try:
                employer = vacancy['employer']['name']
            except KeyError:
                employer = None
            requirement = vacancy['snippet']['requirement']
            schedule = vacancy['schedule']['name']
            vacancy_instance = Vacancy(id, name, url, salary,currency, area, employer, requirement, schedule)
            # print(vacancy_instance.__dict__())
            list_of_vacancy_instances.append(vacancy_instance)
    return list_of_vacancy_instances


def add_vacancies_to_json(json_obj, list_of_vacancy_instances):
    for vacancy in list_of_vacancy_instances:
        json_obj.add_vacancy(vacancy)


def user_interaction():
    # Функция для взаимодействия с пользователем
    print("Добрый день! Здесь Вы можете найти вакансии с сайта HeadHunter.ru")
    result = input("Введите ключевое слово:\n")
    city = input("Введите город:\n")
    # Создаем объект класса и получаем вакансии с сайта HeadHunter
    hh = HeadHunterAPI("HeadHunter.ru")
    hh.load_vacancies(result)
    hh_result = hh.vacancies
    # for vac in hh_result:
    #     print(vac['employment']['name'])
    list_of_vacancy_instances = get_vacancy_from_hh_data(hh_result, city)
    file_name = os.path.join('data', 'vacancies.json')
    # print(os.path.exists(file_name))
    json_obj = JSONInteraction(file_name)
    # print(json_obj)
    # print(os.path.exists(file_name))
    add_vacancies_to_json(json_obj, list_of_vacancy_instances)

    # Запускаем цикл с выбором аргумента для поиска по вакансиям
    while True:
        user_choice = input(f"""Выберите действие:
1) Выборка по зарплате
2) Все найденные
3) Вывести топ N вакансий по зарплате
4) Вывести только удалённую работу
5) Завершить работу программы\n""")
        print()
        if user_choice == "1":
            salary = input("Введите минимальный порог зарплаты:\n")
            print()
            # Вызываем функцию поиска по минимальной зарплате
            list_of_vacancies = json_obj.get_vacancies_by_salary(salary)
            for vacancy in list_of_vacancies:
                print(vacancy)
        elif user_choice == "2":
            # Вызываем функцию для отображения всех найденных вакансий по ключевому слову
            list_of_vacancies = json_obj.get_vacancies()
            for vacancy in list_of_vacancies:
                print(vacancy)
        elif user_choice == "3":
            top = input("Введите количество вакансий, которое нужно вывести:\n")
            print()
            # Вызываем функцию вывода определенного количества вакансий, отсортированных по минимальной зарплате
            list_of_vacancies = json_obj.get_top_vacancies(top)
            for vacancy in list_of_vacancies:
                print(vacancy)
        elif user_choice == "4":
            # Вызываем функцию для отображения всех найденных вакансий с удаленной формой занятости
            list_of_vacancies = json_obj.get_remote_vacancies()
            for vacancy in list_of_vacancies:
                print(vacancy)
        elif user_choice == "5":
            break
        else:
            continue
        answer = input("<Конец выборки>\n\nНажмите 'n' для выхода или любую другую клавишу, чтобы продолжить\n")
        if answer == "n":
            break
        else:
            continue
