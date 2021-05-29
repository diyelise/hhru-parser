import asyncio
from typing import List
import pytest
from configuration.hhru import HeadHunterConfig
from utils.parser import JobParser


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope='module')
async def get_parser() -> JobParser:
    _parser = JobParser(
        config=HeadHunterConfig
    )
    yield _parser
    await _parser.close()


class TestJobParser:

    @pytest.mark.parametrize('vacancy, exp_code', [
        (000000000, 404),
        (11111111, 200),
    ])
    @pytest.mark.asyncio
    async def test_get_vacancy(
            self,
            vacancy,
            exp_code,
            get_parser
    ):
        _parser = get_parser
        code, response = await _parser.get_vacancy(vacancy_id=vacancy)
        assert code == exp_code

    @pytest.mark.parametrize('params, exp_code', [
        ([
             ('text', 'python'),
             ('area', 113),
             ('only_with_salary', 'true'),
             ('period', 1)
         ], 200),
        ([
             ('text', 'abcfgrtd'),
             ('area', 113),
             ('only_with_salary', 'true'),
             ('period', 1)
         ], 404)
    ])
    @pytest.mark.asyncio
    async def test_get_vacancies(self, params, exp_code, get_parser):
        _parser = get_parser
        code, vacancies_list = await _parser.get_vacancies(
            params=params
        )
        assert code == exp_code
        assert isinstance(vacancies_list, List)

    @pytest.mark.asyncio
    async def test_extract_vacancies(self, get_parser):
        vacancies_list = [
            11111111,
            2222222,
        ]
        job = get_parser
        response = await job.extract_vacancies(
            vacancies_list=vacancies_list
        )
        assert isinstance(response, List) is True

    @pytest.mark.parametrize('f_pages, result', [
        (10, 10),
        (21, 20),
    ])
    def test_calculate_max_pages(self, f_pages, result, get_parser):
        _parser = get_parser
        max_iterate_pages = _parser._calculate_max_pages(f_pages)
        assert max_iterate_pages == result

    @pytest.mark.asyncio
    async def test_transform_data(self, get_parser):
        vacancies_list = [
            11111111,
            2222222,
        ]
        _parser = get_parser
        need_keys = [
            'id',
            'area',
            'experience',
        ]
        extracted_vacancies = await _parser.extract_vacancies(
            vacancies_list=vacancies_list
        )
        transformed_data = list(
            map(
                lambda p: JobParser.transform(
                    body=p, required_keys=need_keys
                ), extracted_vacancies
            )
        )
        assert set([i for x in transformed_data for i in x]) == set(need_keys)
