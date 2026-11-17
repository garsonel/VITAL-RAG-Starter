
"""Student exercise: implement retrieval over the fictional clinic policies."""

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = Path(__file__).parent / "knowledge_base"


def load_documents(directory=DOCS):
    """Return list of (filename, text) for *.txt files."""
    documents = []

    for file in sorted(Path(directory).glob("*.txt")):
        text = file.read_text(encoding="utf-8")
        documents.append((file.name, text))

    return documents


def retrieve(question: str, k: int = 2, documents=None):
    """Return top-k (filename, text, score) matches using TF-IDF."""
    if documents is None:
        documents = load_documents()

    if not documents or k <= 0:
        return []

    texts = [text for filename, text in documents]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(texts)
    query_vector = vectorizer.transform([question])

    scores = cosine_similarity(query_vector, matrix).flatten()

    results = []
    for i, (filename, text) in enumerate(documents):
        if scores[i] > 0:
            results.append((filename, text, float(scores[i])))

    results.sort(key=lambda item: (-item[2], item[0]))

    return results[:k]


def build_context(results):
    """Format hits with [Source: filename] headers."""
    context = []

    for filename, text, score in results:
        context.append(f"[Source: {filename}]\n{text}")

    return "\n\n".join(context)
