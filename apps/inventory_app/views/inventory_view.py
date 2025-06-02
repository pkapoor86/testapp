def display_inventory(items):
    return "\n".join([f"{item['name']} in {item['zone']}" for item in items])
