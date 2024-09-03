import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройки доступа к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/workbench-1723986981578-5087fa0fe44d.json", scope)
client = gspread.authorize(creds)


def get_sheet_names(sheet_id):
    """
    Возвращает список названий всех листов в Google Sheets по заданному ID.
    """
    try:
        sheet = client.open_by_key(sheet_id)
        return [worksheet.title for worksheet in sheet.worksheets()]
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{sheet_id}' not found.")
        return []


def get_data_from_sheet(sheet_id, sheet_names):
    """
    Получает данные из указанных листов Google Sheets.
    """
    all_data = []

    # Проверка наличия листов для обработки
    if not sheet_names:
        print("No sheet names provided.")
        return all_data

    for sheet_name in sheet_names:
        try:
            sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
            data = sheet.get_all_records()
            print(f"Data from {sheet_name}:")
            print(data)  # Выводим данные для проверки
            all_data.extend(data)  # Добавляем данные в общий список
        except gspread.exceptions.WorksheetNotFound:
            print(f"Error: Worksheet '{sheet_name}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return all_data



def clean_column_headers(df):
    # Удаление всех специальных символов и пробелов из заголовков столбцов
    df.columns = [re.sub(r'[^\w\s]', '', col).strip() for col in df.columns]
    return df


