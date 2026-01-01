# DevOps RAG Pipeline

A specialized Retrieval-Augmented Generation (RAG) pipeline designed to ingest, classify, and chunk DevOps infrastructure code (Dockerfiles, GitHub Actions, Terraform) for high-quality LLM retrieval.

## 🚀 Features

-   **Strict File Classification**: Automatically tags files with `authority` (Critical/High), `execution_risk`, `environment`, and `service`.
-   **Smart Chunking**:
    -   **Dockerfiles**: Chunks by instruction block types (Build vs Runtime stages).
    -   **GitHub Actions**: Chunks by individual jobs locally within the workflow context.
    -   **Terraform**: Chunks by resources and modules, preserving provider context.
-   **Vector Storage**: Integrated with **ChromaDB** for local persistence and **OpenAI** for high-quality embeddings.

## 📂 Project Structure

```
rag_pipeline/
├── main.py                 # Entry point for ingestion & indexing
├── requirements.txt        # Python dependencies
├── src/
│   ├── classifier.py       # Rule-based metadata tagging
│   ├── vector_store.py     # ChromaDB wrapper with OpenAI embedding
│   └── chunkers/           # Specialized parsers
│       ├── docker.py
│       ├── github.py
│       └── terraform.py
└── rag_pipeline_output.json # Intermediate structured output (verify before indexing)
```

## 🛠️ Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r rag_pipeline/requirements.txt
    ```

2.  **Set Environment Variables**:
    You must provide an OpenAI API Key for embedding generation.
    ```bash
    export OPENAI_API_KEY=sk-your-key-here
    ```

## 🏃 Usage

### 1. Run Data Ingestion
This script will:
1.  Scan `rag_data_source/`.
2.  Classify and chunk all files.
3.  Save structured chunks to `rag_pipeline_output.json`.
4.  Generate embeddings and index them into `chroma_db/`.

```bash
python3 rag_pipeline/main.py
```

### 2. Verify / Query
Run the sample query script to test retrieval:

```bash
python3 rag_pipeline/query.py "How do we build the order service?"
```

## 🧠 Design Principles (Phase 3)

1.  **Authority Matters**: Infrastructure as Code (Terraform) trumps Documentation (README). The classifier assigns `authority: critical` to Terraform files.
2.  **Context Preservation**: Chunks are not arbitrary text splits. They are semantic units (e.g., a "Build Job" or an "AWS EKS Cluster resource").
3.  **Risk Awareness**: Files are tagged with `execution_risk` to help the LLM decide if it's safe to execute code found in them.
