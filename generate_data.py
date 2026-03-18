import argparse
import csv
import os
import random
from datetime import datetime, timedelta


def generate_rows(n_rows, seed):
    random.seed(seed)

    base_time = datetime(2025, 1, 1)

    drinks = ["latte", "americano", "mocha", "cappuccino"]
    stores = ["downtown", "campus", "mall", "airport"]

    for i in range(n_rows):

        customer_id = random.randint(1, 100000)

        drink = random.choice(drinks)

        store = random.choice(stores)

        price = round(random.uniform(2.5, 7.5), 2)

        quantity = random.randint(1, 5)

        timestamp = base_time + timedelta(seconds=i)

        yield [
            i,
            customer_id,
            drink,
            store,
            price,
            quantity,
            timestamp.isoformat()
        ]


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--rows", type=int, default=1000)

    parser.add_argument("--seed", type=int, default=42)

    parser.add_argument("--output", type=str, default="data")

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    output_file = os.path.join(args.output, "coffee_sales.csv")

    with open(output_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "order_id",
            "customer_id",
            "drink",
            "store",
            "price",
            "quantity",
            "timestamp"
        ])

        for row in generate_rows(args.rows, args.seed):
            writer.writerow(row)

    print(f"Generated {args.rows} rows in {output_file}")


if __name__ == "__main__":
    main()
