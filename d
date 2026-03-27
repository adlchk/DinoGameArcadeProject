import requests

BASE_URL = 'http://127.0.0.1:5000/api/v2/users'


def show(response):
    print(response.status_code)
    try:
        print(response.json())
    except Exception:
        print(response.text)
    print()


r = requests.get(BASE_URL)
show(r)

r = requests.post(
    BASE_URL,
    json={
        'surname': 'Ivanov',
        'name': 'Ivan',
        'age': 20,
        'position': 'engineer',
        'speciality': 'builder',
        'address': 'module_1',
        'email': 'ivan@test.com'
    }
)
show(r)

r = requests.post(
    BASE_URL,
    json={
        'surname': 'Petrov'
    }
)
show(r)

r = requests.get(f'{BASE_URL}/1')
show(r)

r = requests.get(f'{BASE_URL}/999')
show(r)

r = requests.delete(f'{BASE_URL}/1')
show(r)

r = requests.delete(f'{BASE_URL}/999')
show(r)
