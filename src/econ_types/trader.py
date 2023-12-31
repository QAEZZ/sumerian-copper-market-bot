
class Trader:
    def __init__(self, user_id: int, bal_low_grade: int = 0, bal_medium_grade: int = 0, bal_high_grade: int = 0):
        self.__user_id = user_id
        self.__low_grade_balance = bal_low_grade
        self.__medium_grade_balance = bal_medium_grade
        self.__high_grade_balance = bal_high_grade

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def low_grade_balance(self) -> int:
        return self.__low_grade_balance
    
    @low_grade_balance.setter
    def low_grade_balance(self, new_balance: int) -> None:
        self.__low_grade_balance = new_balance

    @property
    def medium_grade_balance(self) -> int:
        return self.__medium_grade_balance
    
    @medium_grade_balance.setter
    def medium_grade_balance(self, new_balance: int) -> None:
        self.__medium_grade_balance = new_balance

    @property
    def high_grade_balance(self) -> int:
        return self.__high_grade_balance
    
    @high_grade_balance.setter
    def high_grade_balance(self, new_balance: int) -> None:
        self.__high_grade_balance = new_balance

    def __str__(self):
        return f"Trader(user_id={self.user_id}, low_grade_balance={self.low_grade_balance}, medium_grade_balance={self.medium_grade_balance}, high_grade_balance={self.high_grade_balance})"
