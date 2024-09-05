import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import numpy as np 
import dash_daq as daq

# Sample data for machines and processes
process_data = {
    'Paste Grinding': {
        'x': [1, 2, 3, 4, 5],
        'y': [10, 11, 10, 11, 10],
        'status': 'Running',
        'lot_num': 20005,
        'fr': 5
    },
    'Machine 1': {
        'x': [1, 2, 3, 4, 5],
        'y': [10, 15, 13, 17, 14],
        'status': 'Running',
        'lot_num': 20002,
        'mat_used':32.4,
        'mat_waste': 4.2
    },
    'Machine 2': {
        'x': [1, 2, 3, 4, 5],
        'y': [5, 9, 7, 14, 10],
        'status': 'Running',
        'lot_num': 20004,
        'mat_used':42.5,
        'mat_waste': 5.3
    },
    'Machine 3': {
        'x': [1, 2, 3, 4, 5],
        'y': [2, 3, 4, 2, 5],
        'status': 'Stopped',
        'lot_num' :'Nil',
    },
    'Furnace': {
        'x': [1, 2, 3, 4, 5],
        'y': [8, 9, 7, 9, 8],
        'status': 'Running',
        'lot_num': 19999
    },
    'Wirecut': {
        'x': [1, 2, 3, 4, 5],
        'y': [7, 7, 8, 8, 7],
        'status': 'Running',
        'lot_num': 20000
    },
    'Machining': {
        'x': [1, 2, 3, 4, 5],
        'y': [14, 13, 15, 14, 16],
        'status': 'Stopped',
        'lot_num' :'Nil',
        'fr': 4
    },
    'Dimension': {
        'x': [1, 2, 3, 4, 5],
        'y': [3, 4, 3, 4, 3],
        'status': 'Running',
        'lot_num': 19998,
        'fr': 4
    },
    'Tensile': {
        'x': [1, 2, 3, 4, 5],
        'y': [6, 6, 7, 6, 5],
        'status': 'Running',
        'lot_num': 19998,
        'fr': 10
    },
    'Packing': {
        'x': [1, 2, 3, 4, 5],
        'y': [1, 2, 1, 2, 1],
        'status': 'Running',
        'lot_num': 19997
    },
    'Shipping': {
        'x': [1, 2, 3, 4, 5],
        'y': [4, 3, 4, 3, 4],
        'status': 'Running',
        'lot_num': 19996
    },
}

# Process names
processes = [
    'Paste Grinding', 'Machine 1', 'Machine 2', 'Machine 3', 
    'Furnace', 'Wirecut', 'Machining', 
    'Dimension', 'Tensile', 
    'Packing', 'Shipping'
]

# Current and expected lot run times
current_run_time = [1.3, 20, 74, 0, 8, 3, 0, 1, 0.5, 1, 1]
expected_run_time = [1.5, 30, 108, 0, 10, 4, 0, 3, 1, 1, 2]
performance = np.round(np.array(current_run_time) * 100/np.array(expected_run_time),1)
expected_run_time_percentage = [100,100,100,0,100,100,0,100,100,100,100]
pdt = [8,12,40,3,4,15,20,30,14,70,70]
unitsproduced = [1043,205,102,733,1037,1036,1035,1034,1034,1033,1032]
downtime_100 = [100,100,100,100,100,100,100,100,100,100,100]
frate = [5,0,0,0,0,0,4,4,10,0,0]
matused = ['   No Info', '   32.4 KG', '   42.5 KG', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info']
matwaste = ['   No Info', '   4.2 KG', '   5.5 KG', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info', '   No Info']
availability = np.round(np.array(downtime_100) - np.array(pdt),1)
quality = np.array(downtime_100) - np.array(frate)
oee = np.round(performance * quality * availability / 10000,1)
runtime = ['Running', 'Running', 'Running', 'Stopped', 'Running' , 'Running' , 'Stopped', 'Running', 'Running', 'Running', 'Running'
]
count = 0
for i in processes:
    process_data[i]['availability'] = availability[count]
    process_data[i]['quality'] = quality[count]
    process_data[i]['performance'] = performance[count]
    process_data[i]['oee'] = oee[count]
    process_data[i]['unitsproduced'] = unitsproduced[count]
    process_data[i]['matused'] = '   ' + matused[count]
    process_data[i]['matwaste'] = '   ' + matwaste[count]
    process_data[i]['fpr'] = frate[count]
    process_data[i]['cur'] = current_run_time[count]
    process_data[i]['exp'] = expected_run_time[count]
    count += 1 

status_divs = []
status_rows = []
for i in range(0, len(processes), 2):  # Iterate in steps of 2
    row_divs = []
    for j in range(i, min(i + 2, len(processes))):  # Create a row with up to 2 items
        process = processes[j]
        status = runtime[j]
        status_color = 'green' if status == 'Running' else 'red'
        row_divs.append(
            html.Div(
                [
                    html.Div(
                        process,
                        style={
                            'fontSize': '15px',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'marginBottom': '5px'  # Space between process name and status
                        }
                    ),
                    html.Div(
                        status,
                        style={
                            'margin': '4px',
                            'fontSize': '13px',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'backgroundColor': status_color,
                            'padding': '5px',
                            'borderRadius': '5px',
                            'display': 'inline-block'
                        }
                    )
                ],
                style={
                    'width': '45%',  # Adjust the width to fit two items per row
                    'textAlign': 'center',
                    'margin': '5px'
                }
            )
        )
    
    # Center the last row if it contains only one item
    if len(row_divs) == 1:
        row_divs[0] = html.Div(
            row_divs[0],
            style={
                'width': '100%',  # Full width for centering
                'display': 'flex',
                'justifyContent': 'center'
            }
        )
    
    status_rows.append(
        html.Div(
            row_divs,
            style={'display': 'flex', 'justifyContent': 'space-between'}  # Display items side by side
        )
    )


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1("Overview", style={'textAlign': 'center'}),
        html.P("This section includes an overview of the entire process statistics, such as Lot Times, Down Times and Units Produced."),
        html.Div([
        dcc.Graph(
        id='bar-graph',
        figure={
            'data': [
                go.Bar(
                    y=processes,
                    x=expected_run_time_percentage,
                    name='Expected Run Time (%)',
                    marker_color='red',
                    opacity=0.6,
                    orientation='h'
                ),
                go.Bar(
                    y=processes,
                    x=np.round(np.array(current_run_time) * 100/np.array(expected_run_time),0),
                    name='Current Run Time (%)',
                    marker_color='green',
                    orientation='h'
                )
            ],
            'layout': go.Layout(
                barmode='overlay',
                title='Performance of steps process (%)',
                yaxis={'title': 'Processes', 'automargin' : True},
                xaxis={'title': 'Run Time (%)'},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
        id='bar-graph2',
        figure={
            'data': [
                go.Bar(
                    y=processes,
                    x=downtime_100,
                    name='Total Downtime (%)',
                    marker_color='red',
                    opacity=0.6,
                    orientation='h'
                ),
                go.Bar(
                    y=processes,
                    x=np.round(np.array(downtime_100) - np.array(pdt),0),
                    name='Total Uptime (%)',
                    marker_color='green',
                    orientation='h'
                )
            ],
            'layout': go.Layout(
                barmode='overlay',
                title= 'Availability of steps process (%)',
                yaxis={'title': 'Processes', 'automargin' : True},
                xaxis={'title': 'Run Time (%)'},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),


        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
        dcc.Graph(
        id='bar-graph3',
        figure={
            'data': [
                go.Bar(
                    y=processes,
                    x=downtime_100,
                    name='Failure Rate (%)',
                    marker_color='red',
                    opacity=0.6,
                    orientation='h'
                ),
                go.Bar(
                    y=processes,
                    x=np.array(downtime_100) - np.array(frate),
                    name='Functional Rate (%)',
                    marker_color='green',
                    orientation='h',
                    text=np.array(downtime_100) - np.array(frate),  # Adding the value labels
                    textposition='auto' 
                )
            ],
            'layout': go.Layout(
                barmode='overlay',
                title='Quality of steps process (%)',
                yaxis={'title': 'Processes', 'automargin' : True},
                xaxis={'title': 'Run Time (%)'},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
        id='bar-graph4',
        figure={
            'data': [
                go.Bar(
                    y=processes,
                    x=oee,
                    marker_color='#004D40',
                    opacity=0.6,
                    orientation='h',
                    text=oee,  # Adding the value labels
                    textposition='auto'  # Automatically position the labels
                )
            ],
            'layout': go.Layout(
                barmode='overlay',
                title= 'Overall Equipment Effectiveness, OEE(%)',
                yaxis={'title': 'Processes', 'automargin' : True},
                xaxis={'title': 'Effectiveness (%)'},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),


        ], style={'width': '50%', 'display': 'inline-block'}),
        
        
        html.Div([
    html.Div(
        dcc.Graph(
            id='bar-graph5',
            figure={
                'data': [
                    go.Bar(
                        y=processes,
                        x=unitsproduced,
                        name='Total Units Produced',
                        marker_color='blue',
                        opacity=0.6,
                        orientation='h',
                        text=unitsproduced
                    )
                ],
                'layout': go.Layout(
                    barmode='overlay',
                    title='Total Units Produced by each Step',
                    yaxis={'title': 'Processes', 'automargin': True},
                    xaxis={'title': 'Total Units Produced'},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest'
                )
            }
        ),
        style={'width': '75%', 'padding': '10px'}  # Adjust width and add padding
    ),
    html.Div(
        [
            html.H3('Status', style={'textAlign': 'center', 'marginBottom': '20px'}),  # Title centered
            *status_rows
        ],
        style={'width': '25%', 'padding': '10px'}  # Adjust width and add padding
    )
], style={'display': 'flex', 'flexDirection': 'row'}),
        
        # Add more content here for the overview section
    ], style={'width': '75%', 'float': 'left', 'padding': '20px', 'backgroundColor': '#f1f1f1', 'borderRadius': '10px'}),
    
    html.Div([
        html.H1("Specific Step View", style={'textAlign': 'center'}),
        html.P("You can view specific statistics regarding each step here"),
        dcc.Dropdown(
            id='dropdown-example',
            options=[{'label': key, 'value': key} for key in process_data.keys()],
            value='Paste Grinding',
            style={'width': '100%', 'padding': '10px', 'borderRadius': '10px'}
        ),
        html.Div(id='dropdown-content-example', style={'marginTop': '20px'}),
    ], style={'width': '25%', 'float': 'right', 'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px'})
], style={'width': '100%', 'padding': '20px', 'display': 'flex', 'flexDirection': 'row'})

@app.callback(
    Output('dropdown-content-example', 'children'),
    Input('dropdown-example', 'value')
)
def render_content(selected_process):
    if selected_process in process_data:
        status_text = process_data[selected_process]['status']
        status_color = 'red' if status_text == 'Stopped' else 'green'
        lot_num = process_data[selected_process]['lot_num']
        if 'availability' in process_data[selected_process]:
            return html.Div([
                html.Div(
                        f'Running Status: {status_text}',
                        style={
                            'marginTop': '10px',
                            'fontSize': '18px',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'backgroundColor': status_color,
                            'padding': '10px',
                            'borderRadius': '5px',
                            'display': 'inline-block'
                        }
                    ),
                    html.Div(
                        f'Current Lot: {lot_num}',
                        style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold'
                        }
                    ),
                    html.Div(style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold',
                            'marginTop': '20px'
                        }),
                html.Div([
    html.Div([
        html.Div([
            daq.Gauge(
                color={"gradient": True, "ranges": {"green": [80, 100], "yellow": [50, 80], "red": [0, 50]}},
                value=process_data[selected_process]['availability'],
                label='Availability',
                max=100,
                min=0,
                size=150
            ),
            html.Div(f"{process_data[selected_process]['availability']}%", 
                     style={'text-align': 'center', 'margin-top': '10px', 'font-weight': 'bold'})
        ], style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '1px', 'text-align': 'center'}),
        
        html.Div([
            daq.Gauge(
                color={"gradient": True, "ranges": {"green": [80, 100], "yellow": [50, 80], "red": [0, 50]}},
                value=process_data[selected_process]['performance'],
                label='Performance',
                max=100,
                min=0,
                size=150
            ),
            html.Div(f"{process_data[selected_process]['performance']}%", 
                     style={'text-align': 'center', 'margin-top': '10px', 'font-weight': 'bold'})
        ], style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '1px', 'text-align': 'center'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    
    html.Div([
        html.Div([
            daq.Gauge(
                color={"gradient": True, "ranges": {"green": [80, 100], "yellow": [50, 80], "red": [0, 50]}},
                value=process_data[selected_process]['quality'],
                label='Quality',
                max=100,
                min=0,
                size=150
            ),
            html.Div(f"{process_data[selected_process]['quality']}%", 
                     style={'text-align': 'center', 'margin-top': '10px', 'font-weight': 'bold'})
        ], style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '1px', 'text-align': 'center'}),
        
        html.Div([
            daq.Gauge(
                color={"gradient": True, "ranges": {"green": [80, 100], "yellow": [50, 80], "red": [0, 50]}},
                value=process_data[selected_process]['oee'],  # Assuming this is intended
                label='OEE',
                max=100,
                min=0,
                size=150
            ),
            html.Div(f"{process_data[selected_process]['oee']}%", 
                     style={'text-align': 'center', 'margin-top': '10px', 'font-weight': 'bold'})
        ], style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '1px', 'text-align': 'center'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '10px'})
]),
        html.Div([
        html.Div([
            html.Div(f"Units Produced: {process_data[selected_process]['unitsproduced']}",
                     style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-weight': 'bold'}),
        ], style={'flex': '1', 'margin-right': '10px'}),
        
        html.Div([
            html.Div(f"Failure Rate: {process_data[selected_process]['fpr']}%",
                     style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-weight': 'bold'}),
        ], style={'flex': '1', 'margin-right': '10px'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '20px'}),
    
    html.Div([
        html.Div([
            html.Div(f"Materials Used: {process_data[selected_process]['matused']}",
                     style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-weight': 'bold'}),
        ], style={'flex': '1', 'margin-right': '10px'}),
        
        html.Div([
            html.Div(f"Materials Wasted: {process_data[selected_process]['matwaste']}",
                     style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-weight': 'bold'}),
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '20px'}),

    html.Div([
        html.Div([
            html.Div(f"Expected Lot Run Time: {process_data[selected_process]['exp']} Hours",
                     style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-weight': 'bold'}),
        ], style={'flex': '1', 'margin-right': '10px'}),
        
        html.Div([
            html.Div(f"Current Lot Run Time: {process_data[selected_process]['cur']} Hours",
                     style={'border': '2px solid #ccc', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-weight': 'bold'}),
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '20px'})

            ])
            
        elif 'mat_used' in process_data[selected_process]:
            mat_used =str(process_data[selected_process]['mat_used']) + " (KG)"
            mat_waste = str(process_data[selected_process]['mat_waste']) + " (KG)"
            fig = px.pie(
                values=[process_data[selected_process]['mat_used']-process_data[selected_process]['mat_waste'], 100 - process_data[selected_process]['mat_waste']],
                names=['Waste', 'Used'],
                hole=.5
            )
            fig.update_layout(title=f'{selected_process} Material Waste',
                              width=400,  # Set the desired width
                                height=400)
            return html.Div([
                html.Div(
                        f'Running Status: {status_text}',
                        style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'backgroundColor': status_color,
                            'padding': '10px',
                            'borderRadius': '5px',
                            'display': 'inline-block'
                        }
                    ),
                    html.Div(
                        f'Current Lot: {lot_num}',
                        style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold'
                        }
                    ),
                    
                    html.Div(),
                    dcc.Graph(
                        id=f'graph-{selected_process.lower().replace(" ", "-")}',
                        figure=fig,
                        style={'marginTop': '20px'}
                    ),
                    html.Div(
                        f'Materials Used: {mat_used}',
                        style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold'
                        }
                    ),
                    html.Div(
                        f'Materials Wasted: {mat_waste}',
                        style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold'
                        }
                    ),
            ])
        else: 
            return html.Div([
                    html.Div(
                        f'Running Status: {status_text}',
                        style={
                            'marginTop': '5px',
                            'fontSize': '18px',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'backgroundColor': status_color,
                            'padding': '10px',
                            'borderRadius': '5px',
                            'display': 'inline-block'
                        }
                    ),
                    html.Div(
                        f'Current Lot: {lot_num}',
                        style={
                            'marginTop': '20px',
                            'fontSize': '18px',
                            'fontWeight': 'bold'
                        }
                    ),
                    html.Div()
                    
])


if __name__ == '__main__':
    app.run_server(debug=True)
