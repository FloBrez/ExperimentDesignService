import streamlit as st
#import plotly.express as px
from datetime import date, datetime
import time
import pandas as pd
import numpy as np

# st.set_page_config(layout='wide')

st.set_page_config(page_title="PanDaS A/B Experiment Design", page_icon="🐼", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title('Experiment Design')

if not "ngroups" in st.session_state:
    st.session_state["ngroups"] = 2

# c_up contains the form
# c_down contains the add and remove buttons
st.subheader('Define Experiment Design')
c_up = st.container()
c_down = st.container()

with c_up:
    with st.form("myForm"):
        c1 = st.container() # c1 contains choices
        c2 = st.container() # c2 contains submit button
        with c2:
            st.form_submit_button("Submit")

with c_down:
    #col_l, col_r = st.columns(2)
   # with col_l:
    if st.button("Add Group"):
        st.session_state["ngroups"] += 1

    #with col_r:
    if st.button("Remove Group") and st.session_state["ngroups"] > 2:
        st.session_state["ngroups"] -= 1
        st.session_state.pop(f'{st.session_state["ngroups"]}')


for x in range(st.session_state["ngroups"]): # create many choices
    with c1:
        st.subheader("Group " + chr(65+x))
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Label for Group " + chr(65+x), key=str(x), value='Treatment' if x == 0 else 'Control')
        with col2:
            st.number_input("Size of Group " + chr(65+x), key='A' + str(x), min_value=0.00, max_value=1.00, value=0.5, step=0.01)

total_size = sum([st.session_state[f"A{x}"] for x in range(st.session_state["ngroups"])])
group_size = [st.session_state[f"A{x}"] / total_size for x in range(st.session_state["ngroups"])]

#for x in range(st.session_state["ngroups"]):
#    st.session_state[f"A{x}"] = st.session_state[f"A{x}"] / total_size


#{chr(65+x): st.session_state[f"{x}"] for x in range(st.session_state["ngroups"])}
st.subheader('Review Experiment Design')
st.table(data=pd.DataFrame([{'Group': chr(65+x), 
                             'Label': st.session_state[f"{x}"],
                             'Size': st.session_state[f"A{x}"] / total_size
                            } for x in range(st.session_state["ngroups"])]))



st.subheader("Dataset")
data_file = st.file_uploader("Upload CSV", type=["csv"])

if data_file is not None:

    file_details = {"filename":data_file.name, "filetype":data_file.type,
                    "filesize":data_file.size}
    
    df = pd.read_csv(data_file)
    #st.dataframe(df)
    #np.random.choice(['A', 'B'], replace=True, p=group_size)
    df = df.assign(assignment=np.random.choice([chr(65+x) for x in range(st.session_state["ngroups"])], size=len(df), replace=True, p=group_size))

    st.markdown("Distribution of Group Assignment")
    df_chk = df.groupby(['assignment'])\
        .agg(Observations=('assignment', 'count'))\
        .assign(Share=lambda x: x.Observations / len(df))
    st.table(df_chk)

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=data_file.name,
        mime='text/csv',
 )