
import random
import json
from locust import HttpUser, task, between, events
from gevent.lock import Semaphore, BoundedSemaphore
import uuid

class UnlinkRequest(HttpUser):
    TOTAL_DB_RECORDS = 1000  # Total records in the database
    REQUEST_COUNT_IN_SINGLE_API = 100  # Requests per batch
    USER_COUNTER = 0  # Global counter for user instances
    REQUEST_ID_COUNTER = 1  # Global counter for request IDs
    completion_semaphore = BoundedSemaphore()
    COMPLETED_REQUESTS=0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_semaphore = Semaphore()
        self.start_id = 0  
        self.end_id = 0  
        self.local_completed_requests = 0  # Counter for completed requests per user
        self.user_index = UnlinkRequest.USER_COUNTER
        UnlinkRequest.USER_COUNTER += 1

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
            self.unlink()

    def assign_id_range(self):
        with UnlinkRequest.completion_semaphore:
            self.start_id = UnlinkRequest.REQUEST_ID_COUNTER
            UnlinkRequest.REQUEST_ID_COUNTER += UnlinkRequest.REQUEST_COUNT_IN_SINGLE_API
            self.end_id = UnlinkRequest.REQUEST_ID_COUNTER - 1

        print(f"User {self.user_index} ID range: {self.start_id} - {self.end_id}")

    def generate_unlink_request(self):
        unlink_request = []
        for i in range(self.start_id, self.end_id + 1):
            request = {
                "reference_id": "string",
                "timestamp": "2024-05-08T11:57:18.517525Z",
                "fa": f"id-{i}",
                "id": f"id-{i}",
                "name": "string",
                "scope": "details",
                "additional_info": [],
                "locale": "en",
            }
            unlink_request.append(request)
            i += 1  # Incrementing i within the loop
        return unlink_request

    def unlink(self):
        payload = {
            "signature": "string",
            "header": {
                "version": "1.0.0",
                "message_id": "string",
                "message_ts": "string",
                "action": "unlink",
                "sender_id": "string",
                "sender_uri": "",
                "receiver_id": "",
                "total_count": 0,
                "is_msg_encrypted": False,
                "meta": "string",
            },
            "message": {
                "transaction_id": "string",
                "unlink_request": self.generate_unlink_request(),
            },
        }
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            "/sync/unlink", data=json.dumps(payload), headers=headers
        )
        # print(
        #             "0th Record:",
        #             json.loads(response.text),
        #         )
        self.local_completed_requests += UnlinkRequest.REQUEST_COUNT_IN_SINGLE_API
        UnlinkRequest.COMPLETED_REQUESTS += 1

        if UnlinkRequest.COMPLETED_REQUESTS * UnlinkRequest.REQUEST_COUNT_IN_SINGLE_API >= UnlinkRequest.TOTAL_DB_RECORDS:
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
