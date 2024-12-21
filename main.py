from streamlit_option_menu import option_menu
from ResearchBot.app import about, account, home
import streamlit as st
import random



st.set_page_config(page_title="ResearchBot")

class MultiApp:
    def __init__(self):
        self.apps = []
        
    def add_apps(self,title,function):
        self.apps.append({
            "title":title,
            "function":function
        })
    def get_research_tip(self) -> str:
        tips = [
            "Dedicate 30 minutes daily to reading a research paper or article to stay updated in your field.",
            "Join an online forum or community to discuss and exchange ideas on your area of interest.",
            "Practice active recall and spaced repetition to solidify your understanding of complex topics.",
            "Experiment with a hands-on project to apply a concept you’ve recently learned.",
            "Take a 10-minute break every hour while studying to maintain focus and prevent burnout.",
        ]
        return random.choice(tips)    
    def run(self):
  
        with st.sidebar:
            app = option_menu(
                menu_title="Research Bot",
                options=['Home','Account','About'],
                icons=['house','person','info-circle'],
                menu_icon='chat-text',
                default_index=1,
                styles={
                "container": {
                    "padding": "8!important",
                    "background-color": "#262730",
                    "border-radius": "10px", 
                    
                },
                
                "icon": {
                    "color": "white",
                    "font-size": "20px",  
                    "margin-right": "10px",  
                },
                "nav-link": {
                    "color": "white",
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",  
                    "border-radius": "6px", 
                    "transition": "background-color 0.3s ease",  
                },
                "nav-link-selected": {
                    "background-color": "black",
                    "color": "white",  
                    "font-weight": "bold", 
                    "icon-color": "white !important", 
                },
                "nav-link:hover": {
                    "background-color": "#444",  
                    "cursor": "pointer", 
                },
                "menu-title": {
                    "color": "#ffffff", 
                    "font-size": "24px",
                    "font-weight": "bold",  
                    "margin-bottom": "20px",  
                },
                "menu-icon": {
                    "color": "#ffffff",  
                    "font-size": "24px", 
                },
               
                
            },
        )
        if app=='Home':
            home.app()
        elif app=="Account":
            account.app()
        elif app=="About":
            about.app()
            
        st.sidebar.title("💡 Reasearch Goals")
        tip = self.get_research_tip()
        st.sidebar.write(tip)
        
        
        
        


if __name__ == "__main__":
    app = MultiApp()
    app.run()
