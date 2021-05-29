from typing import List


class HeadHunterConfig(object):
    API_URL: str = 'https://api.hh.ru'
    VACANCIES_URL: str = API_URL + '/vacancies'
    VACANCY_ID_URL: str = VACANCIES_URL + '/{id}'
    LIMIT_RESULT: int = 1999
    LIMIT_REQUESTS: int = 50
    RESULT_PER_PAGE: int = 20
    FIELDS_TO_TAKE: List = [
        'id', 'area', 'experience', 'schedule', 'employment', 'salary'
    ]