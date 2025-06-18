import sys
from psycopg2 import sql
sys.path.insert(1, r"src")

import DataImporter as DI
from PyUtils import ColNames, TableNames, DBNames, DBSecrets, AreYouSureError

########
# MAIN #
########
Secrets = DI.DBSecrets.load()
Database = DI.DBNames.Toy.value
importer = DI.Importer(Secrets, database = Database)

'''print("===== STARTING TO IMPORT DATA ========")
importer.importData(r"data/Toy Dataset")  # path to your data folder
print("========== IMPORT COMPLETE ===========")'''

query = sql.SQL("""SELECT {uid}, {uname} FROM {table} WHERE ({uname} = %s)""").format(
    uid=sql.Identifier(DI.ColNames.UserId.value),
    uname=sql.Identifier("username"),
    table=sql.Identifier(DI.TableNames.User.value)
)

vars = ("Jane Doe",)

conn, cursor, err = importer.executeSQL(query, closeConn = False)

if (err is None):
    print(cursor.fetchone())
    conn.close()
else:
    conn.close()
    raise err


 