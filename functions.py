import json

# ==== Carregar comandos customizados | Load custom commands ====
def Load_CustomCommands():
    try:
        with open('custom.json', 'r', encoding='utf-8') as json_file:
            custom_commands = json.load(json_file)
            print("\n [ ✅ ] Custom commands loaded - custom.json \n")
    except:
        custom_commands = {}
        print("\n [ ❌ ] ERROR - LOAD custom.json \n")
    return custom_commands

# ==== Atualizar comandos customizados | Update custom commands ====
def UpCustomCommand(custom_commands):
    try:
        with open('custom.json', 'w', encoding='utf-8') as json_file:
            json.dump(custom_commands, json_file, ensure_ascii=False, indent=4)
    except:
        print("\n [ ❌ ] ERROR - UP custom.json \n")

# ==== Carregar blacklist | Load blacklist ====
def Load_Blacklist():
    try:
        with open('ban.json', 'r') as ban_file:
            ban_users = json.load(ban_file)
            print("\n [ ✅ ] Blacklist loaded - ban.json \n")  
    except:
        ban_users = {}
        print("\n [ ❌ ] ERROR - LOAD ban.json \n")
    return ban_users

# ==== Atualizar blacklist | Update blacklist ====
def UpBlacklist(ban_data):
    try:
        with open('ban.json', 'w') as ban_file:
            json.dump(ban_data, ban_file)
    except:
        print("\n [ ❌ ] ERROR - UP ban.json \n")

# ==== Carregar dados dos servidores | Load server data ====
def Load_ServersData():
    try:
        with open('servers_data.json', 'r', encoding='utf-8') as f:
            servers_data = json.load(f)
            print("\n [ ✅ ] Servers data loaded - servers_data.json \n")  
    except:
        servers_data = {"servers": {}}
        print("\n [ ❌ ] ERROR - LOAD servers_data.json \n")
    return servers_data

# ==== Atualizar dados dos servidores | Update servers data ====
def UpServerData(servers_data):
    try:
        with open('servers_data.json', 'w') as file:
            json.dump(servers_data, file, indent=2)
    except:
        print("\n [ ❌ ] ERROR - UP servers_data.json \n")

# ==== Carregar triggers| Load triggers ====
def Load_Triggers():
    try:
        with open('trigger.json', 'r', encoding='utf-8') as f:
            triggers_data = json.load(f)
    except:
        triggers_data = {}
        print("\n [ ❌ ] ERROR - LOAD trigger.json \n")
    return triggers_data

# ==== Atualizar triggers | Update triggers ====
def UpTrigger(guild_id, input_text, output_text, exact_value, author_id):
    try:
        triggers_data = Load_Triggers()

        if guild_id not in triggers_data:
            triggers_data[guild_id] = {}

        triggers_data[guild_id][input_text] = {
            "output": output_text,
            "exact": exact_value,
            "author_id": author_id
        }

        with open('trigger.json', "w", encoding="utf-8") as f:
            json.dump(triggers_data, f, ensure_ascii=False, indent=4)
    except:
        print("\n [ ❌ ] ERROR - UP trigger.json \n")