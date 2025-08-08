import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    "Year": [2020, 2021, 2022],
    "Registrations": [15000, 18000, 21000]
})

fig = px.bar(df, x="Year", y="Registrations", title="Test Plot")
fig.show()
