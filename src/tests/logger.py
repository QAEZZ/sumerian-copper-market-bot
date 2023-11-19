from colorama import init, Fore, Back, Style

class Logger():
    def __init__(self, prefix):
        self.prefix = prefix
        init(True)

    
    def important(self, message: str, start_newline: bool = False):
        print_str = f'{Style.BRIGHT}{Back.MAGENTA}{Fore.BLACK}{self.prefix}{Style.RESET_ALL}{Style.BRIGHT} IMPT:{Style.RESET_ALL}{Style.DIM} {message}'

        if start_newline:
            print_str = f'\n{print_str}'

        print(print_str)
    
    
    def info(self, message: str, start_newline: bool = False):
        print_str = f'{Style.BRIGHT}{Back.BLUE}{self.prefix}{Style.RESET_ALL}{Style.BRIGHT} INFO:{Style.RESET_ALL}{Style.DIM} {message}'

        if start_newline:
            print_str = f'\n{print_str}'

        print(print_str)
    
    
    def success(self, message: str, start_newline: bool = False):
        print_str = f'{Style.BRIGHT}{Back.GREEN}{self.prefix}{Style.RESET_ALL}{Style.BRIGHT} DONE:{Style.RESET_ALL}{Style.DIM} {message}'

        if start_newline:
            print_str = f'\n{print_str}'

        print(print_str)
    

    def error(self, message: str, start_newline: bool = False):
        print_str = f'{Style.BRIGHT}{Back.RED}{Fore.BLACK}{self.prefix}{Style.RESET_ALL}{Style.BRIGHT}  ERR:{Style.RESET_ALL}{Style.DIM} {message}'

        if start_newline:
            print_str = f'\n{print_str}'

        print(print_str)
