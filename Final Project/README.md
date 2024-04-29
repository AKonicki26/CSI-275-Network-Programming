# CSI-275 Final Project

## File contents:
1. client.py: the client side code
2. server.py: the server side code
3. constants.py: a small collection of constants 
including the server IP
4. utils.py: 2 utility functions made for sending and receiving
messages in the correct form

## Socket ports can be found in constants.py
This address is used throughout the entire program. The default value is ("184.171.154.216", 49343)<br/>
This address is an arbitrary port and the ip address of my computer on Champlain College's local Wi-Fi,
as testing was done on multiple machines to make sure it worked<br/>
Because I will not be running this server constantly, please change the IP to one of your choosing, most likely "localhost"

## How to run:
Run server.py, and then client.py. Order can theoretically be swapped, but server.py __must__
be running before the client enters their username

*Usernames must be alphanumeric only. No special characters are allowed*
### How to send messages:
Broadcast messages: type any string of characters into the terminal as normal, no special parameters needed<br/>
Private messages: type '/p' into the console, then the name of the user you would like to message, then the message you would like to send them. (ex: /p ScottBarrett Hello Scott!!)<br/>
Exit message: type /EXIT. Message must be in all caps

## I/O Examples:
{text} is used as a way of replacing variables, similar to an f-string

[08:53:58 PM] SERVER: Welcome to the server, {username}!<br/>
*typing a message to send to the console*<br/>
[08:54:07 PM] {username}: typing a message to send to the console

### Enjoy using the server!
