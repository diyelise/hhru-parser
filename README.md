# HeadHunter parser
A Simple parser for working with HeadHunter API without authentication

## Important

> We can't get results more than 2000 jobs. This is a limited API for unauthorized

## Example
### First stage. Create instance

```python
job_parser = JobParser(config=HeadHunterConfig)
```

### Getting one vacancy
If you want to get one vacancy and you know her id, you can call ``get_vacancy`` method
In response, we will get a tuple from the code and the body of the response.

```python
async def get_one_vacancy():
  job_parser = JobParser(config=HeadHunterConfig)
  code, response = await job_parser.get_vacancy(11111111)
  await job_parser.close()
  return code, response
```
> Response 200, {'id': 1111111, 'employment': 'full', 'schedule': ...}


### Getting more vacancies
HeadHunter does not give the job bodies completely in requests with parameters, so to get the full job bodies, you must first get their IDs
To do this, call the ``get_vacancies`` method

The method takes an optional params argument, in which you can target search results from HeadHunter

Learn more: https://github.com/hhru/api/blob/master/docs/vacancies.md#запрос

As example:

```python
async def get_more_vacancies():
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
    
    code, vacancies_list = await job_parser.get_vacancies(params=attributes)
    return vacancies_list
```
> Response: [11111111, 222222, 3333333, ...]

## Extract vacancies

After this actions, we can extract them using method ``extract_vacancies``

We will get the full contents of the vacancies in the list with JSONs inside

```python
async def extract(vacancies_list):
    extracted_vacancies = await job_parser.extract_vacancies(
        vacancies_list=vacancies_list
    )
    return extracted_vacancies
```
> Response: [{'id': 1111111, 'schedule': 'full', 'employment': 'full'}, {'id': 2222222, ...}]

## Transform response

If you want to remove extra keys from the result, you can call method ``transform``
At the output, only the keys that you specified in need_keys will remain in JSON

```python
def transform_my_data(extracted_vacancies):
   need_keys = [
        'id',
        'area',
        'experience',
        'schedule',
    ]
    transformed_data = list(
        map(
            lambda p: JobParser.transform(
                body=p, required_keys=need_keys
            ), extracted_vacancies
        )
    )
    return transformed_data
```
> Response: [{'id': ..., 'area': ..., 'experience': ..., 'schedule': ...}]
