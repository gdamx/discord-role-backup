To setup this container is simple

First, download the docker compose file Next enter the values for the radarr server IP and api key. DO NOT USE QUOTATIONS Enter the discord server id by right clicking the server and clicking copy id.

Copy the following settings on the discord developers page under bot

![image](https://github.com/gdamx/discord-role-backup/assets/99370593/adf0c232-ee8f-4f8a-9bf8-e8b22ba6a560)


After, click reset token to get the token. Paste in in the docker compose file. DO NOT USE QUOTATIONS

![image](https://github.com/gdamx/discord-role-backup/assets/99370593/51f0478d-dd85-478c-a042-41ae09b2309e)


To invite the bot do the following. Copy and paste the link into your browser and voila.

![image](https://github.com/gdamx/discord-role-backup/assets/99370593/926e61c3-66e6-4739-921c-dbd8158c30e9)





Login to the web admin consoole for myphp and setup a db. make sure the db name is the same as the one in the enviroment file. Then create a table called discord_roles with one column called "name" varchar(255). After that you can add roles to backup
via discord.

![image](https://github.com/gdamx/discord-role-backup/assets/99370593/82cb2947-8257-4929-97d1-a85be98ffa00)

![image](https://github.com/gdamx/discord-role-backup/assets/99370593/ad6d796d-e310-4f06-a58a-098ec0e2f32b)

After that go to the discord bot and do /add-role to add the name of a role to backup. Then to restore do /frestore do restore all roles to all users. Thats all there is too it. Could make it simpler but Im lazy

![image](https://github.com/gdamx/discord-role-backup/assets/99370593/4d02a373-36dd-45ae-a621-7fceff49c9b1)

