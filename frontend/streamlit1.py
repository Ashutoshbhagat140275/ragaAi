import streamlit as st
import requests
from gtts import gTTS
import os

BACKEND_URL = "https://your-backend-service.onrender.com"
# st.title("hello,streamlit")
# st.write("this is streamlit")

# name=st.text_input("Please input your name")
# age=st.number_input("Please entre your age",min_value=0,max_value=90,step=2)

# if(name and age):
#     st.write(f"Hi {name} your age is {age}")

# if "count" not in st.session_state:
#     st.session_state.count=0

# if st.button("Increment"):
#     st.session_state.count+=1

# if st.button("double"):
#     st.session_state.count*=2

# st.write(f"Current count:{st.session_state.count}")

# st.title("multi-step from example")

# if "step" not in st.session_state:
#     st.session_state.step=1
# if "form_data" not in st.session_state:
#     st.session_state.form_data={}

# if st.session_state.step==1:
#     name=st.text_input("Enter name")
#     if st.button("Next",key="Next1"):
#         st.session_state.form_data["name"]=name
#         st.session_state.step=2

# if st.session_state.step==2:
#     age=st.number_input("Enter your age",min_value=0,max_value=60,step=1)
#     if st.button("Next",key="Next2"):
#         st.session_state.form_data["age"]=age
#         st.session_state.step=3

# if st.session_state.step==3:
#     sex=st.selectbox("select your sex",["Male","Female"])
#     if st.button("Submit",key="Submit"):
#         st.session_state.form_data["gender"]=sex
#         st.session_state.step=4

# if st.session_state.step==4:
#     st.write("Form data:")
#     st.write(st.session_state.form_data)
#     if st.button("Restart",key="Restart"):
#         st.session_state.step=1
#         st.session_state.from_data={}

# if "step" not in st.session_state:
#     st.session_state.step=1
# if "form_data" not in st.session_state:
#     st.session_state.form_data={}

# if st.session_state.step == 1:
#     name = st.text_input("Enter name")
#     if st.button("Next", key="next1"):
#         st.session_state.form_data["name"] = name
#         st.session_state.step = 2

# if st.session_state.step == 2:
#     age = st.number_input("Enter your age", min_value=0, max_value=60, step=1)
#     if st.button("Next", key="next2"):
#         st.session_state.form_data["age"] = age
#         st.session_state.step = 3

# if st.session_state.step == 3:
#     sex = st.selectbox("select your sex", ["Male", "Female"])
#     if st.button("Submit", key="submit"):
#         st.session_state.form_data["gender"] = sex
#         st.session_state.step = 4

# if st.session_state.step == 4:
#     st.write("From data:")
#     st.write(st.session_state.form_data)
#     if st.button("Restart", key="restart"):
#         st.session_state.step = 1
#         st.session_state.form_data = {}
        


if "question" not in st.session_state:
    st.session_state.question=""

question=st.text_input("please inter you question")

if st.button("Ask"):
    if question:
        response=requests.get(
            f"{BACKEND_URL}/ask_question",
            params={"question":question}
        )

        if response.status_code==200:
            st.write("API Response:",response.json())
            result=response.json()
            text_to_speak=result
            print(text_to_speak)
            tts=gTTS(text=text_to_speak,lang='en')
            tts.save("response.mp3")
            audio_file=open("response.mp3","rb")
            audio_bytes=audio_file.read()
            st.audio(audio_bytes,format="audio/mp3")
            audio_file.close()
            os.remove("response.mp3")
        else:
            st.write("Error:",response.status_code)


# if st.button("Delete"):
#     response=requests.get(
#         "http://localhost:8000/delete_collection"
#     )
#     if response.status_code==200:
#         st.write("deleted successfully")
#     else:
#         st.write("The db is not present")

if st.button("add_data"):
    response=requests.get(
        f"{BACKEND_URL}/Scraping_data"
    )
    if response.status_code==200:
        st.write("file added successfully")
    else:
        st.write("Error in adding data") 




