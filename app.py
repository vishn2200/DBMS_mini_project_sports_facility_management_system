import streamlit as st
from streamlit_card import card
import hashlib
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta


def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='dbms1234',
        database='sfbs'
    )


# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# User registration
def register_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO auth (srn, passwd) VALUES (%s, %s)",
                   (username, hashed_password))
    conn.commit()


# User login
def login_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT passwd FROM auth WHERE srn = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    if result is not None and result[0] == hash_password(password):
        return True
    return False


# Authentication page
def login_page():
    st.title("User Authentication")
    st.markdown("<h1 style='color: #87CEEB;'>Login</h1>",
                unsafe_allow_html=True)
    username = st.text_input("SRN")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.user = username  # Store the username in session_state
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials")
    st.write("Forgot password? Contact the administrator to reset password.")

    st.markdown("<h1 style='color: #87CEEB;'>Register</h1>",
                unsafe_allow_html=True)
    new_username = st.text_input("Enter your SRN")
    new_password = st.text_input("Enter Password", type="password")
    if st.button("Register"):
        register_user(new_username, new_password)
        st.success("Registration successful!")


def main_page():
    user_srn = st.session_state.user
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM users WHERE srn = %s", (user_srn,))
    result = cursor.fetchone()
    cursor.close()
    st.write(f"Welcome, {result[0]}!")

    cursor = conn.cursor()
    cursor.execute("SELECT plan FROM users WHERE srn = %s", (user_srn,))
    result = cursor.fetchone()
    conn.close()
    plan = result[0]
    st.sidebar.markdown(
        "<style>.plan-name {color: pink; font-size: 20px; text-align: left;}</style>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f"<h1 class='plan-name'>{plan}</h1>", unsafe_allow_html=True)
    
    menu_option = st.sidebar.radio(
        "Options:",
        ("Buy Membership", "Book Facility", "Cancel Booking",
         "Booking History", "Facility and Coach Details", "Provide Feedback", "Logout")
    )

    if menu_option == "Buy Membership":
        buy_membership_page(user_srn)
    elif menu_option == "Book Facility":
        book_facility_page(user_srn, plan)
    elif menu_option == "Cancel Booking":
        cancel_booking(user_srn)
    elif menu_option == "Booking History":
        booking_history(user_srn)
    elif menu_option == "Facility and Coach Details":
        details()
    elif menu_option == "Provide Feedback":
        feedback(user_srn)
    elif menu_option == "Logout":
        log_out()


def log_out():
    st.session_state.user = None
    st.success("Logged out successfully!")
    login_page()


def buy_membership_page(srn):
    st.markdown("<h1 style='color: #87CEEB;'>Buy Membership</h1>",
                unsafe_allow_html=True)
    st.write("## Price: Rs. 10,000/-")
    st.write("The PES Sports Facility membership is valid for one academic year. Members have access to all the sports facilities i.e. all the sports courts and gym 7 days a week. All you have to do is make a booking and use the slot to the fullest. Pay once and book for free!")

    try:
        if st.button("Purchase Membership"):
            result = buy_membership(srn)
            if result == "success":
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT user_name, plan, plan_validity FROM users u, plan p WHERE u.srn = %s AND p.plan_type = 'Member'", (srn,))
                membership_details = cursor.fetchone()
                st.success("You are now a member!")
                st.write("## Membership Details:")
                st.text(f"Name: {membership_details[0]}")
                st.text(f"Plan Type: {membership_details[1]}")
                st.text(f"Plan Validity: {membership_details[2]}")
                st.text("Amount paid: Rs. 10000/-")
            elif result == "already_member":
                st.error("You are already a member.")
            else:
                st.error("An error occurred while purchasing the membership.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def buy_membership(srn):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT plan FROM users WHERE srn = %s", (srn,))
        result = cursor.fetchone()

        if result and result[0] == "Member":
            return "already_member"
        cursor.execute(
            "UPDATE users SET plan = 'Member' WHERE srn = %s", (srn,))
        conn.commit()
        return "success"
    except Exception as e:
        return "error"
    finally:
        conn.close()



def book_facility_page(srn, plan):
    st.markdown("<h1 style='color: #87CEEB;'>Book Facility</h1>",
                unsafe_allow_html=True)
    if plan == 'Non-Member':
        st.write("Price = Rs. 100/-")
        current_day = datetime.now().weekday()
        if current_day == 4:  # Friday
            available_dates = [datetime.now().date(), (datetime.now() + timedelta(days=3)).date(), (datetime.now() + timedelta(days=4)).date()]
        elif current_day == 3:  # Thursday
            available_dates = [datetime.now().date(), (datetime.now() + timedelta(days=1)).date(), (datetime.now() + timedelta(days=3)).date()]
        elif current_day == 5:
            available_dates = [(datetime.now() + timedelta(days=2)).date(), (datetime.now() + timedelta(days=3)).date(), (datetime.now() + timedelta(days=4)).date()]
        elif current_day == 6:
            available_dates = [(datetime.now() + timedelta(days=1)).date(), (datetime.now() + timedelta(days=2)).date(), (datetime.now() + timedelta(days=3)).date()]
        else:
            available_dates = [datetime.now().date(), (datetime.now() + timedelta(days=1)).date(), (datetime.now() + timedelta(days=2)).date()]
    else:
            available_dates = [datetime.now().date(), (datetime.now() + timedelta(days=1)).date(), (datetime.now() + timedelta(days=2)).date()]    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT sport_name FROM sports")
    result = cursor.fetchall()
    cursor.close()
    sport_names = [sport[0] for sport in result]
    sport = st.selectbox("Select sport", sport_names)
    date = st.date_input("Select date:", available_dates[0], min_value=available_dates[0], max_value=available_dates[2])
    start_time = datetime.strptime("13:00:00", "%H:%M:%S")
    end_time = datetime.strptime("20:00:00", "%H:%M:%S")
    time_slots = [start_time + timedelta(hours=i) for i in range (8)]
    cursor = conn.cursor()
    query_slots = f"SELECT facility.facility_id, facility.facility_name, facility.fac_location, bookings.start_time, bookings.end_time \
            FROM facility \
            JOIN sports ON facility.sport_id = sports.sport_id \
            LEFT JOIN bookings ON facility.facility_id = bookings.facility_id AND bookings.date_booked = '{date}' \
            WHERE sports.sport_name = '{sport}' \
            AND (bookings.start_time IS NULL OR bookings.end_time IS NULL OR bookings.start_time >'12:00:00' OR bookings.end_time < '20:00:00')"
    cursor.execute(query_slots)
    results = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(results, columns=['facility_id', 'facility_name', 'fac_location', 'start_time', 'end_time'])

    if not df.empty:
        selected_facility = st.selectbox("Select Facility:", df['facility_name'].unique())
        cursor = conn.cursor()
        cursor.execute("SELECT facility_id FROM facility WHERE facility_name=%s", (selected_facility,))
        result = cursor.fetchone()
        cursor.close()
        facility_id = result[0]
        available_time_slots = []
        current_datetime = datetime.now()
        for slot in time_slots:
            formatted_slots = slot.strftime("%H:%M:%S")
            current_datetime_with_slot_date = datetime(current_datetime.year, current_datetime.month, current_datetime.day, slot.hour, slot.minute, slot.second)
            if (date == current_datetime.date() and current_datetime_with_slot_date > current_datetime) or date > current_datetime.date():
                if df[(df['start_time'] <= formatted_slots) & (formatted_slots < df['end_time'])].empty:
                    available_time_slots.append(formatted_slots)

        selected_start_time = st.selectbox("Select start time:",available_time_slots)
        if selected_start_time:
            selected_start_time = datetime.strptime(str(selected_start_time), "%H:%M:%S")
            selected_end_time = selected_start_time + timedelta(hours=1)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bookings WHERE srn = %s AND date_booked = %s", (srn, date))
            existing_booking = cursor.fetchone()
            cursor.close()
            if existing_booking:
                st.warning("You already have a booking on this date. Please choose a different date.")
            else:
                if st.button("Confirm Booking"):
                    book_facility(srn, sport, facility_id, date, selected_start_time, selected_end_time, plan)
        else:
            st.warning("Please select a start time.")



def book_facility(srn, sport, facility_id, date, selected_start_time, selected_end_time, plan):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings(srn, sport_name, facility_id, date_booked, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s)", (srn, sport, facility_id, date, selected_start_time, selected_end_time))
    conn.commit()
    st.success("Booking successful!")
    st.write("## Booking Details:")
    st.text(f"SRN: {srn}")
    st.text(f"Sport: {sport}")
    st.text(f"Facility ID: {facility_id}")
    st.text(f"Date: {date}")
    st.text(f"Start time: {selected_start_time.time()}")
    if plan == 'Non-Member':
        st.text("Amount paid: Rs. 100/-")    


def timedelta_to_str(timedelta):
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:00"

def cancel_booking(user_srn):
    st.markdown("<h1 style='color: #87CEEB;'>Cancel Booking</h1>",
                unsafe_allow_html=True)
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    # Fetch upcoming bookings for the logged-in user
    cursor.execute("SELECT * FROM bookings WHERE srn=%s AND (date_booked > CURDATE() OR (date_booked = CURDATE() AND start_time > NOW()))", (user_srn,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if result:
        st.header('Your Upcoming Bookings')
        bookings_df = pd.DataFrame(result)
        filtered_bookings_df = bookings_df[(bookings_df['start_time'].dt.total_seconds() > 0) & (bookings_df['end_time'].dt.total_seconds() > 0)]
        filtered_bookings_df['start_time'] = filtered_bookings_df['start_time'].astype(str).str[7:]
        filtered_bookings_df['end_time'] = filtered_bookings_df['end_time'].astype(str).str[7:]
        st.markdown(filtered_bookings_df.to_markdown(), unsafe_allow_html=True)
        
        # User selects booking to cancel
        selected_booking_index = st.selectbox("Select booking to cancel", bookings_df.index)
        selected_booking = bookings_df.loc[selected_booking_index]
        start_time_str = timedelta_to_str(selected_booking['start_time'])

        # Show details of the selected booking
        st.write("## Selected Booking Details:")
        st.text(f"SRN: {selected_booking['srn']}")
        st.text(f"Sport: {selected_booking['sport_name']}")
        st.text(f"Facility ID: {selected_booking['facility_id']}")
        st.text(f"Date: {selected_booking['date_booked']}")
        st.text(f"Start time: {start_time_str}")
        
        # Button to confirm cancellation
        if st.button("Confirm Cancellation"):
            cancel_upcoming_booking(user_srn, selected_booking['date_booked'], start_time_str)
    else:
        st.warning("You have no upcoming bookings.")


def cancel_upcoming_booking(srn, date, start_time):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        # Check if the user has a booking at the specified date and start_time
        cursor.execute("SELECT * FROM bookings WHERE srn = %s AND date_booked = %s AND start_time = %s", (srn, date, start_time))
        existing_booking = cursor.fetchone()
        if existing_booking:
            # Delete the booking
            cursor.execute("DELETE FROM bookings WHERE srn = %s AND date_booked = %s AND start_time = %s", (srn, date, start_time))
            conn.commit()
            st.success("Booking canceled successfully!")
        else:
            st.warning("No booking found at the specified date and time.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        conn.close()


def booking_history(srn):
    st.markdown("<h1 style='color: #87CEEB;'>Booking History</h1>", unsafe_allow_html=True)
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch upcoming bookings (after the current date or for today with start time later than now)
        cursor.execute("SELECT * FROM bookings WHERE srn=%s AND (date_booked > CURDATE() OR (date_booked = CURDATE() AND start_time > NOW()))", (srn,))
        upcoming_bookings = cursor.fetchall()
        cursor.close()
        
        # Display upcoming bookings
        if upcoming_bookings:
            st.header('Upcoming Bookings')
            upcoming_bookings_df = pd.DataFrame(upcoming_bookings)
            filtered_upcoming_bookings_df = upcoming_bookings_df[(upcoming_bookings_df['start_time'].dt.total_seconds() > 0) & (upcoming_bookings_df['end_time'].dt.total_seconds() > 0)]
            filtered_upcoming_bookings_df['start_time'] = filtered_upcoming_bookings_df['start_time'].astype(str).str[7:]
            filtered_upcoming_bookings_df['end_time'] = filtered_upcoming_bookings_df['end_time'].astype(str).str[7:]
            st.markdown(filtered_upcoming_bookings_df.to_markdown(), unsafe_allow_html=True)
        else:
            st.warning("You have no upcoming bookings.")
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings WHERE srn=%s AND (date_booked < CURDATE() OR (date_booked = CURDATE() AND end_time < NOW()))", (srn,))
        completed_bookings = cursor.fetchall()
        cursor.close()
        
        # Display completed bookings
        if completed_bookings:
            st.header('Completed Bookings')
            completed_bookings_df = pd.DataFrame(completed_bookings)
            filtered_completed_bookings_df = completed_bookings_df[(completed_bookings_df['start_time'].dt.total_seconds() > 0) & (completed_bookings_df['end_time'].dt.total_seconds() > 0)]
            filtered_completed_bookings_df['start_time'] = filtered_completed_bookings_df['start_time'].astype(str).str[7:]
            filtered_completed_bookings_df['end_time'] = filtered_completed_bookings_df['end_time'].astype(str).str[7:]
            st.markdown(filtered_completed_bookings_df.to_markdown(), unsafe_allow_html=True)
        else:
            st.warning("You have no completed bookings.")
        
        # Fetch cancelled bookings
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cancelled_bookings WHERE srn=%s", (srn,))
        cancelled_bookings = cursor.fetchall()
        cursor.close()
        
        # Display cancelled bookings
        if cancelled_bookings:
            st.header("Cancelled Bookings")
            cancelled_bookings_df = pd.DataFrame(cancelled_bookings)
            filtered_cancelled_bookings_df = cancelled_bookings_df[(cancelled_bookings_df['start_time'].dt.total_seconds() > 0) & (cancelled_bookings_df['end_time'].dt.total_seconds() > 0)]
            filtered_cancelled_bookings_df['start_time'] = filtered_cancelled_bookings_df['start_time'].astype(str).str[7:]
            filtered_cancelled_bookings_df['end_time'] = filtered_cancelled_bookings_df['end_time'].astype(str).str[7:]
            st.markdown(filtered_cancelled_bookings_df.to_markdown(), unsafe_allow_html=True)
        else:
            st.warning("You have no cancelled bookings.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



def details():
    st.markdown("<h1 style='color: #87CEEB;'>PES Sports Facility Details</h1>",
                unsafe_allow_html=True)
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT 
    sport_name,
    (SELECT GROUP_CONCAT(facility_name SEPARATOR ', ') 
     FROM facility 
     WHERE facility.sport_id = sports.sport_id) AS All_Facilities,
    (SELECT CONCAT(coach_name, ', ', phone_number, ', ', email, ', ', sex) 
     FROM coaches 
     WHERE coaches.coach_id = sports.coach_id) AS Coach_Name_PhoneNumber_Email_Sex
    FROM sports''')
    result = cursor.fetchall()
    cursor.close()
    details_df = pd.DataFrame(result)     
    st.markdown(details_df.to_markdown(), unsafe_allow_html=True)

def feedback(srn):
    options = []
    st.markdown("<h1 style='color: #87CEEB;'>Feedback</h1>",
                unsafe_allow_html=True)
    st.write("Please leave your feedback/complaints here.")
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sport_name, facility_id FROM bookings WHERE srn=%s AND date_booked < CURDATE() OR (date_booked = CURDATE() AND end_time < NOW())", (srn,))
    result = cursor.fetchall()
    if result:
        for booking in result:
            sport, facility = booking
            option = sport + "-" + facility
            options.append(option)
        options_set = set(options)
        dropdown = st.selectbox("Select the sport & facility:", options_set)
        data = dropdown.split("-")
        facility_id = data[1]
        review = st.text_input("Review")
        if st.button("Submit"):
            update_feedback_table(srn, facility_id, review)


def update_feedback_table(srn, facility, review):
    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback values(%s, %s, CURDATE(), %s)", (srn, facility, review))
        conn.commit()
        st.success("Your feedback has reached us! Thank you.")
    except:
        st.warning("You have already provided feedback for this booking.")


def main():
    st.markdown("<h1 style='color: orange;'>PES SPORTS FACILITY BOOKING SYSTEM</h1>",
                unsafe_allow_html=True)

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_page()
    else:
        main_page()


if __name__ == '__main__':
    main()
