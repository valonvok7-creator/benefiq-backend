# llm_client.py — Bloc imports + client Groq

import os
from groq import Groq

# Chargement de la clé API Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialisation du client Groq
client = Groq(api_key=GROQ_API_KEY)

# ---------------------------------------------------------
# PROMPT MAÎTRE BENEFIQ IA — VERSION STRICTE ANTI-HALLUCINATIONS (OPTIMISÉE)
# ---------------------------------------------------------
def build_benefiq_prompt(context: str, question: str, mode: str) -> str:
    """
    Prompt maître BenefiQ IA — Version ULTRA STRICTE anti-hallucinations.
    """

    base_instructions = f"""
Tu es BenefiQ IA, assistant AFA suisse.

RÈGLES ULTRA STRICTES :
- Tu réponds UNIQUEMENT à partir du CONTEXTE ci-dessous.
- Tu n'utilises AUCUNE connaissance externe.
- Tu NE COMPLÈTES PAS les acronymes si leur signification n’est pas dans le contexte.
- Tu NE CRÉES PAS de lois, sigles, définitions, chiffres ou règles absents du contexte.
- Tu ne modifies pas le sens du contexte.
- Si une information n’est pas dans le contexte, tu réponds EXACTEMENT :
  "Cette information n’est pas présente dans le corpus AFA."

CONTEXTE :
{context}

QUESTION :
{question}

MODE :
{mode}
"""

    # ---------------------------------------------------------
    # MODES PÉDAGOGIQUES — VERSION ULTRA COMPACTE
    # ---------------------------------------------------------

    if mode == "clair":
        mode_instructions = """
Réponds avec :
1) Résumé (1 phrase)
2) Schéma mental (3–6 lignes)
3) Explication simple
4) Checklist (4–6 points)
5) Piège AFA
6) Mini cas (2–4 lignes)
7) Mnémotechnique
8) Sources
"""
    elif mode == "terrain":
        mode_instructions = """
Réponds avec :
1) À retenir
2) Comment l’expliquer
3) Questions clients (2–3)
4) Réponses prêtes
5) Pièges terrain
6) Exemple réel
7) Phrase simple
8) Sources
"""
    elif mode == "expert":
        mode_instructions = """
Réponds avec :
1) Définition
2) Structure légale (si présente)
3) Analyse AFA
4) Cas expert
5) Points de contrôle
6) Pièges examen
7) Sources
"""
    else:
        mode_instructions = """
Mode inconnu. Réponds de manière structurée en respectant STRICTEMENT le contexte.
"""


    # ---------------------------------------------------------
    # ASSEMBLAGE FINAL
    # ---------------------------------------------------------

    final_prompt = f"""{base_instructions}

{mode_instructions}

RAPPEL FINAL :
- Aucune connaissance externe.
- Aucune invention.
- Aucune complétion d’acronyme.
- Si l’information n’est pas dans le contexte :
  "Cette information n’est pas présente dans le corpus AFA."
"""

    return final_prompt

# ---------------------------------------------------------
# FONCTION PRINCIPALE : ABSTRACTION LLM
# ---------------------------------------------------------
def llm_completion(context: str, question: str, mode: str = "clair", max_tokens: int = 800) -> str:
    """
    Fonction d'abstraction LLM — version ULTRA STRICTE et optimisée Groq.
    Toute l’app passe par ici.
    """

    prompt = build_benefiq_prompt(context=context, question=question, mode=mode)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es BenefiQ IA, assistant AFA suisse. "
                        "Tu dois répondre UNIQUEMENT à partir du contexte fourni. "
                        "Tu n'utilises AUCUNE connaissance externe. "
                        "Tu ne complètes PAS les acronymes. "
                        "Tu n'inventes PAS de lois, sigles, définitions ou chiffres. "
                        "Si une information n'est pas dans le contexte, tu réponds EXACTEMENT : "
                        "\"Cette information n’est pas présente dans le corpus AFA.\""
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.0,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Erreur LLM : {str(e)}"

