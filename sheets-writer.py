import pickle
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
# ID du Google Sheet (à récupérer dans l'URL du sheet)
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]



# Correspondance catégorie → nom de l'onglet dans Google Sheets
CATEGORY_TO_SHEET = {
    "Problème technique": "Problème technique",
    "Demande administrative": "Demande administrative",
    "Problème d'accès": "Problème d'accès",
    "Support utilisateur": "Support utilisateur",
    "Bug": "Bug"
}

def get_sheets_service():
    """
    Se connecte à Google Sheets avec le token généré.
    """
    with open("token_sheets.pickle", "rb") as f:
        creds = pickle.load(f)
    
    service = build("sheets", "v4", credentials=creds)
    return service

def write_ticket_to_sheet(sujet, urgence, synthese, categorie):
    """
    Écrit un ticket dans le bon onglet du Google Sheet.
    """
    service = get_sheets_service()
    
    # Récupère le nom de l'onglet selon la catégorie
    sheet_name = CATEGORY_TO_SHEET.get(categorie, "Support utilisateur")
    
    # La ligne à écrire : [Sujet, Urgence, Synthèse]
    values = [[sujet, urgence, synthese]]
    
    body = {"values": values}
    
    # Écrit à la suite dans le bon onglet
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A:C",
        valueInputOption="RAW",
        body=body
    ).execute()
    
    print(f"✅ Ticket écrit dans l'onglet : {sheet_name}")

if __name__ == "__main__":
    # Test rapide
    write_ticket_to_sheet(
        sujet="Test sujet",
        urgence="Modérée",
        synthese="Ceci est un test",
        categorie="Bug"
    )