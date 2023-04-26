import base64
import email
import email.header
import email.utils
import mimetypes
import os
from email.message import EmailMessage


def composeMail(
    fromUser: str, toUser: str, subject: str, body: str, attachments: list[str]
):
    message = EmailMessage()

    message["To"] = toUser
    message["From"] = fromUser
    message["Subject"] = subject

    message.set_content(body)

    for file in attachments:
        # Guess the content type based on the file's extension. Encoding will be
        # ignored, although we should check for simple things like gzip'd or
        # compressed files.
        ctype, encoding = mimetypes.guess_type(file)

        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)

        filename = os.path.basename(file)

        with open(file, "rb") as f:
            content = f.read()
            message.add_attachment(
                content, maintype=maintype, subtype=subtype, filename=filename
            )

    return message


def parseMail(msg):
    date = ""
    subject = ""
    fromUser = ""
    toUser = ""
    body = ""

    parsedMsg = email.message_from_bytes(base64.urlsafe_b64decode(msg["raw"]))

    if parsedMsg["Date"] is not None:
        dateRaw = parsedMsg["Date"]
        parsedDate = email.utils.parsedate_to_datetime(dateRaw)
        date = parsedDate.strftime("%Y-%m-%d %H:%M:%S")

    if parsedMsg["Subject"] is not None:
        subject = email.header.decode_header(parsedMsg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

    if parsedMsg["From"] is not None:
        fromUser = email.header.decode_header(parsedMsg["From"])[0][0]
        if isinstance(fromUser, bytes):
            fromUser = fromUser.decode()

    if parsedMsg["To"] is not None:
        toUser = email.header.decode_header(parsedMsg["To"])[0][0]
        if isinstance(toUser, bytes):
            toUser = toUser.decode()

    body_data = []
    if parsedMsg.is_multipart():
        for part in parsedMsg.get_payload():
            if part.is_multipart():
                for subpart in part.get_payload():
                    if "text" in subpart.get_content_maintype():
                        body_data.append(
                            subpart.get_payload(decode=True).decode("utf-8")
                        )
            else:
                if "text" in part.get_content_maintype():
                    body_data.append(part.get_payload(decode=True).decode("utf-8"))
    else:
        body_data = parsedMsg.get_payload(decode=True).decode("utf-8")
    if body_data is not None:
        body = "".join(body_data)

    return {
        "date": date,
        "subject": subject,
        "from": fromUser,
        "to": toUser,
        "body": body,
    }
