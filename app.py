import streamlit as st
import forallpeople
import handcalcs.render
from handcalcs.decorator import handcalc
import math 
from dataclasses import dataclass
from typing import List, Optional

# Initialize the environment
forallpeople.environment('structural', top_level=True)



# Streamlit sidebar inputs
st.sidebar.header("Shearwall Geometry Input")
d_f = st.sidebar.number_input("Nominal diameter of fastener (mm)", value=2.84)
s = st.sidebar.number_input("Edge nail spacing (mm)", value=150)
t_1 = st.sidebar.selectbox("Head side member thickness (mm)", [data.nominal_thickness for data in data_list])
t_2 = st.sidebar.number_input("Length of penetration into point side (mm)", value=38)
a = st.sidebar.number_input("Larger dimension of the panel (mm)", value=2440)
b = st.sidebar.number_input("Smaller dimension of the panel (mm)", value=1220)

st.sidebar.header("Shearwall Material Properties Input")
G = st.sidebar.number_input("G factor", value=0.42)
G_f3 = st.sidebar.number_input("G_f3 factor", value=0.42)

st.sidebar.header("Shearwall Resistance Factor")
phi = st.sidebar.number_input("Resistance factor (phi)", value=0.8)
K_D = st.sidebar.number_input("K_D factor", value=1.15)
K_SF = st.sidebar.number_input("K_SF factor", value=1.0)
K_T = st.sidebar.number_input("K_T factor", value=1.0)
K_s = st.sidebar.number_input("Service condition factor (K_s)", value=1.0)


# Display results
st.header("Shearwall Calculations")
st.write("### Unit Lateral Strength Resistance")
st.latex(n_u)

st.write("### Sheathing to Framing Shear")
st.latex(V_rs)

st.write("### Panel Buckling Strength")
st.latex(v_pb)

st.write("### Panel Buckling Shear")
st.latex(V_rsbuckling)

st.write("### Final Shear Value")
st.latex(v_rs)
