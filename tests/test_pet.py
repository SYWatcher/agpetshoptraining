import allure, requests

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