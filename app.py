import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
#data for stacked bar
def load_data_bar():
    data = pd.read_csv('final_data_result_2.csv')
    data['final_date'] = pd.to_datetime(data['final_date'], format='mixed')  # Correctly handling date conversion
    data['year'] = data['final_date'].dt.year
    return data

bar_data = load_data_bar()

@st.cache_data
#data for donut police
def load_police():
    data = pd.read_csv('agency_police_grouped.csv')
    data = data.sort_values(by = 'Count', ascending = False)
    return data

police_data = load_police()
# print(police_data)

@st.cache_data
# data for child safety severity
def load_child_safety():
    data = pd.read_csv('child_safety_with_service_type_new_counts_for_severity.csv')
    severity_order = ['Extremely High', 'Very High', 'High','Medium','Low']

    data['ServiceSeverityName'] = pd.Categorical(
    data['ServiceSeverityName'],
    categories=severity_order,
    ordered=True)

    data = data.sort_values(by = 'ServiceSeverityName')
    return data

child_safety = load_child_safety()


def main():
    st.header('Monthly Incident Reports For Alexandra Desai')
    col1, col2 = st.columns([1, 5])  # Adjust the ratio as needed
    bar_data = load_data_bar()
    
   
    with col1:
        if 'selected_year' not in st.session_state:
            st.session_state['selected_year'] = bar_data['year'].dropna().min()

# Define the selectbox using the session state
        selected_year = st.selectbox('Select a year', options=bar_data['year'].dropna().unique(), key='selected_year')

# Filter the dataframe based on the selected year
        filtered_df = bar_data[bar_data['year'] == st.session_state.selected_year]
        st.button('Reset', on_click=reset)

    with col2:
        fig = plot_stacked_bars(filtered_df)
        st.plotly_chart(fig,config={'displayModeBar': False}, use_container_width=True)
        # col1, col2 = st.columns(2)
    col1, col2 = st.columns(2)
    with col1:
    # with col3:
        fig = plot_childsafety_donut(child_safety)
        st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

    with col2:
        fig = plot_police_donut(police_data)
        st.plotly_chart(fig, config={'displayModeBar': False},use_container_width=True)


# Define the reset function
def reset():
    # Reset the selected year to the default value
    st.session_state.selected_year = bar_data['year'].dropna().min()



#stacked bar visualisation
def plot_stacked_bars(data):
        
        def create_hover_text(category, count, IncidentCount):
             return [f"<b>Category: {category}</b><br><b>Incident Count: {c}</b><br><b>Total Incident for a month: {i}</b><br>" for c, i in zip(count, IncidentCount)]
        fig = go.Figure()
        # Stacked Bars
        fig.add_trace(go.Bar(x=data['final_date'], y=data['Child Safety Department'], 
                             name='Child Safety', marker_color='royalblue',
                             hoverinfo='text',
                             text=create_hover_text('Child Safety',data['Child Safety Department'],data['Total Incident Count']),
                              textposition='none'
                             ))
        
        fig.add_trace(go.Bar(x=data['final_date'], 
                             y=data['Department of Justice and Attorney General'],
                             name='Department of Justice and Attorney General', 
                             marker_color='indianred',
                             hoverinfo='text', 
                             text=create_hover_text('Department of Justice and Attorney General',data['Department of Justice and Attorney General'], data['Total Incident Count']),
                             textposition='none'))
        
        fig.add_trace(go.Bar(x=data['final_date'], 
                             y=data['Emergency Services Department'],
                             name='Emergency Services Department', 
                             marker_color='lightseagreen', 
                             hoverinfo='text',
                            text=create_hover_text('Emergency Services Department',data['Emergency Services Department'], data['Total Incident Count']),
                            textposition='none'))


        fig.add_trace(go.Bar(x=data['final_date'], 
                             y=data['Hospital and Health Service'],
                             name='Hospital and Health Service', 
                             marker_color='Gray', 
                             hoverinfo='text',
                             text=create_hover_text('Hospital and Health Service',data['Hospital and Health Service'], data['Total Incident Count']),
                             textposition='none'))


        fig.add_trace(go.Bar(x=data['final_date'], 
                             y=data['Not for Profit Organisation'], 
                             name='Not for Profit Organisation', 
                             marker_color='BurlyWood',
                             hoverinfo='text',
                             text=create_hover_text('Not for Profit Organisation',data['Not for Profit Organisation'], data['Total Incident Count']),
                             textposition='none'))


        fig.add_trace(go.Bar(x=data['final_date'], 
                             y=data['Police'], 
                             name='Police', 
                             marker_color='LightSalmon',
                             hoverinfo='text',
                             text=create_hover_text('Police',data['Police'], data['Total Incident Count']),
                             textposition='none'))


        fig.add_trace(go.Bar(x=data['final_date'], 
                             y=data['Youth Justice Department (Juvenile Justice)'],
                             name='Youth Justice Department (Juvenile Justice)', 
                             marker_color='pink', 
                             hoverinfo='text',
                             text=create_hover_text('Youth Justice Department (Juvenile Justice)',data['Youth Justice Department (Juvenile Justice)'], data['Total Incident Count']),
                             textposition='none'))


    # add a line trace for incident costs
        def create_hover_text_2(IncidentCost):
             return [f"<b>Total Cost for a month: {i} AUD</b>" for i in IncidentCost]
        if 'IncidentCost' in data.columns:
            fig.add_trace(go.Scatter(
                x=data['final_date'], y=data['IncidentCost'],
                mode='lines+markers', marker=dict(color='black'), yaxis='y2',
                name='Incident Cost',
                hoverinfo='text',
                text = create_hover_text_2(data['IncidentCost'])
        ))

    # Update the layout to integrate the secondary y-axis for cost
        fig.update_layout(
            barmode='stack',
            title='Monthly Incident Reports',
            yaxis=dict(title='Incident Count'),
            yaxis2=dict(title='Total Cost (AUD)', overlaying='y', side='right', showgrid=False),
            height=400, 
            width=800,
            legend=dict(
            x=1.09),
            hovermode='closest')
        return fig

def plot_police_donut(data):
    fig = go.Figure(data=[go.Pie(
    labels=data["ServiceName"],
    values=data["Count"],
    hole=0.5,
    sort=True,
    marker=dict(colors=px.colors.sequential.Aggrnyl),
    hoverinfo='none',  # This disables the default hoverinfo
    hovertemplate="<b>Service Name: %{label}</b><br><b>Total Count: %{value}</b><extra></extra>")])

    fig.update_layout(title={
            'text': "Incident breakdown by Service for Agency: Police",
            'y':0.9,
            'x':0.35,
            'xanchor': 'center',
            'yanchor': 'top'
        })
    return fig
# title="Incident breakdown by Service for Agency: Police",

# Aggrnyl
def plot_childsafety_donut(data):
    fig = go.Figure(data=[go.Pie(
    labels=data["ServiceSeverityName"],
    values=data["incident_count"],
    hole=0.5,
    marker=dict(colors=px.colors.sequential.RdBu),
    sort=False,
    hoverinfo='none',  # This disables the default hoverinfo
    hovertemplate="<b>Severity: %{label}</b><br><b>Incident Count: %{value}</b><extra></extra>")])

    fig.update_layout(title={
        "text":"Incident breakdown by Severity for Agency: Child Safety Department",
        'y':0.9,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig




if __name__ == "__main__":
    main()