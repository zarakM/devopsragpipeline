import os
import json
import logging
from src.classifier import FileClassifier
from src.chunkers.docker import DockerfileChunker
from src.chunkers.github import GitHubActionsChunker
from src.chunkers.terraform import TerraformChunker

# Configuration
DATA_SOURCE = "rag_data_source"
OUTPUT_FILE = "rag_pipeline_output.json"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_file(file_path):
    """
    Classifies and chunks a single file.
    """
    # 1. Classify
    metadata = FileClassifier.classify(file_path)
    file_type = metadata["file_type"]
    
    # 2. Select Chunker
    chunker = None
    if file_type == "container_runtime":
        chunker = DockerfileChunker()
    elif file_type == "ci_pipeline":
        chunker = GitHubActionsChunker()
    elif file_type == "infra_iac":
        chunker = TerraformChunker()
    
    if not chunker:
        logging.warning(f"No chunker found for {file_path} (Type: {file_type})")
        return []

    # 3. Read Content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        logging.error(f"Failed to read {file_path}: {e}")
        return []

    # 4. Chunk
    try:
        chunks = chunker.chunk(file_path, content)
    except Exception as e:
        logging.error(f"Failed to chunk {file_path}: {e}")
        return []

    # 5. Enrich chunks with file-level metadata
    enriched_chunks = []
    for chunk in chunks:
        # Merge chunk-specific metadata with file-level metadata
        # Chunk metadata takes precedence if keys overlap, but usually they are distinct
        combined_metadata = metadata.copy()
        combined_metadata.update(chunk["metadata"])
        
        chunk["metadata"] = combined_metadata
        enriched_chunks.append(chunk)

    return enriched_chunks

def main():
    if not os.path.exists(DATA_SOURCE):
        logging.error(f"Data source {DATA_SOURCE} not found.")
        return

    all_chunks = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(DATA_SOURCE):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip hidden files or unrelated items if needed
            if file.startswith("."): # except .github is a dir, but files might be .something
                 # Actually .github/workflows/*.yml matches logic, but .gitignore etc might not
                 # logic handles unknown types gracefully
                 pass

            logging.info(f"Processing {file_path}...")
            file_chunks = process_file(file_path)
            all_chunks.extend(file_chunks)
            logging.info(f"  -> Generated {len(file_chunks)} chunks.")

    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
    
    logging.info(f"Pipeline complete. {len(all_chunks)} total chunks saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
