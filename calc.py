import json
import os


# Между классами / функциями / блоками импорта должно быть 2 пустые строки (PEP8)
class UserData:
    """
    Класс, описывающий текущие значение баланса / профита / продаж и т.д.
    """

    def __init__(self):
        self.earned = 0.0  # Заработанные средства (те, что выведены на карту)
        self.spent = 0.0  # Потраченные средства
        self.balance = 0.0  # Текущий баланс (на аккаунте FunPay)

        self.sold = 0  # Кол-во продаж
        self.refunds = 0  # Кол-во возвратов

        self.load()

    # А между функциями внутри класса - 1 пустая строка.
    def sell(self, count: int, price: float) -> None:
        """
        Регистрирует продажу (прибыль).
        :param count: кол-во купленного товара.
        :param price: цена за 1 единицу товара.
        :return: текущий баланс, текущее кол-во проданного товара.
        """
        self.balance += price * count
        self.sold += count
        self.save()

    def buy(self, count: int, price: float) -> None:
        """
        Регистрирует покупку (убыль).
        :param count: кол-во купленного товара.
        :param price: цена за 1 единицу товара.
        :return: текущая потраченная сумма.
        """
        self.spent += price * count
        self.save()

    def refund(self, price: float) -> None:
        """
        Регистрирует возврат (убыль)
        :param price: сумма возврата.
        :return: текущее кол-во возвратов, текущее кол-во продаж, текущий баланс.
        """
        self.refunds += 1
        self.sold -= 1
        self.balance -= price
        self.save()

    def withdraw(self) -> None:
        """
        Регистрирует вывод средств (с учетом комисси сайта (3%))
        :return: общую сумму выводов, сумму текущего вывода.
        """
        if self.balance * 0.03 < 30:
            withdraw_sum = self.balance - 30.0
            self.earned += round(withdraw_sum, 2)
        else:
            withdraw_sum = self.balance * 0.97
            self.earned += round(withdraw_sum, 2)
        self.balance = 0
        self.save()

    def profit_count(self) -> None:
        """
        Изменяет текущий профит.
        """
        profit = round((self.earned - self.spent), 2)
        self.save()

    def save(self) -> None:
        """
        Сохраняет все данные.
        """
        to_save = {
            "earned": self.earned,
            "spent": self.spent,
            "balance": self.balance,
            "sold": self.sold,
            "refunds": self.refunds
        }

        with open("save.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(to_save, indent=4))

    def load(self) -> None:
        """
        Загружает данные из сохранения.
        """
        if not os.path.exists("save.json"):
            # Если файл сохранения не найден
            return

        with open("save.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())

        self.earned = data["earned"]
        self.spent = data["spent"]
        self.balance = data["balance"]
        self.sold = data["sold"]
        self.refunds = data["refunds"]