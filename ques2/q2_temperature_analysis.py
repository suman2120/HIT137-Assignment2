import os
import csv
from statistics import pstdev

month = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
         "october", "november", "december"]
def month_to_season(m):
  if m == 12 or m == 1 or m == 2:
  return "Summer"
elif m == 3 or m == 4 or m == 5:
return "Autumn"
elif m == 6 or m == 7 or m == 8:
return"Winter"
else:
return "Spring"
