# ALU Regex Data Extraction & Secure Validation

## 1. Project Overview

For this project, I used **Python and Regular Expressions (Regex)** to extract different types of information from a text file.

The text file is designed to look like data that could come from an external customer support system or API. Since information from an external source cannot automatically be trusted, I also added some basic validation and security checks.

The program extracts four types of information:

* Email addresses
* URLs
* Phone numbers
* Credit-card numbers

The program then saves the extracted information into a JSON file.

---

## 2. Project Structure

```text
alu-regex-data-extraction_{GithubUsername}/
│
├── input/
│   └── raw-text.txt
│
├── src/
│   └── main.py
│
├── output/
│   └── sample-output.json
│
└── README.md
```

### What each file does

* **`input/raw-text.txt`** - Contains the sample customer and API data that the program reads.
* **`src/main.py`** - Contains all the Python code for extracting and validating the data.
* **`output/sample-output.json`** - Contains the results produced by the program.
* **`README.md`** - Explains how the project works and how it addresses the assignment requirements.

---

# 3. What I Extracted

I chose these four data types for the project:

1. Email addresses
2. URLs
3. Phone numbers
4. Credit-card numbers

Email addresses and credit-card numbers were required parts of the assignment, and I added URLs and phone numbers as the other two data types.

---

# 4. Email Extraction

I used a regular expression to find email addresses in the input text.

The pattern I used is:

```python
email_expression = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
```

This allows the program to find emails such as:

```text
aline.mukamana@example.com
brian.k@example.org
backup.email@example.net
```

I also added some extra checks so that obvious malformed emails are not accepted.

Examples of malformed emails in my input are:

```text
john@@example.com
missing-domain@
@jane..doe@example.com
user@example
user @example.com
```

---

# 5. ALU Email Validation

The assignment required me to identify three different ALU email types.

### Official ALU email

```text
username@alueducation.com
```

Example:

```text
aline.mukamana@alueducation.com
```

### ALU Alumni email

```text
username@alumni.alueducation.com
```

Example:

```text
brian.k@alumni.alueducation.com
```

### ALU SI email

```text
username@si.alueducation.com
```

Example:

```text
chantal.uwase@si.alueducation.com
```

The program checks each extracted email against these patterns.

If the email does not belong to one of these ALU domains, I classify it as:

```text
external
```

For example:

```text
aline.mukamana@example.com
```

is classified as an external email.

---

# 6. URL Extraction

I also used Regex to find URLs in the input.

The program looks for URLs starting with:

```text
http://
https://
```

Examples from my input include:

```text
https://www.alueducation.com/students/aline-mukamana
https://www.alueducation.com/alumni/events
https://portal.example.com/Account/1044
https://support.example.com/help/contact
http://portal.example.com/login
```

For example, these are included in the input as invalid examples:

```text
javascript:alert('hello')
javascript://example.com
ftp://example.com/file
not-a-real-url
```

The reason for this is that I wanted my Regex to look specifically for the URL formats that I expect instead of accepting every possibility.

---

# 7. Phone Number Extraction

The program also extracts Rwandan phone numbers.

I included both international and local formats.

Examples include:

```text
+250 788 123 456
+250-722-456-789
+250 790 111 222
0788 987 654
```

The Regex allows spaces or hyphens between the groups of numbers.

I included some invalid examples:

```text
123
12345
abc-def-ghij
+250 123
```

These should not be returned as valid phone numbers.

---

# 8. Credit-Card Extraction

Credit-card numbers are another required part of the assignment.

I used Regex to find numbers that look like credit-card numbers.

For my test data, I used three 16-digit test card numbers:

```text
4111 1111 1111 1111
5555-5555-5555-4444
6011 1111 1111 1117
```

These are test card numbers and are not real customer payment information.

The Regex helps me find possible card numbers, but Regex by itself does not prove that a card number is valid.

Because of this, I added another validation step using the **Luhn algorithm**.

---

# 9. Luhn Validation

After finding a possible credit-card number, the program removes spaces and hyphens and then checks the number using the Luhn algorithm.

The process is:

```text
Credit-card text
       ↓
Regex finds possible card
       ↓
Remove spaces/hyphens
       ↓
Luhn check
       ↓
If valid, keep the card
       ↓
Mask the card number
```

This gives me an extra validation step instead of trusting every number that matches the Regex.

---

# 10. Protecting Credit-Card Information

Credit-card numbers are sensitive information, so I did not want the full numbers to appear in my output file.

Instead, the program masks them.

For example, instead of:

```text
4111 1111 1111 1111
```

the output contains:

```text
**** **** **** 1111
```

Only the last four digits are shown.

This is one of the security measures I used to avoid unnecessarily exposing sensitive information.

---

# 11. Treating Input as Untrusted

One of the security requirements of the assignment is to treat raw input as **untrusted data**.

My `raw-text.txt` includes some examples of potentially dangerous-looking input, such as:

```text
<script>alert('Injected content')</script>
javascript:alert(document.cookie)
DROP TABLE customers;
${process.env.SECRET_KEY}
<img src=x onerror="alert('test')">
```

The program does not execute any of these values.

They are simply text inside the input file.

The program only extracts information that matches the Regex patterns that I created.

For example, I only allow URLs beginning with:

```text
http://
https://
```

so a string such as:

```text
javascript:alert(document.cookie)
```

is not extracted as a valid URL.

---

# 12. Basic Input Validation

I added a few basic checks before processing the input.

### Input size

I set a maximum input size of:

```python
max_input_size = 100_000
```

If the input is larger than this, the program rejects it.

I added this because extremely large input could unnecessarily use system resources.

### Null bytes

I also check for null bytes:

```python
if "\x00" in text:
    return False
```

If one is found, the input is rejected.

These are basic defensive checks. They are not meant to be a complete security system.

---

# 13. Edge Cases I Tested

I included different types of edge cases in my input file.

### Email edge cases

```text
john@@example.com
missing-domain@
@jane..doe@example.com
user@example
user @example.com
```

### Phone edge cases

```text
123
12345
abc-def-ghij
+250 123
```

### URL edge cases

```text
not-a-real-url
javascript:alert('hello')
javascript://example.com
ftp://example.com/file
```

### Potentially hostile input

```text
<script>alert('Injected content')</script>
javascript:alert(document.cookie)
DROP TABLE customers;
${process.env.SECRET_KEY}
<img src=x onerror="alert('test')">
```

These examples helped me test that the program does not simply accept everything it finds in the input.

---

# 14. Realistic Input Design

I tried to make the input look more realistic than just having a list of emails, URLs, phone numbers, and cards.

The input file is written as if it came from an external customer-support API.

It contains:

* Customer records
* Customer names
* Account statuses
* Different email addresses
* ALU email addresses
* External email addresses
* Phone numbers
* Profile URLs
* Payment records
* Customer messages
* Malformed records
* Potentially hostile input

I also used different formats, such as spaces and hyphens in phone numbers and credit-card numbers.

This makes the input more similar to what a program might receive from different external systems.

---

# 15. Output

After processing the input, the program creates:

```text
output/sample-output.json
```

The output is stored as JSON.

A simplified example looks like:

```json
{
    "Emails": [
        {
            "Email": "aline.mukamana@example.com",
            "Type": "external"
        },
        {
            "Email": "aline.mukamana@alueducation.com",
            "Type": "official"
        }
    ],
    "URL": [
        "https://www.alueducation.com/students/aline-mukamana"
    ],
    "Phone_Numbers": [
        "+250 788 123 456"
    ],
    "Cards": [
        "**** **** **** 1111"
    ]
}
```

The credit-card numbers are masked in the output.

---

# 16. How to Run the Program

I used Python for this project.

From the main project folder, run:

```bash
python src/main.py
```

If your computer uses `python3`, you can run:

```bash
python3 src/main.py
```

If everything works correctly, the program displays:

```text
Data extraction completed successfully.
Results saved to: output/sample-output.json
```

The results can then be viewed in the `output` folder.

---

# 17. Security

Some of the security ideas I applied in this project are:

### Untrusted input

I treated the raw text as untrusted because it is supposed to represent information received from an external system.

### Validation

I did not assume that something was valid just because it looked similar to the expected format.

For example, credit-card candidates are checked with the Luhn algorithm after Regex extraction.

### Sensitive data protection

I masked credit-card numbers before saving the results.

### Allowing expected formats

For URLs, I specifically look for `http` and `https` instead of accepting every protocol.

### Not executing input

Potentially dangerous strings such as JavaScript, SQL, HTML, or environment variables are treated as text.

### Regex is not enough for complete security

I also learned that Regex is mainly useful for finding patterns. It should not be considered a complete security solution.

A real application would need more security measures depending on the system, such as authentication, authorization, encryption, secure database handling, and proper logging.

---


# 18. What I Learned

Through this project, I learned how to:

* Create and use Regex patterns in Python.
* Extract information from unstructured text.
* Validate extracted information.
* Use different Regex patterns for different data types.
* Classify ALU email addresses.
* Use the Luhn algorithm for credit-card validation.
* Mask sensitive information.
* Think about input as untrusted data.
* Test Regex patterns using both valid and invalid examples.
* Organize a small Python project into separate input, source, and output files.

Overall, this project helped me understand that data extraction is not only about finding patterns. The extracted information also needs to be checked and handled carefully, especially when the original input comes from an external source.

