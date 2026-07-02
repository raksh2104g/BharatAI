"""
========================================
Project : BharatAI
Module  : Chunk Service
Purpose : Split Long Text into Chunks
========================================
"""

from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 800
) -> List[str]:

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start = end

    return chunks