import forallpeople
forallpeople.environment('structural', top_level=True)
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
st.title('**Concrete Flexural Reinforcement Calculator**')
# st.divider()  # 👈 Draws a horizontal rule

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

    st.write(f'Factored moment = **{M_f}** N-mm/m')
    st.write(f'Concrete section height, h_c = **{h_c}** mm')
    st.write(f'Concrete section width,b= **{b}** mm')
    st.write(f'Clear cover = **{cover}** mm')
    st.write(f'Bar diameter,db = **{db}** mm')
    st.write(f'phi_c = **{phi_c}**')
    st.write(f'Concrete compressive strength, f_c = **{f_c}** MPa')
    st.write(f'Steel yield strength, f_y = **{f_y}** MPa')
    st.write(f'Effective depth, d = **{d}** mm')
else:

    M_f = st.sidebar.number_input('M_f (lb-ft/ft)')
    h_c = st.sidebar.number_input('h_c (in)')
    b = st.sidebar.number_input('b (in)')
    cover = st.sidebar.number_input('cover (in)')
    db = st.sidebar.number_input('db (in)')
    phi_c = st.sidebar.number_input('phi_c',value = 0.65)
    f_c = st.sidebar.number_input('f_c (MPa)', value = 30)
    f_y = st.sidebar.number_input('f_y (MPa)',value = 400)


    M_f_mod = ((M_f/(0.2448*0.03937))/10**6)*3.28 # N-mm/m
    d = min(0.9*(h_c), h_c-cover-db/2)*25.4 # mm

    st.write(f'Factored moment = {M_f_mod} kN-m/m')
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


st.write(f':one: Required Area Calculation')

@handcalc()
def as_calc(f_c,b,d,M_f):
    As_req = 0.0015*f_c*b*(d - sqrt(d**2 - (3.85*M_f)/(f_c * b)))
    return As_req

if unit_selected == "Metric":

    As_latex, As_req = as_calc(f_c,b,d,M_f)
    st.latex(As_latex)
else:

    As_latex, As_req = as_calc(f_c,b,d,M_f_mod*10**6)
    st.latex(As_latex)


st.write(f'Required steel area = {round(As_req,1)} mm2/m')




# Use the quick calc and compared error percentage 
st.write(f':two: Required Area Calculation (Approximation)')
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
bar_dia_list = [10, 15, 20, 25,30,35,45,55]

Area_list_imp = [0.11,0.20,0.31,0.44,0.60,0.79,1.0,1.27]
bar_dia_list_imp = [3, 4, 5, 6,7,8,9,10]

st.write('### Options:')

for i in range(len(bar_dia_list)):

    if unit_selected == "Metric":
        no_of_bar = As_req/Area_list[i]
        spacing = 1000/(no_of_bar-1) # per m 
    else:
        no_of_bar = As_req/(Area_list[i])
        spacing = 1000/(no_of_bar-1) # per m 
    if no_of_bar<1:
        no_of_bar = 1
        spacing = 1000/(no_of_bar)
        # per m 
    st.write(f'({i+1}) Provide **{round(no_of_bar,0)}** - {bar_dia_list[i]}M  bar at **{round(spacing,0)}** mm or **{round(spacing/25.4,0)}** inch o.c')




