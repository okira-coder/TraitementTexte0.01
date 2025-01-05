from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
from fastapi.middleware.cors import CORSMiddleware



# Initialiser l'application FastAPI
app = FastAPI()

# Ajout de CORSMiddleware à FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à toutes les origines d'accéder
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les en-têtes
)

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
        print("texte_propre: ",texte_propre)

        response_data = {"texte_nettoye": texte_propre}
        return response_data 
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
