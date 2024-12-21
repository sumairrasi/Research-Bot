import streamlit as st


def app():
    st.title("About")
    st.write(
        """
        ### Chatbot for Learning Research Papers and Documents
        
        This application is designed to help researchers, students, and professionals 
        interact with research papers and documents more efficiently. By leveraging 
        advanced natural language processing techniques, the chatbot provides insightful 
        answers to queries, summarizes content, and highlights key information from 
        uploaded documents.
        
        ---
        
        **Developer Details:**
        
        - 📧 Email: [sumairrazi585@gmail.com](mailto:sumairrazi585@gmail.com)
        - 💼 LinkedIn: [Sumair Rasi](https://www.linkedin.com/in/sumairrasi)  
        - 🖥️ GitHub: [Sumair Rasi](https://github.com/SumairRasi)
        
        ---
        
        If you encounter any issues or have suggestions, feel free to reach out!
        """
    )

    # Adding logos with hyperlinks
    st.write("**Connect with me:**")
    st.markdown(
        """
        [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sumair.rasi@gmail.com)
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sumairrasi)
        [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SumairRasi)
        """
    )
