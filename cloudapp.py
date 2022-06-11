import streamlit as st
import boto3

ddb = boto3.resource('dynamodb')
tbl = ddb.Table('experiments')
data = tbl.get_item(Key={'experimentId': '6a9f3671-193e-11eb-a153-f06e0bddbe76'}).get('Item')

st.markdown('# My Cloud App')
st.write(data)