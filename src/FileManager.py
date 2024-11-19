from abc import ABC, abstractmethod
import os
import json


class VacancyFileManager(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях
    """

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class JSONInteraction(VacancyFileManager):
    """
    Класс для сохранения информации о вакансиях в JSON - файл
    и работы с ней
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.__check_file_existing()

    def __check_file_existing(self):
        # if not os.path.exists(self.file_name):
        with open(self.file_name, "w", encoding="utf-8") as json_file:
            empty_list = []
            json.dump(empty_list, json_file)

    def add_vacancy(self, vacancy):
        """
        Открывает файл и добавляет в список экземпляр объекта вакансии
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        # if vacancy in content:
        #     print("Такая вакансия уже есть")
        # else:
        content.append(vacancy.__dict__())
        with open(self.file_name, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, ensure_ascii=False, indent=2)

    def get_vacancies(self):
        """
        Открывает файл, получает все вакансии и
        возвращает список строк в нужном формате
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        list_of_vacancies = []
        for vacancy in content:
            list_of_vacancies.append(f"{vacancy['name']}\nЗ/п от: {vacancy['salary']} {vacancy['currency']}\n"
                                     f"Город: {vacancy['area']}\n"
                                     f"Компания: {vacancy['employer']}\nЗанятость: {vacancy['schedule']}\n"
                                     f"Полное описание: {vacancy['url']}\n")
        return list_of_vacancies

    def get_vacancies_by_salary(self, salary):
        """
        Открывает файл, сортирует информацию по значению "salary" от меньшего к большему и
        возвращает список строк в нужном формате
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        list_of_vacancies_for_sort = []
        for vacancy in content:
            if vacancy["salary"] >= int(salary):
                list_of_vacancies_for_sort.append(vacancy)
        sorted_vacancies = sorted(list_of_vacancies_for_sort, key=lambda x: x["salary"])
        list_of_vacancies = []
        for vacancy in sorted_vacancies:
            list_of_vacancies.append(f"{vacancy['name']}\nЗ/п от: {vacancy['salary']} {vacancy['currency']}"
                                     f"\nГород: {vacancy['area']}\n"
                                     f"Компания: {vacancy['employer']}\nЗанятость: {vacancy['schedule']}\n"
                                     f"Полное описание: {vacancy['url']}\n")
        return list_of_vacancies

    # def get_vacancies_by_city(self, city):
    #     """
    #     Открывает файл, фильтрует информацию по значению "area" и
    #     возвращает список строк в нужном формате
    #     """
    #     with open(self.file_name, "r", encoding="utf-8") as json_file:
    #         content = json.load(json_file)
    #     result = filter(lambda x: x['area'] == city, content)
    #     list_of_vacancies = []
    #     for vacancy in result:
    #         list_of_vacancies.append(f"{vacancy['name']}\nЗ/п от: {vacancy['salary']} {vacancy['currency']}\n"
    #                                  f"Город: {vacancy['area']}\n"
    #                                  f"Компания: {vacancy['employer']}\nЗанятость: {vacancy['schedule']}\n"
    #                                  f"Полное описание: {vacancy['url']}\n")
    #     return list_of_vacancies

    def get_top_vacancies(self, top):
        """
        Открывает файл, сортирует информацию по значению "salary" от большего к меньшему, и
        возвращает список требуемого количества строк в нужном формате
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        sorted_vacancies = sorted(content, key=lambda x: x["salary"], reverse=True)
        list_of_vacancies = []
        for digit in range(int(top)):
            list_of_vacancies.append(f"""{sorted_vacancies[digit]['name']}
        З/п от: {sorted_vacancies[digit]['salary']} {sorted_vacancies[digit]['currency']}
        Город: {sorted_vacancies[digit]['area']}
        Компания: {sorted_vacancies[digit]['employer']}
        Занятость: {sorted_vacancies[digit]['schedule']}
        Полное описание: {sorted_vacancies[digit]['url']}
        """)
        return list_of_vacancies

    def get_remote_vacancies(self):
        """
        Открывает файл, фильтрует информацию по значению "employment" и
        возвращает список строк в нужном формате
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        result = filter(lambda x: x['schedule'] == "Удаленная работа", content)
        list_of_vacancies = []
        for vacancy in result:
            list_of_vacancies.append(f"{vacancy['name']}\nЗ/п от: {vacancy['salary']} {vacancy['currency']}\n"
                                     f"Город: {vacancy['area']}\n"
                                     f"Компания: {vacancy['employer']}\nЗанятость: {vacancy['schedule']}\n"
                                     f"Полное описание: {vacancy['url']}\n")
        return list_of_vacancies

    def delete_vacancy(self, vacancy_id):
        """
        Удаляет вакансию из списка в файле по её id
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        for vacancy in content:
            if vacancy["id"] == vacancy_id:
                content.pop(vacancy)
        with open(self.file_name, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, ensure_ascii=False, indent=2)
