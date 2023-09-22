import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Function to draw a steel W section
def draw_steel_w_section(width, height, flange_width, flange_thickness, web_thickness):
    fig, ax = plt.subplots()

    # Draw the flanges
    flange_left = patches.Rectangle((0, 0), flange_width, height, linewidth=1, edgecolor='b', facecolor='none')
    flange_right = patches.Rectangle((width - flange_width, 0), flange_width, height, linewidth=1, edgecolor='b', facecolor='none')

    # Draw the web
    web = patches.Rectangle((flange_width, height / 2 - web_thickness / 2), width - 2 * flange_width, web_thickness, linewidth=1, edgecolor='b', facecolor='none')

    # Add the shapes to the plot
    ax.add_patch(flange_left)
    ax.add_patch(flange_right)
    ax.add_patch(web)

    # Set plot limits
    ax.set_xlim(0, width)
    ax.set_ylim(0, height + 1)

    # Add dimensions to the plot
    ax.text(width / 2, -0.5, f"Width: {width}", ha='center')
    ax.text(-0.5, height / 2, f"Height: {height}", va='center', rotation='vertical')
    ax.text(flange_width / 2, height + 0.5, f"Flange Width: {flange_width}", ha='center')
    ax.text(width - flange_width / 2, height + 0.5, f"Flange Width: {flange_width}", ha='center')
    ax.text(width / 2, height / 2, f"Flange Thickness: {flange_thickness}", ha='center')
    ax.text(width / 2, height / 2 - web_thickness / 2, f"Web Thickness: {web_thickness}", ha='center')

    return fig

# Create a Streamlit app
st.title("Steel W Section Dimensions")

# Define steel W section dimensions (you can modify these values)
width = st.slider("Width:", 100, 1000, 300)
height = st.slider("Height:", 50, 500, 150)
flange_width = st.slider("Flange Width:", 10, 200, 50)
flange_thickness = st.slider("Flange Thickness:", 5, 50, 15)
web_thickness = st.slider("Web Thickness:", 5, 50, 10)

# Draw the steel W section and display it in Streamlit
st.pyplot(draw_steel_w_section(width, height, flange_width, flange_thickness, web_thickness))
