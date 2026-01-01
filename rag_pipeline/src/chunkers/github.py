from .base import BaseChunker
from typing import List, Dict, Any
import yaml

class GitHubActionsChunker(BaseChunker):
    def chunk(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        chunks = []
        try:
            workflow = yaml.safe_load(content)
        except yaml.YAMLError:
            # Fallback for invalid yaml or empty files
            return []

        if not workflow:
            return []

        name = workflow.get('name', 'unnamed-workflow')
        triggers = list(workflow.get('on', {}).keys()) if isinstance(workflow.get('on'), dict) else [workflow.get('on')] if workflow.get('on') else []
        
        jobs = workflow.get('jobs', {})
        
        for job_id, job_data in jobs.items():
            # Construct meaningful content for the chunk
            # We dump specific job data back to YAML to preserve structure but isolate context
            job_yaml = yaml.dump({job_id: job_data}, sort_keys=False)
            
            chunk = {
                "content": job_yaml,
                "metadata": {
                    "workflow_name": name,
                    "triggers": triggers,
                    "job_name": job_id,
                    "runs_on": job_data.get("runs-on", "unknown"),
                    "chunk_type": "ci_job"
                }
            }
            chunks.append(chunk)

        return chunks
