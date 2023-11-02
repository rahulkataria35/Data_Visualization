import fpdf
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi

df = pd.read_csv("app/static/sales_data_sample.csv")
print(df.info())


df.drop(["Region", "Country", "Item Type", "Sales Channel", "Order Priority"], axis=1, inplace=True)
df = df[:20]


def color_pos_neg_value(value):
    if value < 0:
        color = 'red'
    elif value > 0:
        color = 'green'
    else:
        color = 'black'
    return 'color: %s' % color


# Apply styling to dataframe
styled_df = df.style.format({'Units Sold': "{:.0f}",
                      'Unit Price': "{:.2f}",
                      'Unit Cost': "{:.2f}",
                      'Total Revenue': "{:.2f}",
                      'Total Cost': "{:.2f}",
                      'Total Profit': "{:.2f}",
                     }).hide(axis="index").bar(subset=["Units Sold",], color='lightgreen').applymap(color_pos_neg_value, subset=['Unit Price'])


dfi.export(styled_df, 'annual_sales.png')



