import forallpeople
forallpeople.environment('structural', top_level=True)
import math
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc

#________________________________________________________________________________________________________
# How to run this app:
# open anaconda prompt
# Open task manager and right click twice to get the properties tab
# Change start in ""H:\_Personal\07 Spreadsheet Development\07-Projects\Streamlit_app" with the file location
# Go to streamlit and write "stremlit run app.py" replace app.py with the python files name
#________________________________________________________________________________________________________

st.set_page_config(layout='wide')
st.title('**:blue[Concrete Flexural Reinforcement Calculator]**')
st.divider()  # 👈 Draws a horizontal rule

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

unit = ['Metric', 'Imperial']
unit_selected = st.sidebar.selectbox('Select unit:', unit)


if unit_selected == "Metric":
    M_f = st.sidebar.number_input('Factored moment, M_f (kN-m/m)',value = 70)
    h_c = st.sidebar.number_input('Concrete section height, h_c (mm)',value = 250)
    b = st.sidebar.number_input('Concrete section width, b (mm)',value = 1200)
    cover = st.sidebar.number_input('Concrete cover (mm)',value = 38)
    db = st.sidebar.number_input('Bar diameter, db (mm)',value = 0.65)
    phi_c = st.sidebar.number_input('phi_c',value = 0.65)
    f_c = st.sidebar.number_input('Concrete compressive strength, f_c (MPa)', value = 30)
    f_y = st.sidebar.number_input('Steel yield strength, f_y (MPa)',value = 400)


    M_f = M_f*10**6  # N-mm/m
    d = min(0.9*(h_c), h_c-cover-db/2) # mm


    # Create two columns using st.beta_columns()
    left_column, right_column = st.columns(2)

    # Add text to the left column
    with left_column:
        st.write("### **Input paramerts:**")
        st.write(f'	:black_medium_small_square:  Factored moment = **{M_f}** N-mm/m')
        st.write(f':black_medium_small_square: Concrete section height, h_c = **{h_c}** mm')
        st.write(f':black_medium_small_square: Concrete section width,b= **{b}** mm')
        st.write(f':black_medium_small_square: Clear cover = **{cover}** mm')
        st.write(f':black_medium_small_square: Bar diameter,db = **{db}** mm')
        st.write(f':black_medium_small_square: phi_c = **{phi_c}**')
        st.write(f':black_medium_small_square: Concrete compressive strength, f_c = **{f_c}** MPa')
        st.write(f':black_medium_small_square: Steel yield strength, f_y = **{f_y}** MPa')
        st.write(f':black_medium_small_square: Effective depth, d = **{d}** mm')
    # Add an image to the right column
    # Add an image to the right column with a specified width and height
    with right_column:
        image_filename = 'd.png'  # Replace with the actual image file
        st.image(image_filename, caption='Fig 1: Section parameters', width=400)
else:

    M_f = st.sidebar.number_input('M_f (kip-ft/ft)',value = 20)
    h_c = st.sidebar.number_input('h_c (in)',value = 30)
    b = st.sidebar.number_input('b (in)',value = 20)
    cover = st.sidebar.number_input('cover (in)',value = 1.5)
    db = st.sidebar.number_input('db (in)',value = 0.31)
    phi_c = st.sidebar.number_input('phi_c',value = 0.65)
    f_c = st.sidebar.number_input('f_c (MPa)', value = 30)
    f_y = st.sidebar.number_input('f_y (MPa)',value = 400)


    M_f = M_f*4448221.6 # N-mm/m
    d = min(0.9*(h_c), h_c-cover-db/2)*25.4 # mm

    st.write(f'Factored moment = {M_f} kN-m/m')
    st.write(f'h_c = {h_c*25.4} mm')
    st.write(f'b= {b*25.4} mm')
    st.write(f'Clear cover = {cover*25.4} mm')
    st.write(f'db = {db*25.4} mm')
    st.write(f'phi_c = {phi_c} ')
    st.write(f'f_c = {f_c} MPa')
    st.write(f'f_y = {f_y} MPa')
    

    # Convert all the inch to mm 
    h_c = h_c*25.4
    b = b*25.4
    cover = cover*25.4
    db = db*25.4
    phi_c = phi_c
    f_c = f_c
    f_y = f_y


st.write(f':one: :blue[Required Area Calculation]')

@handcalc()
def as_calc(f_c,b,d,M_f):
    As_req = 0.0015*f_c*b*(d - sqrt(d**2 - (3.85*M_f)/(f_c * b)))
    return As_req

if unit_selected == "Metric":

    As_latex, As_req = as_calc(f_c,b,d,M_f)
    st.latex(As_latex)
else:

    As_latex, As_req = as_calc(f_c,b,d,M_f)
    st.latex(As_latex)


st.write(f'Required steel area = {round(As_req,1)} mm2/m')




# Use the quick calc and compared error percentage 
st.write(f':two: :blue[Required Area Calculation (Approximation)]')
@handcalc()
def rough_check(M_f,d):
    As_new  = M_f/(300*d)
    return As_new

As_check_latex,As_new = rough_check(M_f,d)

st.latex(As_check_latex)
st.write(f'Required steel area (Using rough calc) = {round(As_new,1)} mm2/m')
st.write(f'Error percentage  = {round(((As_new-As_req)/As_new)*100,1)} %')




# List of bar area and bar diameter 
Area_list = [100,200,300,500,700,1000,1500,2500]
bar_dia_list = [10, 15, 20, 25, 30, 35, 45, 55]

Area_list_imp = [0.11,0.20,0.31,0.44,0.60,0.79,1.0,1.27]
bar_dia_list_imp = [3, 4, 5, 6,7,8,9,10]

st.divider()  # 👈 Draws a horizontal rule
st.write('#### Reinforcing Options:')

for i in range(len(bar_dia_list)-1):

    if unit_selected == "Metric":
        no_of_bar = math.ceil(As_req/(Area_list[i]))
        if no_of_bar<=1:
            no_of_bar = 1
            spacing = b/(no_of_bar)
        else:
            spacing = b/(no_of_bar-1) # per m 
    else:
        no_of_bar = math.ceil((As_req/3.28)/(Area_list[i]))
        if no_of_bar<=1:
            no_of_bar = 1
            spacing = b/(no_of_bar)
        else:
            spacing = b/(no_of_bar-1) # per m 

        # per m 
    st.write(f'({i+1}) Provide **{round(no_of_bar,0)}** - {bar_dia_list[i]}M  bar at **{round(spacing,0)}** mm or **{round(spacing/25.4,0)}** inch o.c')

st.divider()  # 👈 Draws a horizontal rule


image_filename_2 = 'bar_diameter_table.png'  # Replace with the actual image file
st.image(image_filename_2, caption='Fig 2: Bar diameter and area', width=600)

s