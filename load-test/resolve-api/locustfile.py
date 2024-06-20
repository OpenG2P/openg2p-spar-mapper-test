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
