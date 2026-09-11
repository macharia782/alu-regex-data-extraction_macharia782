from pathlib import Path
import json
import re

# File paths
input_file = Path("input/raw-text.txt")
output_file = Path("output/sample-output.json")

max_input_size = 100_000

# Regular Expressions
email_expression = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

url_expression = re.compile(
    r"https?://[A-Za-z0-9.-]+(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?"
)

phone_expression = re.compile(
    r"(?<!\d)(?:"
    r"\+250[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}"
    r"|"
    r"0\d{3}[\s-]?\d{3}[\s-]?\d{3}"
    r")(?!\d)"
)

card_expression = re.compile(
    r"(?<!\d)(?:\d{4}[- ]?){3}\d{4}(?!\d)"
)

# Read input file


def read_input():
    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    text = input_file.read_text(encoding="utf-8")

    return text

# Input Validation


def is_safe_input(text):
    if len(text) > max_input_size:
        return False

    if "\x00" in text:
        return False

    return True

# Email extraction and validation


def is_valid_email(email):
    if ".." in email:
        return False

    if ".@" in email:
        return False

    if email.count("@") != 1:
        return False

    return True


def extract_email(text):
    matches = email_expression.findall(text)

    valid_emails = []

    for email in matches:
        if is_valid_email(email):
            valid_emails.append(email)

    return sorted(set(valid_emails))


# ALU email classes

alu_official = re.compile(
    r"^[A-Za-z0-9._%+-]+@alueducation\.com$"
)

alu_alumni = re.compile(
    r"^[A-Za-z0-9._%+-]+@alumni\.alueducation\.com$"
)

alu_si = re.compile(
    r"^[A-Za-z0-9._%+-]+@si\.alueducation\.com$"
)


def classify_email(email):
    if alu_official.fullmatch(email):
        return "official"

    if alu_alumni.fullmatch(email):
        return "alumni"

    if alu_si.fullmatch(email):
        return "si"

    return "external"

# URL extraction


def extract_urls(text):
    matches = url_expression.findall(text)

    return sorted(set(matches))

# Phone number extraction


def extract_number(text):
    matches = phone_expression.findall(text)

    return sorted(set(matches))

# Card extraction


def card_format(card):
    return re.sub(r"[- ]", "", card)


def luhn_check(card_number):
    digits = [int(num) for num in card_number if num.isdigit()]

    if len(digits) < 13 or len(digits) > 19:
        return False

    card_sum = 0
    parity = len(digits) % 2

    for index, num in enumerate(digits):
        if index % 2 == parity:
            num *= 2

            if num > 9:
                num -= 9

        card_sum += num

    return card_sum % 10 == 0


def mask_card(card_number):
    return "**** **** **** " + card_number[-4:]

def extract_cards(text):
    matches = card_expression.findall(text)

    valid_cards = []

    for card in matches:
        checked_card = card_format(card)

        if luhn_check(checked_card):
            valid_cards.append(mask_card(checked_card))

    return sorted(set(valid_cards))

# Results

def get_data(text):
    emails = extract_email(text)

    email_results = []

    for email in emails:
        email_results.append({
            "Email": email,
            "Type": classify_email(email)
        })

    urls = extract_urls(text)

    phone_numbers = extract_number(text)

    cards = extract_cards(text)

    return {
        "Emails": email_results,
        "URL": urls,
        "Phone_Numbers": phone_numbers,
        "Cards": cards
    }

# Save the results

def save_output(data):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )


def main():
    try:
        text = read_input()

        if not is_safe_input(text):
            print("Input not safe or over allowed size")
            return

        data = get_data(text)

        save_output(data)

        print("Data extraction completed successully")
        print(f"Results saved to: {output_file}")

    except FileNotFoundError as error:
        print(error)

    except Exception as error:
        print(f"Unexpected error: {error}")

if __name__ == "__main__":
    main()    