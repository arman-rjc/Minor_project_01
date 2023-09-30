import forallpeople
forallpeople.environment('structural', top_level=True)
import math
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc

st.set_page_config(layout='wide')

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




st.title('**:blue[Steel Plate Web Crippling ]**')
# st.divider()  # 👈 Draws a horizontal rule


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
# st.divider()  # 👈 Draws a horizontal rule

st.write(f'Project Name: {project_name}')
st.write(f'Job No: {job_no}')
st.write(f'Designer: {designer}')
st.write(f'Date: {date}')
# st.divider()  # 👈 Draws a horizontal rule


st.sidebar.write('## Input parameters')

w = st.sidebar.number_input('Steel Plate thickness/web thickness, w (mm)',value = 10)
N = st.sidebar.number_input('Support element width, N (mm)',value = 250)
t = st.sidebar.number_input('Flange thickness, t (mm)',value = 10)
tcp = st.sidebar.number_input('Column cap plate thickness (if any), tcp',value = 25)
Fy = st.sidebar.number_input('Steel yield strength, f_y (MPa)',value = 345)

P = st.sidebar.number_input('Axial applied force, P (kN)',value = 100)




st.write('## :blue[Input parameters]')
st.write('##### [Calculations are based on CSA S16 Clause 14.3.2]')

# Create two columns using st.beta_columns()
left_column,middle_column, right_column = st.columns(3)


@handcalc(precision = 1)
def web_cripling_resistance(w,N,t,Fy=345, tcp = 0):
    E = 200000 # Modulus of elasticity, MPa
    Fy = 345  # Steel yield strength, MPa
    Phi_bi = 0.8
    B_r1 = Phi_bi*w*(N+10*t)*Fy  # Bearing resistance, N
    B_r2 = 1.45*Phi_bi*w**2*sqrt(Fy*E)  # Bearing resistance, N
    B_rg = min(B_r1,B_r2)/1000   # Maximum bearing resistance, kN
    return B_rg


Brg_latex, B_rg = web_cripling_resistance(w,N,t,Fy=345, tcp = 0)


with left_column:

    st.latex(Brg_latex)



if B_rg>P:
    st.write(f'#### Bearing resistance ({round(B_rg)} kN)  is greater than axial force ({round(P)}kN)')
    st.write('#### [:green[Stiffner not reauired]]')
else:
    st.write(f'#### Bearing resistance ({round(B_rg)} kN) is less than axial force ({round(P)} kN)')   
    st.write('#### [:red[Stiffener required]]')

# Create two columns using st.beta_columns()
left_column,middle_column, right_column = st.columns(3)

with middle_column:
    image_filename = 'Web_crippling.png'  # Replace with the actual image file
    st.image(image_filename, caption='Fig 1: Section parameters', width=800)


with st.expander(f"### Reference Material"):
    st.write('###### [:blue[According to CSA S16 CL11.0]]')
    image_filename = 'section_classes.JPG'  # Replace with the actual image file
    st.image(image_filename, caption='Fig 1: Concept behind section class', width=600)