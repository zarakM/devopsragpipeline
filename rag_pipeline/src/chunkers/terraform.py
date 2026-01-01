from .base import BaseChunker
from typing import List, Dict, Any
import hcl2

class TerraformChunker(BaseChunker):
    def chunk(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        chunks = []
        try:
            # HCL2 library parses into a dict
            data = hcl2.loads(content)
        except Exception:
            return []

        # Iterate through common top-level blocks
        block_types = ['resource', 'module', 'variable', 'output', 'data', 'provider']

        for block_type in block_types:
            if block_type in data:
                items = data[block_type]
                for item in items:
                    # HCL2 parsing structure varies slightly
                    # resource/data Items are dicts like { "type": { "name": { config... } } }
                    # module/variable Items are dicts like { "name": { config... } }
                    
                    for key, val in item.items():
                        chunk_metadata = {
                            "block_type": block_type,
                            "chunk_type": "terraform_block"
                        }
                        
                        chunk_content = ""
                        # Reconstruct a pseudo-HCL string for the chunk content
                        # This is a simplification; for production, we might want exact original text slicing
                        # But transforming back to string is good enough for semantic embedding
                        
                        if block_type in ['resource', 'data']:
                             # Key is the type (e.g. aws_s3_bucket), val is dict of names
                             resource_type = key
                             for name, config in val.items():
                                 chunk_metadata["resource_type"] = resource_type
                                 chunk_metadata["resource_name"] = name
                                 chunk_content = f'{block_type} "{resource_type}" "{name}" {{ ... }}' 
                                 # We store the config dict as string representation for now 
                                 # or use a dumper if available. standard json dump is safer.
                                 import json
                                 chunk_content = f'{block_type} "{resource_type}" "{name}" ' + json.dumps(config, indent=2)
                                 
                                 chunks.append({
                                     "content": chunk_content,
                                     "metadata": chunk_metadata
                                 })
                        else:
                             # module, variable, output
                             # Key is the name
                             name = key
                             config = val
                             chunk_metadata["name"] = name
                             
                             import json
                             chunk_content = f'{block_type} "{name}" ' + json.dumps(config, indent=2)

                             chunks.append({
                                 "content": chunk_content,
                                 "metadata": chunk_metadata
                             })

        return chunks
