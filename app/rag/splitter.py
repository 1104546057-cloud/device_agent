def splitter_text(
        text: str,
        chunk_size: int = 100,
        overlap: int = 20,
        source: str = ""
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于0")

    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap 必须大于等于0且小于 chunk_size")

    chunks =[]
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = {
            "chunk_id": len(chunks),
            "text": text[start:end],
            "source": source,
            "start_index": start,
            "end_index": end
        }

        chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks

