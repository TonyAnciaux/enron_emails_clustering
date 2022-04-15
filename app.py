import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import data.model as model


def bar_of_topic(topic):
    x = [t[1] for t in topic]
    y = [t[0] for t in topic]
    fig = go.Figure(go.Bar(
            x=x,
            y=y,
            orientation='h'))
    return fig

def keyword_in_topic(keyword, topic):
    _, top = topic
    keywords = [l[0] for l in top]
    return (keyword in keywords)

def format_func(topic):
    idx, top = topic
    return 'Topic: {} \nWords: {}'.format(idx, ', '.join([w[0] for w in top]))

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
         st.title("Email analysis tool")
         st.subheader("Menu View")
         st.write("Allows you to visualize the most relevant words within each topic or in a global way.")
         st.write("Usage: Select the option from the drop down menu.")
         st.subheader("Menu Topics")
         st.write("This opens the main page where you can access each email pertaining to the selected topic.")
         st.write("Usage: Select the topic you wish to explore from the drop down menu.")
         st.image("bat.png")
         keyword = side.text_input("Search topic from keyword", "tax")
         list_of_topics = [
             topic for topic in model.topics if keyword_in_topic(keyword, topic)
         ]
         side.selectbox(f"Topics for '{keyword}'", list_of_topics, format_func=format_func)
    else:
        topic = side.selectbox("Topics",model.topics, format_func=format_func)
        if topic:
            st.title(f"This is topic no {topic[0]}")
            idx, top = topic
            col1, col2 = st.columns(2)
            with col2:
                st.image(f"bat_topic_{idx}.png")
            with col1:
                st.plotly_chart(bar_of_topic(top))

            series_of_emails = model.mails_of_topic(idx, thresh=0.8)
            email = st.selectbox("Emails",series_of_emails)
            keyword = side.text_input("Search topic from keyword", "tax")
            list_of_topics = [
                topic for topic in model.topics if keyword_in_topic(keyword, topic)
            ]
            side.selectbox(f"Topics for '{keyword}'", list_of_topics, format_func=format_func)
            message = model.email_of_path(email)
            st.write(message)
if __name__ == '__main__':
    main()
