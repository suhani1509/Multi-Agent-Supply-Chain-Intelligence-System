from crewai.tools import tool
import pandas as pd


@tool("Inventory Checker Tool")
def check_inventory():
    """
    Reads inventory and identifies low stock items
    """

    df = pd.read_csv("data/inventory.csv")

    low_stock = df[df["stock"] < df["minimum_required"]]

    result = f"""
Total Parts: {len(df)}

LOW STOCK ITEMS:
{low_stock.to_string(index=False)}
"""

    return result