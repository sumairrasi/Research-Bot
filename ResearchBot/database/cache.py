import streamlit as st
import json
import redis
import os
import uuid

from dotenv import load_dotenv
load_dotenv()



redis_client = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'),password=os.environ.get('REDIS_PASSWORD'), decode_responses=True)


def save_session_to_redis(session_id, session_data):
    try:
        # Store the session data in Redis as a JSON string
        redis_client.set(session_id, json.dumps(session_data))
        print(f"Session saved to Redis: {session_id}")
    except redis.ConnectionError as e:
        st.error("Could not connect to Redis while saving session.")
        print(f"Redis save error: {e}")




def generate_new_session_id():
    return str(uuid.uuid4())