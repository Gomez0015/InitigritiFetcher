import requests, time, json, argparse
from datetime import datetime
from bcolors import bcolors

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

TOKEN = config['TOKEN']

argparser = argparse.ArgumentParser(description='InitigritiFetcher  -  Fetches all the programs and invites from Intigriti', formatter_class=argparse.RawTextHelpFormatter)

argparser.add_argument('-j', '--json', metavar="FILE", type=str, help='Save raw output in a json file', action='store')
argparser.add_argument('-s', '--sort', metavar="SORT_CODE(s)", type=str, help="""Sort output using code(s):
1: sort by last update
2: sort by name
3: sort by status
4: sort by max bounty""", action='store')
args = argparser.parse_args()

def sort_by_last_update(list):
    return list['lastUpdatedAt'] * -1

def sort_by_name(list):
    return list['name']

def sort_by_status(list):
    return list['status']

def sort_by_max_bounty(list):
    return list['maxBounty']["value"] * -1

sort_funcs = []
def setup():
    global sort_funcs

    if(TOKEN == "YOUR_TOKEN_HERE"):
        print("Please configure the config.json file with your token")
        exit()
    
    args.sort = args.sort.split(',')
    for x in args.sort:
        match x:
            case '1':
                sort_funcs.append(sort_by_last_update)
            case '2':
                sort_funcs.append(sort_by_name)
            case '3':
                sort_funcs.append(sort_by_status)
            case '4':
                sort_funcs.append(sort_by_max_bounty)
            case _:
                pass

    main()

def main():
    print('Getting the list of all the programs/invites')

    total_json = []

    invite_json = requests.get("https://api.intigriti.com/core/researcher/invite", headers={"Authorization": "Bearer " + TOKEN}).json()

    print("Invites: ")

    for invite in invite_json:
        total_json.append(invite)
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

    if(len(sort_funcs) > 0):
        # sort by all sort_funs
        program_json = sorted(program_json, key=lambda k: [ func(k) for func in sort_funcs ])
    else:
        program_json = sorted(program_json, key=sort_funcs[0])

    for program in program_json:
        total_json.append(program)

        status = ""

        match program['status']:
            case 4:
                status = bcolors.fail("Suspended")
            case 3:
                status = bcolors.ok("Open")
            case _:
                status = bcolors.warning("Unknown")

        print(f"- {program['name']} | {status}")
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

    if(args.json):
        with open(args.json, 'w') as outfile:
            json.dump(total_json, outfile)

if __name__ == '__main__':
    setup()
