from locust import HttpUser, task, between
import json
import random


class ResolveRequest(HttpUser):
    TOTAL_DB_RECORDS = (
        10000000  # Make sure this is same as the total records in the database
    )
    REQUEST_COUNT_IN_SINGLE_API = 1000

    def generate_resolve_request(self):
        resolve_request = [
            {
                "reference_id": "string",
                "timestamp": "2024-05-08T11:57:18.517525Z",
                "fa": "",
                "id": f"id-{random.randint(1, self.TOTAL_DB_RECORDS)}",
                "name": "string",
                "scope": "details",
                "additional_info": [],
                "locale": "en",
            }
            for _ in range(self.REQUEST_COUNT_IN_SINGLE_API)
        ]
        return resolve_request

    @task
    def resolve(self):
        payload = {
            "signature": "string",
            "header": {
                "version": "1.0.0",
                "message_id": "string",
                "message_ts": "string",
                "action": "resolve",
                "sender_id": "string",
                "sender_uri": "",
                "receiver_id": "",
                "total_count": 0,
                "is_msg_encrypted": False,
                "meta": "string",
            },
            "message": {
                "transaction_id": "string",
                "resolve_request": self.generate_resolve_request(),
            },
        }

        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            "/sync/resolve", data=json.dumps(payload), headers=headers
        )

        # Log the response to see the record randomization
        # print(
        #     "0th Record:",
        #     json.loads(response.text)["message"]["resolve_response"][0]["id"],
        # )
        # print(
        #     "100th Record:",
        #     json.loads(response.text)["message"]["resolve_response"][100]["id"],
        # )
        # print(
        #     "200th Record:",
        #     json.loads(response.text)["message"]["resolve_response"][200]["id"],
        # )

# import random
# import json
# from locust import HttpUser, task, between, events
# from gevent.lock import Semaphore, BoundedSemaphore
# import uuid
# class LinkRequest(HttpUser):
#     TOTAL_DB_RECORDS = 1000  # Make sure this is same as the total records in the database
#     user_count = 0  # Placeholder for user count
#     REQUEST_COUNT_IN_SINGLE_API = 50  # Placeholder for requests per user
#     TOTAL_REQUESTS = 0  # Total number of requests to be made by all users
#     COMPLETED_REQUESTS = 0  # Counter for completed requests
#     TOTAL_REQUEST_COUNT__SINGLE = 0  # Shared counter for tracking request IDs
#     request_id_counter = 1
#     user_counter = 0
#     completion_semaphore = BoundedSemaphore()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user_semaphore = Semaphore()
#         self.start_id = 0  
#         self.end_id = 0  
#         self.user_counter += 1
#         self.user_index = self.user_counter

#     def calculate_requests_per_user(self):
#         if self.environment.runner and self.environment.runner.user_count > 0:
#             self.TOTAL_REQUEST_COUNT__SINGLE = int(self.TOTAL_DB_RECORDS / 10)
#         # print(f"User {self.user_index} will handle {self.REQUEST_COUNT_IN_SINGLE_API} requests.")

#     def on_start(self):
#         self.run_tasks()

#     @task
#     def run_tasks(self):
#         with self.user_semaphore:
#             self.calculate_requests_per_user() 
#             LinkRequest.start_id = LinkRequest.request_id_counter
#             LinkRequest.request_id_counter += self.REQUEST_COUNT_IN_SINGLE_API
#             LinkRequest.end_id = self.request_id_counter - 1
#             LinkRequest.TOTAL_REQUESTS = self.TOTAL_DB_RECORDS
#             LinkRequest.TOTAL_REQUEST_COUNT__SINGLE-=LinkRequest.REQUEST_COUNT_IN_SINGLE_API
#             print(f"User {self.user_index} ID range: {LinkRequest.start_id} - {LinkRequest.end_id} {LinkRequest.TOTAL_REQUEST_COUNT__SINGLE}")
            
#         while True:
#             self.link()

#     def generate_link_request(self):
#         link_request = [
#         ]
#         for _ in range(self.start_id, self.end_id + 1):
#             request = {
#                 "reference_id": "string",
#                 "timestamp": "2024-05-08T11:57:18.517525Z",
#                 "fa": f"id-{uuid.uuid4()}",
#                 "id":  f"id-{uuid.uuid4()}",
#                 "name": "string",
#                 "scope": "details",
#                 "additional_info": [],
#                 "locale": "en",
#             }
#             link_request.append(request)
#         return link_request

#     @task
#     def link(self):
#         payload = {
#             "signature": "string",
#             "header": {
#                 "version": "1.0.0",
#                 "message_id": "string",
#                 "message_ts": "string",
#                 "action": "link",
#                 "sender_id": "string",
#                 "sender_uri": "",
#                 "receiver_id": "",
#                 "total_count": 0,
#                 "is_msg_encrypted": False,
#                 "meta": "string",
#             },
#             "message": {
#                 "transaction_id": "string",
#                 "link_request": self.generate_link_request(),
#             },
#         }
#         headers = {"Content-Type": "application/json"}
#         response = self.client.post(
#             "/sync/link", data=json.dumps(payload), headers=headers
#         )
#         LinkRequest.COMPLETED_REQUESTS += 1
#         with LinkRequest.completion_semaphore:
#             if LinkRequest.COMPLETED_REQUESTS >= LinkRequest.TOTAL_REQUESTS:
#                 print(f"All requests completed. Exiting Locust.")
#                 self.environment.runner.quit()
        

# # Catch exceptions raised in greenlets
# @events.init.add_listener
# def on_locust_init(environment, **kwargs):
#     def greenlet_exception_handler(greenlet):
#         environment.events.report_event(
#             "greenlet_exception",
#             locust_environment=environment,
#             exception=greenlet.exception,
#             tb=greenlet.traceback,
#         )
#     for greenlet in environment.runner.greenlet.greenlets:
#         greenlet.link_exception(greenlet_exception_handler)

