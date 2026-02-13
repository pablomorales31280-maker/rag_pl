# Mini RAG (Retrieval-Augmented Generation) sur un corpus HTML (Help Center)

Ce projet met en place un mini pipeline RAG à partir d’un ZIP contenant des pages HTML exportées (format help center Intercom / Next.js).

Objectifs :
1) Parser et nettoyer les fichiers HTML du ZIP pour extraire uniquement le contenu utile.
2) Découper le texte en chunks.
3) Créer des embeddings, indexer avec FAISS.
4) Permettre de poser une question en CLI : récupérer les passages pertinents (top-k), générer une réponse basée sur le contexte, afficher les sources.

---

## Pré-requis

- Python 3.10+ recommandé
- Accès Internet au premier lancement (téléchargement des modèles HuggingFace)

---


## Installation

Créer un environnement virtuel et installer les dépendances : (avec conda pour ma part)
conda create -n rag_pl python=3.11
cd "path"
pip install -r requirements.txt

---


## Utilisation

Le ZIP est déjà dans data/raw
Parsing / nettoyage HTML : 

python -m scripts.build_corpus

Chunking + indexation

python -m scripts.build_index

Question / Réponse :

python -m scripts.ask --q "My question" --k 5


---

## Example

python -m scripts.build_corpus
python -m scripts.build_index
python -m scripts.ask --q "Comment reconnecter une banque ou resynchroniser des transactions ?" --k 5

=== PASSAGES RETROUVÉS (top-k) ===

[1] score=0.6880 | title=Reconnecter une banque ou resynchroniser des transactions
    source=https://help.pennylane.com/fr/articles/18615-reconnecter-une-banque-ou-resynchroniser-des-transactions
    excerpt=dernière synchronisation, forcer une nouvelle synchronisation ne change rien. Pour forcer la synchronisation d’un compte : Accédez à Paramètres entreprise > Connexions bancaires . Naviguez jusqu’au compte à synchroniser. Cliquez sur les points de suspension en bout de ligne (…). ...

[2] score=0.6834 | title=Reconnecter une banque ou resynchroniser des transactions
    source=https://help.pennylane.com/fr/articles/18615-reconnecter-une-banque-ou-resynchroniser-des-transactions
    excerpt=En théorie, la connexion entre Pennylane et votre banque reste active pendant 180 jours. En pratique, votre banque peut couper la connexion avant l’expiration de ce délai. Si votre connexion est coupée, vous pouvez la réparer en vous connectant à nouveau à votre banque depuis la ...

[3] score=0.6662 | title=Reconnecter une banque ou resynchroniser des transactions
    source=https://help.pennylane.com/fr/articles/18615-reconnecter-une-banque-ou-resynchroniser-des-transactions
    excerpt=iquez sur Récupérer des transactions en haut à droite. Sélectionnez le compte à resynchroniser partiellement. Renseignez la plage temporelle à interroger (31 jours max) puis cliquez sur Prévisualiser . Les transactions manquantes s’affichent alors, avec la mention Manquante . Les...

[4] score=0.6461 | title=Tout comprendre sur les connexions bancaires (API, EBICS, Agrégation)
    source=https://help.pennylane.com/fr/articles/18678-tout-comprendre-sur-les-connexions-bancaires-api-ebics-agregation
    excerpt=), synchronisation 3 fois par jour. Limites : déconnexions fréquentes, nécessité de se reconnecter régulièrement, possibles doublons si vous changez d’agrégateur. Nous ne connectons pas les banques de crypto-monnaies pour le moment. ✍️ Si la banque n'est pas accessible en EBICS, ...

[5] score=0.6210 | title=Paramétrer les comptes bancaires (Comptabilité)
    source=https://help.pennylane.com/fr/articles/18648-parametrer-les-comptes-bancaires-comptabilite
    excerpt=Seuls les cabinets comptables et les entreprises disposant d'un plan d'abonnement Comptabilité internalisée accéder aux fonctionnalités évoquées dans cet article. Associer un IBAN à un compte bancaire Vous vous situez au sein d'un dossier et souhaitez paramétrer les comptes banca...


=== RÉPONSE (basée sur le contexte) ===

Éléments trouvés dans la documentation :
- Lire l’article
Anticiper la déconnexion automatique des banques
Archiver les doublons
Archivez les transactions importées en double pour conserver une liste d’opérations propre et lisible.
- Si vous constatez un écart entre les transactions visibles du côté de votre banque et celles qui apparaissent sur Pennylane, vous pouvez lancer une nouvelle synchronisation pour récupérer les transactions laissées de côté lors d’une éventuelle coupure.
- iquez sur
Récupérer des transactions
en haut à droite.
- dernière synchronisation, forcer une nouvelle synchronisation ne change rien.
- Prochaines étapes
Éviter les déconnexions intempestives
Anticipez les déconnexions imposées par votre banque pour limiter les coupures.

=== SOURCES UTILISÉES ===

- https://help.pennylane.com/fr/articles/18615-reconnecter-une-banque-ou-resynchroniser-des-transactions
- https://help.pennylane.com/fr/articles/18678-tout-comprendre-sur-les-connexions-bancaires-api-ebics-agregation
- https://help.pennylane.com/fr/articles/18648-parametrer-les-comptes-bancaires-comptabilite