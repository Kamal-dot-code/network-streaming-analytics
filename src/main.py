import os
from producer import generate_network_data

if __name__ == "__main__":
    os.makedirs("../data/raw", exist_ok=True)
    df = generate_network_data(500)
    df.to_csv("../data/raw/network_data.csv", index=False)
    df.to_json("../data/raw/network_data.json", orient="records", lines=True)
    print(f"{len(df)} lignes générées")