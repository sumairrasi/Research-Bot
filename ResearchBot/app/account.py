from ResearchBot.database.cache import save_session_to_redis,redis_client,generate_new_session_id
from ResearchBot.database.database import login_user,register_user,initialize_database
from streamlit_lottie import st_lottie 
from pathlib import Path
import streamlit as st
import redis
import json


def app():
    initialize_database()
    path = Path("animations") / "1732818093903.json"
    with open(path, "r") as file:
        url = json.load(file)
    col1, col2, col3 = st.columns([1, 4, 3])
    with col2:
        st_lottie(
            url,
            reverse=True,
            height=100,
            width=100,
            speed=1,
            loop=True,
            quality='high',
            key='Car'
        )
    try:
        redis_client.ping()
    except redis.ConnectionError:
        st.error("Redis server is not running. Please start the Redis server.")
        return

    if 'session_id' not in st.session_state or st.session_state.session_id is None:
        # Handle the case when the session_id is not initialized or expired
        st.session_state.session_id = generate_new_session_id()  # Generate a new session ID
        print(f"New session ID generated: {st.session_state.session_id}")

    st.title("Welcome to the :green[Learning Class]")

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user = st.session_state.user
        st.title(f"Welcome back, {user['username']}!")
        st.write(f"You are logged in as a {user['role']}.")

        if st.button('Logout'):
            redis_client.delete(st.session_state.session_id)
            st.session_state.clear() 
            st.success("You have logged out successfully.")
            st.rerun()
    else:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])
        if choice == 'Login':
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            login_button = st.button('Login')  

            if login_button:
                user = login_user(email, password)
                if user: 
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    save_session_to_redis(st.session_state.session_id, {
                        'logged_in': True,
                        'user': user
                    })
                    st.balloons() 
                    st.rerun() 
                else:
                    st.error("Invalid email or password. Please try again.")

        else:
            username = st.text_input("Username")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            role = st.selectbox('Role', ['student', 'Teacher'])
            sign_up_button = st.button('Sign Up') 

            if sign_up_button:
                success = register_user(username, email, password, role)
                if success:
                    st.balloons()  
                    st.success("Account created successfully!")
                    st.markdown("Please login using your credentials.")
                else:
                    st.error("An error occurred while creating the account. Please try again.")