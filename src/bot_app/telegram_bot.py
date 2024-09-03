import nest_asyncio

nest_asyncio.apply()

import config
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from telegram import InputFile, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from google_sheets import get_sheet_names, get_data_from_sheet

# Определение глобального sheet_id
sheet_id = "1w5MAeMSZZJ6_3_s2res3hJPcw2NJxNIaFV4lV0j7ePI"


def create_chart(info_type, df):
    # Очищаем данные
    df.columns = df.columns.str.strip()
    df['Месяц'] = df['Месяц'].str.strip()
    df[info_type] = df[info_type].astype(str).str.strip()

    # Проверяем наличие столбца с очищенным именем
    info_type_clean = info_type.strip()
    if info_type_clean not in df.columns:
        print(f"Error: Info type '{info_type_clean}' not found in data.")
        return BytesIO()

    # Создаем график для всех месяцев
    plt.figure(figsize=(10, 6))
    plt.bar(df['Месяц'], df[info_type_clean].astype(float), color='blue')
    plt.xlabel('Month')
    plt.ylabel(info_type_clean)
    plt.title(f'{info_type_clean} for All Months')

    # Сохраняем график в буфер и возвращаем его
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf



async def start(update: Update, context: CallbackContext) -> None:
    companies = get_sheet_names(sheet_id)
    keyboard = [[InlineKeyboardButton(company, callback_data=f'company_{company}')] for company in companies]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите компанию:', reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    company = query.data.split('_')[1]

    # Сохраняем выбранную компанию
    context.user_data['company'] = company

    # Получаем данные для выбранной компании
    sheet_names = [company]
    data = get_data_from_sheet(sheet_id, sheet_names)
    df = pd.DataFrame(data)

    # Определяем доступные типы информации
    info_types = [col for col in df.columns if col != 'Месяц']

    keyboard = [[InlineKeyboardButton(info, callback_data=f'{company}:{info}')] for info in info_types]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(f'Выберите тип информации для {company}:', reply_markup=reply_markup)


async def info_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    company, info_type = data.split(':', 1)

    print(f"Received company: {company}")
    print(f"Received info_type: {info_type}")

    if company and info_type:
        try:
            sheet_names = [company]
            data = get_data_from_sheet(sheet_id, sheet_names)
            df = pd.DataFrame(data)

            # Удаление пробелов, табуляций и других лишних символов
            df.columns = df.columns.str.strip().str.replace(r'[\t\n\r]+', '', regex=True)
            df = df.applymap(lambda x: x.strip().replace('\t', '') if isinstance(x, str) else x)

            print("Data available in DataFrame:")
            print(df.head())

            if not df.empty and 'Месяц' in df.columns:
                # Убираем пробелы и табуляции в 'info_type' для точного соответствия столбцам
                info_type_cleaned = info_type.strip().replace('\t', '')

                if info_type_cleaned in df.columns:
                    chart_buf = create_chart(info_type_cleaned, df)

                    if chart_buf.getvalue():
                        await query.message.reply_photo(photo=InputFile(chart_buf, filename='chart.png'))
                    else:
                        await query.message.reply_text('Ошибка при создании графика. Попробуйте снова.')
                else:
                    await query.message.reply_text(f'Тип данных "{info_type}" не найден в таблице.')
            else:
                await query.message.reply_text('Данные для выбранной компании пусты или некорректны.')
        except Exception as e:
            print(f"An error occurred: {e}")
            await query.message.reply_text('Произошла ошибка при обработке данных. Попробуйте снова.')
    else:
        await query.message.reply_text('Неверный выбор. Пожалуйста, начните снова.')


async def main() -> None:
    application = Application.builder().token(config.TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern=r'^company_.*$'))
    application.add_handler(CallbackQueryHandler(info_button, pattern=r'^[^:]+:[^:]+$'))

    await application.run_polling()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(main())
    else:
        loop.run_until_complete(main())



