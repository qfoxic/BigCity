from mongoengine import Q
from pyparsing import (
    CaselessLiteral, Word, delimitedList, Optional,
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString,
    ZeroOrMore, Keyword
)


MONGO_BINARY_OPERATIONS = {
    '>': 'gt',
    '<': 'lt',
    '!=': 'ne',
    '>=': 'gte',
    '<=': 'lte',
    'in': 'in',
    '=': ''
}


#def test(s):
#    try:
#        tokens = simpleSQL.parseString(s)
#    except ParseException:
#        return
#    return tokens


def parseWhereCond(strng, location, token):
    t = token[0]
    if t[0] != '(':
        field, op, values = t[0], t[1], t[2]
        if op == 'in':
            values = map(lambda x: x.strip('"\''), t[3:-1])
        elif op == '=':
            return Q(**{'{}'.format(field): values})
        return Q(**{'{}__{}'.format(field, MONGO_BINARY_OPERATIONS[op]): values})
    else:
        try:
            left, op, right = t[1], t[2], t[3]
        except IndexError:
            return t[1]
        if op == 'and':
            return (left & right)
        elif op == 'or':
            return (left | right)
        return Q()
    return token


def parseWhereExpr(strng, loc, token):
    try:
        left, op, right = token[0]
    except ValueError:
        return token[0][0]
    if op == 'or':
        return left | right
    elif op == 'and':
        return left & right
    return token[0]


selectStmt = Forward()
selectToken = Keyword('select', caseless=True)
fromToken = Keyword('from', caseless=True)

ident = Word(alphas, alphanums).setName('identifier')
columnName = delimitedList(ident)
columnNameList = Group(delimitedList(columnName))
tableName = delimitedList(ident)
tableNameList = Group(delimitedList(tableName))

whereExpression = Forward()
and_ = Keyword('and', caseless=True)
or_ = Keyword('or', caseless=True)
in_ = Keyword('in', caseless=True)
binop = oneOf('= != < > >= <=')
arithSign = Word('+-', exact=1)

realNum = Combine(
    Optional(arithSign) + (
        Word(nums) + '.' +
        Optional(Word(nums)) | ('.' + Word(nums))
    )
)

intNum = Combine(Optional(arithSign) + Word(nums))
columnRval = realNum | intNum | quotedString

whereCondition = Group(
    (columnName + binop + columnRval) |
    (columnName + in_ + '(' + delimitedList(columnRval) + ')') |
    ('(' + whereExpression + ')')
).setParseAction(parseWhereCond)


whereExpression << Group(
    whereCondition + ZeroOrMore((and_|or_) + whereExpression)
).setParseAction(parseWhereExpr)


# define the grammar
selectStmt << (
    selectToken + ('*' | columnNameList).setResultsName('columns') +
    fromToken +
    tableNameList.setResultsName('tables') +
    Optional(Group(CaselessLiteral('where') + whereExpression), '').setResultsName('where'))

#simpleSQL = selectStmt


#parsed = test('select col1, col2 from table where o1 > 1 or a2 >= 1 and (c3<1 or b4>=1 and d5 > 1 or (aBc6=1 and adc7=1)) and bn=1 or ac in (1, 2, "asddasdasda")')

#print parsed
#print parsed.where[0][1].to_query(0)
