from tools.email_tool import read_vendor_emails
from tools.inventory_tool import check_inventory

print("===== EMAILS =====")
print(read_vendor_emails.run())

print("\n===== INVENTORY =====")
print(check_inventory.run())