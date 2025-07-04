import email
import base64

with open("Your_file.eml", "r") as file:
    msg = email.message_from_file(file)

for part in msg.walk():
    content_type = part.get_content_type()
    content_disposition = str(part.get("Content-Disposition"))

    if content_type == "application/octet-stream" and "filename=" in content_disposition:
        filename = part.get_filename()

        audio_data = part.get_payload(decode=True)
        with open(filename, "wb") as f:
            f.write(audio_data)

        print(f"[+] Saved WAV file as: {filename}")