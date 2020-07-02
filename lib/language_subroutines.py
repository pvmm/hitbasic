from . import NO_RULE
from .hitbasic import Surrogate
from .translations import subroutine as subroutine_module


subroutine_type = type('Subroutine', (Surrogate,), dict(subroutine_module.__dict__['CodeBlock'].__dict__))

