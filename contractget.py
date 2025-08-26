import requests, json
from datetime import datetime, timedelta, timezone


regions = [[10000001, 'Derelik'], [10000002, 'The Forge'], [10000003, 'Vale of the Silent'], [10000005, 'Detorid'], [10000006, 'Wicked Creek'], [10000007, 'Cache'], [10000008, 'Scalding Pass'], [10000009, 'Insmother'], [10000010, 'Tribute'], [10000011, 'Great Wildlands'], [10000012, 'Curse'], [10000013, 'Malpais'], [10000014, 'Catch'], [10000015, 'Venal'], [10000016, 'Lonetrek'], [10000018, 'The Spire'], [10000020, 'Tash-Murkon'], [10000021, 'Outer Passage'], [10000022, 'Stain'], [10000023, 'Pure Blind'], [10000025, 'Immensea'], [10000027, 'Etherium Reach'], [10000028, 'Molden Heath'], [10000029, 'Geminate'], [10000030, 'Heimatar'], [10000031, 'Impass'], [10000032, 'Sinq Laison'], [10000033, 'The Citadel'], [10000034, 'The Kalevala Expanse'], [10000035, 'Deklein'], [10000036, 'Devoid'], [10000037, 'Everyshore'], [10000038, 'The Bleak Lands'], [10000039, 'Esoteria'], [10000040, 'Oasa'], [10000041, 'Syndicate'], [10000042, 'Metropolis'], [10000043, 'Domain'], [10000044, 'Solitude'], [10000045, 'Tenal'], [10000046, 'Fade'], [10000047, 'Providence'], [10000048, 'Placid'], [10000049, 'Khanid'], [10000050, 'Querious'], [10000051, 'Cloud Ring'], [10000052, 'Kador'], [10000053, 'Cobalt Edge'], [10000054, 'Aridia'], [10000055, 'Branch'], [10000056, 'Feythabolis'], [10000057, 'Outer Ring'], [10000058, 'Fountain'], [10000059, 'Paragon Soul'], [10000060, 'Delve'], [10000061, 'Tenerifis'], [10000062, 'Omist'], [10000063, 'Period Basis'], [10000064, 'Essence'], [10000065, 'Kor-Azor'], [10000066, 'Perrigen Falls'], [10000067, 'Genesis'], [10000068, 'Verge Vendor'], [10000069, 'Black Rise'], [10000070, 'Pochven'], [10001000, 'Yasna Zakh']]
contracts = {
    "Derelik": [],
    "The Forge": [],
    "Vale of the Silent": [],
    "Detorid": [],
    "Wicked Creek": [],
    "Cache": [],
    "Scalding Pass": [],
    "Insmother": [],
    "Tribute": [],
    "Great Wildlands": [],
    "Curse": [],
    "Malpais": [],
    "Catch": [],
    "Venal": [],
    "Lonetrek": [],
    "The Spire": [],
    "Tash-Murkon": [],
    "Outer Passage": [],
    "Stain": [],
    "Pure Blind": [],
    "Immensea": [],
    "Etherium Reach": [],
    "Molden Heath": [],
    "Geminate": [],
    "Heimatar": [],
    "Impass": [],
    "Sinq Laison": [],
    "The Citadel": [],
    "The Kalevala Expanse": [],
    "Deklein": [],
    "Devoid": [],
    "Everyshore": [],
    "The Bleak Lands": [],
    "Esoteria": [],
    "Oasa": [],
    "Syndicate": [],
    "Metropolis": [],
    "Domain": [],
    "Solitude": [],
    "Tenal": [],
    "Fade": [],
    "Providence": [],
    "Placid": [],
    "Khanid": [],
    "Querious": [],
    "Cloud Ring": [], 
    "Kador": [],
    "Cobalt Edge": [],
    "Aridia": [],
    "Branch": [],
    "Feythabolis": [],
    "Outer Ring": [],
    "Fountain": [],
    "Paragon Soul": [],
    "Delve": [], 
    "Tenerifis": [],
    "Omist": [],
    "Period Basis": [],
    "Essence": [],
    "Kor-Azor": [],
    "Perrigen Falls": [],
    "Genesis": [],
    "Verge Vendor": [],
    "Black Rise": [],
    "Pochven": [],
    "Yasna Zakh": []

}



for x in regions:

    contractregion = []
    contractpage = requests.get("https://esi.evetech.net/latest/contracts/public/" + str(x[0]) + "/?datasource=tranquility&page=1")

    for i in range(1, int(contractpage.headers["X-Pages"])+1): 
        contractpage = requests.get("https://esi.evetech.net/latest/contracts/public/" + str(x[0]) + "/?datasource=tranquility&page=" + str(i))

        for y in contractpage.json():
            if y["type"] == "item_exchange" and datetime.strptime(y["date_issued"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)  > datetime.now(timezone.utc) - timedelta(minutes = 60):
                contractregion.append(y)
            
           

    print(contractregion)                
    for p in contractregion:
        contracts[x[1]].append(p)
    

    
with open("contracts.json", "w", encoding="utf-8") as f:
    json.dump(contracts, f)
        
    