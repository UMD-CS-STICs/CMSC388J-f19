import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# fig = go.Figure(
#     data=[go.Bar(y=[2, 1, 3])],
#     layout_title_text="A Figure Displayed with fig.show()"
# )
# fig.show()

# iris = px.data.iris() # iris is a pandas DataFrame
# fig = px.scatter(iris, x="sepal_width", y="sepal_length")
# fig.show()

# fig = go.Figure(data=go.Scatter(
#     y = np.random.randn(500),
#     mode='markers',
#     marker=dict(
#         size=16,
#         color=np.random.randn(500), #set color equal to a variable
#         colorscale='Viridis', # one of plotly colorscales
#         showscale=True
#     )
# ))

# fig.show()

# N = 100000
# r = np.random.uniform(0, 1, N)
# theta = np.random.uniform(0, 2*np.pi, N)

# fig = go.Figure(data=go.Scattergl(
#     x = r * np.cos(theta), # non-uniform distribution
#     y = r * np.sin(theta), # zoom to see more points at the center
#     mode='markers',
#     marker=dict(
#         color=np.random.randn(N),
#         colorscale='Viridis',
#         line_width=1
#     )
# ))

# fig.show()

# t = np.linspace(0, 10, 100)

# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=t, y=np.sin(t),
#     name='sin',
#     mode='markers',
#     marker_color='rgba(152, 0, 0, .8)'
# ))

# fig.add_trace(go.Scatter(
#     x=t, y=np.cos(t),
#     name='cos',
#     marker_color='rgba(255, 182, 193, .9)'
# ))

# # Set options common to all traces with fig.update_traces
# fig.update_traces(mode='lines', marker_line_width=2, marker_size=10)
# fig.update_layout(title='Styled Scatter',
#                   yaxis_zeroline=False, xaxis_zeroline=False)


# fig.show()

years = [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
         2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]

fig = go.Figure()
fig.add_trace(go.Bar(x=years,
                y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                   350, 430, 474, 526, 488, 537, 500, 439],
                name='Rest of world',
                marker_color='rgb(253, 83, 159)'
                ))
fig.add_trace(go.Bar(x=years,
                y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                   299, 340, 403, 549, 499],
                name='China',
                marker_color='rgb(26, 118, 255)'
                ))

fig.update_layout(
    title='US Export of Plastic Scrap',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()