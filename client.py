# client.py
import requests
from pprint import pprint

BASE = "http://127.0.0.1:8000/api/v1"


def create_user(username, email, display_name=None):
    payload = {"username": username, "email": email, "display_name": display_name}
    r = requests.post(f"{BASE}/users", json=payload)
    r.raise_for_status()
    return r.json()


def list_users():
    r = requests.get(f"{BASE}/users")
    r.raise_for_status()
    return r.json()


def get_user(user_id):
    r = requests.get(f"{BASE}/users/{user_id}")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def update_user(user_id, email=None, display_name=None):
    payload = {}
    if email is not None:
        payload["email"] = email
    if display_name is not None:
        payload["display_name"] = display_name
    r = requests.patch(f"{BASE}/users/{user_id}", json=payload)
    r.raise_for_status()
    return r.json()


def delete_user(user_id):
    r = requests.delete(f"{BASE}/users/{user_id}")
    if r.status_code == 404:
        return False
    r.raise_for_status()
    return True


def create_password(user_id, password):
    payload = {"password": password}
    r = requests.post(f"{BASE}/users/{user_id}/password", json=payload)
    r.raise_for_status()
    return r.status_code == 201


if __name__ == "__main__":
    print("Creating users...")
    alice = create_user("alice", "alice@example.com", "Alice A.")
    bob = create_user("bob", "bob@example.com", "Bobby")
    pprint(alice)
    pprint(bob)

    print("\nListing users:")
    pprint(list_users())

    print("\nGet Alice:")
    pprint(get_user(alice["id"]))

    print("\nUpdate Bob display_name:")
    updated = update_user(bob["id"], display_name="Robert")
    pprint(updated)

    print("\nDelete Alice:")
    ok = delete_user(alice["id"])
    print("deleted:", ok)

    print("\nFinal users:")
    pprint(list_users())
