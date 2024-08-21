import requests

# from rest_framework import serializers
# from django.contrib.auth import get_user_model
import json

# from django.conf import settings
# from rest_framework import status, exceptions
# from django.contrib.auth.models import User


# User = get_user_model()


class Khalti:
    def __init__(self, token=None):
        # self.SECRET_KEY = settings.KHATLI_SECRET_KEY
        # self.PUBLIC_KEY = settings.KHATLI_PUBLIC_KEY
        # self.API_URL = settings.KHATLI_API_URL
        self.SECRET_KEY = "test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
        self.PUBLIC_KEY = "test_public_key_8fa3cfb909e2413483e9192cf21cc0ba"
        self.API_URL = "https://a.khalti.com/api/v2/"
        self.token = token

    #         KHATLI_API_URL='https://a.khalti.com/api/v2/'
    # KHATLI_SECRET_KEY='live_secret_key_68791341fdd94846a146f0457ff7b455'
    # KHATLI_PUBLIC_KEY='test_public_key_8fa3cfb909e2413483e9192cf21cc0ba'

    def generate_payment_link(self, amount: int = 10000, user=None, order=None):
        endpoint = "epayment/initiate/"
        url = f"{self.API_URL}{endpoint}"
        
        payload = json.dumps(
            {
                "return_url": f"http://localhost:8000/payment-verification/K/1",
                "website_url": "http://localhost:8000",
                "amount": int(amount) * 100,
                "purchase_order_id": f"{order}",
                "purchase_order_name": f"{order}",
                "customer_info": {
                    "name": "testuser",
                    "email": "testuser@gmail.com",
                    "phone": "9800000001",
                },
            }
        )
        headers = {
            "Authorization": "key live_secret_key_68791341fdd94846a146f0457ff7b455",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json().get("payment_url")
        khalti_response = response.json()
        error_message = khalti_response
        if khalti_response.get("error_key") is not None:
            error_message = khalti_response.get("detail")
        raise Exception(f"Khalti payment error: \n {error_message}")

    def get_payment_status(self, total_price):
        end_point = "epayment/lookup/"
        response = requests.post(
            url=self.API_URL + end_point,
            headers={
                "Authorization": f"key live_secret_key_68791341fdd94846a146f0457ff7b455",
                "Content-Type": "application/json",
            },
            json={
                #   for test purpose
                #   kkNgakkVCB2dAuP2F9WmXT
                "pidx": self.token
            },
        )
        data = response.json()
        if response.status_code == 200:
            return True

        if response.status_code == 401:
            raise serializers.ValidationError({"details": "Invalid Token"})

        if response.status_code == 404:
            raise serializers.ValidationError(
                {"details": "Incorrect token i.e. Payment Id from khalti "}
            )

        if response.status_code == 504:
            # need to return 504
            raise exceptions.APIException(
                {
                    "details": "Khalit valdiation api not responding.. Connection time out"
                }
            )

        # raise exceptions.APIException({'details':response.text})
        # aile lai temporary ned to check if the status is completed or not
        return serializers.ValidationError(
            {"details": "There might be issue with khalti api.."}
        )


khalti = Khalti()
print(khalti.generate_payment_link())
# print(khalti.get_payment_status('kkNgakkVCB2dAuP2F9WmXT'))
