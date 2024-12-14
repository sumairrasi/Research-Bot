from mysql.connector import Error
import streamlit as st
import sqlitecloud
import sqlite3
import os



def create_connection():
    try:
        conn = sqlitecloud.connect(os.environ.get('DB_URL'))
        if conn.is_connected():
            print("DB connected..")
            return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None


@st.cache_resource
def initialize_database():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("USE DATABASE edu_portal")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student', 'Teacher'))
            )
        """)
        conn.commit()
        conn.close()


def register_user(username, email, password, role):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("USE DATABASE edu_portal")
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                (username, email, password, role)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            st.error(f"Error registering user: {e}")
            return False
    return False


def login_user(email, password):
    try:
        conn = create_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("USE DATABASE edu_portal")
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            row = cursor.fetchone()  
            if row:
                column_names = [description[0] for description in cursor.description]
                user = dict(zip(column_names, row))
                return user
            
            conn.close()
    except sqlite3.Error as e:
            st.error(f"Error logging in: {e}")
            return None
    return None