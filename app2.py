import streamlit as st
#import plotly.express as px
from datetime import date, datetime
import time
import pandas as pd
import numpy as np
from utils import img_to_bytes

# st.set_page_config(layout='wide')

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#set_bg_hack_url()

#st.image('https://images.unsplash.com/photo-1542281286-9e0a16bb7366', caption='Sunrise by the mountains')

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

st.title('Meine Streamlit App')

body = """
# Überschrift
Lorem ipsum

$$ y = f(x) $$
"""

st.markdown(body)

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache
def load_data():
    data = pd.read_json('https://brezinaf-counter.s3.eu-central-1.amazonaws.com/weight.json')
    data = data.assign(CreatedAt = lambda x: pd.to_datetime(x.CreatedAt))
    return data

data_load_state = st.text('Lade Daten...')
data = load_data()
data_load_state.text('Daten geladen!')

with st.spinner(text='In progress'):
    time.sleep(5)
    st.success('Done')

st.metric('Anzahl Datenpunkte', len(data))

if st.checkbox('Rohdaten anzeigen'):
    st.subheader('Daten')
    st.write(data.filter(items=['CreatedAt', 'Weight']))


st.subheader('Uhrzeit der Dateneingabe')
hist_values = np.histogram(data.CreatedAt.dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

with st.expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
     st.image("https://static.streamlit.io/examples/dice.jpg")


st.subheader('Eingabe Gewicht')
with st.form(key='input_form'):
    weight = st.number_input('Gewicht (kg)', min_value=70.0, max_value=100.0, value=85.0, step=0.1, format=None)
    check = st.checkbox('Nüchtern/Morgens')
    input_date = st.date_input('Datum', value=date.today())
    input_time = st.time_input('Zeit')
    st.form_submit_button('Senden')




#chart_data = pd.DataFrame(index = data.CreatedAt, data = {'Weight': data2.Weight})
#data2.set_index('CreatedAt', inplace=True)
#st.write(chart_data)
#st.line_chart(data)
#st.line_chart(data2)



#fig = px.line(data2, x="CreatedAt", y="Weight", title='Life expectancy in Canada')
#st.plotly_chart(fig, use_container_width=True)
#st.line_chart(data2.set_index('CreatedAt'))




#API = 'https://ohwuyhglyl.execute-api.eu-central-1.amazonaws.com/Prod/logs/{logId}/datasets/{datasetId}/entries'
#LOG_ID = 'florianb'
#DATASET_ID = 'weight'
# S3_BUCKET = 'personallogservice-logs-sfvygtvbkrjn'
# URL_BASE = 'https://s3-eu-central-1.amazonaws.com/'
# url = 'https://s3-eu-central-1.amazonaws.com/personallogservice-logs-sfvygtvbkrjn/florianb/weight/weight.json'

# def read_s3_json(key:str) -> dict:
#     s3         = boto3.resource('s3')
#     obj        = s3.Object(bucket, key)
#     data       = json.loads(obj.get()['Body'].read().decode())
#     return data 

# def get_log_data(personal_log_id:str, entry_type:str = None) -> list:
#     key           = '{PersonalLogId}/{EntryType}/{EntryType}.json'.format(PersonalLogId = personal_log_id, EntryType=entry_type)
#     entries_data  = read_s3_json(key=key)
#     return entries_data