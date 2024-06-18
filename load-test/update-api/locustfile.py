import random
import json
from locust import HttpUser, task, between, events
from gevent.lock import Semaphore, BoundedSemaphore
import uuid

class UpdateRequest(HttpUser):
    TOTAL_DB_RECORDS = 1000  # Total records in the database
    REQUEST_COUNT_IN_SINGLE_API = 50  # Requests per batch
    user_counter = 0  # Global counter for user instances
    request_id_counter = 1  # Global counter for request IDs
    completion_semaphore = BoundedSemaphore()
    COMPLETED_REQUESTS=0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_semaphore = Semaphore()
        self.start_id = 0  
        self.end_id = 0  
        self.local_completed_requests = 0  # Counter for completed requests per user
        self.user_index = UpdateRequest.user_counter
        UpdateRequest.user_counter += 1

    def calculate_requests_per_user(self):
        if self.environment.runner and self.environment.runner.user_count > 0:
            self.TOTAL_REQUEST_COUNT__SINGLE = int(self.TOTAL_DB_RECORDS / 10)

    def on_start(self):
        self.calculate_requests_per_user()
        self.run_tasks()

    @task
    def run_tasks(self):
        while self.local_completed_requests < self.TOTAL_REQUEST_COUNT__SINGLE:
            self.assign_id_range()
            self.update()

    def assign_id_range(self):
        with UpdateRequest.completion_semaphore:
            self.start_id = UpdateRequest.request_id_counter
            UpdateRequest.request_id_counter += UpdateRequest.REQUEST_COUNT_IN_SINGLE_API
            self.end_id = UpdateRequest.request_id_counter - 1

        print(f"User {self.user_index} ID range: {self.start_id} - {self.end_id}")

    def generate_update_request(self):
        update_request = []
        for i in range(self.start_id, self.end_id + 1):
            request = {
                "reference_id": "string",
                "timestamp": "2024-05-08T11:57:18.517525Z",
                "fa": f"changedfa-{i}",
                "id": f"id-{i}",
                "name": "string",
                "scope": "details",
                "additional_info": [],
                "locale": "en",
            }
            update_request.append(request)
            i += 1  # Incrementing i within the loop
        return update_request

    def update(self):
        payload = {
            "signature": "string",
            "header": {
                "version": "1.0.0",
                "message_id": "string",
                "message_ts": "string",
                "action": "update",
                "sender_id": "string",
                "sender_uri": "",
                "receiver_id": "",
                "total_count": 0,
                "is_msg_encrypted": False,
                "meta": "string",
            },
            "message": {
                "transaction_id": "string",
                "update_request": self.generate_update_request(),
            },
        }
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            "/sync/update", data=json.dumps(payload), headers=headers
        )
        print(
            "0th Record:",
            json.loads(response.text),
        )
        self.local_completed_requests += UpdateRequest.REQUEST_COUNT_IN_SINGLE_API
        UpdateRequest.COMPLETED_REQUESTS += 1

        if UpdateRequest.COMPLETED_REQUESTS * UpdateRequest.REQUEST_COUNT_IN_SINGLE_API >= UpdateRequest.TOTAL_DB_RECORDS:
            print(f"All requests completed. Exiting Locust.")
            self.environment.runner.quit()

# Catch exceptions raised in greenlets
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    def greenlet_exception_handler(greenlet):
        environment.events.report_event(
            "greenlet_exception",
            locust_environment=environment,
            exception=greenlet.exception,
            tb=greenlet.traceback,
        )
    if environment.runner:
        for greenlet in environment.runner.greenlet.greenlets:
            greenlet.link_exception(greenlet_exception_handler)
