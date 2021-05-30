import asyncio
from typing import List, Tuple, Dict, Any
from aiohttp import ClientSession, TCPConnector
from aiohttp.client_exceptions import ClientError, ClientSSLError


class JobParser:

    def __init__(
            self,
            config,
            name: str = 'Unknown'
    ):
        self._config = config
        self._name = name
        self._session = self.__init_session()

    def __init_session(self) -> ClientSession:
        connector = TCPConnector(
            limit=self._config.LIMIT_REQUESTS
        )
        _session = ClientSession(connector=connector)
        return _session

    async def close(self) -> None:
        await self._session.close()

    async def get_vacancies(
            self,
            params: List[Tuple[str, Any]]
    ) -> Tuple[int, List[int]]:
        try:
            code, url, response = await self.__fetch(
                url=self._config.VACANCIES_URL, params=params
            )
            if not response.get('items'):
                return 404, []

            vacancies = []
            vacancies.extend([x['id'] for x in response['items']])
            max_iterate_pages = self._calculate_max_pages(
                response.get('pages')
            )

            tasks = [
                asyncio.create_task(self.__fetch(
                    url=url + f'&page={i}'
                )) for i in range(1, max_iterate_pages + 1)
            ]
            all_result = await asyncio.gather(*tasks)
            vacancies.extend(
                [
                    i['id'] for x, y, z in all_result for i in z['items']
                    if x == 200
                ]
            )
            return 200, vacancies
        except (Exception, ClientError):
            return 404, []

    def _calculate_max_pages(self, founded_pages: int) -> int:
        limit_pages = int(
            self._config.LIMIT_RESULT / self._config.RESULT_PER_PAGE
        )
        return founded_pages \
            if founded_pages <= limit_pages else limit_pages

    async def extract_vacancies(self, vacancies_list: List) -> List[Dict[str, Any]]:
        """Извлечение вакансий по идентификаторам

        """
        tasks = [
            asyncio.create_task(
                self.get_vacancy(
                    vacancy_id=vac_id
                )
            ) for vac_id in vacancies_list
        ]
        tmp = await asyncio.gather(*tasks)
        response = [y for x, y in tmp if x == 200]
        return response

    async def get_vacancy(self, vacancy_id: int) -> Tuple[int, Dict[str, Any]]:
        """Получение тела вакансии

        """
        code, _, response = await self.__fetch(
            url=self._config.VACANCY_ID_URL.format(**{'id': vacancy_id})
        )
        return code, response

    @staticmethod
    def transform(body: dict, required_keys: List = None) -> Dict[str, Any]:
        if not required_keys:
            return body
        response = {
            key: value for key, value in body.items() if key in required_keys
        }
        return response

    async def __fetch(
            self,
            url: str,
            params: List[tuple] = None
    ) -> Tuple[int, str, Dict[str, Any]]:

        if params:
            _check_per_page = [x for x, y in params if x == 'per_page']
            if not _check_per_page:
                params.append(('per_page', self._config.RESULT_PER_PAGE))

        code: int = 404
        response: dict = {}
        finally_url: str = ''
        try:
            async with self._session.get(url=url, params=params) as client:
                code = client.status
                response = await client.json()
                finally_url = str(client.url)
        except (ClientSSLError, ClientError):
            code = 404
        finally:
            return code, finally_url, response
