import allure, requests, jsonschema
import pytest

from .schemas.pet_schemas import PET_schema

BASE_URL='http://5.181.109.28:9090/api/v3'
@allure.feature('Pet')
class TestPet:

    @allure.title('Попытка обновить несуществующего питомца')
    def test_update_nonexistentpet(self):
        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            payload ={
            'id' : 9999,
            'name' : "Non-existent pet",
            'status' : 'available'
            }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым.'

    @allure.title('Попытка запросить информацию о несуществующем питомце')
    def test_get_nonexistentpet(self):
        with allure.step('Отправка запроса на получение информации о несуществующем питомце'):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым.'

    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_nonexistentpet(self):
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            response = requests.delete(url=f'{BASE_URL}/pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet deleted', 'Текст ошибки не совпал с ожидаемым.'

    @allure.title("Попытка добавить питомца только с обязательными полями")
    def test_add_pet_required_fields(self):
        with allure.step('Отправка запроса на добавление питомца'):
            payload = {
                "id": 10,
                "name": "Buddy",
                "status": "available"}
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа и валидация json-схемы'):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_schema)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload['id'], "id питомца не совпал с ожидаемым"
            assert response_json["name"] == payload['name'], "Имя питомца не совпал с ожидаемым"
            assert response_json["status"] == payload['status'], "Статус питомца не совпал с ожидаемым"

    @allure.title ("Попытка добавить питомца со всеми полями")
    def test_add_pet_all_fields(self):
        with allure.step('Отправка запроса на добавление питомца'):
            payload = {
                "id": 1,
                "name": "doggie",
                "category":
                    {"id": 1,
                     "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"}
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json=response.json()

        with allure.step('Проверка статуса ответа и валидация json-схемы'):
            assert response.status_code == 200
            jsonschema.validate(response.json(),PET_schema)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload['id'],"id питомца не совпал с ожидаемым"
            assert response_json["name"] == payload['name'], "Имя питомца не совпал с ожидаемым"
            assert response_json["category"] == payload["category"],"Категория не совпала с ожидаемой"
            assert response_json["photoUrls"] == payload["photoUrls"], "строка в photoUrls не совпала с ожидаемой"
            assert response_json["tags"] == payload["tags"], "тэг не совпал с ожидаемым"
            assert response_json["status"] == payload['status'],"Статус питомца не совпал с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id (self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id (self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление информации о питомце по ID"):
            response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step("Проверка статуса ответа на удаление питомца"):
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')
        with allure.step("Проверка статуса ответа об удаленном питомце"):
            assert response.status_code == 404

    @allure.title("Обновление информации о питомце по ID")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
            payload = {
                "id": create_pet["id"],
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление информации о питомце по ID"):
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)

        with allure.step("Отправка запроса на получение информации об обновленных данных о питомце по ID"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')
            response_json=response.json()

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response_json["id"] == payload['id'], "id питомца не совпал с ожидаемым"
            assert response_json["name"] == payload['name'], "Имя питомца не совпал с ожидаемым"
            assert response_json["status"] == payload['status'], "Статус питомца не совпал с ожидаемым"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize ("status, expected_status_code",
                              [("available",200), ("sold",200)])
    def test_get_pets_by_status_positive(self,status,expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(url=f'{BASE_URL}/pet/findByStatus', params={"status":status})

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == expected_status_code
                assert isinstance(response.json(),list)

    @pytest.mark.parametrize("status, expected_status_code",
                                         [("unexpected_status", 400), ("", 400)])
    def test_get_pets_by_status_negative(self,status,expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(url=f'{BASE_URL}/pet/findByStatus', params={"status":status})

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == expected_status_code
            assert isinstance(response.json(),dict)



