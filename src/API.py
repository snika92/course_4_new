from abc import ABC, abstractmethod
import requests


class UnsuccessfulRequest(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Не удалось обработать запрос. Статус-код не '200'."


class API(ABC):
    def __init__(self, file_worker=None):
        if file_worker is None:
            self.file_worker = "Some site"
        else:
            self.file_worker = file_worker

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, file_worker=None):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        super().__init__(file_worker)

    @property
    def vacancies(self):
        return self.__vacancies

    def get_status_code(self):
        # Получение статус-кода
        response = requests.get(self.__url)  # отправка GET-запроса
        return response.status_code

    def load_vacancies(self, keyword):
        if self.get_status_code() == 200:
            self.__params['text'] = keyword
            while self.__params.get('page') != 20:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                vacancies = response.json()['items']
                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
        else:
            raise UnsuccessfulRequest


if __name__ == "__main__":
    hh_api = HeadHunterAPI("HeadHunter")
    hh_api.load_vacancies("python")
    # print(hh_api.vacancies)
    print(hh_api.get_status_code())
