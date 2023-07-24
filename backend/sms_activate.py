from time import sleep

import requests


class SmsActivateClient:
    def __init__(self, apiKey):
        self.api_key = apiKey
        self.session = requests.session()

    def get_balance(self):
        """Получение баланса аккаунта"""
        try:
            response = self.session.get(
                f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getBalance").text.split(
                ":")[1]
            return float(response)
        except Exception as ex:
            return -1

    def get_countries_prices_array_telegram(self):
        """Получение списка стран и цен на Telegram"""
        try:
            response = self.session.get(
                f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getTopCountriesByService&service=tg").json()
            countries = {}
            for key in response:
                countries.update({
                    response[key]['country']: response[key]['retail_price']
                })
            return countries
        except Exception as ex:
            pass

    def get_telegram_number(self):
        """Заказ номера Telegram"""
        try:
            while True:
                countries = [6]
                for country in countries:
                    response = self.session.get(
                        f"https://sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getNumber&service=tg&ref=415296&country={country}").text
                    if "ACCESS_NUMBER" in response:
                        return response.split(":")[1], response.split(":")[2]
                    sleep(2)
                sleep(10)
        except Exception as ex:
            print(ex)
        return "", ""

    def get_number_status(self, activationId):
        """Получение статуса активации"""
        try:
            response = self.session.get(
                f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getStatus&id={activationId}").text
            if response == "STATUS_WAIT_CODE":
                return ""
            return response.split(":")[1]
        except:
            pass
        return "", ""

    def ban_number(self, activationId):
        """Отмена заказа активации"""
        try:
            print("BAN " + self.session.get(
                f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=setStatus&id={activationId}&status=8").text)
        except Exception as ex:
            pass

    def confirm_number(self, activationId):
        """Подтверждение заказа активации"""
        try:
            print("CONFIRM " + self.session.get(
                f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=setStatus&id={activationId}&status=6").text)
        except Exception as ex:
            pass
