
# LLMOPS-VERTEX

This project demonstrates how to use Google **Vertex AI** to generate embeddings from a PDF and answer user questions based on the content of the uploaded PDF. The project uses **Streamlit** for the user interface, **pdfplumber** for extracting text from PDF files, and **Google Cloud Storage** for storing the embeddings and extracted paragraphs.

---

## Features:

- Upload a PDF file and extract text from it.
- Generate text embeddings using **Vertex AI**'s **TextEmbeddingModel**.
- Upload generated embeddings and extracted text to **Google Cloud Storage** (GCS).
- Ask questions from the extracted text and get the most relevant answers based on cosine similarity.

---

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.7 or later
- Google Cloud SDK (for authentication with Google services)
- **Streamlit**, **vertexai**, **pdfplumber**, **google-cloud-storage**, **sklearn**, and **dotenv** for environment variable management

Install dependencies using:

```bash
pip install -r requirements.txt
```

### Dependencies:

- **vertexai**: Used for working with Google Vertex AI's API.
- **streamlit**: For building the interactive web interface.
- **pdfplumber**: For extracting text from PDF files.
- **google-cloud-storage**: To upload embeddings and text data to GCS.
- **sklearn**: For calculating cosine similarity between the query and text embeddings.
- **dotenv**: To load environment variables for credentials securely.

---

## Setup

### 1. **Set Up Google Cloud Authentication**

- **Create a Google Cloud project** if you haven't already.
- Enable **Vertex AI** and **Cloud Storage** APIs.
- Create a **Service Account Key** in Google Cloud and download the JSON credentials file.
- Set up the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your credentials file.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-service-account-file.json"
```

For Windows, use:

```bash
set GOOGLE_APPLICATION_CREDENTIALS="path\to\your-service-account-file.json"
```

### 2. **Create a Google Cloud Storage Bucket**

- Create a bucket in **Google Cloud Storage** for storing your PDF content, embeddings, and paragraphs.
- Replace the `bucket_name` variable in the code with your actual bucket name.

---

## How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/paravsyal02/LLMOPS-VERTEX.git
cd LLMOPS-VERTEX
```

2. Run the Streamlit app:

```bash
streamlit run appwithpdfplumber.py
```

3. The app will start running locally on `http://localhost:8501`. Open this URL in your browser.

---

## Features Explained

### 1. **PDF Text Extraction**

Once a PDF file is uploaded via the Streamlit UI, the content is extracted using **pdfplumber**, and the text is split into paragraphs. The extracted text can then be used for generating embeddings and answering questions.

### 2. **Generating Text Embeddings**

- **Vertex AI**'s **TextEmbeddingModel** is used to generate text embeddings from the extracted paragraphs.
- These embeddings capture semantic meaning and allow the system to perform similarity-based question answering.

### 3. **Upload Embeddings and Text to GCS**

- After generating the embeddings, the embeddings and the extracted text are uploaded to **Google Cloud Storage** for persistence.
- The embeddings are stored in `embeddings.json`, and the extracted paragraphs are stored in `sentences.json`.

### 4. **Question Answering**

- The user can enter a question after uploading the PDF.
- The system generates an embedding for the question and calculates cosine similarity between the question's embedding and the PDF content embeddings.
- The most similar paragraph from the PDF is returned as the answer.

---


## Troubleshooting

- **Missing Google Cloud credentials**: Ensure the **`GOOGLE_APPLICATION_CREDENTIALS`** environment variable is set correctly.
- **No embeddings generated**: Double-check the `TextEmbeddingModel` initialization and ensure you're using the correct Vertex AI model (`text-embedding-005`).
- **No answer returned**: If the cosine similarity is low, the system might not find a good match. Ensure the uploaded PDF contains enough context for meaningful answers.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
