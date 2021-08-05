import pandas as pd
import altair as alt
import streamlit as st
import time

df = pd.read_json("data/dtm_julio_a.json")
# Build an empty graph
upper = alt.Chart(df).mark_line().encode(
  x=alt.X('periodo:T',axis=alt.Axis(title='Periodo')),
  y=alt.Y('0:Q',axis=None)
  ).properties(
      width=700
  )

lower = alt.Chart(df).mark_line().encode(
  x=alt.X('periodo:T',axis=alt.Axis(title='Periodo')),
  y=alt.Y('0:Q',axis=None)
  ).properties(
      width=700, height=100
  )
tot = alt.vconcat(upper, lower)

# Plot a Chart
def plot_animation(df):
    alt_X = alt.X('periodo:T', axis=alt.Axis(domain=False, tickSize=0, tickCount=20, title="Periodos"))
    alt_Y = alt.Y('prob_cant:Q', stack='center', axis=None)
    alt_Color = alt.Color('topico:N', scale=alt.Scale(scheme='category20'),
                      legend=alt.Legend(title="Temas",columns=2,
                                        labelFontSize=14,
                                        titleFontSize=16))
    upper = alt.Chart(df).mark_area(interpolate="basis").encode(
        alt_X, alt_Y, alt_Color, tooltip = [alt.Tooltip('topico'), alt.Tooltip('palabras')]).properties(width=700, title="rrss").interactive()
    
    alt_x2 = alt.X('periodo:T', axis=alt.Axis(domain=True, tickSize=0, tickCount=20, title=" "))
    alt_y2 = alt.Y('cant:Q', axis=alt.Axis(domain=False,  tickCount=3, title="Cantidad"))
    alt_Color = alt.Color('grey')
    lower = alt.Chart(df).mark_area().encode(alt_x2, alt_y2).properties(width=700,height=100)
    tot = alt.vconcat(upper, lower)
    return tot


N = df.shape[0] # number of elements in the dataframe
burst = 6       # number of elements (months) to add to the plot
size = burst    # size of the current dataset

# Plot Animation
line_plot = st.altair_chart(tot)
start_btn = st.button('Start')

if start_btn:
    for i in range(1,N):
        step_df = df.iloc[0:size]       
        lines = plot_animation(step_df)
        line_plot = line_plot.altair_chart(lines)
        size = i + burst
        if size >= N:
            size = N - 1  
        time.sleep(0.1)