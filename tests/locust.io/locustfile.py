from locust import HttpUser, SequentialTaskSet, task

class TokenUser(SequentialTaskSet):

    # Initialize variables
    def on_start(self):
        self.token = None

    # Task 1: Perform create token
    @task
    def create_token(self):
        response = self.client.post("/token", json={ "username": "user", "password": "password" })
        response = response.json()
        self.token = response['token']

    # Task 2: Perform validate token
    @task
    def validate_token(self):
        response = self.client.post("/validate", json={ 'token': self.token })
        
    # # Task 3: Perform refresh token
    @task
    def refresh_token(self):
        response = self.client.post("/refresh", json={ 'token': self.token })

class Tasks(HttpUser):
    tasks = [TokenUser]
