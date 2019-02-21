from pydatabase.common import Common
class SQLOperator(Common):
    EQUAL = '=='
    LESS_THAN = '<'
    LESS_THAN_OR_EQUAL = '<='
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='
    IN = 'in'
    NOT_IN = 'not in'
    OR = ''
    NOT_EQUAL = '!='
    ARRAY_CONTAINS = '@>'
    @classmethod
    def init(cls):
        cls.equalOperator = SQLOperator(cls.EQUAL)
        cls.lessThanOperator = SQLOperator(cls.LESS_THAN)
        cls.lessThanOrEqualOperator = SQLOperator(cls.LESS_THAN_OR_EQUAL)
        cls.greaterThanOperator = SQLOperator(cls.GREATER_THAN)
        cls.greaterThanOrEqualOperator = SQLOperator(cls.GREATER_THAN_OR_EQUAL)
        cls.inOperator = SQLOperator(cls.IN)
        cls.notInOperator = SQLOperator(cls.NOT_IN)
        cls.notEqual = SQLOperator(cls.NOT_EQUAL)
        cls.arreyContainsOperator = SQLOperator(cls.ARRAY_CONTAINS)

    def __init__(self,op,field=None,value=None):
        self.operator = op
        self.field = field
        self.value = value
    def comparisonExpression(self):
        if self.operator==SQLOperator.EQUAL:
            return (self.field==self.value)
        if self.operator==SQLOperator.LESS_THAN:
            return (self.field<self.value)
        if self.operator==SQLOperator.LESS_THAN_OR_EQUAL:
            return (self.field<=self.value)
        if self.operator==SQLOperator.GREATER_THAN:
            return (self.field>self.value)
        if self.operator==SQLOperator.GREATER_THAN_OR_EQUAL:
            return (self.field>=self.value)
        if self.operator==SQLOperator.IN:
            return (self.field.in_(self.value))
        if self.operator==SQLOperator.NOT_IN:
            return (~self.field.in_(self.value))
        if self.operator==SQLOperator.NOT_EQUAL:
            return (self.field!=self.value)
        if self.operator==SQLOperator.ARRAY_CONTAINS:
            return (self.field.any(self.value))
        raise ValueError("Invalid operator")
    def filter(self,query):
        return query.filter(self.comparisonExpression())
