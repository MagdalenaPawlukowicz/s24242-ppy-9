import streamlit as st
import pandas as pd
import datetime

users = [
    {"user_id": 1, "name": "John Doe", "email": "johndoe@example.com", "contact_number": "123-456-7890"},
    {"user_id": 2, "name": "Jane Smith", "email": "janesmith@example.com", "contact_number": "234-567-8901"},
    {"user_id": 3, "name": "Bob Johnson", "email": "bobjohnson@example.com", "contact_number": "345-678-9012"},
    {"user_id": 4, "name": "Alice Brown", "email": "alicebrown@example.com", "contact_number": "456-789-0123"},
    {"user_id": 5, "name": "Charlie Davis", "email": "charliedavis@example.com", "contact_number": "567-890-1234"},
    {"user_id": 6, "name": "Diane Wilson", "email": "dianewilson@example.com", "contact_number": "678-901-2345"},
    {"user_id": 7, "name": "Edward Harris", "email": "edwardharris@example.com", "contact_number": "789-012-3456"},
    {"user_id": 8, "name": "Fiona Clark", "email": "fionaclark@example.com", "contact_number": "890-123-4567"},
    {"user_id": 9, "name": "George Miller", "email": "georgemiller@example.com", "contact_number": "901-234-5678"},
    {"user_id": 10, "name": "Hannah Moore", "email": "hannahmoore@example.com", "contact_number": "012-345-6789"}
]

equipment = [
    {"id": 1, "name": "Kayak", "max_available": 10, "price-per-day": 40},
    {"id": 2, "name": "Paddle Board", "max_available": 10, "price-per-day": 30},
    {"id": 3, "name": "Life Jacket", "max_available": 10, "price-per-day": 15},
    {"id": 4, "name": "Canoe", "max_available": 10, "price-per-day": 100},
    {"id": 5, "name": "Water Skis", "max_available": 5, "price-per-day": 100},
    {"id": 6, "name": "Row Boat", "max_available": 5, "price-per-day": 120},
    {"id": 7, "name": "Surfboard", "max_available": 5, "price-per-day": 100},
    {"id": 8, "name": "Sailing Boat", "max_available": 5, "price-per-day": 300},
    {"id": 9, "name": "Snorkel Gear", "max_available": 8, "price-per-day": 45},
    {"id": 10, "name": "Wakeboard", "max_available": 10, "price-per-day": 40}
]

users_data = pd.DataFrame(users)
equipment_data = pd.DataFrame(equipment)

rentals_data = pd.read_csv('rentals.csv')
rentals_data['rental_date'] = pd.to_datetime(rentals_data['rental_date'])
def load_rentals_data():
    try:
        df = pd.read_csv('rentals.csv')
        df['rental_date'] = pd.to_datetime(df['rental_date'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['user_id', 'equipment_id', 'rental_date', 'quantity','price'])
def save_rentals_data(df):
    df.to_csv('rentals.csv', index=False)

def display_available_equipment_for_date(selected_date, equipment_data, rentals_data):
    daily_rentals = rentals_data[rentals_data['rental_date'].dt.date == selected_date]
    rented_quantities = daily_rentals.groupby('equipment_id').quantity.sum().to_dict()
    equipment_available = equipment_data.copy()

    equipment_available['available'] = equipment_available.apply(
        lambda row: row['max_available'] - rented_quantities.get(row['id'], 0), axis=1)

    equipment_available = equipment_available[['id', 'name', 'available']]
    equipment_available.columns = ['Equipment ID', 'Equipment Name', 'Available Quantity']

    st.dataframe(equipment_available)



st.title("Water Equipment Rental Service")
st.write("Welcome to the Water Equipment Rental Service.")

tab1, tab2, tab3, tab4 = st.tabs(["Available Equipment", "Rent Equipment", "Check Rentals", "Rentals This Month"])

with tab1:
    st.header("Available Equipment")
    selected_date = st.date_input("Select Date", value=datetime.date.today())
    display_available_equipment_for_date(selected_date, equipment_data, rentals_data)


with tab2:
    st.header("Rent Equipment")
    rentals_data = load_rentals_data()

    with st.form("rent_form"):
        user_id = st.text_input('User ID')
        equipment_id = st.selectbox('Equipment ID', equipment_data['id'].unique())
        rental_date = st.date_input("Rental Date", value=datetime.date.today())
        quantity = st.number_input("Quantity", min_value=1, value=1)
        submit_rent = st.form_submit_button("Rent")

        if submit_rent:
            if int(user_id) in users_data['user_id'].values:
                rentals_data = load_rentals_data()
                print("="*50, rentals_data)
                rented_quantities = rentals_data[rentals_data['rental_date'].dt.date == rental_date].groupby('equipment_id').quantity.sum()
                max_available = equipment_data.set_index('id').at[int(equipment_id), 'max_available']
                rented = rented_quantities.get(int(equipment_id), 0)
                available_quantity = max_available - rented

                if available_quantity >= int(quantity):
                    price_per_day = equipment_data.set_index('id').at[int(equipment_id), 'price-per-day']
                    total_price = int(quantity) * price_per_day
                    new_rental = pd.DataFrame([{
                        'user_id': int(user_id),
                        'equipment_id': int(equipment_id),
                        'rental_date': rental_date,
                        'quantity': int(quantity),
                        'price': total_price
                    }])
                    new_rental['rental_date'] = pd.to_datetime(new_rental['rental_date'])
                    rentals_data = pd.concat([rentals_data, new_rental], ignore_index=True)
                    print("+"*50, rentals_data)
                    save_rentals_data(rentals_data)
                    st.success("Equipment rented successfully!")
                else:
                    st.error("Not enough equipment available.")
            else:
                st.error("Invalid User ID.")


with tab3:
    st.header("Check Your Rentals")
    input_user_id = st.text_input("Enter your User ID to view your rentals:")
    submit_check = st.button("Check Rentals")
    if submit_check:
        user_rentals = rentals_data[rentals_data['user_id'] == int(input_user_id)]
        if not user_rentals.empty:
            st.dataframe(user_rentals)
        else:
            st.warning("No rental records found for this user.")

with tab4:
    st.write('Oto ciekawe dane:')

    rentals_data = load_rentals_data()

    current_date = datetime.date.today()
    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = (first_day_of_month + pd.offsets.MonthEnd(1)).date()

    date_range = pd.date_range(start=first_day_of_month, end=last_day_of_month, freq='D')

    if not rentals_data.empty:
        rentals_data['rental_date'] = rentals_data['rental_date'].dt.date
        grouped = rentals_data.groupby(['rental_date', 'equipment_id']).quantity.sum()
        daily_equipment_rentals = grouped.unstack(fill_value=0)

        daily_equipment_rentals = daily_equipment_rentals.reindex(date_range.date, fill_value=0)
        daily_equipment_rentals.index = [date.strftime('%d %b') for date in daily_equipment_rentals.index]

        if 'equipment_data' in globals():
            equipment_names_dict = equipment_data.set_index('id').name.to_dict()
            daily_equipment_rentals.columns = [equipment_names_dict.get(int(col), col) for col in daily_equipment_rentals.columns]

        st.line_chart(daily_equipment_rentals)
    else:
        st.write("No rental data available to display.")
        empty_chart_data = pd.DataFrame(0, index=[date.strftime('%d %b') for date in date_range], columns=['No Data'])
        st.line_chart(empty_chart_data)

