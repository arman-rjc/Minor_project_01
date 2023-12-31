import math
from math import sqrt
import forallpeople
import handcalcs.render
forallpeople.environment('structural',top_level=True)

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




st.title('**:blue[Stiffener plate check ]**')
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
# st.divider()  # 👈 Draws a horizontal rule

st.write(f'Project Name: {project_name}')
st.write(f'Job No: {job_no}')
st.write(f'Designer: {designer}')
st.write(f'Date: {date}')
# st.divider()  # 👈 Draws a horizontal rule




@handcalc()
def stiffener_plate_buckling_resistance(b,d):

    Fy= 345
    n = 1.34
    Phi = 0.9
    E = 200000
    k = 0.8 # considering 
    pi = math.pi
    A = B*H
    L = d
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