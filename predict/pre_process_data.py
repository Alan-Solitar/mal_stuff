import pandas as pd
from pandas.io.json import json_normalize
import json

data = json.load(open('results.json','rb'))

# df = pd.read_json('results.json')
df = json_normalize(data)
print(df)
