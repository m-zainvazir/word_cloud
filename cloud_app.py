import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
import plotly.express as px
import base64
from io import BytesIO

# Functions for file reading
def read_txt(file):
    return file.getvalue().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in pdf.pages])


# Function to filter out stopwords
def filter_stopwords(text, 
                     additional_stopwords=[]
                     ):
    words = text.split()
    all_stopwords = STOPWORDS.union(set(additional_stopwords))
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    return " ".join(filtered_words)

# Function to create download link for plot
def get_image_download_link(buffered, format_):
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/{format_};base64,{image_base64}" download="wordcloud.{format_}">Download Plot as {format_}</a>'

# Function to generate a download link for a DataFrame
def get_table_download_link(df, filename, file_label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'

# Streamlit code
#st.title("Word Cloud Generator")
st.markdown("""
    <p style="font-size:46px; font-weight:bold; display:inline;">Word Cloud Generator  </p>
    <p style="font-size:16px; display:inline; color:gray;">   ~By Muhammad Zain Vazir.</p>
    """, unsafe_allow_html=True)
st.subheader("📁 Upload a pdf, docx or text file to generate a word cloud")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
#st.set_option('deprecation.showPyplotGlobalUse', False)

# add author name and info
st.markdown("---")
st.markdown("Created by: [Muhammad Zain Vazir](https://www.linkedin.com/in/muhammad-zain-vazir)")
st.markdown("GitHub![GitHub](https://img.icons8.com/ios-glyphs/30/000000/github.png)[m-zainvazir](https://github.com/m-zainvazir)")
st.markdown("LinkedIn![LinkedIn](https://img.icons8.com/ios-glyphs/30/000000/linkedin.png)[m-zainvazir](https://www.linkedin.com/in/m-zainvazir)")
st.markdown("Kaggle![Kaggle](https://img.icons8.com/?size=30&id=1iP83OYM1FL-&format=png&color=000000)[mzainvazir](https://www.kaggle.com/mzainvazir)")
st.markdown("Contact![Email](https://img.icons8.com/ios-glyphs/30/000000/email.png)[Email](mailto:zainvazir1@gmail.com)")
st.markdown("---")


if uploaded_file:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)

    # Check the file type and read the file
    if uploaded_file.type == "text/plain":
        text = read_txt(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    else:
        st.error("File type not supported. Please upload a txt, pdf or docx file.")
        st.stop()

    # Generate word count table
    words = text.split()
    word_count = pd.DataFrame({'Word': words}).groupby('Word').size().reset_index(name='Count').sort_values('Count', ascending=False)

    # Add custom stopwords to the standard STOPWORDS set
    custom_stopwords = ["a",'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
    's', 't', 'can', 'will', 'just', 'don', 'should', 'now']



    # Sidebar: Checkbox and Multiselect box for stopwords
    use_standard_stopwords = st.sidebar.checkbox("Use standard stopwords?", True)
    top_words = word_count['Word'].head(50).tolist()
    additional_stopwords = st.sidebar.multiselect("Additional stopwords:", sorted(top_words))

    # Determine stopwords based on the checkbox
    if use_standard_stopwords:
        all_stopwords = STOPWORDS.union(set(custom_stopwords)).union(set(additional_stopwords))
        filtered_text = filter_stopwords(text, all_stopwords)  # Exclude custom stopwords
    else:
        all_stopwords = set(additional_stopwords) # Do not include custom stopwords
        filtered_text = filter_stopwords(text, all_stopwords)  # Exclude only selected additional stopwords


    if text:
        # Word Cloud dimensions
        width = st.sidebar.slider("Select Word Cloud Width", 400, 2000, 1200, 50)
        height = st.sidebar.slider("Select Word Cloud Height", 200, 2000, 800, 50)

        # Generate wordcloud
        st.subheader("Generated Word Cloud")
        fig, ax = plt.subplots(figsize=(width/100, height/100))  # Convert pixels to inches for figsize
        wordcloud_img = WordCloud(width=width, height=height, background_color='white', max_words=200, contour_width=3, contour_color='steelblue', stopwords=all_stopwords).generate(text)
        ax.imshow(wordcloud_img, interpolation='bilinear')
        ax.axis('off')

        #all_stopwords = STOPWORDS.union(custom_stopwords)  # Combine sets
        #wordcloud = WordCloud(stopwords=all_stopwords).generate(text)

        # Save plot functionality
        format_ = st.selectbox("Select file format to save the plot", ["png", "jpeg", "svg", "pdf"])
        resolution = st.slider("Select Resolution", 100, 500, 300, 50)
      
    st.pyplot(fig)
    if st.button(f"Save as {format_}"):
        buffered = BytesIO()
        plt.savefig(buffered, format=format_, dpi=resolution)
        st.markdown(get_image_download_link(buffered, format_), unsafe_allow_html=True)
        

    # Second Word Count Table (Excluding Custom Stopwords)
    if use_standard_stopwords or additional_stopwords:
        st.subheader("Word Count Table (Excluding Stopwords)")
        all_stopwords = set(custom_stopwords).union(set(additional_stopwords))
        filtered_text = filter_stopwords(text, all_stopwords)
        words_filtered = filtered_text.split()
        word_count_excl_stopwords = pd.DataFrame({'Word': words_filtered}).groupby('Word').size().reset_index(name='Count').sort_values('Count', ascending=False)
        st.write(word_count_excl_stopwords)

        # Provide download link for table
        if st.button('Download Updated Word Count Table as CSV'):
            st.markdown(get_table_download_link(word_count_excl_stopwords, "word_count.csv", "Click Here to Download"), unsafe_allow_html=True)

    # First Word Count Table (Including Custom Stopwords)
    st.subheader("Word Count Table (All Words Included)")
    word_count_incl_stopwords = pd.DataFrame({'Word': words}).groupby('Word').size().reset_index(name='Count').sort_values('Count', ascending=False)
    st.write(word_count_incl_stopwords)

    if st.button('Download All Word Count Table as CSV'):
        st.markdown(get_table_download_link(word_count_incl_stopwords, "all_word_count.csv", "Click Here to Download"), unsafe_allow_html=True)

