import streamlit as st
import vertexai
import os
import pdfplumber  # For better text extraction from PDF
import json
from google.cloud import storage
from vertexai.language_models import TextEmbeddingModel
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

# Load environment variables from .env file
load_dotenv()

# Set authentication credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Authenticate with Vertex AI
vertexai.init()

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Streamlit UI
st.title("PDF Text Embedding Generator and Question Answering")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

bucket_name = "your-gcs-bucket-name"
embed_file_path = "embeddings.json"
sentence_file_path = "sentences.json"

def extract_paragraphs_from_pdf(file):
    """Extracts paragraphs from an uploaded PDF file using pdfplumber."""
    paragraphs = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                paragraphs.extend(text.split("\n\n"))  # Split by paragraph
    return [para.strip() for para in paragraphs if para.strip()]

def generate_text_embeddings(paragraphs):
    """Generates embeddings using Vertex AI's text embedding model."""
    try:
        model = TextEmbeddingModel.from_pretrained("text-embedding-005")
        embeddings = model.get_embeddings(paragraphs)
        return [embedding.values for embedding in embeddings]
    except Exception as e:
        st.error(f"Error generating embeddings: {e}")
        return []

def upload_to_gcs(bucket_name, destination_blob_name, data):
    """Uploads a JSON file to Google Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(json.dumps(data), content_type="application/json")
        st.success(f"File uploaded to GCS: {destination_blob_name}")
    except Exception as e:
        st.error(f"Error uploading to GCS: {e}")

def get_most_similar_paragraph(query, paragraphs, embeddings):
    """Finds the most similar paragraph from the PDF to the user's query."""
    query_embedding = generate_text_embeddings([query])
    
    if query_embedding:
        # Flatten query embedding for comparison
        query_embedding = query_embedding[0]
        # Compute cosine similarity between the query and each paragraph
        similarities = cosine_similarity([query_embedding], embeddings)
        most_similar_index = np.argmax(similarities)
        return paragraphs[most_similar_index]
    return "Sorry, I couldn't find an answer."

if uploaded_file is not None:
    st.write("Processing PDF...")
    paragraphs = extract_paragraphs_from_pdf(uploaded_file)
    
    if paragraphs:
        st.write("Generating embeddings...")
        embeddings = generate_text_embeddings(paragraphs)
        
        if embeddings:
            # Save embeddings and sentences locally
            try:
                with open(embed_file_path, "w") as embed_file:
                    json.dump(embeddings, embed_file)
                with open(sentence_file_path, "w") as sentence_file:
                    json.dump(paragraphs, sentence_file)
                st.success("Embeddings and paragraphs saved locally.")
            except Exception as e:
                st.error(f"Error saving files locally: {e}")
                
            # Upload to GCS
            upload_to_gcs(bucket_name, "embeddings.json", embeddings)
            upload_to_gcs(bucket_name, "sentences.json", paragraphs)
            
            st.success("Embeddings and paragraphs uploaded to GCS.")
        else:
            st.error("No embeddings generated.")
    else:
        st.error("No paragraphs extracted from PDF.")
    
    # Ask the user for a question
    question = st.text_input("Ask a question from the PDF:")

    if question:
        st.write("Finding answer...")
        answer = get_most_similar_paragraph(question, paragraphs, embeddings)
        st.write("Answer:", answer)
