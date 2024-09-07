# multiplayer-dicegame
This is a simple dice-game project that I had made which I later adapted using Sockets to add multiplayer functionality in Python.
I created this to test some of the python sockets communication functionalities to communicate between two client programs and a server. This currently works on localhost, however with portforwarding on your router enabled, can be played over the internet as well!

# Here is a video, showcasing how to play the dicegame
(NOTE: both the two clients and the server are on localhost in this example, to use over the internet, your public IP address must be reachable and in your router settings, the corresponding port e.g. 25565 in this case, should be port forwarded.)

[![Showcase](https://github.com/user-attachments/assets/263f6316-9d55-47c1-8018-fe2d252eca7c)](https://github.com/user-attachments/assets/263f6316-9d55-47c1-8018-fe2d252eca7c)

# How to set-up?
1) Download the Multiplayer-Sever & Multiplayer-Client folders
2) Using the provided cmd.bat file that should open a terminal window, you can then type "client.py" or "server.py" to launch each respectively
3) Afterwards, you can follow the instructions seen in the video...
4) Depending on the terminal application you use (for example, this video showcases the inbuilt Windows 11 Terminal app) the "Experimental Colours Option" may or may not work for you. There is no way to circumvent this as it is purely based on the inbuilt OS terminal so you can try enable and see if it works in your usecase!

# known issues
When playing over the internet, if the connection ping of one client gets too high or the connection is partially lost, some data may break up and weird results may be seen with the graphical elements of the game (such as the DICE graphics not showing up as intended), however, this never impacts the functionality of the game and fixes itself most of the time if the ping and connection of the client returns to normal.
