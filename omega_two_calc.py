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

# Add a banner image at the top
st.image('Beam_loading.png',width = 600)


st.write(f'### **:black_medium_small_square: Coefficient to account for increased moment resistance (w2)**')
st.write(f'##### **This design is per CSA S16 Clause 13.6.1**')

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


st.write(f'Project Name: {project_name}')
st.write(f'Job No: {job_no}')
st.write(f'Designer: {designer}')
st.write(f'Date: {date}')



st.sidebar.write('## Input parameters')
Span = st.sidebar.number_input('Beam span length, L (ft)',value = 168)
L_u = st.sidebar.number_input('Unbraced beam length, L_u (ft)',value = 70)
L_start = st.sidebar.number_input('Starting point of unbraced length, L_start (ft)',value = 30)

uniform_load = ['Yes','No']
uniform_load_selection = st.sidebar.selectbox('Uniform load applied?:', uniform_load)

if uniform_load_selection == 'Yes':
    uniform_D = st.sidebar.number_input('Unfactored_uniform_Dead, DL (lb/ft)',value = 500)
    uniform_L = st.sidebar.number_input('Unfactored_uniform_Live, LL (lb/ft)',value = 500)
    uniform_S = st.sidebar.number_input('Unfactored_uniform_Snow, SL (lb/ft)',value = 500)

    uniform_start = st.sidebar.number_input('Uniform load start point, L_start',value = 0)
    uniform_end = st.sidebar.number_input('Uniform load end point, L_end',value = Span)



no_of_point_load = st.sidebar.number_input('No of point load, n',value = 0)



# Add point load using for loop

point_load_D = []
point_load_D_x = []

point_load_L = []
point_load_L_x = []

point_load_S = []
point_load_S_x = []

if no_of_point_load>0:
    for i in range (no_of_point_load):
        D = st.sidebar.number_input(f'Point load (DEAD) {i+1}: ',value = 70)
        point_load_D.append(D)
        D_x = st.sidebar.number_input(f'Point load (DEAD) {i+1} distance, x{i+1}: ',value = Span/2)
        point_load_D_x.append(D_x)

        L = st.sidebar.number_input(f'Point load (LIVE) {i+1}: ',value = 70)
        point_load_L.append(L)
        L_x = st.sidebar.number_input(f'Point load (LIVE) {i+1} distance, x{i+1}: ',value = Span/2)
        point_load_L_x.append(L_x)

        S = st.sidebar.number_input(f'Point load (SNOW) {i+1}: ',value = 70)
        point_load_S.append(S)
        S_x = st.sidebar.number_input(f'Point load (SNOW)  {i+1} distance, x{i+1}: ',value = Span/2)
        point_load_S_x.append(S_x)





# Use PyNite to calculate the moment and shear for the beam

simple_beam = FEModel3D()


# Add nodes (14 ft = 168 in apart)
simple_beam.add_node('N1', 0, 0, 0)
simple_beam.add_node('N2', Span, 0, 0)

# Define a material
E = 29000       # Modulus of elasticity (ksi)
G = 11200       # Shear modulus of elasticity (ksi)
nu = 0.3        # Poisson's ratio
rho = 2.836e-4  # Density (kci)

simple_beam.add_material('Steel', E, G, nu, rho)

# Add a beam with the following properties:
# Iy = 100 in^4, Iz = 150 in^4, J = 250 in^4, A = 20 in^2
Iy = 100
Iz = 150
J = 250
A = 20
simple_beam.add_member('M1', 'N1', 'N2', 'Steel', Iy, Iz, J, A)

# Provide simple supports
simple_beam.def_support('N1', True, True, True, False, False, False)
simple_beam.def_support('N2', True, True, True, True, False, False)

simple_beam.add_load_combo('LC1',{'D':1.25,'L':1.5},'strength')
# simple_beam.add_load_combo('LC2',{'D':1.25,'S':1.5},'strength')


if uniform_load_selection == 'Yes':
    # Add a uniform load of xxx lbs/ft to the beam
    simple_beam.add_member_dist_load('M1', 'Fy', -uniform_D, -uniform_D, uniform_start, uniform_end,'D')
    simple_beam.add_member_dist_load('M1', 'Fy', -uniform_L, -uniform_L, uniform_start, uniform_end,'L')
    simple_beam.add_member_dist_load('M1', 'Fy', -uniform_S, -uniform_S, uniform_start, uniform_end,'S')


for i in range(no_of_point_load):
    simple_beam.add_member_pt_load('M1', 'Fy', -point_load_D[i], point_load_D_x[i], 'D') # 5 kips Dead load
    simple_beam.add_member_pt_load('M1', 'Fy', -point_load_L[i], point_load_L_x[i], 'L') # 8 kips Live load
    simple_beam.add_member_pt_load('M1', 'Fy', -point_load_S[i], point_load_S_x[i], 'S') # 8 kips Live load



# Analyze the beam
simple_beam.analyze(check_statics=True)


moment_list = []
shear_list = []
coordinate_list = []
for i in range(Span+1):
    moment_value = simple_beam.Members['M1'].moment('Mz',i,'LC1')
    moment_list.append(moment_value)
    shear_value = simple_beam.Members['M1'].shear('Fy',i,'LC1')
    shear_list.append(shear_value)
    coordinate_list.append(i)


df = pd.DataFrame(
    {'Span (in)':coordinate_list,
    'Moment (lb-in)': moment_list,
    'Shear (lb)': shear_list}
    )
# df

# Find the row with the maximum moment
max_moment_row = df[df['Moment (lb-in)'] == df['Moment (lb-in)'].min()]
# max_moment_row
# Extract the 'Span (in)' value from the row
span_for_max_moment = max_moment_row['Span (in)'].values[0]


# Starting point defined at the beginning of the input data
span_for_max_moment = L_start


L_u0 = span_for_max_moment
L_u1 = span_for_max_moment + L_u

# # Filter the DataFrame for 'Span (in)' values of 4 and 160
# filtered_df = df[df['Span (in)'].isin([L_u0, L_u1])]

# Assuming you have the filtered DataFrame
filtered_df = df[df['Span (in)'].between(L_u0, L_u1)]

# Get the moments within unbraced length 
L_Ma = round(L_u0+((1/4)*L_u))
L_Mb = round(L_u0+((1/2)*L_u))
L_Mc = round(L_u0+((3/4)*L_u))
moment_L_max = abs(filtered_df['Moment (lb-in)'].min())

# Extract moments for each of the lengths separately
moment_L_Ma = abs(filtered_df[filtered_df['Span (in)'] == L_Ma]['Moment (lb-in)'].values[0])
moment_L_Mb = abs(filtered_df[filtered_df['Span (in)'] == L_Mb]['Moment (lb-in)'].values[0])
moment_L_Mc = abs(filtered_df[filtered_df['Span (in)'] == L_Mc]['Moment (lb-in)'].values[0])



# Extract data from the DataFrame
x = filtered_df['Span (in)']
moment = filtered_df['Moment (lb-in)']
shear = filtered_df['Shear (lb)']

# Create two columns using st.beta_columns()
left_column2, middle_column2,right_column2 = st.columns(3)

# with middle_column2:
#     image_filename = 'Beam_loading.png'  # Replace with the actual image file
#     st.image(image_filename, caption='Fig 1: Parameters', width=700)





# Create a Streamlit app
st.write(f'#### **:black_medium_small_square: Moment gradiant for the unbraced portion of the beam**')

# Create two columns using st.beta_columns()
left_column2, middle_column2,right_column2 = st.columns(3)

with middle_column2:
    # Create subplots for moment and shear
    fig, ax1 = plt.subplots(figsize=(3, 1.25))
    ax1.plot(x, moment, linestyle='-', color='b')
    ax1.set_xlabel('Coordinate (in)')
    ax1.set_ylabel('Moment (lb-in)')
    ax1.set_title('Moment vs. Span')

    # Display the Matplotlib plot in Streamlit
    st.pyplot(fig)



st.write(f'#### **:black_medium_small_square: Calculation for the coefficient to account for increased moment resistance (w2)**')

st.write(f'##### Moment within unbraced length of the beam')
st.write(f'##### :black_medium_small_square: M_a = {moment_L_Ma} lb-ft')
st.write(f'##### :black_medium_small_square: M_b = {moment_L_Mb} lb-ft')
st.write(f'##### :black_medium_small_square: M_c = {moment_L_Mc} lb-ft')
st.write(f'##### :black_medium_small_square: M_max = {moment_L_max} lb-ft')
@handcalc()
def omega_two(M_max,Ma,Mb,Mc):
    omega_2 = (4*M_max)/(sqrt(M_max**2+(4*Ma**2)+(7*Mb**2)+(4*Mc**2)))
    return omega_2


omega_2_latex, omega_2 = omega_two(moment_L_max,moment_L_Ma,moment_L_Mb,moment_L_Mc)

st.latex(omega_2_latex)



# Assuming you have already defined x, moment, and shear
# Extract data from the DataFrame
x = df['Span (in)']
moment = df['Moment (lb-in)']
shear = df['Shear (lb)']


# Create subplots for moment and shear
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(x, moment, linestyle='-', color='b')
ax1.set_xlabel('Coordinate (in)')
ax1.set_ylabel('Moment (lb-in)')
ax1.set_title('Moment vs. Span')
ax1.grid(True)  # Add gridlines

ax2.plot(x, shear, linestyle='-', color='k')
ax2.set_xlabel('Coordinate (in)')
ax2.set_ylabel('Shear (lb)')
ax2.set_title('Shear vs. Span')
ax2.grid(True)  # Add gridlines

# Ensure proper spacing between subplots
plt.tight_layout()

# Display the plots using Streamlit
st.pyplot(fig)



#________________________________________________________________________________
with st.expander(":black_medium_small_square: 13.6 Bending - Laterally unsupported members"):
    # Add a banner image at the top
    st.image('omega_two_ref.JPG',width = 600)
    st.image('omega_two_ref2.JPG',width = 600)