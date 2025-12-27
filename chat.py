from llm_client import llm_completion
from rag import retrieve_relevant_chunks, STOPWORDS, save_stopwords, _normalize

def ask_ai(question: str, mode: str = "clair") -> str:
    """
    Fonction centrale : RAG + LLM + auto-apprentissage.
    """

    # 1) Récupération du contexte via RAG
    context = retrieve_relevant_chunks(question)

    print("\n=== CONTEXTE RAG ===")
    print(context)
    print("=== FIN CONTEXTE ===\n")

    # 2) Appel du modèle
    answer = llm_completion(
        context=context,
        question=question,
        mode=mode
    )

    # 3) AUTO-APPRENTISSAGE : si le LLM dit "info absente" mais le RAG a renvoyé un chunk
    if "Cette information n’est pas présente dans le corpus AFA." in answer:
        if context.strip():  # chunk renvoyé → faux positif
            q_terms = _normalize(question).split()
            new_words = [t for t in q_terms if len(t) > 3]
            STOPWORDS.update(new_words)
            save_stopwords(STOPWORDS)

    return answer

