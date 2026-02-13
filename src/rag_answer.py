from transformers import pipeline

class Generator:
    def __init__(self, model_name: str, max_new_tokens: int):
        self.pipe = pipeline(
            task="text2text-generation",
            model=model_name,
        )
        self.max_new_tokens = max_new_tokens

    def answer(self, question: str, contexts: list[str]) -> str:
        """
        Prompt simple:
        - On force la réponse à être basée sur le contexte.
        - On concatène les passages top-k.
        """
        context_block = "\n\n---\n\n".join(contexts)
        prompt = (
            "Tu es un assistant. Réponds uniquement à partir du CONTEXTE.\n"
            "Si le contexte ne suffit pas, dis: \"Je ne sais pas à partir des documents fournis.\".\n\n"
            f"QUESTION: {question}\n\n"
            f"CONTEXTE:\n{context_block}\n\n"
            "RÉPONSE:"
        )

        out = self.pipe(prompt, max_new_tokens=self.max_new_tokens)
        return out[0]["generated_text"].strip()