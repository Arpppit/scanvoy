import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
from crawler import start_crawler
import pandas as pd

results = pd.read_csv("output.csv")

# Streamlit UI
doms = []
business = set()
st.set_page_config(layout="wide")
st.title("Flights Scraper")
# url = st.text_input("Enter Website URL")
col_1, col_2, col_3, col_4, col_5, col_6, col_7 = st.columns(7)
trip_type = col_1.selectbox("Trip Type", ["One Way", "Round Trip"])
source = col_2.selectbox("Depart", ["Mumbai", "Banglore", "Delhi", "Kolkata"])
dest = col_3.selectbox("Arrival", ["Nagpur", "Chennai", "Indore", "Goa"])
date = col_4.date_input(label="Trip Date", format="DD-MM-YYYY")
if trip_type == "Round Trip":
    return_date = col_5.date_input(label="Return Date", format="DD-MM-YYYY")
pax = col_6.selectbox("Passengers", [str(i) for i in range(9)])
seat = col_7.selectbox("Class", ["Economy", "Premium Economy", "Bunesss"])

# Step 1: Scrape the Website
if st.button("Find Flights"):
    st.write("Scraping the website...")
    urls = start_crawler([source, dest])
    
    for url in list(urls):
        # Scrape the website
        # dom_content = scrape_website(url)
        # body_content, title = extract_body_content(dom_content)
        # cleaned_content = clean_body_content(body_content)
        # #st.write(title)
        # if title not in business and dom_content != "":
        #     doms.append(cleaned_content)
        #     # Store the DOM content in Streamlit session state
        #     st.session_state.dom_content = cleaned_content
        #     business.add(title)

            # Display the DOM content in an expandable text box
        business = url.split("www")[1].split('.')[1]
        with st.expander(f"Fetched data from {business}"):
            st.dataframe(results,hide_index=True)
            # dom_content = scrape_website(url)
            # body_content, title = extract_body_content(dom_content)
            # cleaned_content = clean_body_content(body_content)
            #st.text_area("DOM Content", "Data", height=300)
    # Store the DOM content in Streamlit session state

    # Display the DOM content in an expandable text box

print(len(doms))
# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    # parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        # if doms:
        st.write("Parsing the content...")
        for dom in doms:
            # Parse the content with Ollama
            dom_chunks = split_dom_content(dom)
            parsed_result = parse_with_ollama(dom_chunks, None)
            st.write(parsed_result)
