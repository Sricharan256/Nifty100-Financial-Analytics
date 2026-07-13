from utils.db import *

print(get_companies().head())

print(get_ratios("TCS").head())

print("\nDatabase utilities tested successfully.")