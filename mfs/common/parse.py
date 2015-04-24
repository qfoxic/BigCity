from pyparsing import (CaselessLiteral, Word, Upcase, delimitedList, Optional,
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString,
    ZeroOrMore, Keyword)

def test(s):
    try:
        tokens = simpleSQL.parseString(s)
    except ParseException:
        return
    return tokens

from mongoengine import Q


def parseWhereCond(strng, location, token):
    t = token[0]
    if t[0] != '(':
        field, op, value = t[0], t[1], t[2]
        return Q(**{'{}__{}'.format(field, op): value}).to_query(0)
    else:
        left, op, right = t[1], t[2], t[3]
        if op == 'and':
            return (left & right)
        elif op == 'or':
            return (left | right)
        return Q()
    return token


def parseWhereExpr(*arg):
    import pdb;pdb.set_trace()
    return arg[2][0][0]



# define SQL tokens
selectStmt = Forward()
selectToken = Keyword("select", caseless=True)
fromToken   = Keyword("from", caseless=True)

ident          = Word( alphas, alphanums + "_$" ).setName("identifier")
columnName     = Upcase( delimitedList( ident, ".", combine=True ) )
columnNameList = Group( delimitedList( columnName ) )
tableName      = Upcase( delimitedList( ident, ".", combine=True ) )
tableNameList  = Group( delimitedList( tableName ) )

whereExpression = Forward()
and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)
in_ = Keyword("in", caseless=True)

binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
arithSign = Word("+-", exact=1)
realNum = Combine(
    Optional(arithSign) + (
        Word(nums) + "." +
        Optional(Word(nums)) | ("." + Word(nums))
    )
)
intNum = Combine(Optional(arithSign) + Word(nums))

columnRval = realNum | intNum | quotedString | columnName
whereCondition = Group(
    (columnName + binop + columnRval) |
    (columnName + in_ + "(" + delimitedList( columnRval ) + ")") |
    ("(" + whereExpression + ")")).setParseAction(parseWhereCond)

whereExpression << Group(whereCondition + ZeroOrMore((and_|or_) + whereExpression)).setParseAction(parseWhereExpr)


# define the grammar
selectStmt << (
    selectToken + ('*' | columnNameList).setResultsName("columns") +
    fromToken +
    tableNameList.setResultsName("tables") +
    Optional(Group(CaselessLiteral("where") + whereExpression), "").setResultsName("where"))

simpleSQL = selectStmt



parsed = test('select * from table where a>1 or c<1')
print parsed
print parsed.where[0][1]
