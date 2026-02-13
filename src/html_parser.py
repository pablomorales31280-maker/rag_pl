import re
from bs4 import BeautifulSoup
from readability import Document as ReadabilityDocument


def _collapse_whitespace(text: str) -> str:
    """
    Nettoie le texte final:
    - espaces multiples -> 1 espace
    - lignes vides multiples -> 1 bloc vide
    - strip
    """
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def _extract_title(soup: BeautifulSoup) -> str:
    """
    Titre:
    - priorité <h1> (souvent le vrai titre de l'article)
    - sinon <title> (titre de page navigateur)
    """
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)

    if soup.title and soup.title.get_text(strip=True):
        return soup.title.get_text(strip=True)

    return "Untitled"


def _extract_canonical_url(soup: BeautifulSoup) -> str | None:
    """
    Source URL:
    - récupère <link rel="canonical" href="..."> si présent
    """
    link = soup.find("link", attrs={"rel": "canonical"})
    if link and link.get("href"):
        return link["href"].strip()
    return None


def extract_main_text(html: str) -> str:
    """
    Extraction du texte principal:
    - Supprime le bruit (script/style/noscript/svg)
    - Si <article> existe -> texte de <article>
    - Sinon fallback readability-lxml (isole le contenu "lisible")
    - Normalise les espaces
    """
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    article = soup.find("article")
    if article:
        text = article.get_text("\n", strip=True)
        return _collapse_whitespace(text)

    readable = ReadabilityDocument(str(soup))
    cleaned_html = readable.summary(html_partial=True)
    cleaned_soup = BeautifulSoup(cleaned_html, "lxml")
    text = cleaned_soup.get_text("\n", strip=True)
    return _collapse_whitespace(text)


def parse_html_page(html: str, source_file: str) -> dict:
    """
    Interface stable pour le reste du pipeline.
    """
    soup = BeautifulSoup(html, "lxml")

    return {
        "title": _extract_title(soup),
        "source_url": _extract_canonical_url(soup),
        "source_file": source_file,
        "category": None,   # clé non utilisée, plus tard si j'ai le temps
        "main_text": extract_main_text(html),
    }
