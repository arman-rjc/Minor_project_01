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
left_column2, middle_column2,right_column2 = st.columns(3)

with right_column2:
    # Add a banner image at the top
    st.image('owsj_updated.JPG',width = 800)
    

# with middle_column2:
#     # Add a banner image at the top
#     st.image('joist.png',width = 600)


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

# Include the Canam joist table values

df = pd.read_excel('owsj.xlsm','Only_economical_sections')
df_modified = df.set_index(['Span','Joist Depth','Data'])
IDX = pd.IndexSlice

Joist_span = round(Span)
P_f = factored_joist_line_load

df_forwork = df_modified.loc[IDX[Joist_span,:,['Weight','Load']],:]  # get all the weight in one rows 


Factored_load_1 = [4.5,6,7.5,9,10.5,12,13.5,15,16.5,18,19.5,21,22.5]
Factored_load_2 = [4.5,5.4,6.3,7.2,8.1,9,9.9,10.8,11.7,12.6,13.5,14.4,15.3]

if Joist_span <= 15:
    df_forwork.columns = Factored_load_1
else:
    df_forwork.columns = Factored_load_2


st.write(f'#### **:black_medium_small_square: Data Table for the selected Joist span**')
st.write(f'##### **This table only showing the information for most economical joist depth**')

df_forwork

first_column_index_gt_5 = df_forwork.columns[df_forwork.columns > P_f].min()
selected_column = df_forwork[first_column_index_gt_5]


# drop all the rows with "NaN" value
selected_column.dropna(inplace=True)
df = pd.DataFrame(selected_column)  


# Mass per unit length for the joist
weight = df.loc[:,:,'Weight'].values[0]
weight = float(weight)
# weight

# Percentager of live load to produce L/360 deflection
Load = df.loc[:,:,'Load'].values[0]
Load = float(Load)
# Load


economical_joist_depth = float(df.index[0][1])
P_r_table = float(df.columns[0])

st.write(f'#### **:black_medium_small_square: Output**')

J_d1 = st.write(f'##### Selected joist depth: {economical_joist_depth} mm')
P_r1 = st.write(f'##### Estimated linear weight, W_r (kg/m): {P_r_table} kg/m')
LL_per1 = st.write(f'##### Live load to produce L/360 deflection: {Load} kN/m')


# J_d = st.number_input('Selected joist depth, d (mm)')
# P_r = st.number_input('Factored OWSJ resistance, P_r (kN/m)')
# S_r = st.number_input('Service load resistance, S_r (kN/m)')
# LL_per = st.number_input('Percentager of live load to produce L/360 deflection, (%)')

allowable_service_live = Load


# @handcalc()
# def allowable_service_live(LL_per1):

#     allowable_service_live =  LL_per1  # kN/m

#     return allowable_service_live

# allowable_service_live_latex,allowable_service_live = allowable_service_live(LL_per1)

# st.latex(allowable_service_live_latex)




if Servicability_live>allowable_service_live:
    st.write(f'#### **:red[Service live load {round(Servicability_live,1)} kN/m is greater than allowable {round(allowable_service_live,1)} kN/m (NOT OK) - Check Joist Depth]**')
else:
    st.write(f'#### **:blue[Service live load {round(Servicability_live,1)} kN/m is less than allowable {round(allowable_service_live,1)} kN/m (OK) - Use Joist Depth of {economical_joist_depth} mm]**')


# with st.expander(":black_medium_small_square: Canam Joist Selection Table for Reference"):
#     df = pd.read_excel('owsj.xlsm','Only_economical_sections')
#     df_modified = df.set_index(['Span','Joist Depth','Data'])
#     df_modified


# Second part of this app
# Step 1: show the table with data for all other available depth
# Step 2; take joist depth input
# Step 3: Show all the calculation

st.write(f'#### **__________________________________________________________________________________________________________**')
st.write(f'#### **:black_medium_small_square: Data Table for all other Joist span**')
st.write(f'##### **:black_medium_small_square: Select any other joist depth below to check the capacity**')

J_d = st.number_input('Select the joist depth you want to check, d (mm)', value = economical_joist_depth )


df = pd.read_excel('owsj.xlsm','data')
df_modified = df.set_index(['Span','Joist Depth','Data'])
# df_modified

Joist_span = round(Span)
P_f = factored_joist_line_load

df_forwork = df_modified.loc[IDX[Joist_span,:,['Weight','Load']],:]  # get all the weight in one rows 


Factored_load_1 = [4.5,6,7.5,9,10.5,12,13.5,15,16.5,18,19.5,21,22.5]
Factored_load_2 = [4.5,5.4,6.3,7.2,8.1,9,9.9,10.8,11.7,12.6,13.5,14.4,15.3]

if Joist_span <= 15:
    df_forwork.columns = Factored_load_1
else:
    df_forwork.columns = Factored_load_2

df_forwork


first_column_index_gt_5 = df_forwork.columns[df_forwork.columns > P_f].min()
selected_column = df_forwork[first_column_index_gt_5]
# selected_column

# df_forwork = selected_column.loc[IDX[Joist_span,:,['Weight','Load']],:]  # get all the weight in one rows 

Joist_mass = selected_column.loc[Joist_span,J_d,'Weight']  # get all the weight in one rows 
Joist_service_load = selected_column.loc[Joist_span,J_d,'Load']  # get all the weight in one rows 

st.write(f'#### **:black_medium_small_square: Output**')

J_d2 = st.write(f'##### Selected joist depth: {J_d} mm')
P_r2 = st.write(f'##### Estimated linear weight, W_r (kg/m): {Joist_mass} kg/m')
LL_per2 = st.write(f'##### Live load to produce L/360 deflection: {Joist_service_load} kN/m')



if Servicability_live>Joist_service_load:
    st.write(f'#### **:red[Service live load {round(Servicability_live,1)} kN/m is greater than allowable {round(Joist_service_load,1)} kN/m (NOT OK) - Check Joist Depth]**')
else:
    st.write(f'#### **:blue[Service live load {round(Servicability_live,1)} kN/m is less than allowable {round(Joist_service_load,1)} kN/m (OK) - Use Joist Depth of {J_d} mm]**')

# df_forwork
# selected_column.loc[IDX['Span',],:]

# # drop all the rows with "NaN" value
# selected_column.dropna(inplace=True)
# df = pd.DataFrame(selected_column)  


# # Mass per unit length for the joist
# weight = df.loc[:,:,'Weight'].values[0]
# weight = float(weight)
# # weight

# # Percentager of live load to produce L/360 deflection
# Load = df.loc[:,:,'Load'].values[0]
# Load = float(Load)
# # Load


# economical_joist_depth = float(df.index[0][1])
# P_r_table = float(df.columns[0])



with st.expander("Old catalogue for reference"):
    st.image('OWSJ_check.JPG',width = 800)
