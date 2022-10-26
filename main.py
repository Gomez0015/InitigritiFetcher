import requests, time, json
from datetime import datetime
from bcolors import bcolors

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

TOKEN = config['TOKEN']

# Name
# Max Bounty
# Tier
# Scope
# Last Updated

def main():
    print('Getting the list of all the programs/invites')

    invite_json = requests.get("https://api.intigriti.com/core/researcher/invite", headers={"Authorization": "Bearer " + TOKEN}).json()

    print("Invites: ")

    for invite in invite_json:
        print(f"- {invite['programName']}")
        print(f"- {invite['maxBounty']['value']} {invite['maxBounty']['currency']}")
        print(f"- {datetime.fromtimestamp(invite['programLastUpdatedAt'])}")
        data = requests.get(f"https://api.intigriti.com/core/researcher/program/{invite['companyHandle']}/{invite['programHandle']}", headers={"Authorization": "Bearer " + TOKEN}).json()
    
        for domain in data['domains'][0]['content']:
            tier = ""

            match domain['businessImpact']:
                case 4:
                    tier = bcolors.fail("1")
                case 3:
                    tier = bcolors.warning("2")
                case 2:
                    tier = bcolors.okblue("3")
                case 1:
                    tier = bcolors.ok("4")

            print(f"    - Endpoint: {bcolors.header(domain['endpoint'])}, Tier: {tier}")

        print(f"https://app.intigriti.com/researcher/programs/{invite['companyHandle']}/{invite['programHandle']}/detail")

        print("\n")

    print("-"*25)

    print("Programs: ")

    program_json = requests.get("https://api.intigriti.com/core/researcher/program", headers={"Authorization": "Bearer " + TOKEN}).json()

    for program in program_json:
        print(f"- {program['name']}")
        print(f"- {program['maxBounty']['value']} {program['maxBounty']['currency']}")
        print(f"- {datetime.fromtimestamp(program['lastUpdatedAt'])}")
        
        r = requests.get(f"https://api.intigriti.com/core/researcher/program/{program['companyHandle']}/{program['handle']}", headers={"Authorization": "Bearer " + TOKEN})

        if(r.status_code == 200):

            data = r.json()

            for domain in data['domains'][0]['content']:
                tier = ""

                match domain['businessImpact']:
                    case 4:
                        tier = bcolors.fail("1")
                    case 3:
                        tier = bcolors.warning("2")
                    case 2:
                        tier = bcolors.okblue("3")
                    case 1:
                        tier = bcolors.ok("4")

                print(f"    - Endpoint: {bcolors.header(domain['endpoint'])}, Tier: {tier}")
        else:
            print(f"    - {bcolors.fail('Forbidden')}")

        print(f"https://app.intigriti.com/researcher/programs/{program['companyHandle']}/{program['handle']}/detail")

        print("\n")

    print("-"*25)

if __name__ == '__main__':
    main()
