import streamlit as st
import requests
import os
import dotenv

# Custom page layout
st.set_page_config(
    page_title="Movie Information App",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

dotenv.load_dotenv()

class OMDbConnection:
    def _connect(self):
        self.base_url = "http://www.omdbapi.com/"
        self.api_key = os.getenv("API")

    def cursor(self):
        return self.session

    @staticmethod
    @st.cache_data(ttl=600)  # Cached for 10 minutes to avoid unnecessary API calls
    def query(movie_title):  
        base_url = "http://www.omdbapi.com/"
        api_key = os.getenv("API")
        full_url = f"{base_url}?apikey={api_key}&t={movie_title}"
        response = requests.get(full_url)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch movie information. Status code: {response.status_code}")
            return None

def main():
    # Page header
    st.title("Movie Information App")
    st.markdown("---")

    omdb_conn = OMDbConnection()
    omdb_conn._connect()

    # Sidebar layout
    st.sidebar.subheader("Search Movie")
    movie_title = st.sidebar.text_input("Enter a movie title:")
    st.sidebar.markdown("---")

    if st.sidebar.button("Search"):
        try:
            if movie_title:
                movie_info = omdb_conn.query(movie_title)  # Pass only the movie title as an argument
                if "Error" not in movie_info:
                    # Display movie details in a collapsible container
                    with st.expander(f"Movie Information: {movie_info.get('Title', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(movie_info.get("Poster", ""), caption=movie_info.get("Title", ""), use_column_width=True)
                        with col2:
                            st.write("Year:", movie_info.get("Year", "N/A"))
                            st.write("Genre:", movie_info.get("Genre", "N/A"))
                            st.write("Director:", movie_info.get("Director", "N/A"))
                            st.write("Plot:", movie_info.get("Plot", "N/A"))
                else:
                    error = movie_info["Error"]
                    st.error(f"Error: {error}")
        except Exception as e:
            st.error("An error occurred. Please try again.")

    # Page footer
    st.markdown("---")
    st.info("Developed by Amarjeet Mohanty | [GitHub Repo](https://github.com/AmarjeetMohanty/Streamlit-Hackathon) | Powered by Streamlit")

if __name__ == "__main__":
    main()



