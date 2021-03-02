import glob
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# sidebarにおけるパラメータ設定
st.sidebar.markdown('Set Parameter')
year_ = st.sidebar.number_input(
  'input year',
  value=2021
)
st.sidebar.markdown(f'Your select is: {year_} year')

month_ = st.sidebar.number_input(
  'input month',
  min_value=1,
  max_value=12,
  value=1
)
st.sidebar.markdown(f'Your select is: {month_} month')

# メインコンテンツ
st.header('Visualization of goal achievement')
"""
日々の目標7つを毎日記録し、ひと月ごとに集計して振り返るためのデータ  
データフレームでひと月の結果を確認
"""
date = str(year_) + str(month_).zfill(2)
path = f"../data/{date}/*_preprocess.csv"
df = pd.read_csv(glob.glob(path)[0])
st.dataframe(df)

# 集約したデータフレーム
st.subheader('Display aggregated dataframe')
"""
集計したデータフレームの結果を確認する
"""
sum_list = []
achive_list = []
for col in df.columns[1:]:
    col_sum = df[col].values.astype(int).sum()
    sum_list.append(col_sum)
    achive_list.append(np.round(col_sum/len(df), 4)*100)

data = {
    "項目": df.columns[1:],
    "回数": sum_list,
    "達成率": achive_list
}
agg_df = pd.DataFrame(data)
st.dataframe(agg_df)

# 図の可視化
st.subheader('Visualization bar plot')
"""
棒グラフで達成度合いを可視化して確認する
"""
# Create figure
fig = go.Figure(
    go.Bar(
        name='回数', 
        x=agg_df["項目"].values.tolist(), 
        y=agg_df["回数"].values.tolist(), 
        text=agg_df["達成率"].values.tolist(), 
        width=0.3,
        marker=dict(color="#89cff0")
    )
)

# Add figure title
fig.update_layout(title_text="目標達成度")

# Set x-axis title
fig.update_xaxes(title_text="項目")

# Set y-axes titles
fig.update_yaxes(title_text="回数", range=[0, len(df)])

# Set traces text
fig.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
st.plotly_chart(fig)
