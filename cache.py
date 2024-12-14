import streamlit as st
import json
import redis
import os
from dotenv import load_dotenv
load_dotenv()



redis_client = redis.StrictRedis(host=st.secrets['REDIS_HOST'], port=st.secrets['REDIS_PORT'],password=st.secrets['REDIS_PASSWORD'], decode_responses=True)


def save_session_to_redis(session_id, data, expiry=86400):
    try:
        redis_client.set(session_id, json.dumps(data), ex=expiry)
        print(f"Session saved to Redis: {session_id} -> {data}")
    except redis.ConnectionError as e:
        st.error("Could not save session to Redis.")
        print(f"Redis save error: {e}")

def load_session_from_redis(session_id):
    try:
        data = redis_client.get(session_id)
        print(f"Session loaded from Redis: {session_id} -> {data}")
        return json.loads(data) if data else None
    except redis.ConnectionError as e:
        st.error("Could not connect to Redis.")
        print(f"Redis load error: {e}")
        return None