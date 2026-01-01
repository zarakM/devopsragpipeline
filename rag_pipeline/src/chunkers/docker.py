from .base import BaseChunker
from typing import List, Dict, Any
import re

class DockerfileChunker(BaseChunker):
    def chunk(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        chunks = []
        lines = content.splitlines()
        current_chunk = []
        current_instruction = None
        current_stage = "unknown"
        base_image = "unknown"

        # Regex to capture instructions like FROM, RUN, CMD, etc.
        instruction_pattern = re.compile(r'^\s*(FROM|RUN|CMD|ENTRYPOINT|COPY|ADD|ENV|ARG|width|LABEL|EXPOSE|USER|WORKDIR|VOLUME|STOPSIGNAL|ONBUILD|HEALTHCHECK|SHELL)\s+')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            match = instruction_pattern.match(line)
            if match:
                # If we have accumulated lines for a previous instruction block, save them
                if current_chunk:
                    chunks.append(self._create_chunk_obj(current_chunk, current_instruction, current_stage, base_image))
                    current_chunk = []

                # New instruction starts
                current_instruction = match.group(1)
                
                # Update stage info if it's a FROM instruction
                if current_instruction == 'FROM':
                    parts = line.split()
                    if len(parts) >= 2:
                        base_image = parts[1]
                        if 'AS' in parts:
                           current_stage = parts[parts.index('AS') + 1]
                        else:
                           current_stage = "final" # Assumption for simple dockerfiles
                
            current_chunk.append(line)
        
        # Add the last chunk
        if current_chunk:
             chunks.append(self._create_chunk_obj(current_chunk, current_instruction, current_stage, base_image))

        return chunks

    def _create_chunk_obj(self, lines, instruction, stage, base_image):
        return {
            "content": "\n".join(lines),
            "metadata": {
                "instruction_type": instruction,
                "docker_stage": stage,
                "base_image": base_image
            }
        }
