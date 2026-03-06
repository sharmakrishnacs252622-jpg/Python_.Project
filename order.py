class Order:
    def __init__(self):
        self.items = {}

    def add_item(self, name, price):
        if name in self.items:
            self.items[name]["qty"] += 1
        else:
            self.items[name] = {"qty": 1, "price": price}

    def clear(self):
        self.items.clear()

    @property
    def total(self):
        return sum(data["qty"] * data["price"] for data in self.items.values())

    def get_items_summary(self):
        summary = []
        for name, data in self.items.items():
            subtotal = data["qty"] * data["price"]
            summary.append(f"{name} x{data['qty']} = ₹{subtotal:.2f}")
        return summary