PRIORITY = {
        '@': 15, # label
        'I': 15, # ignored word
        'K': 15, # reserved keyword (i. e., commands)
        'P': 15, # parameters
        'L': 14, # parse tree node [L]eaf (variable, literal, function call, etc.)
        '^': 13,
        'S': 12, # [S]ignaled
        '*': 11, '//': 11,
        '\\': 10,
        'Mod': 9,
        '+': 8, '-': 8,
        '=': 7, '<>': 7, '<=': 7, '<': 7, '>=': 7, '>': 7, 'Is': 7, 'IsNot': 7,
        'Not': 6,
        'And': 5,
        'Or': 4,
        'Xor': 3,
        'Eqv': 2,
        'Imp': 1,
        ',': 0, ';': 0, 'A': 0 # [A]ttribution
}
