#imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from io import StringIO

#functions
def group_by_months(df,num):
    count=0
    a=[]
    for i in range(df.shape[1]):
        if df.dtypes[i]=='object':
            a.append(df.columns[i])
            count=count+1
    num_cols = len(df.columns) - count
    features_data=[]
    for l in range(0,count):
        features_data.append(df.iloc[:,l])
    features_dataset=pd.concat(features_data,axis=1,ignore_index=True)
    df=df.drop(a,axis=1)
    division=num_cols % num
    quocient=num_cols //num
    if division==0:
        month_cols=quocient
        grouped_df = [df.iloc[:,j:j+num].sum(axis=1) for j in range(0,num_cols,num)]
    else:
        month_cols=quocient+1
        restant=num_cols - num_cols % num
        grouped_cols= [df.iloc[:, j:j+num].sum(axis=1) for j in range(0, restant, num)]
        remaining_cols=[df.iloc[:,k:k+restant].sum(axis=1) for k in range(restant, num_cols, num_cols-restant)]
        grouped_df=grouped_cols+remaining_cols
    dataset= pd.concat(grouped_df, axis=1, ignore_index=True)
    df_total=pd.concat([features_dataset,dataset],axis=1, ignore_index=True)

    return df_total,num

def rename_columns(df):
    df['Familia']=df.iloc[:,0]
    df['Stopers']=df.iloc[:,1]
    df['Sliders']=df.iloc[:,2]
    df['Teeth']=df.iloc[:,3]
    df['Color']=df.iloc[:,4]
    df['Label']=df.iloc[:,5]
    df['Llargada']=df.iloc[:,6]
    df=df.drop([0,1,2,3,4,5,6],axis=1)
    col_names = df.columns.values.tolist()
    new_col_names = ['Familia', 'Stopers', 'Sliders', 'Teeth', 'Color', 'Label', 'Llargada']
    for col_name in col_names:
        if col_name not in new_col_names:
            new_col_names.append(col_name)
    df = df[new_col_names]       
    return df

def encoding_data(df):
    values_dict = {}
    tipus = df.columns.to_series().groupby(df.dtypes).groups
    text=tipus[np.dtype('object')]
    for c in text:
        df[c], _ = pd.factorize(df[c])
        values_dict[c]=(df[c].unique(), _)
    return df,values_dict

def on_value_change(new_value):
    if new_value:
        st.write(f'El valor del widget ha canviat a {new_value}')
    return new_value

def generate_num():
    st.write('Please enter how you would like to group the months of the year to make the prediction. For example, if you want to do it by quarters, enter 3, if you want to do it by semesters, enter 6... ')
    default_value = st.session_state.get('numero', 1)
    num = st.number_input('Insert the number: ', value=default_value, min_value=None, max_value=12)
    if num == 1:
        num_display = ' '
    else:
        num_display = str(num)

    st.write(f'You entered: {num_display}')
    st.session_state['numero'] = num
    return num

#starting of the action

if "dataframe45" in st.session_state:
    dataset=st.session_state["dataframe45"]


    
columns=dataset.columns
st.title('Data Distribution')
st.write('')
st.write('')
st.write('Before seeing how the Data is Distributed, we will do some modifications to our data in order to work better.')
num=generate_num()
has_finish=st.button('Sumbit number',key='19')
df=dataset.dropna()
df=df.drop(['Codi','Codi sense etiqueta','Descripció'], axis=1)
df=df.drop('Total',axis=1)

dataset_grouped,numero=group_by_months(df,num)
dataset_grouped=rename_columns(dataset_grouped)
df_not_encoded= dataset_grouped.copy()
dataset_grouped,values_dict=encoding_data(dataset_grouped)

if 'diccionari' not in st.session_state:
    st.session_state['diccionari']=values_dict
if 'function' not in st.session_state:
    st.session_state['function']=encoding_data
if 'function2' not in st.session_state:
    st.session_state['function2']=group_by_months
if 'function3' not in st.session_state:
    st.session_state['function3']=rename_columns



#button
if has_finish:
    st.write('This is the dataset grouped by',num, 'months: ')
    st.write(dataset_grouped)
    st.write('Here we will see some graphics of the features.')
    with st.expander("See general plots of our dataset"):
        tab1,tab2,tab3, tab4, tab5,tab6,tab7= st.tabs(["Family Distribution", " Stopers Distribution", "Sliders Distribution","Teeth Distribution",'Color Distribution','Label Distribution','Llargada Distribution'])
        with tab1:
            value_counts = df_not_encoded['Familia'].value_counts()
            st.write('Here you can find from the Familia feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Familia')
            ax.axis('equal')
            st.pyplot(fig)


        with tab2:  
            value_counts = df_not_encoded['Stopers'].value_counts()
            st.write('Here you can find from the Stopers feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Stopers')
            ax.axis('equal')
            st.pyplot(fig)


        with tab3: 
            value_counts = df_not_encoded['Sliders'].value_counts()
            st.write('Here you can find from the Sliders feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Sliders')
            ax.axis('equal')
            st.pyplot(fig)
        with tab4: 
            value_counts = df_not_encoded['Teeth'].value_counts()
            st.write('Here you can find from the Teeth feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Teeth')
            ax.axis('equal')
            st.pyplot(fig)

        with tab5: 
            value_counts = df_not_encoded['Color'].value_counts()
            st.write('Here you can find from the Color feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Color')
            ax.axis('equal')
            st.pyplot(fig)
        with tab6: 
            value_counts = df_not_encoded['Label'].value_counts()
            st.write('Here you can find from the Label feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Label')
            ax.axis('equal')
            st.pyplot(fig)
        with tab7: 
            value_counts = df_not_encoded['Llargada'].value_counts()
            st.write('Here you can find from the Llargada feature the most types sold.')
            st.write(value_counts)
            fig, ax = plt.subplots()
            value_counts = value_counts.head(5)
            st.write('The plot show us the 5 top ones: ')
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart for Llargada')
            ax.axis('equal')
            st.pyplot(fig)

    if 'data_processed' not in st.session_state:
        st.session_state['data_processed']=dataset_grouped