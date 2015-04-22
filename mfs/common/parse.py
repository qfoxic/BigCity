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

