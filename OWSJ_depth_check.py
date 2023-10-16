import forallpeople
forallpeople.environment('structural', top_level=True)
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from math import pi,sqrt
import PyNite
from PyNite import FEModel3D


#________________________________________________________________________________________________________
# How to run this app:
# open anaconda prompt
# Open task manager and right click twice to get the properties tab
# Change start in ""H:\_Personal\07 Spreadsheet Development\07-Projects\Streamlit_app" with the file location
# Go to streamlit and write "stremlit run app.py" replace app.py with the python files name
#________________________________________________________________________________________________________




# Setting page layout 
st.set_page_config(layout='wide')

st.write(f'## **:blue[ OWSJ depth checking]**')
st.write(f'##### **As per the steps mentioned in "Structural Steel for Canadian Buildings" book page -127**')

# Custom CSS for changing the font size, making it bold, and using Times New Roman font
custom_css = """
<style>
    /* Apply to all text in the app */
    body {
        font-family: "Times New Roman", Times, serif;
        font-size: 16px; /* Adjust the font size as needed */
        font-weight: bold;
    }
</style>
"""

# Display the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)


with st.expander("See disclaimer"):
    # Define the disclaimer text
    disclaimer_text = """
    **Disclaimer of Warranty and Liability**

    By using this app, you acknowledge and agree that the results it provides are for informational purposes only. The engineer using this tool is solely responsible for verifying and validating the accuracy of the results obtained. This app is provided "as is," without any warranty or guarantee of any kind, express or implied. In no event shall the developers or contributors be liable for any damages or consequences arising from the use of this app. You are encouraged to exercise due diligence and professional judgment when relying on the output of this tool.
    """

    # Display the disclaimer text if the checkbox is checked
    st.markdown(disclaimer_text)

# Add a checkbox for users to acknowledge the disclaimer
disclaimer_accepted = st.checkbox("I have read and agree to the Disclaimer of Warranty and Liability")

with st.expander(":black_medium_small_square: Project Information"):
    #  Create a Streamlit app
    # st.sidebar.write("Project Information")

    # Add text input boxes for Project Name, Job No, Designer, and Date
    project_name = st.text_input("Project Name:")
    job_no = st.text_input("Job No:")
    designer = st.text_input("Designer:")
    date = st.text_input("Date:")


# Create two columns using st.beta_columns()
left_column2, right_column2 = st.columns(2)

with right_column2:
    # Add a banner image at the top
    st.image('OWSJ_check.JPG',width = 800)


#
# #  Create a Streamlit app
# st.sidebar.write("Project Information")

# # Add text input boxes for Project Name, Job No, Designer, and Date
# project_name = st.sidebar.text_input("Project Name:")
# job_no = st.sidebar.text_input("Job No:")
# designer = st.sidebar.text_input("Designer:")
# date = st.sidebar.text_input("Date:")




# Display the input values


# st.write(f'Project Name: {project_name}')
# st.write(f'Job No: {job_no}')
# st.write(f'Designer: {designer}')
# st.write(f'Date: {date}')


# st.sidebar.write('## Input parameters')

# Span = st.sidebar.number_input('Beam span length, L (m)',value = 8)
# DL = st.sidebar.number_input('Area dead load, DL (kPa)',value = 1.2)
# LL = st.sidebar.number_input('Area live/snow load, LL/SL (kPa)',value = 1.4)
# WL = st.sidebar.number_input('Area wind uplift load, WL (kPa)',value = 0.38)

# TW = st.sidebar.number_input('Joist tributary width, TW (m)',value = 2.0)


with left_column2:
    st.write('## Input parameters')

    Span = st.number_input('Beam span length, L (m)',value = 8)
    DL = st.number_input('Area dead load, DL (kPa)',value = 1.2)
    LL = st.number_input('Area live/snow load, LL/SL (kPa)',value = 1.4)
    WL = st.number_input('Area wind uplift load, WL (kPa)',value = 0.38)

    TW = st.number_input('Joist tributary width, TW (m)',value = 2.0)

st.write(f'#### **:black_medium_small_square: Factored Area Load (kPa)**')

@handcalc()
def factored_area_load(DL,LL,WL):

    factored_area_load = 1.25*DL+1.5*LL+0.4*WL  # kPa

    return factored_area_load


factored_area_load_latex,factored_area_load = factored_area_load(DL,LL,WL)

st.latex(factored_area_load_latex)

st.write(f'#### **:black_medium_small_square: Factored Joist Line Load (kN/m)**')


@handcalc()
def factored_joist_line_load(factored_area_load,TW):

    factored_joist_line_load = factored_area_load*TW  # kN/m

    return factored_joist_line_load

factored_joist_line_load_latex,factored_joist_line_load = factored_joist_line_load(factored_area_load,TW)

st.latex(factored_joist_line_load_latex)


st.write(f'#### **:black_medium_small_square: Unfactored Line Load on the Joist (kN/m)**')


@handcalc()
def unfactored_joist_line_load(LL,TW):

    unfactored_joist_line_load = LL*TW  # kN/m


    return unfactored_joist_line_load

unfactored_joist_line_load_latex,unfactored_joist_line_load = unfactored_joist_line_load(LL,TW)

st.latex(unfactored_joist_line_load_latex)



@handcalc()
def Servicability_live(unfactored_joist_line_load):

    Servicability_live = 0.9*unfactored_joist_line_load  # kN/m

    return Servicability_live

    
Servicability_live_latex,Servicability_live = Servicability_live(unfactored_joist_line_load)

st.latex(Servicability_live_latex)

J_d = st.number_input('Selected joist depth, d (mm)')
P_r = st.number_input('Factored OWSJ resistance, P_r (kN/m)')
S_r = st.number_input('Service load resistance, S_r (kN/m)')
LL_per = st.number_input('Percentager of live load to produce L/360 deflection, (%)')

@handcalc()
def allowable_service_live(S_r,LL_per):

    allowable_service_live =  (LL_per/100)*S_r  # kN/m

    return allowable_service_live

allowable_service_live_latex,allowable_service_live = allowable_service_live(S_r,LL_per)

st.latex(allowable_service_live_latex)




if Servicability_live>allowable_service_live:
    st.write(f'#### **:red[Service live load {Servicability_live} kN/m is greater than allowable {allowable_service_live} kN/m (NOT OK) - Check Joist Depth]**')
else:
    st.write(f'#### **:blue[Service live load {Servicability_live} kN/m is less than allowable {allowable_service_live} kN/m (OK) - Use Joist Depth of {J_d} mm]**')
