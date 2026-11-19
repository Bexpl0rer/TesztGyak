
import random
from locust import HttpUser, between, task


class SzamosszegzoUser(HttpUser):
    wait_time = between(0.1, 0.3)

    @task
    def szam_bekuldese(self):
        number = random.randint(-100, 100)

        self.client.post(
            "/api/numbers",
            json={"number": number},
            name="POST /api/numbers"
        )
