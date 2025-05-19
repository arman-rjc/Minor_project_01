import forallpeople
forallpeople.environment('structural', top_level=True)
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from streamlit.components.v1 import html

#________________________________________________________________________________________________________
# How to run this app:
# open anaconda prompt
# Open task manager and right click twice to get the properties tab
# Change start in ""H:\_Personal\07 Spreadsheet Development\07-Projects\Streamlit_app" with the file location
# Go to streamlit and write "stremlit run app.py" replace app.py with the python files name
#________________________________________________________________________________________________________

def CISC_database_reader(filename:str,I_check = 1):
    '''
    Collects all the available W sections in Canada, stores them in a list and 
    Returns the list of W sections from CISC databse.
    '''
    df = pd.read_excel(filename,skipfooter =2)
    mask2 = df.loc[:,"Avl"]== 'a'                               # This function will only store all the W sections that are readily available in Canada and commonly used
    df_sort = df.loc[mask2,["Ds_i","Ds_m","D","B","T","W","BT","HW",
                        "A_Th","Ix","Sx","Zx","Iy",
                       "Sy","Zy","J","Cw","Mass"]]
    # mask3 = df.loc[:,"Ix"]>=I_check
    # df_sort = df.loc[mask3,["Ds_i","Ds_m","D","B","T","W","BT","HW",
    #                     "A_Th","Ix","Sx","Zx","Iy",
    #                    "Sy","Zy","J","Cw","Mass"]]
    # df_sort = df_sort.sort_values("Mass")
    df_sort
    
    return df_sort

def Most_economical_section(filename):
    '''
    Collects all the available W sections in Canada, stores them in a list and 
    Returns the list of W sections from CISC databse based on Ix value from low to high.
    '''
    get_section_list = CISC_database_reader(filename)
    Economical_section_list = get_section_list.sort_values("Mass")
    return Economical_section_list


def List_of_selected_depth(filename,selected_depth = "W",Criteria = "Ix"):
    '''
    List all W sections based on specific depth selected and also the sorting of data canbe controlled by using criteria. 
    If no criteria is selected, it will sort the values based on Ix
    '''
    df_eco = CISC_database_reader(filename)
    section_list = df_eco[df_eco['Ds_i'].str.startswith(selected_depth)]
    section_list = section_list.sort_values(Criteria)
    return section_list


# Setting page layout 
st.set_page_config(layout='wide')

# Add a banner image at the top
st.image('gerber_beam.JPG',width = 400)



# Add a banner image at the top
# st.image('steel_beam.png', use_container_width=True)

st.write(f'### **:black_medium_small_square: Steel Section Geometry:**')


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

#
#  Create a Streamlit app
st.sidebar.write("Project Information")

# Add text input boxes for Project Name, Job No, Designer, and Date
project_name = st.sidebar.text_input("Project Name:")
job_no = st.sidebar.text_input("Job No:")
designer = st.sidebar.text_input("Designer:")
date = st.sidebar.text_input("Date:")

# Display the input values
st.divider()  # 👈 Draws a horizontal rule

st.write(f'Project Name: {project_name}')
st.write(f'Job No: {job_no}')
st.write(f'Designer: {designer}')
st.write(f'Date: {date}')
st.divider()  # 👈 Draws a horizontal rule


st.sidebar.write('## Input parameters')
units = ['Metric','Imperial']
selected_units = st.sidebar.selectbox('Beam section unit:', units)

# Get the column name for which you want to display unique items
column_name = 'Ds_i'  # Replace 'YourColumnName' with the actual column name
column_name_m = 'Ds_m'  # Replace 'YourColumnName' with the actual column name
filename = "W_CISC.xlsm"

selected_depth = "W8"
Criteria = "Mass"


df = CISC_database_reader(filename)

if selected_units == 'Metric':
    # Get unique items from the specified column
    unique_items = df[column_name_m].unique()
else:
    # Get unique items from the specified column
    unique_items = df[column_name].unique()    

# Create a selectbox widget in the Streamlit sidebar
selected_item = st.sidebar.selectbox("Select beam section", unique_items)


if selected_units == 'Metric':
    mask = df.loc[:,"Ds_m"] == selected_item
else:
    mask = df.loc[:,"Ds_i"] == selected_item 

st.write(f'### **:black_medium_small_square: Selected Section Geometry:**')
df_section = df.loc[mask,["Ds_i","Ds_m","D","B","T","W","BT","HW",
                        "A_Th","Ix","Sx","Zx","Iy",
                       "Sy","Zy","J","Cw"]]
df_section



# Create two columns using st.beta_columns()
left_column, right_column = st.columns(2)

# Add text to the left column
with left_column:
    D = df_section.loc[:,'D'].unique()
    B = df_section.loc[:,'B'].unique()
    T = df_section.loc[:,'T'].unique()
    W = df_section.loc[:,'W'].unique()

    # st.write(f'### **:black_medium_small_square: List of parameters:**')
    # st.write(f':black_medium_small_square: Depth of beam, d  = **{D[0]}** mm [**{round(D[0]/25.4,1)}** in]')
    # st.write(f':black_medium_small_square: Width of beam, b  = **{B[0]}** mm [**{round(B[0]/25.4,1)}** in]')
    # st.write(f':black_medium_small_square: Flange thickness, t  = **{T[0]}** mm [**{round(T[0]/25.4,1)}** in]')
    # st.write(f':black_medium_small_square: Web thickness, w  = **{W[0]}** mm [**{round(W[0]/25.4,1)}** in]')

    # Sample data
    data = {
        'Parameters': ['Depth of beam, d = ', 'Width of beam, b = ', 'Flange thickness, t = ', 'Web thickness, w = '],
        'mm':  [D[0], B[0], T[0], W[0]],
        'in': [round(D[0]/25.4,1), round(B[0]/25.4,1), round(T[0]/25.4,1), round(W[0]/25.4,1)]
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create a Streamlit app
    st.write(f'### **:black_medium_small_square: Data Table for {selected_item}**')


    # Display the table
    st.table(df)


    # Add an image to the right column with a specified width and height
with right_column:
    image_filename = 'Generic_section.png'  # Replace with the actual image file
    st.image(image_filename, caption='Fig 1: Section parameters', width=400)



# Just checking if still having issue with github push

# Add Buy Me a Coffee button
floating_button = """
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 100;">
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
data-name="bmc-button" 
data-slug="armans01" 
data-color="#FFDD00" 
data-emoji=""  
data-font="Cookie" 
data-text="Buy me a coffee" 
data-outline-color="#000000" 
data-font-color="#000000" 
data-coffee-color="#ffffff" >
</script>
</div>
"""
html(floating_button, height=80)
