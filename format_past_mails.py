import csv
import re
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "past_emails_raw.csv")  
output_file = os.path.join(script_dir, "gradio_app", "past_emails.csv")

with open(input_file, "r", newline="", encoding="utf-8") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:

    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames + ["body_formatted"]
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        subject = row.get("subject", "")
        if subject.lower().startswith("fw") or subject.lower().startswith("fwd"):
            continue  # skip forwarded mails

        body = row.get("body", "")
        lines = body.splitlines()
        formatted_lines = []

        for line in lines:
            if "<" in line:
                break  # stop at first line containing '<'
            formatted_lines.append(line)

        row["body_formatted"] = "\n".join(formatted_lines).strip()
        writer.writerow(row)

print("csv with 'body_formatted' created, forward mails excluded:", output_file)