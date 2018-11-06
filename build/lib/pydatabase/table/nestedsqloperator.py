from pydatabase.table.sqloperator import SQLOperator
class NestedSQLOperator(SQLOperator):

    OR = '|'
    AND = '&'
    @classmethod
    def init(cls):
        cls.orOperator = NestedSQLOperator(cls.OR)
        cls.andOperator = NestedSQLOperator(cls.AND)

    def __init__(self,op,operators):
        self.operator = op
        self.operators = operators

    def comparisonExpression(self):
        if self.operator==NestedSQLOperator.OR:
            return ((self.operators[0].comparisonExpression())|(self.operators[1].comparisonExpression()))
        if self.operator==NestedSQLOperator.AND:
            return ((self.operators[0].comparisonExpression())&(self.operators[1].comparisonExpression()))
        raise ValueError("Invalid operator")

