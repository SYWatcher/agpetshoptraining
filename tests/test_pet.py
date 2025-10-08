import allure, requests, jsonschema
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

    @allure.title ("Попытка добавить несуществующего питомца")
    def test_add_nonexistentpet(self):
        with allure.step('Отправка запроса на добавление несуществующего питомца'):
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



