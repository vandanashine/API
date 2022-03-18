import requests
import pytest
import yaml
from requests.structures import CaseInsensitiveDict
import random


class TestUsers(object):
    """
    Test for testing users endpoint of https://gorest.co.in
    """
    format = "json"
    endpoint = "https://gorest.co.in"
    url = "/public/v2/users/"
    test_url = endpoint + url

    @staticmethod
    def search_key_in_response(full_response, search_for):
        """
        Test Helper method to find a specific string in the response body.
        """
        check = True
        user_list = full_response
        if search_for not in user_list.text:
            check = False
        else:
            user_list = user_list.json()
            for users in user_list:
                for keys in users:
                    if users[keys] == search_for:
                        check = True
        return check

    def setup_method(self):
        """
        This method is responsible to get all the configuration details required for this test set
        """
        test_config_file = open("test_config.yaml", "r")
        setting = yaml.safe_load(test_config_file)
        self.headers = CaseInsensitiveDict()
        self.headers["Accept"] = setting["Content-Type"]
        self.headers["Authorization"] = setting["authorization"]

    @staticmethod
    def payload_generator():
        """
        This method returns payload Json with random email
        :return: json
        """
        num = random.randint(0, 1000000)
        payload = {
            "name": "vandana" + str(num),
            "email": "vandana" + str(num) + "@mailinator.com",
            "gender": "male",
            "status": "active"
        }
        return payload

    # Test-1
    def test_get_users(self):
        """
        First Case : To get user specific user from https://gorest.co.in/public/v2/users using email address
        """
        response = requests.get(self.test_url, headers=self.headers)
        assert response.status_code == 200

    # Test-2
    def test_create_a_user(self):
        """
        Second Case : Create a user by specifying name, email, gender, status
        """
        payload = self.payload_generator()
        response = requests.post(self.test_url, params=payload, headers=self.headers)
        assert response.status_code == 201
        # now checking if the user has been created or not using GET method.
        response_after = requests.get(self.test_url, params={"email": payload['email']}, headers=self.headers)
        assert self.search_key_in_response(response_after, payload['email'])

    # Test-3
    @pytest.mark.parametrize("gender", ["female"])
    def test_get_a_user(self, gender):
        """
        Third Case : List all users having gender as female
        """
        payload = {"gender": gender}
        response = requests.get(self.test_url, params=payload, headers=self.headers)
        # searching if gender is present in response or not.
        check = self.search_key_in_response(response, gender)
        assert check is True

    # Test-4
    def test_create_an_existing_user(self):
        """
        Fourth Case : Try to create an existing user - Expected Return Code: 422
        """
        payload = self.payload_generator()
        response = requests.post(self.endpoint + self.url, params=payload, headers=self.headers)
        assert response.status_code == 201

        # Again trying to create user with same parameters
        response_duplicate = requests.post(self.endpoint + self.url, data=payload, headers=self.headers)
        assert response_duplicate.status_code == 422

    # Test-5
    def test_create_user_without_authentication(self):
        """
        Fifth Case : Try to create new user without authentication
        """
        payload = self.payload_generator()
        response = requests.post(self.endpoint + self.url, params=payload)
        assert response.status_code == 401

    # Test-6
    def test_create_user_with_invalid_endpoint(self):
        """
        sixth Case : Try to create new user with invalid endpoint
        """
        invalid_test_url = "https://gorest.co.in/public/v/users"
        payload = self.payload_generator()
        response = requests.post(invalid_test_url, params=payload)
        assert response.status_code == 404

    # Test-7
    def test_delete_user(self):
        """
        Seventh Case : Delete users
        """
        response = requests.get(self.test_url, headers=self.headers)
        for users in response.json():
            user_id = users['id']
        delete_test_url = self.test_url + str(user_id)
        response = requests.delete(delete_test_url, headers=self.headers)
        assert response.status_code == 204

    # Test 8
    def test_update_user(self):
        """
        Eighth Case : user is successfully able to update user info with id
        """
        user_id = 23182
        update_test_url = self.test_url + str(user_id)
        payload = self.payload_generator()
        response = requests.patch(update_test_url, params=payload, headers=self.headers)
        assert response.status_code == 200
