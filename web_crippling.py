import forallpeople
forallpeople.environment('structural', top_level=True)
import math
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc

st.set_page_config(layout='wide')
st.title('**:blue[Steel Plate web crippling ]**')
# st.divider()  # 👈 Draws a horizontal rule

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

w = st.sidebar.number_input('Steel Plate thickness/web thickness, w (mm)',value = 10)
N = st.sidebar.number_input('Support element width, N (mm)',value = 250)
t = st.sidebar.number_input('Flange thickness, t (mm)',value = 10)
tcp = st.sidebar.number_input('Column cap plate thickness (if any), tcp',value = 25)
Fy = st.sidebar.number_input('Steel yield strength, f_y (MPa)',value = 345)



@handcalc()
def web_cripling_resistance(w,N,t,Fy=345, tcp = 0):
    '''
    this function will retun the web crippling resistance (Brg) of beam or girder or a steel plate
    w = thickness of the plate/ web thickness/ load per unit length 
    N = length of bearing of an applied load 
    '''
    E = 200000 # MPa
    Fy = 345  # MPa
    phi_bi = 0.8
    Br_1 = phi_bi*w*(N+10*t)*Fy
    Br_2 = 1.45*phi_bi*w**2*sqrt(Fy*E)
    Brg = min(Br_1,Br_2)/1000
    return Brg


Brg_latex, Brg = web_cripling_resistance(w,N,t,Fy=345, tcp = 0)
