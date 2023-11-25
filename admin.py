import streamlit as st
import mysql.connector
import pandas as pd


def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='dbms1234',
        database='sfbs'
    )


def login_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT admin_passwd FROM admin WHERE admin_id = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    if result is not None and result[0] == password:
        return True
    return False


def login_page():
    st.title("Admin Authentication")
    st.write("## Login")
    username = st.text_input("Admin ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.user = username  # Store the username in session_state
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials")


def main_page():
    st.title("Admin Portal")
    admin = st.session_state.user
    st.write(f"Welcome, {admin}!")
    menu_option = st.sidebar.radio(
        "Options:",
        ("Users Data", "Insert User", "View Bookings",
         "Generate Statistics", "User Feedback", "Logout")
    )
    if menu_option == 'Users Data':
        users_data()
    elif menu_option == 'Insert User':
        insert_user()
    elif menu_option == 'View Bookings':
        view_bookings()
    elif menu_option == 'Generate Statistics':
        generate_statistics()
    elif menu_option == 'User Feedback':
        user_feedback()
    elif menu_option == 'Logout':
        log_out()


def log_out():
    st.session_state.user = None
    st.success("Logged out successfully!")
    login_page()


def generate_statistics():
    st.title("Non-Members Statistics")
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('CALL generate_non_member_booking_statistics()')
    result = cursor.fetchall()
    stats_df = pd.DataFrame(result)
    st.markdown(stats_df.to_markdown(), unsafe_allow_html=True)
    st.title(f"\n")
    st.bar_chart(data=stats_df,x="sport_name",y="total_bookings", width=5)
    cursor.close()
    conn.close()

    st.title("Member Statistics")
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('CALL generate_member_booking_statistics()')
    result = cursor.fetchall()
    cursor.close()
    stats_df = pd.DataFrame(result)
    st.markdown(stats_df.to_markdown(), unsafe_allow_html=True)
    st.bar_chart(data=stats_df,x="sport_name",y="total_bookings", width=5)
    conn.close()


def users_data():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    users_df = pd.DataFrame(result)
    st.markdown(users_df.to_markdown(), unsafe_allow_html=True)
    conn.close()


def insert_user():
    st.title("Insert New User")
    srn = st.text_input("SRN")
    user_name = st.text_input("User Name")
    email = st.text_input("Email")
    phone_number = st.number_input("Phone Number", value=0)
    dob = st.date_input("Date of Birth")
    sex = st.selectbox("Sex", ('M', 'F'))
    plan = st.selectbox("Plan", ('Member', 'Non-Member'))

    if st.button("Insert"):
        insert_new_user(srn, user_name, email, phone_number, dob, sex, plan)


def insert_new_user(srn, user_name, email, phone_number, dob, sex, plan):
    conn = connect_to_database()
    cursor = conn.cursor()

    insert_query = "INSERT INTO users (srn, user_name, email, phone_number, dob, sex, plan) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    user_data = (srn, user_name, email, phone_number, dob, sex, plan)

    try:
        cursor.execute(insert_query, user_data)
        conn.commit()
        st.success("New user inserted successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def view_bookings():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings")
    result = cursor.fetchall()
    cursor.close()
    bookings_df = pd.DataFrame(result)
    st.title("Bookings Made")
    filtered_bookings_df = bookings_df[(bookings_df['start_time'].dt.total_seconds(
    ) > 0) & (bookings_df['end_time'].dt.total_seconds() > 0)]
    filtered_bookings_df['start_time'] = filtered_bookings_df['start_time'].astype(
        str).str[7:]
    filtered_bookings_df['end_time'] = filtered_bookings_df['end_time'].astype(
        str).str[7:]
    st.markdown(filtered_bookings_df.to_markdown(), unsafe_allow_html=True)
    conn.close()

    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cancelled_bookings")
    result = cursor.fetchall()
    cursor.close()
    cancelled_bookings_df = pd.DataFrame(result)
    st.title("Bookings Cancelled")
    filtered_cancelled_bookings_df = cancelled_bookings_df[(cancelled_bookings_df['start_time'].dt.total_seconds(
    ) > 0) & (cancelled_bookings_df['end_time'].dt.total_seconds() > 0)]
    filtered_cancelled_bookings_df['start_time'] = filtered_cancelled_bookings_df['start_time'].astype(
        str).str[7:]
    filtered_cancelled_bookings_df['end_time'] = filtered_cancelled_bookings_df['end_time'].astype(
        str).str[7:]
    st.markdown(filtered_cancelled_bookings_df.to_markdown(),
                unsafe_allow_html=True)
    conn.close()


def user_feedback():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback")
    result = cursor.fetchall()
    cursor.close()
    fb_df = pd.DataFrame(result)
    st.markdown(fb_df.to_markdown(), unsafe_allow_html=True)
    conn.close()


def main():
    st.title("PES Sports Facility Booking System")

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_page()
    else:
        main_page()


if __name__ == '__main__':
    main()
