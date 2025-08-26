import discord, requests, json
import pandas as skibidi #this is cals fault
from datetime import datetime, timedelta
from discord.ext import tasks
from numerize import numerize


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)





@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    contract_get.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@tasks.loop(minutes=5.0)
async def contract_get():
   
    channel = client.get_channel(1377634397116956692)
    kami = await client.fetch_user(1002598822314262638)
    fisk = await client.fetch_user(269745898337206272)
    print("starting.")
    with open("contracts.json", "r", encoding="utf-8") as json_data:
        contracts = json.load(json_data)
        json_data.close()

    with open("current.json", "r", encoding="utf-8") as json_data:
        current = json.load(json_data)
        json_data.close()


    df = skibidi.read_csv('typeids.csv')
    typeids = df.values.tolist()

    atships = ["Adrestia","Bestla","Caedes","Cambion","Chameleon","Chremoas","Cybele","Etana","Fiend","Freki","Geri","Gold Magnate","Hydra","Imp","Laelaps","Malice","Mimir","Moracha","Rabisu","Raiju","Shapash","Silver Magnate","Tiamat","Utu","Victor","Virtuoso","Whiptail","Sidewinder","Python","Cobra",]
    purpleofficers = ["Tobias", "Gotan", "Hakim", "Mizuro", "Ramaku", "Sila", "Zohar", "Estamel", "Vepas", "Thon", "Kaikka", "Panola", "Hanaruwa", "Hakuzosu", "Draclira", "Ahremen", "Raysere", "Tairei", "Makra", "Ryhad", "Makur", "Chelm", "Vizan", "Selynne", "Brokara", "Usara", "Nija", "Cormack", "Setele", "Tuvan", "Brynn", "Asine", "Gara", "Zorya", "Kasiha", "W-634", "P-343554", "F-435454", "D-34343"]
    supertitans = ["Aeon", "Wyvern", "Nyx", "Hel", "Revenant", "Vendetta", "Avatar", "Leviathan", "Erebus", "Ragnarok", "Vanquisher", "Azariel", "Molok", "Komodo"]
    contractidnew = []
    contractidnewpricehold = []
    contractidnewprice = []
    contractidold = []
    contractitems = []
    contractsitems = []
    

    if contracts != current:
        for r in contracts:
            for c in contracts[r]:
                contractidnew.append(c["contract_id"])
                contractidnewpricehold.append([c["contract_id"], c["price"]])

        for r in current:
            for c in current[r]:
                contractidold.append(c["contract_id"])
        
     
        if current != {}:
            newcontracts = set(contractidnew) - set(contractidold)
        else:
            newcontracts = contractidnew
        

        

        for c in newcontracts:  
            contractitems = []
            contractitempage = requests.get("https://esi.evetech.net/latest/contracts/public/items/" + str(c) + "/?datasource=tranquility&page=1")
            try:
                for z in range(1, int(contractitempage.headers["x-pages"])+1):
                    contractitempage = requests.get("https://esi.evetech.net/latest/contracts/public/items/" + str(c) + "/?datasource=tranquility&page=" + str(z))
                    
                    for w in contractitempage.json():
                
                        contractitems.append(w)
                   
                        
                    
            except:
                print("contract has no x-page header.")
   
            contractsitems.append([c, contractitems])

        for z in contractsitems:
            for c in contractidnewpricehold:
                if c[0] == z[0]:
                    contractidnewprice.append(c[1])

        for i in contractsitems:
            pinged = 0 
            index = contractsitems.index(i)
            contractitemsstring = []
            for item in contractsitems[index][1]:

                
                for j in range(len(typeids)):
                    if typeids[j][0] == item["type_id"]:
                        contractitemsstring.append([typeids[j][1], item["quantity"], item["is_included"]])
            itemlist = ""
            for x in range(len(contractitemsstring)):

                if contractitemsstring[x][2] == True:
                    itemlist += contractitemsstring[x][0] + " " + str(contractitemsstring[x][1]) + "\n"
                else:
                    itemlist += "YOU PAY" + contractitemsstring[x][0] + " " + str(contractitemsstring[x][1]) + "\n"
            if pinged == 0:
                for item in contractitemsstring:
                    if item[0] in atships: 
                        pinged = 1
                        await channel.send(kami.mention)
                        await channel.send(fisk.mention)
                        embed=discord.Embed(title="Contract Found with at ship!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```"+itemlist+"```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```" + "<@1002598822314262638> \n <@269745898337206272>")
                        if len(embed) > 4096:
                            await channel.send(embed=discord.Embed(title="Contract Found with at ship!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```Contract too long!```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```" + "<@1002598822314262638> \n <@269745898337206272>"))
                        else:
                            await channel.send(embed=embed)
                        break
                    elif any(elem in item[0] for elem in purpleofficers):
                        pinged = 1  
                        embed = discord.Embed(title="Contract Found with purple mod!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```"+itemlist+"```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```" )
                        if len(embed) > 4096:
                            await channel.send(embed=discord.Embed(title="Contract Found with purple mod!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```Contract too long!```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```"))
                        else:
                            await channel.send(embed=embed)
                    elif item[0] in supertitans and int(contractidnewprice[index]) < 30000000000:
                        pinged = 1
                        await channel.send(kami.mention)
                        await channel.send(fisk.mention)
                        embed = discord.Embed(title="Contract Found with Super/Titan for under 30b!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```"+itemlist+"```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```" )
                        if len(embed) > 4096:
                            await channel.send(discord.Embed(title="Contract Found with Super/Titan for under 30b!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```Contract too long!```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```" ))
                        else:
                            await channel.send(embed=embed)
                        break

            if int(contractidnewprice[index]) > 19999999999 and pinged == 0:

                itemlist = ""
                for x in range(len(contractitemsstring)):
                    if contractitemsstring[x][2] == True:
                        itemlist += contractitemsstring[x][0] + " " + str(contractitemsstring[x][1]) + "\n"
                    else:
                        itemlist += "YOU PAY" + contractitemsstring[x][0] + " " + str(contractitemsstring[x][1]) + "\n"
                embed=discord.Embed(title="Contract Found over 20b!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```"+itemlist+"```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```" )
                if len(embed) > 4096:
                    await channel.send(embed=discord.Embed(title="Contract Found over 20b!", description=numerize.numerize(contractidnewprice[index]) + " ISK\n" + "```Contract too long!```" + "\n" +  "```" + "<url=contract:30000142//" + str(i[0]) + ">" + str(i[0]) + "</url>```"))
                else:
                    await channel.send(embed=embed)

    else:
        print("no new contracts!")               

    print("scanned all new contracts!")
    print(datetime.now())
    current = contracts

    with open('current.json', 'w') as f:
        json.dump(current, f)



client.run('insert key here')
