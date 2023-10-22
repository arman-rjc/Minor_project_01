import forallpeople
forallpeople.environment('structural', top_level=True)
import math
from math import sqrt
import streamlit as st
from handcalcs.decorator import handcalc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches



#________________________________________________________________________________________________________
# How to run this app:
# open anaconda prompt
# Open task manager and right click twice to get the properties tab
# Change start in ""H:\_Personal\07 Spreadsheet Development\07-Projects\Streamlit_app" with the file location
# Go to streamlit and write "stremlit run app.py" replace app.py with the python files name
#________________________________________________________________________________________________________


st.set_page_config(layout='wide')
st.title('**:blue[Roof or Floor Dead Load Calculator]**')


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

with st.expander(":black_medium_small_square: Project Information"):
    #  Create a Streamlit app
    # st.sidebar.write("Project Information")

    # Add text input boxes for Project Name, Job No, Designer, and Date
    project_name = st.text_input("Project Name:")
    job_no = st.text_input("Job No:")
    designer = st.text_input("Designer:")
    date = st.text_input("Date:")


    

roof_or_floor = st.selectbox(
    "Select either roof or floor assembly",
    ("Roof Assembly","Floor Assembly")
    )    


st.write('## Input parameters')

if roof_or_floor == "Floor Assembly":
    # Create two columns using st.beta_columns()
    left_column_input,right_column_input = st.columns([1,2])


    with left_column_input:

        partition = st.selectbox(
            "1- Partition Load",
            ("Partition wall","N/A")
            )
            
        floor_finish = st.selectbox(
            "2 - Floor Finish",
            ("Floor finish","N/A")
            )

        steel_deck = st.selectbox(
            "3 - Steel Deck",
            ("38 mm - upto 0.91 mm thick","38 mm - 1.22mm to 1.52mm thick",
            "76mm (Narrow rib) mm - upto 0.91 mm thick","76mm (Narrow rib) mm - 1.22mm to 1.52mm thick",
            "76mm (wide rib) mm - upto 0.91 mm thick","76mm (wide rib) mm - 1.22mm to 1.52mm thick",
            )
            )

        owsj = st.selectbox(
            "4 - OWSJ or Steel Beam",
            ("Open Web Steel Joist - OWSJ","Steel Beam")
            )

        mech_or_elec = st.selectbox(
            "5 - Mechanical or Electrical",
            ("Mechanical or Electrical","Other")
            )

        suspended_ceiling = st.selectbox(
            "6 - Suspended Ceiling",
            ("Suspended Ceiling","Other")
            )



        add_load = st.number_input('10 - Additional Loading',value = 0.20)

    # Partition Wall
    #_____________________________________________________
    if partition == "Partition wall":
        a = 1.00
    else:
        a = 0.00


    # floor_finish
    #_____________________________________________________
    if floor_finish == "Floor finish":
        b = 0.15
    else:
        b = 0.00


    # Steel Deck
    #_____________________________________________________
    if steel_deck == "38 mm - upto 0.91 mm thick":
        f = 0.10
    elif steel_deck == "38 mm - 1.22mm to 1.52mm thick":
        f = 0.15
    elif steel_deck == "76mm (Narrow rib) mm - upto 0.91 mm thick":
        f = 0.15 
    elif steel_deck == "76mm (Narrow rib) mm - 1.22mm to 1.52mm thick":
        f = 0.30 
    elif steel_deck == "76mm (wide rib) mm - upto 0.91 mm thick":
        f = 0.10
    else:
        f = 0.15

    # OWSJ or Steel Beam
    #_____________________________________________________
    if owsj == "Open Web Steel Joist - OWSJ":
        g = 0.20
    else:
        g = 0.30

    # Mechanical or electrical
    #_____________________________________________________
    if mech_or_elec == "Mechanical or Electrical":
        h = 0.25
    else:
        h = 0.30


    # suspended_ceiling
    #_____________________________________________________
    if suspended_ceiling == "Suspended Ceiling":
        i = 0.20
    else:
        i = 0.30



    # Create two columns using st.beta_columns()
    top_right,bottom_right = st.columns(2)

    # with right_column_input:
    with right_column_input:
        st.write(f'**Floor Assembly Load**')
        # # Sample data
        data = {
            'Item': [f'Partition wall  = ', f'Floor finish  = ',f'Steel Deck ({steel_deck}) = ',f'OWSJ or Steel Beam ({owsj}) = ',
                    f'Mechanical or Electrical ({mech_or_elec}) = ',f"Suspended Ceiling ({suspended_ceiling}) = ",f"Additional Loading = ", f'Total Load ='],
            'kPa':  [a, b,f,g,h,i,add_load,(a+b+f+g+h+i+add_load)]
        }


        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        
        st.dataframe(df,width = 900,height=350)



    # with right_column_input:
    with right_column_input:
        st.image('floor_assembly.PNG',width = 500 )


    st.write(f'### **:black_medium_small_square: Floor Loading**')
    st.write(f'_____________________________________________________________________________________')

    S = st.number_input('Floor live load, L (kPa)',value = 2.0)
    P_downward = st.number_input('Wind load, w (kPa)',value = 2.0)
    Girder = st.number_input('Girder dead load, gd (kPa)',value = 2.0)
    SteelDeck = f
    MechElect = h
    OWSJ = g
    Roofing = (a+b+f+g+h+i+add_load) - SteelDeck - MechElect - OWSJ



    data = {'Dead (kPa)': [0, 0, Roofing, SteelDeck, (Roofing+SteelDeck),MechElect,OWSJ,(Roofing+SteelDeck+MechElect+OWSJ),Girder,(Roofing+SteelDeck+MechElect+OWSJ+Girder)],
            'Live (kPa)': [S, 0, 0, 0, S,0,0,S,0,S],
            'Wind (kPa)': [0, P_downward, 0, 0, P_downward,0,0,P_downward,0,P_downward],
            'Factored (1.25*D+1.5*L+0.4*W) (kPa)': [1.5*S, 0.4*P_downward, 1.25*Roofing, 1.25*SteelDeck, (1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck),1.25*MechElect,1.25*OWSJ,(1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ),1.25*Girder,(1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ+1.25*Girder)],
            'Service (1.00*D+0.9*L) (kPa)': [0.9*S,0, 1.00*Roofing, 1.00*SteelDeck, (0.9*S+1.00*Roofing+1.00*SteelDeck),1.00*MechElect,1.00*OWSJ,(0.9*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ),1.00*Girder,(0.90*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ+1.00*Girder)]
            }

    df_all = pd.DataFrame(data, index=['Floor Live','Wind','Roofing/Insulation/Ceiling','Steel Deck','**Total Deck Design Load**','MechElect','OWSJ','**Total Load for Joist Design**','Girder','**Total load for Girder**'])
    st.dataframe(df_all,width = 1800,height=450)
    # #df.style
    # print (tabulate(df, headers ="keys",tablefmt = "fancy_grid"))

    st.write(f'### **:black_medium_small_square: Summary**')
    st.write(f'_____________________________________________________________________________________')

    # Create two columns using st.beta_columns()
    left_c,middle_c,right_c = st.columns(3)

    with left_c:
        st.write(f'### **Total Deck Design Load:**')
        st.write(f'##### **Dead Load: {round(Roofing+SteelDeck,2)} kPa**')
        st.write(f'##### **Live Load: {round(S,2)} kPa**')
        st.write(f'##### **Wind Load: {round(P_downward,2)} kPa**')
        st.write(f'##### **Factored (1.25*D+1.5*L+0.4*W) Load: {round((1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck),2)} kPa**')
        st.write(f'##### **Service (1.00*D+0.9*L) Load: {round((0.9*S+1.00*Roofing+1.00*SteelDeck),2)} kPa**')


    with middle_c:
        st.write(f'### **Total Load for Joist Design:**')
        st.write(f'##### **Dead Load: {round((Roofing+SteelDeck+MechElect+OWSJ),2)} kPa**')
        st.write(f'##### **Live Load: {round(S,2)} kPa**')
        st.write(f'##### **Wind Load: {round(P_downward,2)} kPa**')
        st.write(f'##### **Factored (1.25*D+1.5*L+0.4*W) Load: {round((1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ),2)} kPa**')
        st.write(f'##### **Service (1.00*D+0.9*L) Load: {round((0.9*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ),2)} kPa**')
        st.write(f'##### **check out this [link](https://owsjdepthcheckpy-72hsgrdfq2gf45usmwsgaa.streamlit.app/)  for joist depth check **')

    with right_c:
        st.write(f'### **Total Load for Girder Design:**')
        st.write(f'##### **Dead Load: {round((Roofing+SteelDeck+MechElect+OWSJ+Girder),2)} kPa**')
        st.write(f'##### **Live Load: {round(S,2)} kPa**')
        st.write(f'##### **Wind Load: {round(P_downward,2)} kPa**')
        st.write(f'##### **Factored (1.25*D+1.5*L+0.4*W) Load: {round((1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ+1.25*Girder),2)} kPa**')
        st.write(f'##### **Service (1.00*D+0.9*L) Load: {round((0.90*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ+1.00*Girder),2)} kPa**')




else:

    # Create two columns using st.beta_columns()
    left_column_input,right_column_input = st.columns([1,2])


    with left_column_input:

        roof_mem = st.selectbox(
            "1-Multi-Ply Membrane",
            ("3-ply asphalt no gravel","4-ply asphalt no gravel","3-ply asphalt and gravel","4-ply asphalt and gravel","Asphalt strip shingles","Other type")
            )
            
        fiber_board = st.selectbox(
            "2 - Fiber board",
            ("12.7 mm thick","15.9 mm thick","19 mm thick")
            )

        rigid_insulation = st.selectbox(
            "3 - Rigid Insulation (per 100 mm thick)",
            ("Glass fiber- batt","Glass fiber- blown","Glass fiber- rigid","Urethane - rigid foam","Insulating concrete")
            )
        vapor_bariar = st.selectbox(
            "4 - Vapor Barrier",
            ("Vapor Barrier","N/A")
            )

        gypsum = st.selectbox(
            "5 - Gypsum wallboard per 10mm",
            ("13 mm","19 mm")
            )


        steel_deck = st.selectbox(
            "6 - Steel Deck",
            ("38 mm - upto 0.91 mm thick","38 mm - 1.22mm to 1.52mm thick",
            "76mm (Narrow rib) mm - upto 0.91 mm thick","76mm (Narrow rib) mm - 1.22mm to 1.52mm thick",
            "76mm (wide rib) mm - upto 0.91 mm thick","76mm (wide rib) mm - 1.22mm to 1.52mm thick",
            )
            )

        owsj = st.selectbox(
            "7 - OWSJ or Steel Beam",
            ("Open Web Steel Joist - OWSJ","Steel Beam")
            )

        mech_or_elec = st.selectbox(
            "8 - Mechanical or Electrical",
            ("Mechanical or Electrical","Other")
            )

        suspended_ceiling = st.selectbox(
            "9 - Suspended Ceiling",
            ("Suspended Ceiling","Other")
            )



        add_load = st.number_input('10 - Additional Loading',value = 0.20)

    # Roof membrane
    #_____________________________________________________
    if roof_mem == "3-ply asphalt no gravel":
        a = 0.15
    elif roof_mem == "4-ply asphalt no gravel":
        a = 0.20
    elif roof_mem == "3-ply asphalt and gravel":
        a = 0.27 
    elif roof_mem == "4-ply asphalt and gravel":
        a = 0.32 
    elif roof_mem == "Asphalt strip shingles":
        a = 0.15
    else:
        a = 0.15


    # Fiber board
    #_____________________________________________________
    if fiber_board == "12.7 mm thick":
        b = 0.06
    elif fiber_board == "15.9 mm thick":
        b = 0.08
    else:
        b = 0.12


    # rigid_insulation
    #_____________________________________________________
    if rigid_insulation == "Glass fiber- batt":
        c = 0.05
    elif rigid_insulation == "Glass fiber- blown":
        c = 0.04
    elif rigid_insulation == "Glass fiber- rigid":
        c = 0.007 
    elif rigid_insulation == "Urethane - rigid foam":
        c = 0.003
    else:
        c = 0.006


    # Vapor Barrier
    #_____________________________________________________
    if vapor_bariar == "Vapor Barrier":
        d = 0.10
    else:
        d = 0.00

    # Gypsum wallboard
    #_____________________________________________________
    if gypsum == "13 mm":
        e = 0.104
    else:
        e = 0.152


    # Steel Deck
    #_____________________________________________________
    if steel_deck == "38 mm - upto 0.91 mm thick":
        f = 0.10
    elif steel_deck == "38 mm - 1.22mm to 1.52mm thick":
        f = 0.15
    elif steel_deck == "76mm (Narrow rib) mm - upto 0.91 mm thick":
        f = 0.15 
    elif steel_deck == "76mm (Narrow rib) mm - 1.22mm to 1.52mm thick":
        f = 0.30 
    elif steel_deck == "76mm (wide rib) mm - upto 0.91 mm thick":
        f = 0.10
    else:
        f = 0.15

    # OWSJ or Steel Beam
    #_____________________________________________________
    if owsj == "Open Web Steel Joist - OWSJ":
        g = 0.20
    else:
        g = 0.30

    # Mechanical or electrical
    #_____________________________________________________
    if mech_or_elec == "Mechanical or Electrical":
        h = 0.25
    else:
        h = 0.30


    # suspended_ceiling
    #_____________________________________________________
    if suspended_ceiling == "Suspended Ceiling":
        i = 0.20
    else:
        i = 0.30

    # Create two columns using st.beta_columns()
    top_right,bottom_right = st.columns(2)

    # with right_column_input:
    with right_column_input:
        st.write(f'**Roof Assembly Load**')
        # # Sample data
        data = {
            'Item': [f'Multi-Ply Membrane ({roof_mem}) = ', f'Fiber board ({fiber_board}) = ', f'Rigid Insulation (per 100 mm thick) ({rigid_insulation})= ',
                    f'Vapor Barrier = ',f'Gypsum wallboard per 10mm = ',f'Steel Deck ({steel_deck}) = ',f'OWSJ or Steel Beam ({owsj}) = ',
                    f'Mechanical or Electrical ({mech_or_elec}) = ',f"Suspended Ceiling ({suspended_ceiling}) = ",f"Additional Loading = ", f'Total Load ='],
            'kPa':  [a, b, c, d,e,f,g,h,i,add_load,(a+b+c+d+e+f+g+h+i+add_load)]
        }


        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        
        st.dataframe(df,width = 900,height=450)



    # with right_column_input:
    with right_column_input:
        st.image('Roof_assembly.PNG',width = 700)


    st.write(f'### **:black_medium_small_square: Roof Loading**')
    st.write(f'_____________________________________________________________________________________')

    S = st.number_input('Roof snow load, S (kPa)',value = 2.0)
    P_downward = st.number_input('Wind load, w (kPa)',value = 2.0)
    Girder = st.number_input('Girder dead load, gd (kPa)',value = 2.0)
    SteelDeck = f
    MechElect = h
    OWSJ = g
    Roofing = (a+b+c+d+e+f+g+h+i+add_load) - SteelDeck - MechElect - OWSJ



    data = {'Dead (kPa)': [0, 0, Roofing, SteelDeck, (Roofing+SteelDeck),MechElect,OWSJ,(Roofing+SteelDeck+MechElect+OWSJ),Girder,(Roofing+SteelDeck+MechElect+OWSJ+Girder)],
            'Snow (kPa)': [S, 0, 0, 0, S,0,0,S,0,S],
            'Wind (kPa)': [0, P_downward, 0, 0, P_downward,0,0,P_downward,0,P_downward],
            'Factored (1.25*D+1.5*S+0.4*W) (kPa)': [1.5*S, 0.4*P_downward, 1.25*Roofing, 1.25*SteelDeck, (1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck),1.25*MechElect,1.25*OWSJ,(1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ),1.25*Girder,(1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ+1.25*Girder)],
            'Service (1.00*D+0.9*S) (kPa)': [0.9*S,0, 1.00*Roofing, 1.00*SteelDeck, (0.9*S+1.00*Roofing+1.00*SteelDeck),1.00*MechElect,1.00*OWSJ,(0.9*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ),1.00*Girder,(0.90*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ+1.00*Girder)]
            }

    df_all = pd.DataFrame(data, index=['Roof snow','Wind','Roofing/Insulation/Ceiling','Steel Deck','**Total Deck Design Load**','MechElect','OWSJ','**Total Load for Joist Design**','Girder','**Total load for Girder**'])
    st.dataframe(df_all,width = 1800,height=450)
    # #df.style
    # print (tabulate(df, headers ="keys",tablefmt = "fancy_grid"))

    st.write(f'### **:black_medium_small_square: Summary**')
    st.write(f'_____________________________________________________________________________________')

    # Create two columns using st.beta_columns()
    left_c,middle_c,right_c = st.columns(3)

    with left_c:
        st.write(f'### **Total Deck Design Load:**')
        st.write(f'##### **Dead Load: {round(Roofing+SteelDeck,2)} kPa**')
        st.write(f'##### **Snow Load: {round(S,2)} kPa**')
        st.write(f'##### **Wind Load: {round(P_downward,2)} kPa**')
        st.write(f'##### **Factored (1.25*D+1.5*S+0.4*W) Load: {round((1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck),2)} kPa**')
        st.write(f'##### **Service (1.00*D+0.9*S) Load: {round((0.9*S+1.00*Roofing+1.00*SteelDeck),2)} kPa**')


    with middle_c:
        st.write(f'### **Total Load for Joist Design:**')
        st.write(f'##### **Dead Load: {round((Roofing+SteelDeck+MechElect+OWSJ),2)} kPa**')
        st.write(f'##### **Snow Load: {round(S,2)} kPa**')
        st.write(f'##### **Wind Load: {round(P_downward,2)} kPa**')
        st.write(f'##### **Factored (1.25*D+1.5*S+0.4*W) Load: {round((1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ),2)} kPa**')
        st.write(f'##### **Service (1.00*D+0.9*S) Load: {round((0.9*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ),2)} kPa**')
        st.write(f'##### **check out this [link](https://owsjdepthcheckpy-72hsgrdfq2gf45usmwsgaa.streamlit.app/)  for joist depth check **')

    with right_c:
        st.write(f'### **Total Load for Girder Design:**')
        st.write(f'##### **Dead Load: {round((Roofing+SteelDeck+MechElect+OWSJ+Girder),2)} kPa**')
        st.write(f'##### **Snow Load: {round(S,2)} kPa**')
        st.write(f'##### **Wind Load: {round(P_downward,2)} kPa**')
        st.write(f'##### **Factored (1.25*D+1.5*S+0.4*W) Load: {round((1.5*S+0.4*P_downward+1.25*Roofing+1.25*SteelDeck+1.25*MechElect+1.25*OWSJ+1.25*Girder),2)} kPa**')
        st.write(f'##### **Service (1.00*D+0.9*S) Load: {round((0.90*S+1.00*Roofing+1.00*SteelDeck+1.00*MechElect+1.00*OWSJ+1.00*Girder),2)} kPa**')


with st.expander("Typical steel deck components - for reference"):
    st.image('Typical_steel_deck.PNG',width = 800)

# with st.expander("Dead Load Table "):
#     st.image('dead_loads.PNG',width = 1000)


# file = "dead_loads.pdf"
# def displayPDF(file):
#     # Opening file from file path
#     with open(file, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')

#     # Embedding PDF in HTML
#     # pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
#     pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#     # Displaying File

# st.markdown(pdf_display, unsafe_allow_html=True)



# # Display the "Buy me a coffee" button
# if st.button("Buy me a coffee!"):
#     # Add your e-transfer link here
#     etransfer_link = "YOUR_ETRANSFER_LINK"
#     st.write(f"Click the link below to send me money for coffee: [Buy me a coffee]({etransfer_link})")
