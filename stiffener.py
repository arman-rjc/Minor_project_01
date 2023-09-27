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




st.title('**:blue[Stiffener Plate Resistance]**')
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

st.write(f'Project Name: {project_name}')
st.write(f'Job No: {job_no}')
st.write(f'Designer: {designer}')
st.write(f'Date: {date}')
# st.divider()  # 👈 Draws a horizontal rule

st.sidebar.write('## Input parameters')

B = st.sidebar.number_input('Steel Plate thickness/web thickness, b (mm)',value = 10.00,step=0.01,format="%.2f")
H = st.sidebar.number_input('Height of steel plate, d (mm)',value = 250.00,step=0.01,format="%.2f")

B = float(B)
H = float(H)

st.write("### **Input paramerts:**")

# Create two columns using st.beta_columns()
left_column,middle_column, right_column = st.columns(3)



@handcalc(precision=3)
def stiffener_plate_buckling_resistance(B: float, H: float):

    Fy= 345             # MPa
    n = 1.34            # For hot rolled steel 
    Phi = 0.9           # Force reduction factor 
    E = 200000          # Modulus of elasticity 
    k = 0.8             # considering plate attached to the top and bottom flange of a beam/column
    pi = math.pi
    A = B*H
    L = H
    I_x = (B*H**3)/12
    r_x = sqrt(I_x/A)
    Fex = (pi**2*E)/((k*L)/r_x)**2
    
    I_y = (H*B**3)/12
    r_y = sqrt(I_y/A)
    Fey = (pi**2*E)/((k*L)/r_y)**2
    
    Fe = min(Fex,Fey) # MPa
    
    lamda = sqrt(Fy/Fe)
    Cr = (Phi*A*Fy)/(1+lamda**(2*n))**(1/n)
    Cr_kN = Cr/1000 # kN
    
    return Cr_kN


Cr_kN_latex, Cr_kN = stiffener_plate_buckling_resistance(B,H)

with left_column:
    st.latex(Cr_kN_latex)
    st.write(f'#### Compressive strength of the plate is {round(Cr_kN)} kN')

    