import streamlit as st
import pickle
import pandas as pd

# Load the model
model = pickle.load(open("flight_rf.pkl", "rb"))

# Streamlit App
def main():
    st.title("Flight Price Prediction")

    # Input fields
    st.header("Enter flight details")

    date_dep = st.date_input("Departure Date", value=pd.Timestamp.now())
    time_dep = st.time_input("Departure Time", value=pd.Timestamp.now().time())
    date_arr = st.date_input("Arrival Date and Time", value=pd.Timestamp.now() + pd.DateOffset(days=1))
    time_arr = st.time_input("Arrival Time", value=pd.Timestamp.now().time())

    total_stops = st.selectbox("Total Stops", options=[0, 1, 2, 3, 4])

    airline = st.selectbox("Airline", options=[
        'Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 'SpiceJet',
        'Vistara', 'GoAir', 'Multiple carriers Premium economy', 'Jet Airways Business',
        'Vistara Premium economy', 'Trujet'
    ])

    source = st.selectbox("Source", options=['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
    destination = st.selectbox("Destination", options=['Cochin', 'Hyderabad', 'Kolkata'])

    # Process inputs
    Journey_day = int(date_dep.day)
    Journey_month = int(date_dep.month)
    Dep_hour = int(time_dep.hour)
    Dep_min = int(time_dep.minute)
    Arrival_hour = int(time_arr.hour)
    Arrival_min = int(time_arr.minute)

    # Calculate duration
    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)

    # Map inputs to model features
    airlines = ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers Premium economy', 'Jet Airways Business', 'Vistara Premium economy', 'Trujet']
    airline_features = [1 if airline == a else 0 for a in airlines]

    sources = ['Delhi', 'Kolkata', 'Mumbai', 'Chennai']
    source_features = [1 if source == s else 0 for s in sources]

    destinations = ['Cochin', 'Delhi', 'New_Delhi', 'Hyderabad', 'Kolkata']
    destination_features = [1 if destination == d else 0 for d in destinations]

    features = [
        total_stops, Journey_day, Journey_month, Dep_hour, Dep_min,
        Arrival_hour, Arrival_min, dur_hour, dur_min,
        *airline_features, *source_features, *destination_features
    ]

    # Predict
    if st.button("Predict"):
        prediction = model.predict([features])
        output = round(prediction[0], 2)
        st.success(f"Your Flight price is Rs. {output}")

if __name__ == "__main__":
    main()