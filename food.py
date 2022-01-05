    
#Importing Libraries:
import streamlit as st 
import pickle
from PIL import Image

import time
import pandas as pd
import re
import random
#-------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title="ABC Private Limited",page_icon="random",layout="wide",
                       menu_items={'Get Help': 'https://www.linkedin.com/in/vinoth24/',
                                   'Report a bug': "https://www.linkedin.com/in/vinoth24/",
                                   'About': "# This is a Food suggestion Algorithm with a simple interface. Very Easy to use!"})

@st.cache(allow_output_mutation=True) #For Autoupdate in app.

def loading_model():
    loaded_model = pickle.load(open('model.sav', 'rb'))
    return loaded_model
with st.spinner('Model is being loaded..'):
    model=loading_model()     #Model is loaded.
    
cmn = [' sugar', ' ginger', ' garam masala', ' ghee', ' curry leaves',     # all ingredients taken
       ' jaggery', ' urad dal', 'Rice flour', ' milk', ' tomato',
       ' garam masala powder', ' mustard oil', 'Chana dal',
       ' sesame seeds', ' saffron', ' turmeric', ' coconut',
       'Whole wheat flour', ' clarified butter', ' cardamom',
       ' gram flour', ' mustard seeds', ' lemon juice', ' garlic',
       ' potato', 'Urad dal', ' baking soda', 'Rice', ' salt',
       'Wheat flour']
    

# Reading File:
concat = pd.read_csv("concat.csv")

#-------------------------------------------------------------------------------------------------------------------------------
st.write("""
         # FOOD SUGGESTION ALGORITHM
         """)

# Model Prediction func:
def predict_food(final_input):
    pred=model.predict([final_input])
    pred = int(re.sub(r'[^\w\s]', '', str(pred)))
    prediction=(concat.loc[concat["clust"] == pred])["name"].values
    prediction=",".join(random.sample(list(prediction), k=5))

    return prediction
#-------------------------------------------------------------------------------------------------------------------------------
def processing_inputs(f,d,c,t,r,i):
# Values for ingredients
    ingredient_list = i
    ans = []
    for i in cmn:
        if i in ingredient_list:

            x=i
            i = 1
            ans.append(str(x) +"="+ str(i))
        else:
            x=i
            i = 0
            ans.append(str(x) +"="+ str(i))
    ingred_list=[]
    for i in ans:
        last = int(i[-1])
        ingred_list.append(last)
    final_input = ingred_list
    
    #flavor
    if f == "sweet":
        f = 4
    elif f == "spicy":
        f = 3
    elif f == "sour":
        f = 2
    elif f == "bitter":
        f = 1
    elif f == "neutral":
        f = 0
    final_input.append(f)
    
    #diet
    if d == "Yes":
        d = "0"
    elif d == "No":
        d = "1"
    final_input.append(d) 
    
    #course
    if c == "desert":
        c = 0
    elif c == "main course":
        c = 1
    elif c == "starter" :
        c = 3
    elif c == "snack":
        c = 2
    final_input.append(c)
    
    #Prep time
    if t == "very fast (<10 mins)":
        t = 0
    elif t == "medium fast (10-30 mins)":
        t = 1
    elif t == "slow (>30 mins)":
        t = 2
    final_input.append(t)   
    
    # region    
    if r == "East":
        r = 1
    if r == "West":
        r = 6
    if r == "North":
        r = 3
    if r == "South":
        r = 5
    if r == "North East":
        r = 4
    if r == "Neutral":
        r = 2
    final_input.append(r)
    return final_input
#-------------------------------------------------------------------------------------------------------------------------------

#Input func:
def input_data():
    flavor = st.sidebar.selectbox("Flavor choice",["sweet", "sour", "bitter", "spicy", "neutral"],help="Choose one falvor")
    diet = st.sidebar.selectbox("Are you Non-Veg",["Yes", "No"])
    course = st.sidebar.selectbox("Type of course",["main course","snack","starter", "desert"], help="Choose one type")
    time = st.sidebar.selectbox("Ho much time you can wait", ["very fast (<10 mins)","medium fast (10-30 mins)","slow (>30 mins)"], help="Time taken can vary a little")
    region=st.sidebar.selectbox("Which region style you prefer",["North","East", "West", "South", "North East"], help="choose wisely")
    ingredients=st.sidebar.multiselect('Some ingredients you would like in your food: ',cmn, default=None, help=" you can choose multiple ingredients ")
    return(flavor,diet,course,time,region,ingredients)

#--------------------------------------------------------------------------------------------------------------------------------

# Decor Func:    
def decor():
    html_temp = """
    <div style="background-color:Chocolate;padding:15px">
    <h1 style="color:white;text-align:center;">Food Suggestion Algorithm Interface </h1>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    image = Image.open('Indian-Food.jpg')
    st.image(image, caption='')    

#--------------------------------------------------------------------------------------------------------------------------------

def main():
    
    decor()
    name=st.sidebar.text_input("Enter customer's name :")
    if name:
        st.write("# Customers Name : %s"%name)
    col3,col4=st.columns(2)
# taking Inputs:
    with col3:
        check=st.checkbox("Are you ready to order",value=False)
        if check:
            f,d,c,t,r,i=input_data()
        
            final_input = processing_inputs(f,d,c,t,r,i)     
            #st.write(final_input)                                         
# Result:       
            if st.sidebar.button("See Suggested foods"):
                result=predict_food(final_input)
            

                st.success("### Your Suggested foods: {}".format(result))
        else:
            st.write("Check the box if youre hungry")
    st.markdown("---")

#---------------------------------------------------------------------------------------------------------------------------

# Team Details:
    with col4:
        expander=st.expander("My Details",expanded=False)
        with expander:
            st.info("Kasi Vinoth S")
            st.info("Data Science Enthusiast")
            st.info("I learn by doing projects on ML and AI")
            st.info("Hobbies: Chess")
    

#-----------------------------------------------------------------------------------------------------

# Program Starts:
if __name__=='__main__':
    main()
