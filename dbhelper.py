#dbhelper.py
from sqlite3 import connect, Row

database:str = 'studentinfo.db'

def postprocess(sql:str) -> bool:
	db:object = connect(database)
	cursor:object = db.cursor()
	try:
		cursor.execute(sql)
		db.commit()
		ok = True
	except:
		pass
	finally:
		cursor.close()
	return True if cursor.rowcount > 0 else False

def getprocess(sql:str) -> list:
	db:object = connect(database)
	cursor:object = db.cursor()
	cursor.row_factory = Row
	cursor.execute(sql)
	data:list = cursor.fetchall()
	cursor.close()
	return data

def getall_records(table:str) -> list:
	sql:str = f'SELECT * FROM `{table}`'
	return getprocess(sql)

def getone_record(table:str, **kwargs) -> bool:
	keys:list = list(kwargs.keys())
	values:list = list(kwargs.values())
	sql:str = f"SELECT * FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
	return getprocess(sql)

def add_record(table:str, **kwargs) -> bool:
	keys:list = list(kwargs.keys())
	values:list = list(kwargs.values())
	fields:str = "`, `".join(keys)
	data:str = "','".join(values) 
	sql:str = f"INSERT INTO `{table}` (`{fields}`) VALUES('{data}')"
	return postprocess(sql)

def update_record(table:str, **kwargs) -> bool:
	keys:list = list(kwargs.keys())
	values:list = list(kwargs.values())
	fields:list = []
	for i in range(1,len(keys)):
		fields.append(f"'{keys[i]}' = '{values[i]}'")
	field:str = ','.join(fields)
	sql:str = f"UPDATE `{table}` SET {field} WHERE `{keys[0]}` = '{values[0]}'"
	return postprocess(sql)

def delete_record(table:str, **kwargs) -> list:
	keys:list = list(kwargs.keys())
	values:list = list(kwargs.values())
	sql:str = f"DELETE FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
	return postprocess(sql)

