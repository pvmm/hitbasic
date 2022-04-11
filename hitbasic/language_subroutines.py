from . import NO_RULE, subc
from .hitbasic import Surrogate
from .translations import subroutine as module


subroutine_type = type('Subroutine', (Surrogate,), subc(module, 'CodeBlock'))
