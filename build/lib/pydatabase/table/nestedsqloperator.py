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
        """
        if self.operator==NestedSQLOperator.OR:
            return ((self.operators[0].comparisonExpression())|(self.operators[1].comparisonExpression()))
        if self.operator==NestedSQLOperator.AND:
            return ((self.operators[0].comparisonExpression())&(self.operators[1].comparisonExpression()))
        """
        ce = (self.operators[0].comparisonExpression())
        for i in range(0,len(self.operators)):
            if i==0:
                continue
            if self.operator == NestedSQLOperator.OR:
                ce = ce | (self.operators[i].comparisonExpression())
            elif self.operator == NestedSQLOperator.AND:
                ce = ce & (self.operators[i].comparisonExpression())
        return (ce)
        raise ValueError("Invalid operator")

