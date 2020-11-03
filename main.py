from input_reader import InputParser
from math import ceil


class EmiCalculator:
    def __init__(self, loan_list, payment_list, balance_list):
        self.loan_list = loan_list
        self.payment_list = payment_list
        self.balance_list = balance_list

    def loan_processor(self):
        data_dict = {}
        index_dict = {"isalnum": 0, "isalpha": 1, "isnum": [2, 3, 4]}
        for item in self.loan_list:
            splitted_values = item.split()
            length = len(splitted_values)
            if not self.check_assign(splitted_values, length, index_dict):
                print(
                    f"please validate the input loan list and list is str(self.loan_list)"
                )
                continue
            bank, name, numeric_list = self.check_assign(
                splitted_values, length, index_dict
            )
            if not all([bank, name, numeric_list]):
                print(
                    f"please validate the input loan list and list is str(self.loan_list)"
                )
                continue
            principal = float(numeric_list[0])
            no_of_years = float(numeric_list[1])
            rate_of_interest = float(numeric_list[2])
            try:
                floatted_numericals = map(float, numeric_list)
                raw_interest = self.multiply(floatted_numericals)
                interest = raw_interest / 100
                total_amount = principal + interest
            except Exception as exe:
                print(f"Loan calculation Failed and exe is {exe} for {bank}, {name}")
            total_month = no_of_years * 12
            emi_count = ceil(total_amount / total_month)

            # To keep data dict key  unique  formatted with name and bank name

            data_dict[f"{name}_{bank}"] = {
                "total_amount": total_amount,
                "emi_count": emi_count,
                "principal": principal,
                "no_of_years": no_of_years,
                "rate_of_interest": rate_of_interest,
            }
        return data_dict

    def payment_processor(self):
        index_dict = {"isalnum": 0, "isalpha": 1, "isnum": [2, 3]}
        data_dict = self.loan_processor()
        for item in self.payment_list:
            splitted_values = item.split()
            length = len(splitted_values)
            if not self.check_assign(splitted_values, length, index_dict):
                print(
                    f"please validate the input loan list and list is str(self.loan_list)"
                )
                continue
            bank, name, numeric_list = self.check_assign(
                splitted_values, length, index_dict
            )
            if not all([bank, name, numeric_list]):
                print(
                    f"please validate the input loan list and list is str(self.loan_list)"
                )
                continue
            lumpsum = float(numeric_list[0])
            no_of_emi_payed = float(numeric_list[1])
            data_dict = self.loan_processor()
            total_amount = data_dict[f"{name}_{bank}"].get("total_amount")
            emi_amount = data_dict[f"{name}_{bank}"].get("emi_amount")
            installments_payed = emi_amount * no_of_emi_payed
            payed_amount = lumpsum + installments_payed
            remaining_amount = total_amount - payed_amount

            payment_func_data = {"remaining_amount": remaining_amount}
            data_dict[f"{name}_{bank}"].update(payment_func_data)
        return data_dict

    def balance_processor(self):
        index_dict = {"isalnum": 0, "isalpha": 1, "isnum": [2]}
        data_dict = self.balance_processor()
        for item in self.balance_list:
            splitted_values = item.split()
            length = len(splitted_values)
            if not self.check_assign(splitted_values, length, index_dict):
                print(
                    f"please validate the input loan list and list is str(self.loan_list)"
                )
                continue
            bank, name, numeric_list = self.check_assign(
                splitted_values, length, index_dict
            )
            if not all([bank, name, numeric_list]):
                print(
                    f"please validate the input loan list and list is str(self.loan_list)"
                )
                continue
            needed_count = float(numeric_list[0])

            paid_sofar = data_dict[f"{name}_{bank}"].get("total_amount") - data_dict[
                f"{name}_{bank}"
            ].get("remaining_amount")
            total_paid = paid_sofar + needed_count * data_dict[f"{name}_{bank}"].get(
                "emi_amount"
            )
            balance = data_dict[f"{name}_{bank}"].get("total_amount") - total_paid
            if balance > data_dict[f"{name}_{bank}"].get("emi_amount"):
                balance = data_dict[f"{name}_{bank}"].get("emi_amount")
            remaining_emi_count = ceil(balance / data_dict[f"{name}_{bank}"].get("emi_amount"))
            data_dict[f"{name}_{bank}"]["remaining_amount"] = balance
            data_dict[f"{name}_{bank}"]["remaining_emi_count"] = remaining_emi_count
        return data_dict

    def final_data(self):
        data_list = []
        data_dict = self.balance_processor()
        for key, value in data_dict.items():
            name = key.split("_")[0]
            bank = key.split("_")[1]
            balance = value.get("remaining_amount", "")
            no_of_emi_remaining = value.get("remaining_emi_count", "")
            data_list.append(f"{name} {bank} {balance} {no_of_emi_remaining}")
        return data_list

    def check_assign(splitted_values, length, index_dict):

        """ basic input check """

        isalnum = index_dict.get("isalnum")
        isalpha = index_dict.get("isalpha")
        isnum = index_dict.get("isnum")
        bank = None
        name = None
        numeric_list = []
        if len(splitted_values) != 5:
            print("Please check the length of the input, some params missing")
            return False

        if splitted_values[isalnum].isalnum():
            bank = splitted_values[0]
        if splitted_values[isalpha].isalpha():
            name = splitted_values[1]
        if all(x.isdigit() for x in splitted_values[isnum:]):
            numeric_list = splitted_values[isnum:]
        return bank, name, numeric_list

    def multiply(self, numbers):
        total = 1
        for x in numbers:
            total *= x
        return total


if __name__ == "__main__":
    data = InputParser.input_reader()
    splitted_inp = InputParser.input_splitting(data)
    loan_list, payment_list, balance_list = InputParser.categorize_input(splitted_inp)
    final_data = EmiCalculator.final_data()
    print(final_data)
