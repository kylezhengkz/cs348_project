from enum import Enum

class TagTypes(Enum):
    Warning = '93'
    Success = '92'
    Error = '91'

def print_tagged_message(type: TagTypes, label, message):
    print(f'\033[{type.value}m[{label}]\033[0m {message}')

def print_header(label):
    print(f'===== {label} ========\n')