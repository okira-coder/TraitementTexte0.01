from flask import Flask, request, jsonify
import re

# Initialiser l'application Flask
app = Flask(__name__)

# Route pour nettoyer le texte
@app.route("/nettoyer-texte/", methods=["POST"])
def nettoyer_texte():
    try:
        # Récupérer les données JSON envoyées par le client
        data = request.get_json()

        # Vérifier si la clé 'texte' existe dans la requête
        if "texte" not in data:
            return jsonify({"error": "Le champ 'texte' est requis"}), 400
        
        # Texte brut à nettoyer
        texte = data["texte"]

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

        # Retourner la réponse sous forme JSON
        response_data = {"texte_nettoye": texte_propre}
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
