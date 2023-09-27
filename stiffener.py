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
