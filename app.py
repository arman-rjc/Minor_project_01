import streamlit as st
import forallpeople
import handcalcs.render
from handcalcs.decorator import handcalc
import math 
from dataclasses import dataclass
from typing import List, Optional

# Initialize the environment
forallpeople.environment('structural', top_level=True)

@dataclass
class ThicknessData:
    nominal_thickness: float
    no_of_plies: int
    Ba_0: int
    Ba_90: int
    Bv: int

# Creating a list of ThicknessData objects
data_list: List[ThicknessData] = [
    ThicknessData(7.5, 3, 55000, 24000, 3400),
    ThicknessData(9.5, 3, 55000, 28000, 4300),
    ThicknessData(12.5, 3, 81000, 39000, 5700),
    ThicknessData(15.5, 4, 59000, 75000, 7100),
    ThicknessData(18.5, 5, 83000, 69000, 8600),
    ThicknessData(20.5, 5, 100000, 89000, 9500),
    ThicknessData(22.5, 6, 130000, 69000, 10000),
    ThicknessData(25.5, 7, 120000, 98000, 12000),
]

# Function to get the data based on nominal thickness
def get_data_by_thickness(thickness: float) -> Optional[ThicknessData]:
    for data in data_list:
        if data.nominal_thickness == thickness:
            return data
    return None

@handcalc()
def unit_lateral_strength_resistance(d_f, t_1, t_2, J_x, G, G_f3):
    f_y = 50 * (16 - d_f)
    p_head = 3 * d_f
    p_point = 5 * d_f

    f_1 = 51 * (1 - 0.1 * d_f)
    f_2 = 50 * G * (1 - 0.01 * d_f) * J_x
    f_3 = 110 * G_f3 ** 1.8 * (1 - 0.01 * d_f) * J_x

    a = f_1 * d_f * t_1
    b = f_2 * d_f * t_2
    c = 0.5 * f_2 * d_f * t_2
    d = f_1 * d_f ** 2 * (math.sqrt((f_y * f_3) / (6 * (f_1 + f_3) * f_1)) + (t_1 / (5 * d_f)))
    e = f_1 * d_f ** 2 * (math.sqrt((f_y * f_3) / (6 * (f_1 + f_3) * f_1)) + (t_2 / (5 * d_f)))
    f = f_1 * d_f ** 2 * (1 / 5) * ((t_1 / d_f) + ((f_2 / f_1) * (t_2 / d_f)))
    g = f_1 * d_f ** 2 * math.sqrt((2 * f_3 * f_y) / (3 * (f_1 + f_3) * f_1))

    n_u = min(a, b, d, e, f, g)

    return n_u

def fastener_spacing_factor(s):
    if s >= 150:
        J_s = 1.0
    else:
        J_s = 1 - ((150 - s) / 150) ** 4.2
    return J_s

@handcalc()
def sheathing_to_framing_shear(phi, N_u, s, J_D, n_s, J_us, J_s, J_hd):
    V_rs = phi * (N_u / s) * J_D * n_s * J_us * J_s * J_hd
    return V_rs

@handcalc()
def panel_buckling_strength(a, b, t, B_v, B_a0, B_a90):
    alpha = (a / b) * (B_a90 / B_a0) ** (1 / 4)
    eta = (2 * B_v) / math.sqrt(B_a0 * B_a90)
    k_pb = 1.7 * (eta + 1) * math.exp((-alpha / (0.05 * eta + 0.75))) + (0.5 * eta + 0.8)
    v_pb = k_pb * ((math.pi ** 2 * t ** 2) / (3000 * b)) * (B_a0 * B_a90 ** 3) ** (1 / 4)
    return v_pb

@handcalc()
def panel_buckling_shear(phi, K_D, K_s, K_T, v_pb):
    V_rs = phi * v_pb * K_D * K_s * K_T
    return V_rs

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
J_x = 1.0
J_D = 1.3
n_s = 1.0
J_us = 1.0
J_hd = 1.0
J_s = fastener_spacing_factor(s)

# Get thickness data
thickness_data = get_data_by_thickness(t_1)
B_v = thickness_data.Bv if thickness_data else 0
B_a0 = thickness_data.Ba_0 if thickness_data else 0
B_a90 = thickness_data.Ba_90 if thickness_data else 0

# Calculations
n_u = unit_lateral_strength_resistance(d_f, t_1, t_2, J_x, G, G_f3)
n_u = round(n_u, 0)
N_u = n_u * K_D * K_SF * K_T
V_rs = sheathing_to_framing_shear(phi, N_u, s, J_D, n_s, J_us, J_s, J_hd)
v_pb = panel_buckling_strength(a, b, t_1, B_v, B_a0, B_a90)
V_rsbuckling = panel_buckling_shear(phi, K_D, K_s, K_T, v_pb)
v_rs = round(min(V_rs, V_rsbuckling), 2)

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
