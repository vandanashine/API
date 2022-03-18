# API Testing for 

This repo contains POC for API test automation to test https://gorest.co.in/ using the requests library of python

Test Cases
API test for testing users endpoint of https://gorest.co.in endpoint

1. Get all users.
2. Create new user
3. Get a user with gender.
4. Create an already existing user.
5. Create user without using authentication
6. Cretae user with invalid endpoint
7. Delete user
8. Update Existing user.

Prerequisites
Install prequisites using the below command

pip install -r requirements.txt

To run the tests type the command py.test test_api.py
