import sys


class InputParser:
    def input_reader():
        print("Enter the data and Use Ctrl+d to stop the input ")
        data = sys.stdin.readlines()
        data = [item.strip() for item in data]
        return data

    def input_splitting(data):
        inp_dict = {}
        input_list = []
        for item in data:
            inp_dict["process"] = item.split()[0]
            inp_dict["values"] = item.split()[1:]
            input_list.append(inp_dict)
        return input_list

    def categorize_input(self, input_list):
        loan_list = []
        payment_list = []
        balance_list = []
        for item in input_list:
            if item["process"] == "LOAN":
                loan_list.append(item["value"])
            elif item["process"] == "PAYMENT":
                payment_list.append("value")
            elif item["process"] == "BALANCE":
                balance_list.append("value")
            else:
                print("Please check the inputs")

        return loan_list, payment_list, balance_list
