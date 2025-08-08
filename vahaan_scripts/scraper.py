
import pandas as pd

data = {
    "Year": [2024, 2025],
    "Category": ["4W", "4W"],
    "Vehicle Class": ["MOTOR CAR", "MOTOR CAR"],
    "Count": [2000000, 2298441]
}

df = pd.DataFrame(data)
df.to_csv("../data/vahan_data.csv", index=False)
print("Sample data written to /data/vahan_data.csv")
