import streamlit as st
import requests

API_URL="http://127.0.0.1:8000/predict"

st.title("HOUSE PRICE PREDICTOR")

st.markdown("Enter your details below:")

bhk = st.number_input("Number of bedrooms",min_value=0,value=3)
propertytype=st.selectbox("what type of property",options=["Villa","House","Flat"])
location=st.text_input("city",value="Ahmedabad")
sqft=st.number_input("give me approx square foots",min_value=100,value=1000)

if st.button("predict house price"):
    
    input_data= {
        "bhk":bhk,
        "propertytype":propertytype,
        "location":location,
        "sqft":sqft

    
}
    
    try:
        with st.spinner("predicting price..."):
         response=requests.post(API_URL,json=input_data)
         if response.status_code==200:
            result=response.json()
            st.success(f"predicted housing price : **{result['predicted_houseprice']}**")
         else:
            st.error(f"API Error :{response.status_code}-{response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FASTAPI server,make sure it's running on port 8000")
