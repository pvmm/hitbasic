# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import cfg


def processor(select_stmt, symbol_table):
    print("select_case.processor called")
    #symbol_table.create_label(prefix='bla')
    return select_stmt


class SelectStmt(Node):
    keyword = 'SELECT'
