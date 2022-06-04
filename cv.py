import streamlit as st
import json
#import plotly.express as px
from datetime import date, datetime
import time
import pandas as pd
import numpy as np
import plotly.express as px
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
    img_to_bytes("header-cv.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

st.header('Curriculum Vitae')

abstract = """
I'm a trained economist with a strong background in statistics and econometrics. I apply statistics, machine
learning and causal analysis to solve business problems. I'm experienced in forcasting business
KPIs and individual customer behavior, analyzing and optimizing marketing campaigns, and building business
reports. I'm profcient with SQL, R, Python and Spark (Scala API). I commit my code to Git.
I built data pipelines and feature sets at large scale. I visualize data with Tableau and Power BI. I'm
eager to learn new technologies and new methods and tackle difficult problems. I have a strong scientific
mindset, but solve problems pragmatically.

You can find a small sample of coding projects in my public [GitHub](https://github.com/FloBrez) repositories.
"""


st.markdown(abstract)

with open('language-experience.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
fig = px.line(df, x='year', y='weight', color='language')
#data_canada = px.data.gapminder().query("country == 'Canada'")
#fig = px.bar(data_canada, x='year', y='pop')
st.plotly_chart(fig)




df = pd.DataFrame([
    dict(Task="Uni Regensburg", Start='2010-09-01', Finish='2012-03-31', Resource = "Alice"),
    dict(Task="Job B", Start='2021-09-05', Finish='2021-11-15', Resource = "Ron"),
    dict(Task="Job C", Start='2021-09-20', Finish='2021-11-30', Resource = "Alice")
])
job_gantt = px.timeline(
    df, 
    x_start="Start", 
    x_end="Finish", 
    y="Task",
    color = "Resource", #Color attribute
    template = "plotly_white", #Template attribute
)
st.plotly_chart(job_gantt)

# Data Scientist Profile

st.header('Data Scientist Profile')
st.markdown('Some explanatory text that has some **highlights** and some _other_ interesting features.')

df_ds_profile = pd.DataFrame([
    dict(domain="Math", skill_level=4),
    dict(domain="Statistics", skill_level=7),
    dict(domain="Machine Learning", skill_level=6, comment="Not good at NLP."),
    dict(domain="Causal Inference", skill_level=9),
    dict(domain="Visualization", skill_level=7),
    dict(domain="Communication", skill_level=8),
    dict(domain="Coding", skill_level=6),
    dict(domain="Engineering", skill_level=6),
])
fig_profile = px.bar(
    df_ds_profile, 
    x="skill_level", 
    y="domain",
    orientation='h',
    #title="My Data Scientist Profile",
    labels={"skill_level": "Skill Level (0-10)",
            "domain":""},
    #text="comment",
    template='plotly_white',
    hover_data={'domain':True, # remove species from hover data
                'skill_level':False, # add other column, default formatting
                'comment':True # add other column, customized formatting
     }
)
fig_profile.update_traces(hovertemplate='GDP: %{text} <br>Life Expectancy: %{y}') #
st.plotly_chart(fig_profile, config={'displayModeBar': False})

st.markdown('---')

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