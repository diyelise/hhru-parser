import asyncio
from datetime import datetime, timedelta
from configuration.hhru import HeadHunterConfig
from utils.parser import JobParser


async def example_get_vacancy():
    """Get vacancy body

    If you want to get full info
    about vacancy, we can use get_vacancy method

    get_vacancy returned tuple parameters
    as response code and vacancy body
    """
    job = JobParser(config=HeadHunterConfig)
    code, body = await job.get_vacancy(11111111)
    print(code, body)
    await job.close()  # close session


async def example_get_vacancies():
    """Get one or more vacancies

    You can use query attributes that
    make it more targeted.
    """

    # last hour
    start_date = (
        datetime.now() - timedelta(hours=1)
    ).strftime('%Y-%m-%dT%H:%M:%S')

    attributes = [
        ('text', 'python'),
        ('area', 113),
        ('only_with_salary', 'true'),
        ('date_from', start_date),
    ]
    job = JobParser(config=HeadHunterConfig)
    code, vacancies_list = await job.get_vacancies(params=attributes)
    print(vacancies_list)
    await job.close()


async def example_extract_vacancies():
    """Extracting received vacancies

    At the last stage, you received a list of vacancies.
    Now you can extract them and get the job bodies
    """
    vacancies_list = [
        11111111,
        2222222,
    ]
    job = JobParser(config=HeadHunterConfig)
    extracted_vacancies = await job.extract_vacancies(
        vacancies_list=vacancies_list
    )
    print(extracted_vacancies)
    await job.close()


async def example_transform():
    """Transform received vacancies

    You can use your list of required keys
    to convert the received vacancies

    By default, all fields will be returned
    :return:
    """
    vacancies_list = [
        11111111,
        2222222,
    ]
    _parser = JobParser(config=HeadHunterConfig)

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
    print(transformed_data)
    await _parser.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(example_transform())
