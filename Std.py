import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# website
# https://standards.streamlit.app/

# title, read data
st.title("IfG Powder Standard Database")
df_data = pd.read_csv('PowderStds.csv', sep=';')
LookUp = pd.read_csv('LookUpTable.csv', sep=';')
df_meta = pd.read_csv('PowderStds Meta.csv', sep=';')
df_abb = pd.read_csv('Abbreviations.csv', sep=';')
df_ci = pd.read_csv('CI-MORB-OIB-PM.csv', sep=';')
#df_alplst = pd.read_csv('AlphabeticListStd.csv', sep=';') 
df_overview = pd.read_csv('Overview.csv', sep=';') 
## error_bad_lines=False
# st.write(df_data) # show data

std_names = df_data['Standard'].drop_duplicates() # list standard names

# LookUp.set_index("Element", inplace=True)
#st.write(LookUp) # show further information

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview Standards", "Standard", "Element", "Search", "CI, MORB, OIB, PM", "Abbreviations"])

with tab1:
   st.header("Overview Standards")
   st.write("List of Standards stored in Room x.xxx. you can find further information or search for specific information in the other tabs.")
   st.write(df_overview)

with tab2:
   standard = st.multiselect("Select one or more standards:", options = df_data["Standard"].unique()) #, default = df_data["Standard"].unique())
   if len(standard) > 0:
      st.write("Element concentrations for selected standard(s):")
      df_data_selection = df_data.query("Standard == @standard")
      ###df_data_selection
      #df_data_selection.index = df_data_selection['Standard']
      st.dataframe(df_data_selection.T)

      st.write('Information for the selected standard(s):')
      df_meta.set_index("Standard", inplace = True)

      standardlist = []
      for i in standard:
         standardlist.append(i)

      metadata = df_meta.loc[standardlist]
      st.dataframe(metadata.T)
          
with tab3:
   elements = df_data.columns[32:111]
   element = st.multiselect("Select one element", options=list(elements)) #, default=list(df_data.columns[26:27]))
   if len(element) > 0:
      fil = df_data['Constituent'] == 'Concentration'
      df_data_conc_only = df_data[fil] # df_data_conc_only zeigt alle Konzentrationen aller Standards

      fullEllist = []
      for i in element:
         LookUp.set_index("Element", inplace = True)
         furtherinfo = LookUp.loc[i]
         fullEllist.append(i)
     
         for j in furtherinfo: #['Further information']  
            if isinstance(j, str):
               res = j.split('_')
               fullEllist.append(res)
            else:
               res = 'none'

     ### flat nested list
      newlist = []
      for i in fullEllist:
         if type(i) is list:
            for j in i:
               newlist.append(j)
         else:
            newlist.append(i)

      dfselected = df_data[newlist]

      dfstd = df_data[['Standard','Constituent']]
      dfstandard = pd.DataFrame(dfstd)
      dfstandard.columns = ['Standard', 'Constituent']

      dfstandard = dfstandard.join(dfselected)

      zeilen = df_data[df_data['Constituent'] == 'Concentration'].index # Index der Zeilen, in denen Concentration steht
      for i in element: # für jedes Element Spalte herausfinden, Wert Konzentration zusammen mit Zeile herausfinden, Auswahlmöglichkeiten, if/else
        auswahl = df_data.columns.get_loc(i) #Spalten der ausgewählten Elemente herausfinden
        d = df_data.iloc[zeilen, auswahl]#.to_list() # Zeilen mit Konzentration der ausgewählten Elemente anzeigen # Konzentrationswerte aller Standards für Element
        scale = st.radio('Choose a scale', ("linear scale", "log scale"), key=i)
        #st.write(d)
    
        #fig2 = px.scatter(x=std_names, y=d, title = i)

        if scale == "log scale":
            fig2 = px.scatter(x=std_names, y=d, log_y=True,  title = i)
        else:
            fig2 = px.scatter(x=std_names, y=d, title = i)
        fig2.update_layout(xaxis_title="Standards", yaxis_title="Concentration in ppm")
        
        st.plotly_chart(fig2)
   
   
with tab4:
   st.header("Search")
   st.write('To get more information about the standard(s) please switch to the tab "Standards".')
   
   # Search Rock Type
   rocktypes = df_overview['Content'].drop_duplicates()
   rocktype = st.multiselect("Select one or more rock types", options=list(rocktypes)) 
   df_overview.set_index("Content", inplace = True)
   df_overview.loc[rocktype, :]
   
   # Search Producer
   producers = df_overview['Producer'].drop_duplicates()
   producer = st.multiselect("Select one or more producers", options=list(producers)) 
   df_overview.set_index("Producer", inplace = True)
   #st.write(df_alplst)
   df_overview.loc[producer, :]
   
   # Search Location
   locations = df_overview['Location'].drop_duplicates()
   location = st.multiselect("Select one or more locations", options=list(locations)) 
   df_overview.set_index("Location", inplace = True)
   df_overview.loc[location, :]
   
      
with tab5:
   st.header("CI, MORB, OIB, PM")
   st.write("Please select a standard to see the corresponding information.")
   type = st.radio('Choose a standard', ("CI Chondrite", "E-MORB", "N-MORB", "OIB", "PM"))
   df_ci.set_index("Rock", inplace = True)
   #st.write(df_ci)
   df_ci.loc[type, :]
   
      
with tab6:
   st.header("Abbreviations")
   st.write("List of Abbreviations for Entities and US States")
   st.write(df_abb)
