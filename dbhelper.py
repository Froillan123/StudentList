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

def getone_record(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    sql = f"SELECT * FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
    result = getprocess(sql)
    return result

def add_record(table, **kwargs):
    db = connect('studentinfo.db')
    cursor = db.cursor()
    
    keys = ', '.join(kwargs.keys())
    values = ', '.join('?' for _ in kwargs.values())
    
    sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    
    try:
        cursor.execute(sql, tuple(kwargs.values()))
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding record: {e}")
        return False
    finally:
        cursor.close()
        db.close()


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

def userlogin(username: str, password: str) -> bool:
    sql = "SELECT * FROM users WHERE username = ? AND password = ?"
    db = connect('studentinfo.db')
    cursor = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql, (username, password))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return len(data) > 0