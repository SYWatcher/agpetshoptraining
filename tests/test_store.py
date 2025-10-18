import allure, requests, jsonschema

BASE_URL='http://5.181.109.28:9090/api/v3'
@allure.feature('Store')
class TestStore:
    @allure.title("Попытка отправить данные о заказе")
    def test_add_order(self):
        with allure.step("Отправка запроса о заказе"):
            payload = {"id": 1,
             "petId": 1,
             "quantity": 1,
             "status": "placed",
             "complete": True}

        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных о заказе"):
            assert response.status_code == 200, "Статус ответа не совпал с ожидаемым"
            assert response_json["id"] == payload['id'], "id заказа не совпал с ожидаемым"
            assert response_json["petId"] == payload['petId'], "id питомца не совпал с ожидаемым"
            assert response_json["quantity"] == payload['quantity'], "Количество не совпало с ожидаемым"
            assert response_json["status"] == payload['status'], "Статус заказа не совпал с ожидаемым"
            assert response_json["complete"] == payload['complete'], "Статус исполнения не совпал с ожидаемым"

    @allure.title("Попытка получить данные о заказе")
    def test_get_order(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id=create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step("Проверка статуса ответа и данных о заказе"):
            assert response.status_code == 200
            assert response.json()["id"] == order_id, "id заказа не совпал с ожидаемым"

    @allure.title("Попытка удалить данные о заказе")
    def test_delete_order(self):
        with allure.step("Отправка запроса на удаление информации о заказе"):
            response = requests.delete(url=f'{BASE_URL}/store/order/1')

        with allure.step("Проверка статуса ответа на удаление информации о заказе"):
            assert response.status_code == 200, "Статус ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удаленном заказе"):
            response = requests.get(url=f'{BASE_URL}/store/order/1')
        with allure.step("Проверка статуса ответа на получение информации об удаленном заказе"):
            assert response.status_code == 404, "Статус ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_add_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')

        with allure.step("Проверка статуса ответа и данных о заказе"):
            assert response.status_code == 404, "Статус ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию об инвентаре магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение информации об инвентаре магазина"):
            response = requests.get(url=f'{BASE_URL}/store/inventory')

        with allure.step("Проверка статуса ответа и типа данных"):
            assert response.status_code == 200, "Статус ответа не совпал с ожидаемым"
            assert isinstance(response.json(), dict), "Тип данных не совпал с ожидаемым"