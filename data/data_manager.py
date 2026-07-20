import json

# ===================================== custom_commands.json
def Load_CustomCommands():
    try:
        with open('data/custom_commands.json', 'r', encoding='utf-8') as json_file:
            custom_commands = json.load(json_file)
            print("[✅] custom_commands.json")
    except Exception as e:
        custom_commands = {}
        print("[❌] ERRO AO CARREGAR custom_commands.json:", e)
    return custom_commands

def UpCustomCommand(custom_commands):
    try:
        with open('data/custom_commands.json', 'w', encoding='utf-8') as json_file:
            json.dump(custom_commands, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("[❌] ERRO AO SALVAR custom_commands.json:", e)


# ===================================== blacklist.json
def Load_Blacklist():
    try:
        with open('data/blacklist.json', 'r') as ban_file:
            ban_users = json.load(ban_file)
            print("[✅] blacklist.json")
    except Exception as e:
        ban_users = {}
        print("[❌] ERRO AO CARREGAR blacklist.json:", e)
    return ban_users

def UpBlacklist(ban_data):
    try:
        with open('data/blacklist.json', 'w') as ban_file:
            json.dump(ban_data, ban_file)
    except Exception as e:
        print("[❌] ERRO AO SALVAR blacklist.json:", e)


# ===================================== servers_data.json
def Load_ServersData():
    try:
        with open('data/servers_data.json', 'r', encoding='utf-8') as f:
            servers_data = json.load(f)
            print("[✅] servers_data.json")
    except Exception as e:
        servers_data = {"servers": {}}
        print("[❌] ERRO AO CARREGAR servers_data.json:", e)
    return servers_data

def UpServerData(servers_data):
    try:
        with open('data/servers_data.json', 'w') as file:
            json.dump(servers_data, file, indent=2)
    except Exception as e:
        print("\n[❌] ERRO AO SALVAR servers_data.json:", e)


# ===================================== triggers.json
def Load_Triggers():
    try:
        with open('data/custom_triggers.json', 'r', encoding='utf-8') as f:
            triggers_data = json.load(f)
            print("[✅] custom_triggers.json")
    except Exception as e:
        triggers_data = {}
        print("[❌] ERRO AO CARREGAR custom_triggers.json:", e)
    return triggers_data

def UpTrigger(triggers_data):
    try:
        with open('data/custom_triggers.json', "w", encoding="utf-8") as f:
            json.dump(triggers_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("[❌] ERRO AO SALVAR custom_triggers.json:", e)