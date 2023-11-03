import pandas as pd
from catboost import CatBoostClassifier

def predict_satisfaction(model, donnees_passager, valeurs_par_defaut=None):
    """
    Prédit la satisfaction du passager en utilisant un modèle CatBoost.

    Args:
        model (CatBoostClassifier): Le modèle CatBoost entraîné.
        donnees_passager (dict): Un dictionnaire contenant les données du passager pour faire les prédictions.
        valeurs_par_defaut (dict, optionnel): Un dictionnaire contenant les valeurs par défaut pour les données manquantes.
        # est ce que je le rajoute ou pas 

    Returns:
        int: Satisfaction prédite (0 pour non satisfait, 1 pour satisfait).
    """
    if valeurs_par_defaut is not None:
        for cle, valeur in valeurs_par_defaut.items():
            if cle not in donnees_passager:
                donnees_passager[cle] = valeur

    donnees_entree = pd.DataFrame(donnees_passager, index=[0])

    prediction = model.predict(donnees_entree)
    proba = model.predict_proba(donnees_entree)

    return prediction, proba