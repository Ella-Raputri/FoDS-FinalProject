import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from collections import Counter

df = pd.read_csv('ML/classification1/data/old/wiki.csv')
df.info()
