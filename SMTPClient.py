
#Naimo Yasin

#import libraries needed for communication with a secure email server
from socket import *
import ssl
import base64

endmsg = "\r\n.\r\n"
quit_command = "QUIT\r\n"
#the content of the message

body = "\r\n I love computer networks!"

boundary = "----=_NextPart_000_001B_01CC0E4D.76CDD3A0"

with open("c:\\Users\\Naimo\\Downloads\\grey-crowned-crane-bird-crane-animal-45853.jpeg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

encoded_image_lines = '\r\n'.join([encoded_image[i:i+76] for i in range(0, len(encoded_image), 76)])


# Text part of the message
text_part = [
    "--{}".format(boundary),
    "Content-Type: text/plain",
    "",
    body,
    ""
]
image_part = [
    "--{}".format(boundary),
    "Content-Type: image/jpeg",
    "Content-Disposition: attachment; filename=\"image.jpg\"",
    "Content-Transfer-Encoding: base64",
    "",
    encoded_image_lines,
    ""
]
end_part = ["--{}--".format(boundary), ""]


# Choose a mail server (e.g. Google mail server)
mailserver = 'smtp.gmail.com'
# mailserver = "outlook.office.com"

mail_port = 587

# mailserver = 'smtp.outlook.com'

# Create socket called clientSocket and establish a TCP connection with mailserver

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mail_port))
hostname = gethostname()
addr = gethostbyname(hostname)

#Receiving the server's responce
recv = (clientSocket.recv(1024)).decode()
print(recv)


# Send ehlo command to the server and print server response. It
#should be ehlo not helo

ehloCommand = 'EHLO ' + addr +'\r\n'
clientSocket.send((ehloCommand).encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# Send STARTTLS command and print server response.
clientSocket.send('STARTTLS\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)


# Securing the socket
# wrap the socket you created earlier in a ssl context. Assuming you
# named you socket, clientSocket, you can use the following two lines
# to do so:
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)



# Authentication


#username and password
sender_email = input("Enter your email address: ")
password = input("Enter your app password: ")

# Using the auth_plain function
def auth_plain(sender_email, password):
    """ Authobject to use with PLAIN authentication. Requires self.user and
            self.password to be set.
    """
    auth_msg = "\0{}\0{}".format(sender_email, password)
    return base64.b64encode(auth_msg.encode()).decode()

# Encode credentials using auth_plain
base64_str = auth_plain(sender_email, password)


clientSocket.send(('AUTH PLAIN {}\r\n'.format(base64_str)).encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# Specifying the sender and the recipient
sender = input("Enter your email address(sender's): ")
recipient = input("Enter recipient email address: ")

headers = [
    "From: {}".format(sender),
    "To: {}".format(recipient),
    "Subject: Your Subject Here",
    "MIME-Version: 1.0",
    "Content-Type: multipart/mixed; boundary=\"{}\"".format(boundary),
    ""
]

# Combining all parts of the MIME message
mime_message = "\r\n".join(headers + text_part + image_part + end_part)

#sending the address of the sender
clientSocket.send(('MAIL FROM: <{}>\r\n'.format(sender)).encode())
recv = clientSocket.recv(1024).decode()
print(recv)

#sending the recipient's address
clientSocket.send(('RCPT TO: <{}>\r\n'.format(recipient)).encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# Send DATA command
clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

#sending the message
# message = "Subject: {}\r\n\r\n{}\r\n".format(body)
clientSocket.send(mime_message.encode())




# Send the end-of-data indicator
clientSocket.send(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)


# Send the 'QUIT' command
clientSocket.send(quit_command.encode())
recv = clientSocket.recv(1024).decode()
print(recv)


# Close the socket
clientSocket.close()
print("Socket closed")
