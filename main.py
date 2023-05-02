import streamlit as st
from streamlit import sidebar  as sd 
import pandas as pd
import numpy as np


st.markdown("# Home")
st.sidebar.markdown("# Home")


sd.title("Export cards configuration")
sd.title("")

# Add a slider to the sidebar:
lexical_similarity  = sd.slider( 'Select lexical similarity percentage', 0.0, 100.0,value=80.0,step=1.0)
# Add a slider to the sidebar:
semantic_similarity = sd.slider( 'Select semantic similarity percentage', 0.0, 1.0,value=0.8,step=0.1)

loaded = False
data = pd.DataFrame(data={"ru_word":[],"en_word":[],"translation":[]})
NOUN = True
VERB = True
ADJ = True

def load_data():
        data = pd.read_csv('./db_fixed.csv')
        data = data[["ru_word","ru_tag","en_word","translation","syn_ratio","sem_ratio"]]
        if NOUN == False :
           data = data[data["ru_tag"]!="NOUN"]
        if VERB == False :
           data = data[data["ru_tag"]!="VERB"] 
        if ADJ == False :
           data = data[data["ru_tag"]!="ADJ"]  

        data = data[(data['sem_ratio']>=semantic_similarity) & (data['syn_ratio']>=lexical_similarity) ]

        if loaded:   
           data  
           st.write("Total " + str(len(data)))

def convert_df_to_csv():
        data = pd.read_csv('./db_fixed.csv')
        if NOUN == False :
           data = data[data["ru_tag"]!="NOUN"]
        if VERB == False :
           data = data[data["ru_tag"]!="VERB"] 
        if ADJ == False :
           data = data[data["ru_tag"]!="ADJ"]  

        data = data[(data['sem_ratio']>=semantic_similarity) & (data['syn_ratio']>=lexical_similarity) ]
        data = data[["ru_word","en_word","translation"]]
        return data.to_csv(header=False,index=False).encode('utf-8')

NOUN = sd.checkbox('NOUN',key=0,value=True,on_change=load_data())
VERB = sd.checkbox('VERB',key=1,value=True,on_change=load_data())
ADJ = sd.checkbox('ADJ',key=2,value=True,on_change=load_data())                     


st.header("russian|english synonyms flashcards")
st.subheader("Export cards and start learning")
st.title("")
loaded = True
load_data()

st.download_button(
   "Export Cards",
   convert_df_to_csv(),
   "cards.csv",
   "text/csv"
)

# # Create a text element and let the reader know the data is loading.
# data_load_state = sd.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')

# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
