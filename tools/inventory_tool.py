from crewai.tools import tool
import pandas as pd


@tool("Inventory Checker Tool")
def check_inventory():
    """
    Reads inventory CSV and identifies low stock items.
    """

    import pandas as pd

    df = pd.read_csv("data/inventory.csv")

    # High Risk (<60%)
    high_risk = df[df["Current_Stock"] < (0.6 * df["Minimum_Required"])].copy()
    high_risk["Reorder_Qty"] = (
            high_risk["Minimum_Required"] - high_risk["Current_Stock"]
    )

    # Medium Risk (60%-99%)
    medium_risk = df[
        (df["Current_Stock"] >= (0.6 * df["Minimum_Required"])) &
        (df["Current_Stock"] < df["Minimum_Required"])
        ].copy()

    medium_risk["Reorder_Qty"] = (
            medium_risk["Minimum_Required"] - medium_risk["Current_Stock"]
    )

    result = f"""
    TOTAL PARTS: {len(df)}

    HIGH RISK INVENTORY

    {high_risk[['Product_Name',
                'Vendor',
                'Minimum_Required',
                'Current_Stock',
                'Reorder_Qty']].to_markdown(index=False)}

    --------------------------------------------------

    MEDIUM RISK INVENTORY

    {medium_risk[['Product_Name',
                  'Vendor',
                  'Minimum_Required',
                  'Current_Stock',
                  'Reorder_Qty']].to_markdown(index=False)}
    """

    return result