import forallpeople
forallpeople.environment('structural', top_level=True)
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc


st.title('**Concrete Flexural Reinforcement Calculator**')
st.sidebar.write('## Input parameters')

M_f = st.sidebar.number_input('M_f (kN-m)')
h_c = st.sidebar.number_input('h_c (mm)')
b = st.sidebar.number_input('b (mm)')
cover = st.sidebar.number_input('cover (mm)')
db = st.sidebar.number_input('db (mm)')
phi_c = st.sidebar.number_input('phi_c',value = 0.65)
f_c = st.sidebar.number_input('f_c (MPa)', value = 30)
f_y = st.sidebar.number_input('f_y (MPa)',value = 400)


M_f = M_f*10**6
d = min(0.9*(h_c), h_c-cover-db/2) # mm

st.write(f'Factored moment = {M_f} N-m/m')
st.write(f'h_c = {h_c} mm')
st.write(f'b= {b} mm')
st.write(f'Clear cover = {cover} mm')
st.write(f'db = {db} mm')
st.write(f'phi_c = {phi_c} mm')
st.write(f'f_c = {f_c} MPa')
st.write(f'f_y = {f_y} MPa')

@handcalc()
def as_calc(f_c,b,d,M_f):
    As_req = 0.0015*f_c*b*(d - sqrt(d**2 - (3.85*M_f)/(f_c * b)))
    return As_req

As_latex, As_req = as_calc(f_c,b,d,M_f)

st.latex(As_latex)


st.write(f'Required steel area = {round(As_req,1)} mm2/m')


