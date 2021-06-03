class HeadHunterConfig(object):
    API_URL: str = 'https://api.hh.ru'
    VACANCIES_URL: str = API_URL + '/vacancies'
    VACANCY_ID_URL: str = VACANCIES_URL + '/{id}'
    LIMIT_RESULT: int = 2000
    LIMIT_REQUESTS: int = 50
    RESULT_PER_PAGE: int = 100
