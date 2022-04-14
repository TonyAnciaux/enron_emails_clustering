import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import data.model as model
from PIL import Image

my_mask = np.array(Image.open("batman_logo.png"))
#image_colors = ImageColorGenerator(my_mask)
def display_cloud(dict_of_words_and_freq):
    wc = WordCloud(stopwords = set(STOPWORDS),
                   mask = my_mask,
                   max_words = 200,
                   contour_width=3,
                   contour_color="black",
                   max_font_size = 100)
    wc.generate_from_frequencies(dict_of_words_and_freq)
    #wc.recolor(color_func=image_colors)
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    trace = go.Scatter(x=x,
                       y=y,
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',
                       text=word_list
                      )

    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})

    fig = go.Figure(data=[trace], layout=layout)
    return fig

def view_of_label(label):
    pass

def main():
    st.set_page_config(
        page_title="ENRON mails clusters",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    side = st.sidebar
    fst_ = side.selectbox("View",["Global View", "Topic View"])
    if fst_ == "Global View":
         st.title("Triage of ENRON emails")
         st.text("Some small presentation of the app")
         flat_topics = [value for topic in model.topics_union for value in topic]
         st.plotly_chart(display_cloud(dict(flat_topics)))
    else:
        def format_func(topic):
            idx, top = topic
            return 'Topic: {} \nWords: {}'.format(idx, ', '.join([w[0] for w in top]))
        topic = side.selectbox("topics",model.topics, format_func=format_func)
        if topic:
            st.title(f"This is topic no {topic[0]}")
            idx, top = topic
            st.plotly_chart(display_cloud(dict(top)))
if __name__ == '__main__':
    main()
