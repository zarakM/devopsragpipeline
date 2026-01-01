import os

class FileClassifier:
    """
    Classifies files based on their path and name to assign
    authority, risk, file type, and other metadata.
    """

    @staticmethod
    def classify(file_path: str):
        """
        Returns a dictionary of metadata for the given file path.
        """
        filename = os.path.basename(file_path)
        
        # Default metadata
        metadata = {
            "file_path": file_path,
            "file_type": "unknown",
            "authority": "low",
            "execution_risk": "low",
            "environment": "unknown",
            "service": "unknown"
        }

        # 1. Determine File Type & Authority
        if filename == "Dockerfile":
            metadata["file_type"] = "container_runtime"
            metadata["authority"] = "high"
            metadata["execution_risk"] = "critical"
        elif ".github/workflows" in file_path and (filename.endswith(".yml") or filename.endswith(".yaml")):
            metadata["file_type"] = "ci_pipeline"
            metadata["authority"] = "critical"
            metadata["execution_risk"] = "critical"
        elif filename.endswith(".tf"):
            metadata["file_type"] = "infra_iac"
            metadata["authority"] = "critical"
            metadata["execution_risk"] = "critical"
        elif filename.startswith("README"):
            metadata["file_type"] = "docs"
            metadata["authority"] = "medium"
            metadata["execution_risk"] = "none"

        # 2. Extract Service & Environment from path
        # Expected path format: rag_data_source/<service-name>/...
        parts = file_path.split(os.sep)
        if "rag_data_source" in parts:
            try:
                idx = parts.index("rag_data_source")
                if len(parts) > idx + 1:
                    metadata["service"] = parts[idx + 1]
            except ValueError:
                pass

        return metadata
