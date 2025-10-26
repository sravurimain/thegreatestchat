# GreatestChat

## Description

Goal of this project is to ...

## Requirements and Scope

Build a chat messaging service.

- A way to send messages many to many
- User account creation
  -- Unique username and passwords
- Upload images and videos (any object)
- Tag messages (with like/dislike/any other emoji)
- Adding user meta data (adding phone contacts, profiles)
- Chat history. How deep? Current session/past few sessions/day/month/forever
- How many users we can support
- Text limit, file size limit, messaging limit (photos, text, videos)
- Search and add users<200b>
- Search chat history
- End to end encryption between users
- Be able to reply to a specific message
- Last active time period and GeoLocation<200b>
- Show if active now
- Explore Page
- Subscription plans
- GPT Wrapper<200b>
- Scheduled replies<200b>
- Custom replies
  All this into a web app

## Learning

- Week1: Client server model in Python
- Create a user management (create, modify, delete, get, CRUD api)
- Client should send messages to a given user, and server should save it
- Client should receive messages from a given user, and server should save it
- Be able to send and receive any type of message data type
- Time based polling to receive messages from the server
  "

## Running the program

- Install the dependencies, this will also run the server (app.py)
- `python3 -m pip install fastapi uvicorn "pydantic[dotenv]" requests
uvicorn app:app --reload --port 8000`
- Run the client (after the server is running)
- `python3 client.py`
- Example: Curl request to the server to get the list of users
- `curl -k 127.0.0.1:8000/api/v1/users`
- Example: Curl request to add user
- `curl -X POST -H "Content-Type: application/json" -d '{"username":"sai", "email":"sravuri@gmail.com", "display_name":"wasabi"}' http://127.0.0.1:8000/api/v1/users`
