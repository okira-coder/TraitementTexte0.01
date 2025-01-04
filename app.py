from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

# Initialiser l'application FastAPI
app = FastAPI()

# Modèle pour la requête POST
class TextRequest(BaseModel):
    texte: str

# Route pour nettoyer le texte
@app.post("/nettoyer-texte/")
async def nettoyer_texte(request: TextRequest):
    try:
        # Texte brut à nettoyer
        texte = request.texte

        # Supprimer les URL
        texte_sans_url = re.sub(r'http[s]?://\S+', '', texte)

        # Supprimer les balises HTML ou formatage (simples, si applicable)
        texte_sans_balises = re.sub(r'<[^>]*>', '', texte_sans_url)

        # Supprimer les caractères spéciaux inutiles (conserver lettres, chiffres, ponctuation de base)
        texte_sans_caracteres_speciaux = re.sub(r'[^\w\s.,!?\'éèêàçù-]', '', texte_sans_balises)

        # Supprimer les lignes vides
        texte_sans_lignes_vides = re.sub(r'\n\s*\n', '\n', texte_sans_caracteres_speciaux)

        # Supprimer les espaces en début et fin de ligne
        texte_propre = "\n".join(ligne.strip() for ligne in texte_sans_lignes_vides.splitlines())

        return {"texte_nettoye": texte_propre}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
