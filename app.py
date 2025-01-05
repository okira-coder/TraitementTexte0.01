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
        texte = re.sub(r'http[s]?://\S+', '', texte)

        # Supprimer les balises HTML ou formatage (simples, si applicable)
        texte = re.sub(r'<[^>]*>', '', texte)

        # Supprimer les caractères spéciaux inutiles (conserver lettres, chiffres, ponctuation de base)
        texte = re.sub(r'[^\w\s.,!?\'éèêàçù-]', '', texte)

        # Supprimer les lignes vides
        texte = re.sub(r'\n\s*\n', '\n', texte)

        # Supprimer les espaces en début et fin de ligne
        texte = "\n".join(ligne.strip() for ligne in texte.splitlines())

        # Supprimer tout avant "To" s'il existe
        texte = re.sub(r'.*? To ', '', texte, flags=re.DOTALL)

        # Supprimer tout après "Cordialement" ou des mots similaires
        texte = re.sub(r'(Cordialement|Bien à vous|Sincèrement|Respectueusement).+', '', texte, flags=re.DOTALL)

        # Limiter à 1499 caractères
        texte = texte[:1499]

        # Retourner la réponse sous forme JSON
        response_data = {"texte_nettoye": texte}
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
