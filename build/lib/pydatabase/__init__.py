from pydatabase.env.dbenvironment import DBEnvironment
from pydatabase.table.tableobjectnoid import TableObjectNoID
from pydatabase.table.sqloperator import SQLOperator
def init(env):
	print("Initializing all")
	DBEnvironment.init()
	TableObjectNoID.setDatabase(DBEnvironment.getEnv(env))
	SQLOperator.init()