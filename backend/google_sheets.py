import json

import pygsheets
from app_init import get_settings
from database.models import models
from sqlalchemy import inspect
from string import ascii_uppercase
from app_init import engine
from sqlalchemy.orm import Session

ga = pygsheets.authorize(service_file="google_key.json")


#Таблицы которые не следует добавлять в Google Sheets
ignore_tablenames = [
    'admin',
    'admin_login_session',
    'task_make',
    "avatar"
]
config = get_settings()
table = ga.open_by_url(config['google_sheets_table_link'])


def get_columns(model):
    """Получение ключей таблицы в SQL"""
    result_columns = []
    columns = list(inspect(model).attrs)
    ignore_columns = []
    for column in columns:
        if not column.key in ignore_columns:
            result_columns.append(column.key)
    return result_columns


def create_not_exists_sheets(table):
    """Создание необходимых таблиц в Google Sheets"""
    worksheets = table.worksheets()
    worksheets_names = []
    for worksheet in worksheets:
        worksheets_names.append(worksheet.title)
    for model in models:
        if not model.__tablename__ in ignore_tablenames:
            if not model.__tablename__.capitalize() in worksheets_names:
                columns = get_columns(model)
                try:
                    sheet = table.add_worksheet(model.__tablename__.capitalize(), rows=1, cols=len(columns) + 1)
                    worksheets_names.append(sheet.title)
                except:
                    pass
                sheet.update_values(f'A1:{ascii_uppercase[len(columns)]}1', [[column for column in columns] + [
                    "Удалить"
                ]])


def get_current_model(tablename: str):
    """Получение названия модели в SQL"""
    for model in models:
        if model.__tablename__ == tablename:
            return model


def delete_from_table(table, tablename: str):
    """Удаление необходимых строк в SQL с Google Sheets"""
    sheet = table.worksheet_by_title(tablename.capitalize())
    head_row = sheet.get_row(1)
    delete_id = len(head_row)
    ids_col = sheet.get_col(1)
    ids_col.pop(0)
    deleted_col = sheet.get_col(delete_id)
    deleted_col.pop(0)
    deleted_ids = []
    for i in range(len(deleted_col)):
        if deleted_col[i]:
            if ids_col[i]:
                try:
                    deleted_ids.append(int(ids_col[i]))
                except:
                    pass
        model = get_current_model(tablename)
        connection = engine()
        with Session(connection) as session:
            session.query(model).filter(model.id.in_(deleted_ids)).delete()
            session.commit()
        connection.dispose()


def add_to_table(table, tablename: str):
    """Добавление новых строк в SQL из Google Sheets"""
    sheet = table.worksheet_by_title(tablename.capitalize())
    ids_col = sheet.get_col(1)
    ids_col.pop(0)
    rows_to_add = []
    for i in range(len(ids_col)):
        if ids_col[i] == "":
            rows_to_add.append(i + 2)
    head_row = sheet.get_row(1)
    head_row.pop(0)
    head_row.pop(-1)
    connection = engine()
    model = get_current_model(tablename)
    values_to_get = []

    for row_to_add in rows_to_add:
        values_to_get.append(f"B{row_to_add}:{ascii_uppercase[len(head_row)]}{row_to_add}")
    values = sheet.get_values_batch(values_to_get)
    with Session(connection) as session:
        for i in range(len(rows_to_add)):
            row_data = values[i][0]
            model_data = {}
            can_create = True
            for j in range(len(head_row)):
                if not row_data[j]:
                    can_create = False
                    break
                if row_data[j] == "ИСТИНА" or row_data[j] == "TRUE":
                    model_data.update({
                        head_row[j]: True
                    })
                elif row_data[j] == "ЛОЖЬ" or row_data[j] == "FALSE":
                    model_data.update({
                        head_row[j]: False
                    })
                else:
                    model_data.update({
                        head_row[j]: row_data[j]
                    })
            if can_create:
                model_data = model(**model_data)
                session.add(model_data)
        session.commit()
    connection.dispose()


def update_from_table(table, tablename: str):
    """Обновление значений из Google Sheets в SQL"""
    sheet = table.worksheet_by_title(tablename.capitalize())
    values = sheet.get_all_records()
    model = get_current_model(tablename)
    connection = engine()
    dynamic_data = [
        "is_spam",
        "is_ban",
        "is_avatar_updated",
        "is_nickname_and_bio_updated",
        "is_activate",
        "is_active",
        "is_used",
        "client_hash"
    ]
    with Session(connection) as session:
        for value in values:
            try:
                value.pop("Удалить")
                keys = list(value.keys())
                for key in keys:
                    if value[key] == "ИСТИНА" or value[key] == "TRUE":
                        value.update({key: True})
                    elif value[key] == "ЛОЖЬ" or value[key] == "FALSE":
                        value.update({key: False})
                model_data = session.query(model).filter(model.id == value['id']).first()
                model_data = model_data.to_dict()
                for dynamic_key in dynamic_data:
                    if dynamic_key in value:
                        value.pop(dynamic_key)
                for key in model_data:
                    if not model_data[key] == value[key] and value[key]:
                        session.query(model).filter(model.id == value['id']).update(value)
                        break
            except:
                pass
        session.commit()
    connection.dispose()


def synchronize_table(table, tablename: str):
    """Синхронизация таблицы Google Sheets и SQL"""
    sheet = table.worksheet_by_title(tablename.capitalize())
    connection = engine()
    model = get_current_model(tablename)
    columns = get_columns(model)
    with Session(connection) as session:
        count_model = session.query(model).count()
        sheet.resize(rows=int(count_model + 1), cols=int(len(columns) + 1))
        if sheet.rows < count_model:
            sheet.add_rows(count_model - sheet.rows + 1)
        sql_models = session.query(model).all()
        models = []
        for sql_model in sql_models:
            models.append(sql_model.to_array() + [""])
        if models:
            json.dumps(models)
            sheet.update_values(f'A2:{ascii_uppercase[int(len(columns))]}{int(len(models) + 1)}', models, parse=False)
    connection.dispose()
    sheet.adjust_column_width(1, len(columns))