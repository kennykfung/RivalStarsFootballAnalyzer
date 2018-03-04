import plotly
import plotly.graph_objs as go
import pandas as pd
import os
import plotly.dashboard_objs as dashboard

import plotly.plotly as py

current_dir_path = os.path.dirname(os.path.realpath(__file__))


plotly.offline.init_notebook_mode(connected=True)


df = pd.read_csv(current_dir_path+r'/player.csv', index_col='Player Name')

#print df[df.POS == 'QB'][['IR']]

#for Player, Row in df.iterrows():
#    print df.POS

data = []

for col in df[df.POS == 'QB'][['IR','OR','SP','LP']]:
    data.append(go.Box(y=df[col], name=col, showlegend=True))

layout = go.Layout(title='QB')
fig = go.Figure(data=data, layout=layout)

my_dboard = dashboard.Dashboard()


#my_dboard.insert(box_RB, 'below', 1)
plotly.offline.plot(fig, filename='RemoveMe', show_link=False)
