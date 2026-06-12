from crewai.tools import tool
import pandas as pd


@tool("Inventory Checker Tool")
def check_inventory() -> str:
    """
    Reads inventory CSV file from data
    """

    df = pd.read_csv("data/inventory.csv")

    return df.to_string(index=False)