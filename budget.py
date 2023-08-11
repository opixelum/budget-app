class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, dest_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {dest_category.category}")
            dest_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        output = self.category.center(30, "*") + "\n"
        for item in self.ledger:
            description = item["description"][:23]
            amount = "{:.2f}".format(item["amount"]).rjust(30 - len(description))
            output += description + amount + "\n"
        total = "{:.2f}".format(self.get_balance())
        output += "Total: " + total
        return output


def create_spend_chart(categories):
    total_spent = sum(
        sum(item["amount"] for item in cat.ledger if item["amount"] < 0)
        for cat in categories
    )
    spent_percentage = [
        (
            cat,
            sum(item["amount"] for item in cat.ledger if item["amount"] < 0)
            / total_spent
            * 100,
        )
        for cat in categories
    ]

    bars = []
    for percentage in range(100, -1, -10):
        line = str(percentage).rjust(3) + "| "
        for _, percent in spent_percentage:
            line += "o  " if percent >= percentage else "   "
        bars.append(line + (" " * (13 - len(categories) * 3 - len(line))))

    names = [cat.category for cat in categories]
    max_length = max(len(name) for name in names)
    name_lines = []
    for i in range(max_length):
        line = "     "
        for name in names:
            line += name[i] + "  " if i < len(name) else "   "
        name_lines.append(line)

    chart = "Percentage spent by category\n"
    chart += "\n".join(bars)
    chart += "\n    -" + "---" * len(categories)
    chart += "\n" + "\n".join(name_lines)

    return chart
