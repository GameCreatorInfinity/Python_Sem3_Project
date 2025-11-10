import urllib.request
import json

print("=== Online Currency Converter ===")

# Base URL for fetching rates
url = "https://api.exchangerate-api.com/v4/latest/USD"

try:
    print("\nFetching latest exchange rates... Please wait...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        rates = data["rates"]
        base = data["base"]
    print("* Exchange rates updated successfully! *")

    # Display some available currencies
    print("\nAvailable currencies (sample):", ', '.join(list(rates.keys())[:10]), "...")

    while True:
        print("\n--- Currency Conversion Menu ---")
        from_currency = input("Enter FROM currency code (or 'exit' to quit): ").upper()
        if from_currency == "EXIT":
            break

        to_currency = input("Enter TO currency code: ").upper()
        if from_currency not in rates or to_currency not in rates:
            print(" Invalid currency code. Try again.")
            continue

        try:
            amount = float(input("Enter amount: "))
            usd_amount = amount / rates[from_currency]
            converted_amount = usd_amount * rates[to_currency]
            print(f"\n{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")
        except ValueError:
            print(" Please enter a valid number.")

except Exception as e:
    print("\n Error fetching exchange rates:", e)

print("\n=== Thank you for using Online Currency Converter ===")
