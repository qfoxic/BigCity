# simpleSQL.py
#
# simple demo of using the parsing library to do simple-minded SQL parsing
# could be extended to include where clauses etc.
#
# Copyright (c) 2003, Paul McGuire
#
from pyparsing import Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    ZeroOrMore, restOfLine, Keyword

def test( str ):
    print str,"->"
    try:
        tokens = simpleSQL.parseString( str )
        print "tokens = ",        tokens
        print "tokens.columns =", tokens.columns
        print "tokens.tables =",  tokens.tables
        print "tokens.where =", tokens.where
    except ParseException, err:
        print " "*err.loc + "^\n" + err.msg
        print err
    print


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

E = CaselessLiteral("E")
binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
arithSign = Word("+-",exact=1)
realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                                         ( "." + Word(nums) ) ) +
            Optional( E + Optional(arithSign) + Word(nums) ) )
intNum = Combine( Optional(arithSign) + Word( nums ) +
            Optional( E + Optional("+") + Word(nums) ) )

columnRval = realNum | intNum | quotedString | columnName # need to add support for alg expressions
whereCondition = Group(
    ( columnName + binop + columnRval ) |
    ( columnName + in_ + "(" + delimitedList( columnRval ) + ")" ) |
    ( columnName + in_ + "(" + selectStmt + ")" ) |
    ( "(" + whereExpression + ")" )
    )
whereExpression << whereCondition + ZeroOrMore( ( and_ | or_ ) + whereExpression )

# define the grammar
selectStmt      << ( selectToken +
                   ( '*' | columnNameList ).setResultsName( "columns" ) +
                   fromToken +
                   tableNameList.setResultsName( "tables" ) +
                   Optional( Group( CaselessLiteral("where") + whereExpression ), "" ).setResultsName("where") )

simpleSQL = selectStmt

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore( oracleSqlComment )


test( "SELECT * from XYZZY, ABC" )
test( "select * from SYS.XYZZY" )
test( "Select A from Sys.dual" )
test( "Select A,B,C from Sys.dual" )
test( "Select A, B, C from Sys.dual" )
test( "Select A, B, C from Sys.dual, Table2   " )
test( "Xelect A, B, C from Sys.dual" )
test( "Select A, B, C frox Sys.dual" )
test( "Select" )
test( "Select &&& frox Sys.dual" )
test( "Select A from Sys.dual where a in ('RED','GREEN','BLUE')" )
test( "Select A from Sys.dual where a in ('RED','GREEN','BLUE') and b in (10,20,30)" )
test( "Select A,b from table1,table2 where table1.id eq table2.id -- test out comparison operators" )

"""
Test output:
>pythonw -u simpleSQL.py
SELECT * from XYZZY, ABC ->
tokens =  ['select', '*', 'from', ['XYZZY', 'ABC']]
tokens.columns = *
tokens.tables = ['XYZZY', 'ABC']

select * from SYS.XYZZY ->
tokens =  ['select', '*', 'from', ['SYS.XYZZY']]
tokens.columns = *
tokens.tables = ['SYS.XYZZY']

Select A from Sys.dual ->
tokens =  ['select', ['A'], 'from', ['SYS.DUAL']]
tokens.columns = ['A']
tokens.tables = ['SYS.DUAL']

Select A,B,C from Sys.dual ->
tokens =  ['select', ['A', 'B', 'C'], 'from', ['SYS.DUAL']]
tokens.columns = ['A', 'B', 'C']
tokens.tables = ['SYS.DUAL']

Select A, B, C from Sys.dual ->
tokens =  ['select', ['A', 'B', 'C'], 'from', ['SYS.DUAL']]
tokens.columns = ['A', 'B', 'C']
tokens.tables = ['SYS.DUAL']

Select A, B, C from Sys.dual, Table2    ->
tokens =  ['select', ['A', 'B', 'C'], 'from', ['SYS.DUAL', 'TABLE2']]
tokens.columns = ['A', 'B', 'C']
tokens.tables = ['SYS.DUAL', 'TABLE2']

Xelect A, B, C from Sys.dual ->
^
Expected 'select'
Expected 'select' (0), (1,1)

Select A, B, C frox Sys.dual ->
               ^
Expected 'from'
Expected 'from' (15), (1,16)

Select ->
      ^
Expected '*'
Expected '*' (6), (1,7)

Select &&& frox Sys.dual ->
       ^
Expected '*'
Expected '*' (7), (1,8)

>Exit code: 0
"""


#
# simpleBool.py
#
# Example of defining a boolean logic parser using
# the operatorGrammar helper method in pyparsing.
#
# In this example, parse actions associated with each
# operator expression will "compile" the expression
# into BoolXXX class instances, which can then
# later be evaluated for their boolean value.
#
# Copyright 2006, by Paul McGuire
# Updated 2013-Sep-14 - improved Python 2/3 cross-compatibility
#
from pyparsing import infixNotation, opAssoc, Keyword, Word, alphas

# define classes to be built at parse time, as each matching
# expression type is parsed
class BoolOperand(object):
    def __init__(self,t):
        self.label = t[0]
        self.value = eval(t[0])
    def __bool__(self):
        return self.value
    def __str__(self):
        return self.label
    __repr__ = __str__
    __nonzero__ = __bool__

class BoolBinOp(object):
    def __init__(self,t):
        self.args = t[0][0::2]
    def __str__(self):
        sep = " %s " % self.reprsymbol
        return "(" + sep.join(map(str,self.args)) + ")"
    def __bool__(self):
        return self.evalop(bool(a) for a in self.args)
    __nonzero__ = __bool__
    __repr__ = __str__

class BoolAnd(BoolBinOp):
    reprsymbol = '&'
    evalop = all

class BoolOr(BoolBinOp):
    reprsymbol = '|'
    evalop = any

class BoolNot(object):
    def __init__(self,t):
        self.arg = t[0][1]
    def __bool__(self):
        v = bool(self.arg)
        return not v
    def __str__(self):
        return "~" + str(self.arg)
    __repr__ = __str__
    __nonzero__ = __bool__

TRUE = Keyword("True")
FALSE = Keyword("False")
boolOperand = TRUE | FALSE | Word(alphas,max=1)
boolOperand.setParseAction(BoolOperand)

# define expression, based on expression operand and
# list of operations in precedence order
boolExpr = infixNotation( boolOperand,
    [
    ("not", 1, opAssoc.RIGHT, BoolNot),
    ("and", 2, opAssoc.LEFT,  BoolAnd),
    ("or",  2, opAssoc.LEFT,  BoolOr),
    ])


if __name__ == "__main__":
    p = True
    q = False
    r = True
    tests = [("p", True),
             ("q", False),
             ("p and q", False),
             ("p and not q", True),
             ("not not p", True),
             ("not(p and q)", True),
             ("q or not p and r", False),
             ("q or not p or not r", False),
             ("q or not (p and r)", False),
             ("p or q or r", True),
             ("p or q or r and False", True),
             ("(p or q or r) and False", False),
            ]

    print("p =", p)
    print("q =", q)
    print("r =", r)
    print()
    for t,expected in tests:
        res = boolExpr.parseString(t)[0]
        success = "PASS" if bool(res) == expected else "FAIL"
        print (t,'\n', res, '=', bool(res),'\n', success, '\n')



# <statement> ::= ( <select_stmt> | <describe_stmt> ) [';']
#
# <select_stmt> ::= SELECT <select_list> <from_clause> [<where_clause>] [<given_clause>] <additional_clauses>
# <describe_stmt> ::= ( DESC | DESCRIBE ) <index_name>
#
# <select_list> ::= '*' | <column_name_list>
# <column_name_list> ::= <column_name> ( ',' <column_name> )*
#
# <from_clause> ::= FROM <index_name>
#
# <where_clause> ::= WHERE <search_condition>
# <search_condition> ::= <predicates>
#                      | <cumulative_predicates>
#
# <predicates> ::= <predicate> ( AND <predicate> )*
# <predicate> ::= <in_predicate>
#               | <contains_all_predicate>
#               | <equal_predicate>
#               | <not_equal_predicate>
#               | <query_predicate>
#               | <between_predicate>
#               | <range_predicate>
#               | <same_column_or_pred>
#
# <in_predicate> ::= <column_name> [NOT] IN <value_list> [<except_clause>] [<predicate_props>]
# <contains_all_predicate> ::= <column_name> CONTAINS ALL <value_list> [<except_clause>] [<predicate_props>]
# <equal_predicate> ::= <column_name> '=' <value> [<predicate_props>]
# <not_equal_predicate> ::= <column_name> '<>' <value> [<predicate_props>]
# <query_predicate> ::= QUERY IS <quoted_string>
# <between_predicate> ::= <column_name> [NOT] BETWEEN <value> AND <value>
# <range_predicate> ::= <column_name> <range_op> <num>
# <same_column_or_pred> ::= '(' + <cumulative_predicates> + ')'
#
# <cumulative_predicates> ::= <cumulative_predicate> ( ',' <cumulative_predicate> )*
# <cumulative_predicate> ::= <in_predicate>
#                          | <equal_predicate>
#                          | <between_predicate>
#                          | <range_predicate>
#
# <value_list> ::= '(' <value> ( ',' <value> )* ')'
# <value> ::= <quoted_string> | <num>
# <range_op> ::= '<' | '<=' | '>=' | '>'
#
# <except_clause> ::= EXCEPT <value_list>
#
# <predicate_props> ::= WITH <prop_list>
#
# <prop_list> ::= '(' <key_value_pair> ( ',' <key_value_pair> )* ')'
# <key_value_pair> ::= <quoted_string> ':' <quoted_string>
#
# <given_clause> ::= GIVEN FACET PARAM <facet_param_list>
# <facet_param_list> ::= <facet_param> ( ',' <facet_param> )*
# <facet_param> ::= '(' <facet_name> <facet_param_name> <facet_param_type> <facet_param_value> ')'
# <facet_param_name> ::= <quoted_string>
# <facet_param_type> ::= BOOLEAN | INT | LONG | STRING | BYTEARRAY | DOUBLE
# <facet_param_value> ::= <quoted_string>
#
# <additional_clauses> ::= ( <additional_clause> )*
# <additional_clause> ::= <order_by_clause>
#                       | <group_by_clause>
#                       | <limit_clause>
#                       | <browse_by_clause>
#                       | <fetching_stored_clause>
#
# <order_by_clause> ::= ORDER BY <sort_specs>
# <sort_specs> ::= <sort_spec> ( ',', <sort_spec> )*
# <sort_spec> ::= <column_name> [<ordering_spec>]
# <ordering_spec> ::= ASC | DESC
#
# <group_by_clause> ::= GROUP BY <group_spec>
# <group_spec> ::= <facet_name> [TOP <max_per_group>]
#
# <limit_clause> ::= LIMIT [<offset> ','] <count>
# <offset> ::= ( <digit> )+
# <count> ::= ( <digit> )+
#
# <browse_by_clause> ::= BROWSE BY <facet_specs>
# <facet_specs> ::= <facet_spec> ( ',' <facet_spec> )*
# <facet_spec> ::= <facet_name> [<facet_expression>]
# <facet_expression> ::= '(' <expand_flag> <count> <count> <facet_ordering> ')'
# <expand_flag> ::= TRUE | FALSE
# <facet_ordering> ::= HITS | VALUE
#
# <fetching_stored_clause> ::= FETCHING STORED [<fetching_flag>]
# <fetching_flag> ::= TRUE | FALSE
#
# <quoted_string> ::= '"' ( <char> )* '"'
#                   | "'" ( <char> )* "'"
#
# <identifier> ::= <identifier_start> ( <identifier_part> )*
# <identifier_start> ::= <alpha> | '-' | '_'
# <identifier_part> ::= <identifier_start> | <digit>
#
# <column_name> ::= <identifier>
# <facet_name> ::= <identifier>
#
# <alpha> ::= <alpha_lower_case> | <alpha_upper_case>
#
# <alpha_upper_case> ::= A | B | C | D | E | F | G | H | I | J | K | L | M | N | O
#                      | P | Q | R | S | T | U | V | W | X | Y | Z
# <alpha_lower_case> ::= a | b | c | d | e | f | g | h | i | j | k | l | m | n | o
#                      | p | q | r | s | t | u | v | w | x | y | z
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
#
# <num> ::= ( <digit> )+

