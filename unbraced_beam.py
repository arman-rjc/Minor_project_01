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
from streamlit.components.v1 import html

#________________________________________________________________________________________________________
# How to run this app:
# open anaconda prompt
# Open task manager and right click twice to get the properties tab
# Change start in ""H:\_Personal\07 Spreadsheet Development\07-Projects\Streamlit_app" with the file location
# Go to streamlit and write "stremlit run app.py" replace app.py with the python files name
#________________________________________________________________________________________________________

def CISC_database_reader(filename:str,I_check = 1):
    '''
    Collects all the available W sections in Canada, stores them in a list and 
    Returns the list of W sections from CISC databse.
    '''
    df = pd.read_excel(filename,skipfooter =2)
    mask2 = df.loc[:,"Avl"]== 'a'                               # This function will only store all the W sections that are readily available in Canada and commonly used
    df_sort = df.loc[mask2,["Ds_i","Ds_m","D","B","T","W","BT","HW",
                        "A_Th","Ix","Sx","Zx","Iy",
                       "Sy","Zy","J","Cw","Mass"]]
    # mask3 = df.loc[:,"Ix"]>=I_check
    # df_sort = df.loc[mask3,["Ds_i","Ds_m","D","B","T","W","BT","HW",
    #                     "A_Th","Ix","Sx","Zx","Iy",
    #                    "Sy","Zy","J","Cw","Mass"]]
    # df_sort = df_sort.sort_values("Mass")
    # df_sort
    
    return df_sort


def CISC_database_reader_all(filename:str,I_check = 1):
    '''
    Collects all the available W sections in Canada, stores them in a list and 
    Returns the list of W sections from CISC databse.
    '''
    df = pd.read_excel(filename,skipfooter =2)
    mask2 = df.loc[:,"Shp"]== 1                             # This function will only store all the W sections that are readily available in Canada and commonly used
    df_sort = df.loc[mask2,["Ds_i","Ds_m","D","B","T","W","BT","HW",
                        "A_Th","Ix","Sx","Zx","Iy",
                       "Sy","Zy","J","Cw","Mass"]]
    # mask3 = df.loc[:,"Ix"]>=I_check
    # df_sort = df.loc[mask3,["Ds_i","Ds_m","D","B","T","W","BT","HW",
    #                     "A_Th","Ix","Sx","Zx","Iy",
    #                    "Sy","Zy","J","Cw","Mass"]]
    # df_sort = df_sort.sort_values("Mass")
    # df_sort
    
    return df_sort


    
def Most_economical_section(filename):
    '''
    Collects all the available W sections in Canada, stores them in a list and 
    Returns the list of W sections from CISC databse based on Ix value from low to high.
    '''
    get_section_list = CISC_database_reader(filename)
    Economical_section_list = get_section_list.sort_values("Mass")
    return Economical_section_list


def List_of_selected_depth(filename,selected_depth = "W",Criteria = "Ix"):
    '''
    List all W sections based on specific depth selected and also the sorting of data canbe controlled by using criteria. 
    If no criteria is selected, it will sort the values based on Ix
    '''
    df_eco = CISC_database_reader(filename)
    section_list = df_eco[df_eco['Ds_i'].str.startswith(selected_depth)]
    section_list = section_list.sort_values(Criteria)
    return section_list


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
st.image('gerber_beam.JPG',width = 400)


# Add a banner image at the top
# st.image('steel_beam.png', use_container_width=True)

st.write(f'### **:black_medium_small_square: Laterally Unsupported Beam Resistance**')
st.write(f'##### **This design is per CSA S16 Clause 13.4. The results can be verified against design table of "Handbook of Steel Construction"**')

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
units = ['Metric','Imperial']
selected_units = st.sidebar.selectbox('Beam section unit:', units)


w2 = st.sidebar.number_input(' Coefficient to account for increased moment, w2 ',value = 1.0)
L_u = st.sidebar.number_input('Unbraced beam length, L_u (mm)',value = 1000)
Fy = st.sidebar.number_input('Steel yield strength, Fy (MPa)',value = 345)


# Get the column name for which yqou want to display unique items
column_name = 'Ds_i'     # Replace 'YourColumnName' with the actual column name
column_name_m = 'Ds_m'   # Replace 'YourColumnName' with the actual column name
filename = "W_CISC.xlsm"

selected_depth = "W8"
Criteria = "Mass"


df = CISC_database_reader_all(filename)

if selected_units == 'Metric':
    # Get unique items from the specified column
    unique_items = df[column_name_m].unique()
else:
    # Get unique items from the specified column
    unique_items = df[column_name].unique()    

# Create a selectbox widget in the Streamlit sidebar
selected_item = st.sidebar.selectbox("Select beam section", unique_items)


if selected_units == 'Metric':
    mask = df.loc[:,"Ds_m"] == selected_item
else:
    mask = df.loc[:,"Ds_i"] == selected_item 

# st.write(f'### **:black_medium_small_square: Selected Section Geometry:**')
df_section = df.loc[mask,["Ds_i","Ds_m","D","B","T","W","BT","HW",
                        "A_Th","Ix","Sx","Zx","Iy",
                       "Sy","Zy","J","Cw"]]
# df_section


# Create two columns using st.beta_columns()
left_column, right_column = st.columns(2)

# Add text to the left column
with left_column:
    D = df_section.loc[:,'D'].unique()
    B = df_section.loc[:,'B'].unique()
    T = df_section.loc[:,'T'].unique()
    W = df_section.loc[:,'W'].unique()
    Ix = df_section.loc[:,'Ix'].unique()
    Iy = df_section.loc[:,'Iy'].unique()
    Sx = df_section.loc[:,'Sx'].unique()
    Sy = df_section.loc[:,'Sy'].unique()
    Zx = df_section.loc[:,'Zx'].unique()
    J = df_section.loc[:,'J'].unique()
    Cw = df_section.loc[:,'Cw'].unique()

    # st.write(f'### **:black_medium_small_square: List of parameters:**')
    # st.write(f':black_medium_small_square: Depth of beam, d  = **{D[0]}** mm [**{round(D[0]/25.4,1)}** in]')
    # st.write(f':black_medium_small_square: Width of beam, b  = **{B[0]}** mm [**{round(B[0]/25.4,1)}** in]')
    # st.write(f':black_medium_small_square: Flange thickness, t  = **{T[0]}** mm [**{round(T[0]/25.4,1)}** in]')
    # st.write(f':black_medium_small_square: Web thickness, w  = **{W[0]}** mm [**{round(W[0]/25.4,1)}** in]')

    # Sample data
    data = {
        'Parameters': ['Depth of beam, d = ', 'Width of beam, b = ', 'Flange thickness, t = ', 'Web thickness, w = ','Ix = ','Iy = ','Sx = ','Sy = ','Zx = ','J = ','Cw = '],
        'Value':  [round(D[0]), round(B[0]), round(T[0]), round(W[0]), round(Ix[0]), round(Iy[0]), round(Sx[0]), round(Sy[0]), round(Zx[0]), round(J[0]), round(Cw[0])],
        'Units':  ['mm', 'mm', 'mm', 'mm', 'x10^6 mm4', 'x10^6 mm4', 'x10^3 mm3', 'x 10^3 mm3', 'x 10^3 mm3', 'x 10^3 mm4', 'x 10^9 mm6'],
        # 'value_imp': [round((D[0]/25.4)), round(B[0]/25.4), round(T[0]/25.4), round(W[0]/25.4), Ix[0], Iy[0], Sx[0], Sy[0], Zx[0], J[0], Cw[0]],
        # 'Imperial Units': ['in', 'in', 'in', 'in', '10e6mm4', '10e6mm4', '10e3mm3', '10e3mm3', '10e3mm3', '10e3mm4', '10e9mm6']
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create a Streamlit app
    st.write(f'### **:black_medium_small_square: Data Table for {selected_item}**')


    # Display the table
    st.table(df)

# Add an image to the right column with a specified width and height
with right_column:
    image_filename = 'Generic_section.png'  # Replace with the actual image file
    st.image(image_filename, caption='Fig 1: Section parameters', width=400)
#________________________________________________________________________________

st.write(f'### **:black_medium_small_square: Section Class:**')

# Create two columns using st.beta_columns()
left_column2, right_column2 = st.columns(2)

# Add text to the left column
with left_column2:
    

    @handcalc()
    def class_one(B,T,Fy):
        bel = B[0]/2
        t = T[0]

        widthtothickness = bel/t 
        class1_right = 145/sqrt(Fy)
        class2_right = 170/sqrt(Fy)
        class3_right = 200/sqrt(Fy)


    class_1_latex,class_1 = class_one(B,T,Fy)
    st.latex(class_1_latex)


    bel = B[0]/2  # mm
    t = T[0]    # mm
    widthtothickness = bel/t 
    class1_right = 145/sqrt(Fy)
    class2_right = 170/sqrt(Fy)
    class3_right = 200/sqrt(Fy)


    if widthtothickness <= class1_right:
        st.write(f' Since b/t = {round(widthtothickness,1)} is less than or equal to 145/sqrt(Fy) = {round(145/sqrt(Fy),2)}')
        st.write(f' Therefore, section class is class 1 for flange')
        class_flange = 1
    elif (widthtothickness <=class2_right) and (widthtothickness > class1_right):
        st.write(f' Since b/t = {round(widthtothickness,1)} is greater than 145/sqrt(Fy) = {round(145/sqrt(Fy),2)} and less than  170/sqrt(Fy) = {round(170/sqrt(Fy),2)} ')
        st.write(f' Therefore, section class is class 2 for flange')
        class_flange = 2
    else:
        st.write(f' Since b/t = {round(widthtothickness,1)} is greater than 200/sqrt(Fy) = {round(200/sqrt(Fy),2)}')
        st.write(f' Therefore, section class is class 3 for flange')
        class_flange = 3







# Add text to the right column
with right_column2:
    @handcalc()
    def web_class(B,D,T,W,Fy):
        h = D[0]-2*T[0]
        w = W[0]    # mm

        widthtothickness_web = h/w 
        class1_web_right = 1100/sqrt(Fy)
        class2_web_right = 1700/sqrt(Fy)
        class3_web_right = 1900/sqrt(Fy)


    web_class_latex,web_class = web_class(B,D,T,W,Fy)
    st.latex(web_class_latex)

    h = D[0]-2*T[0]
    w = W[0]    # mm
    widthtothickness_web = h/w 
    class1_web_right = 1100/sqrt(Fy)
    class2_web_right = 1700/sqrt(Fy)
    class3_web_right = 1900/sqrt(Fy)



    if widthtothickness_web <= class1_web_right:
        st.write(f' Since b/t = {round(widthtothickness_web,1)} is less than or equal to 1100/sqrt(Fy) = {round(1100/sqrt(Fy),2)}')
        st.write(f' Therefore, section class is class 1 for web')
        class_web = 1
    elif (widthtothickness_web <=class2_web_right) and (widthtothickness_web > class1_web_right):
        st.write(f' Since b/t = {round(widthtothickness_web,1)} is greater than 1100/sqrt(Fy) = {round(145/sqrt(Fy),2)} and less than  1700/sqrt(Fy) = {round(1700/sqrt(Fy),2)} ')
        st.write(f' Therefore, section class is class 2 for web')
        class_web = 2
    else:
        st.write(f' Since b/t = {round(widthtothickness_web,1)} is greater than 1900/sqrt(Fy) = {round(1900/sqrt(Fy),2)}')
        st.write(f' Therefore, section class is class 3 for web')
        class_web = 3

overall_section_class = max(class_flange,class_web)
st.write(f'#### Overall section class = {overall_section_class}')


st.write(f'### **:black_medium_small_square: Laterally Unsupported Beam Resistance per Clause 13.6**')


#________________________________________________________________________________
with st.expander(":black_medium_small_square: Elastic moment resistance, My"):
    @handcalc()
    def factored_moment_my(Fy,Sx):
        My = (Fy*Sx)/1000
        return My
    My_latex, My = factored_moment_my(Fy,Sx)
    st.latex(My_latex)
    st.write(f'#### Elastic moment resistance, My = {round(My[0],1)} kN-m')
#________________________________________________________________________________


#________________________________________________________________________________
with st.expander(":black_medium_small_square: Plastic moment resistance, Mp"):
    @handcalc()
    def factored_moment_mp(Fy,Zx):
        Mp = (Fy*Zx)/1000
        return Mp

    Mp_latex, Mp = factored_moment_mp(Fy,Zx)
    st.latex(Mp_latex)
    st.write(f'#### Plastic moment resistance, Mp = {round(Mp[0],1)} kN-m')
#________________________________________________________________________________



#________________________________________________________________________________
with st.expander(":black_medium_small_square: Critical elastic moment for unbraced segment of the beam, Mu"):
    pi = math.pi
    sqrt = math.sqrt
    E = 200 # GPa
    G = 77
    @handcalc()
    def critical_elastic_moment_mu(w2,L_u,Iy,G,J,E,Cw):
        M_u = (((w2*pi)/L_u)*sqrt((E*Iy*1000000*G*J*1000)+((pi*E)/L_u)**2*Iy*1000000*Cw*1000000000))/1000  # kN-m
        return M_u

    Mu_latex,M_u = critical_elastic_moment_mu(w2,L_u,Iy,G,J,E,Cw)
    st.latex(Mu_latex)
    st.write(f'#### Critical elastic moment for unbraced segment of the beam, Mu = {round(M_u,1)} kN-m')
#________________________________________________________________________________



#________________________________________________________________________________
with st.expander(":black_medium_small_square: Moment resistance for laterally braced beam, Mr"):

    @handcalc()
    def Mr0(overall_section_class,Fy,Sx,Zx):
        Phi = 0.9
        Mr0_1 = Phi*Fy*Zx/1000
        Mr0_2 = Phi*Fy*Sx/1000
        if(overall_section_class<=2):Mr0 = Phi*Fy*Zx
        elif (overall_section_class<=3): Mr0 = Phi*Fy*Sx
        else: Mr0 = 0
        Mr0 = Mr0/1000
        return Mr0

    Mr0_latex,Mr0 = Mr0(overall_section_class,Fy,Sx,Zx)
    st.latex(Mr0_latex)
    st.write(f'#### Moment resistance for laterally braced beam, Mr0 = {round(Mr0[0],1)} kN-m')
#________________________________________________________________________________



# Calculate factored moment resistance 
@handcalc()
def Factored_Moment_resistance_0(Mp,M_u):
    Phi = 0.9
    if M_u<(0.67*Mp): Mr = Phi*M_u
    else: Mr = min(1.15*Phi*Mp*((1-(0.28*Mp/M_u))),Phi*Mp)
    return int(Mr)

def Governing_Mp(Mp,My):
    if overall_section_class<=2: Mp_governs = Mp
    elif overall_section_class<=3: Mp_governs = My
    else: Mp_governs = 0
    return Mp_governs

Mp_governs = Governing_Mp(Mp,My)
Mr_latex,Mr = Factored_Moment_resistance_0(Mp_governs,M_u)
st.latex(Mr_latex)
st.write(f'#### Factored Moment resistance, Mr = :blue[{Mr}] kN-m')



with st.expander("Reference Material"):
    image_filename = 'Section_class.JPG'  # Replace with the actual image file
    st.image(image_filename, caption='Fig 1: Section parameters', width=1000)

    image_filename = 'bending_unbraced.JPG'  # Replace with the actual image file
    st.image(image_filename, caption='Fig 2: Bending equations', width=1000)

# Add Buy Me a Coffee button
bmc_html = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
data-name="bmc-button" 
data-slug="armans01" 
data-color="#FFDD00" 
data-emoji=""  
data-font="Cookie" 
data-text="Buy me a coffee" 
data-outline-color="#000000" 
data-font-color="#000000" 
data-coffee-color="#ffffff" >
</script>
"""
html(bmc_html, height=70)
