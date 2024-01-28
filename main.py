
import discord
import mysql.connector
import os

from discord import app_commands
from discord.app_commands import Choice
from datetime import datetime
from discord.ext import tasks

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
Server_ID = os.environ["SERVER_ID"]

async def auto_backup():
    server = client.get_guild(Server_ID)
    staff_chat = discord.utils.get(server.channels,name="staff-chat")
       
    mydb = mysql.connector.connect(
                    host=os.environ["mysql_ip"],
                    user=os.environ["mysql_uname"],
                    passwd=os.environ["mysql_pass"],
                    database=os.environ["mysql_db"]
                        )
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT COUNT(*) FROM `discord_roles`;")
    count_of_roles = mycursor.fetchone()[0]#gives us the int in the returned tuple
    mycursor.execute("SELECT * FROM `discord_roles`;")
    #roles is the sql role names in discord_roles table
    roles = mycursor.fetchall()
    for role_name in roles:
        role = discord.utils.get(server.roles, name=role_name[0])
        count_in = 0
        count_not_in = 0
        for member in role.members:
                   
            mycursor.execute(f"SELECT COUNT(*) FROM `{role_name[0]}` WHERE `id` = '{member.id}'")
            found = mycursor.fetchone()[0]
        
            if found == 1:
                count_in+=1 #cound of members who weren't added
            else:
                count_not_in+=1
                mycursor.execute(f"INSERT INTO `{role_name[0]}` (`id`) VALUES ('{member.id}');")
                mydb.commit()
                count_not_in+=1 #count of members who were added

        mycursor.execute(f"SELECT COUNT(*) FROM `{role_name[0]}`")
        count_total = mycursor.fetchone()[0]
        embedVar = discord.Embed(title="Role-Restore", description="Made by Joey", color=0x00ff00)
        embedVar.add_field(name=f"User ID's added to {role_name[0]} Database", value=count_not_in, inline=False)
        embedVar.add_field(name=f"Users not added since already in {role_name[0]} Database", value=count_in, inline=False)
        embedVar.add_field(name=f"Total {role_name[0]} ID's in Database", value=count_total, inline=False)
        await staff_chat.send(embed=embedVar)
    mydb.close()
    
        


@tasks.loop(seconds = 43200) 
async def myLoop():
    await auto_backup() #calling auto backup every 12 hours



@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=Server_ID))
    print("App Commands Ready!")
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="Role-Restore"))
    myLoop.start()
    try:        
        await tree.sync(guild=discord.Object(id=Server_ID))

        print(f'Synced')
    except Exception as e:
        print(e)




@tree.command(name = "add-role", description = "Add Role to be Backed up", guild=discord.Object(id=Server_ID)) #keep guild argument since takes long asf for discord to detect this
async def add_role(interaction: discord.Interaction, role_name: str):
    server = client.get_guild(Server_ID)
    owner_role = discord.utils.get(server.roles, name=os.environ["owner-role-name"])
    admin_role = discord.utils.get(server.roles, name="admin-role-name")
    if (owner_role in interaction.user.roles) or (admin_role in interaction.user.roles):
        if (discord.utils.get(server.roles, name = role_name)) == None:
             await interaction.response.send_message("Role Does Not Exist")
        else:

        
            mydb = mysql.connector.connect(
                    host=os.environ["mysql_ip"],
                    user=os.environ["mysql_uname"],
                    passwd=os.environ["mysql_pass"],
                    database=os.environ["mysql_db"]
                        )
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT COUNT(*) FROM `discord_roles` WHERE `name` = '{role_name}'")
            found = mycursor.fetchone()
            if found[0] ==1:
                await interaction.response.send_message("Role is Already in discord_roles table")
            else:
                mycursor.execute(f"INSERT INTO `discord_roles` (`name`) VALUES ('{role_name}');")
                mydb.commit()
                mycursor.execute(f"CREATE TABLE `{role_name}` (id VARCHAR(255));")
                mydb.commit()
                mydb.close()
                await interaction.response.send_message("Role Added Successfully")
    else:
        await interaction.response.send_message("Invalid Perms")


@tree.command(name = "backup", description = "Backup Roles", guild=discord.Object(id=Server_ID)) #keep guild argument since takes long asf for discord to detect this
async def Backup(interaction: discord.Interaction):
    server = client.get_guild(Server_ID)
    owner_role = discord.utils.get(server.roles, name=os.environ["owner-role-name"])
    admin_role = discord.utils.get(server.roles, name="admin-role-name")
    await interaction.response.send_message("Please Wait....")
    if (owner_role in interaction.user.roles) or (admin_role in interaction.user.roles):        
            mydb = mysql.connector.connect(
                    host=os.environ["mysql_ip"],
                    user=os.environ["mysql_uname"],
                    passwd=os.environ["mysql_pass"],
                    database=os.environ["mysql_db"]
                        )
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT COUNT(*) FROM `discord_roles`;")
            count_of_roles = mycursor.fetchone()[0]#gives us the int in the returned tuple
            mycursor.execute("SELECT * FROM `discord_roles`;")
            #roles is the sql role names in discord_roles table
            roles = mycursor.fetchall()
            for role_name in roles:
                role = discord.utils.get(server.roles, name=role_name[0])
                count_in = 0
                count_not_in = 0
                for member in role.members:
                   
                    mycursor.execute(f"SELECT COUNT(*) FROM `{role_name[0]}` WHERE `id` = '{member.id}'")
                    found = mycursor.fetchone()[0]
                    if found == 1:
                        count_in+=1 #cound of members who weren't added
                    else:
                        count_not_in+=1
                        mycursor.execute(f"INSERT INTO `{role_name[0]}` (`id`) VALUES ('{member.id}');")
                        mydb.commit()
                        count_not_in+=1 #count of members who were added

                mycursor.execute(f"SELECT COUNT(*) FROM `{role_name[0]}`")
                count_total = mycursor.fetchone()[0]
                embedVar = discord.Embed(title="Role-Restore", description="Made by Joey", color=0x00ff00)
                embedVar.add_field(name=f"User ID's added to {role_name[0]} Database", value=count_not_in, inline=False)
                embedVar.add_field(name=f"Users not added since already in {role_name[0]} Database", value=count_in, inline=False)
                embedVar.add_field(name=f"Total {role_name[0]} ID's in Database", value=count_total, inline=False)
                await interaction.channel.send(embed=embedVar)
            mydb.close()

    else:
        await interaction.response.send_message("Invalid Perms")

@tree.command(name = "frestore", description = "Full Restore", guild=discord.Object(id=Server_ID)) #keep guild argument since takes long asf for discord to detect this
async def frestore(interaction: discord.Interaction):
    server = client.get_guild(Server_ID)
    owner_role = discord.utils.get(server.roles, name=os.environ["owner-role-name"])
    admin_role = discord.utils.get(server.roles, name="admin-role-name")
    member_role = discord.utils.get(server.roles, name="verified-role-name")
    if (owner_role in interaction.user.roles) or (admin_role in interaction.user.roles):      
            await interaction.response.send_message("Please Wait....")  
            mydb = mysql.connector.connect(
                    host=os.environ["mysql_ip"],
                    user=os.environ["mysql_uname"],
                    passwd=os.environ["mysql_pass"],
                    database=os.environ["mysql_db"]
                        )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM `discord_roles`;")
            role_names=(mycursor.fetchall())
            server_roles = []
            amount = []
            for role in role_names:
                server_roles.append(discord.utils.get(server.roles,name=role[0]))
            for member in member_role.members:
                for x in server_roles:
                    if x not in member.roles:
                        mycursor.execute(f"SELECT COUNT(*) FROM `{x.name}` WHERE `id` = {member.id};")
                        found = mycursor.fetchone()[0]
                        
                        
                    
                    if found == 1:
                        await member.add_roles(x)
                        
            output = []
            print(amount)
            print(len(amount))
            for x in role_names:
                
                output.append([x[0],amount.count(x[0])])  #second val should be 1 but somethings fucked
          
            embedVar = discord.Embed(title="Role-Restore", description="Made by Joey", color=0x00ff00)
            for y in output:   
                embedVar.add_field(name=f"Users Restored From {y[0]} Database", value="N/A", inline=False)
            await interaction.channel.send(embed=embedVar)
    else:
        await interaction.response.send_message("Invalid Perms")


@tree.command(name = "purge", description = "purge the channel", guild=discord.Object(id=Server_ID)) #keep guild argument since takes long asf for discord to detect this
async def purge(interaction: discord.Interaction):
    server = client.get_guild(Server_ID)
    owner_role = discord.utils.get(server.roles, name=os.environ["owner-role-name"])
    admin_role = discord.utils.get(server.roles, name="admin-role-name")
    if (owner_role in interaction.user.roles) or (admin_role in interaction.user.roles):   
        await interaction.response.send_message("Purging this hoe")
        await interaction.channel.purge()


def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st
client.run(os.environ["BOT_TOKEN"])
