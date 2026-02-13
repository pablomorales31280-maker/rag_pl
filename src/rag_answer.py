import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Generator:
    def __init__(self, model_name: str, max_new_tokens: int):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()

        self.max_new_tokens = max_new_tokens

    def _extractive_fallback(self, question: str, contexts: list[str]) -> str:
        """
        Fallback 100% basé sur le contexte : on renvoie les phrases les plus pertinentes.
        Ça garantit une "réponse" même si le modèle LLM est capricieux.
        """
        q_words = set(re.findall(r"\w+", question.lower()))
        scored = []
        for ctx in contexts:
            sents = re.split(r"(?<=[\.\!\?])\s+", ctx.strip())
            for s in sents:
                w = set(re.findall(r"\w+", s.lower()))
                score = len(q_words & w)
                if score > 0 and len(s) > 30:
                    scored.append((score, s.strip()))

        scored.sort(key=lambda x: x[0], reverse=True)
        if not scored:
            return "Je ne sais pas à partir des documents fournis."

        top = [s for _, s in scored[:5]]
        return "Éléments trouvés dans la documentation :\n- " + "\n- ".join(top)

    @torch.no_grad()
    def answer(self, question: str, contexts: list[str]) -> str:
        if not contexts:
            return "Je ne sais pas à partir des documents fournis."

        # limite le contexte (évite prompt trop long)
        contexts = [c.strip()[:700] for c in contexts if c.strip()]
        contexts = contexts[:3]
        context_block = "\n\n---\n\n".join(contexts)

        # Prompt qui force une réponse à partir du contexte (sans proposer "je ne sais pas")
        prompt = (
            "Tu réponds en français.\n"
            "À partir du CONTEXTE uniquement, rédige une procédure en étapes numérotées.\n"
            "N'invente rien : reformule uniquement ce qui est dans le contexte.\n\n"
            f"QUESTION: {question}\n\n"
            f"CONTEXTE:\n{context_block}\n\n"
            "PROCÉDURE (étapes numérotées):"
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            min_new_tokens=60,
            num_beams=4,
            do_sample=False,
            early_stopping=True,
        )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Si le modèle renvoie vide ou renvoie "je ne sais pas", fallback extractif
        if (not text) or ("je ne sais pas" in text.lower()):
            return self._extractive_fallback(question, contexts)

        return text
