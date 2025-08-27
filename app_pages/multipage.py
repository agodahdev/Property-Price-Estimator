import streamlit as st

#creates a multi-page Streamlit app
class MultiPage:
    def __init__(self, app_name):
        self.pages = []
        self.app_name = app_name

        st.set_page_config(
            page_title=self.app_name,
            page_icon="🏠"
        )

    # add pages to the app
    def add_page(self, title, func):
        self.pages.append({
            "title": title,
            "function": func
        })

    # Run the app
    def run(self):
        st.title(self.app_name)

        page = st.sidebar.selectbox(
            'Select Page',
            self.pages,
            format_func=lambda page: page['title']
        )
    
        page['function']()