import random
import math

# TODO: file ismi degistirebilme secebilme txt dosyasi   DONE
# TODO: delete users from txt                            DONE
# TODO: can read all txt / print txt                     DONE
# TODO: Use w+ mode                                      DONE
# TODO: toplam rank puani ile eslsme
# TODO: rastgele eslesme                                 DONE
# TODO: Autofill
# TODO: Rank Siralama
# TODO: takim eslesmeleri


menu = """
Bilkent LoL E-Sport Team Finder by Can

Command List:
-Type 'menu' to bring this command menu.
-Type 'txt' to change/create the text file. Only enter the name of the file, 
not the (.) extension. Ex: not 'players.txt' --> 'players'

-Type 'see' to see raw text file for all player roles/names.
-Type 'number' to see numbered version of text file for all player roles/names.

-Type 'add' to enter additional players to the player list. Type the player roles and names. --> Ex: 'ADC Can'
-Type 'stop' to exit from player inputting.
-Type 'del' to delete players using the 'number' command and typing their player number.

-Type 'start' to create teams.

-Type 'quit' to exit from program.
"""


def numbered_print(file):
    result = ""
    file_handler = open(file, "r")
    for el, start_num in enumerate(file_handler.readlines(), 1):
        start_num = start_num.strip()

        result += "{} {}\n".format(el, start_num)
    player_data.close()

    return result


print(menu)

default = input("Enter text file name to begin!(Ex: 'players'): ")
full_default = str(default) + ".txt"
full_file_name = full_default
file_output = "'{}' will be created/opened and used.".format(full_file_name)
print(file_output)
print('')

inp = input('Enter Command: ')

while inp.lower() != 'quit':

    top = []
    jg = []
    mid = []
    adc = []
    sup = []

    if inp.lower() == 'txt':
        file_name = input("Use another text file!(Ex: 'tourney2'): ")
        full_file_name = str(file_name) + ".txt"
        file_output = "'{}' will be created/opened and used.".format(full_file_name)
        print(file_output)
        print('')

    # Create TXT File with new name if there is none
    # player_data = open(full_file_name, "w+")
    # player_data.close()

    try:
        player_data = open(full_file_name, "r")
        player_data.close()
    except FileNotFoundError:
        player_data = open(full_file_name, "w")
        player_data.close()

    # Check if file is empty
    player_data = open(full_file_name, "r")
    content = player_data.readline()
    if content == "":
        no_content = True
    else:
        no_content = False
    player_data.close()

    # Make Sure TXT ends with \n in an old file
    if not no_content:
        new_line = False
        player_data = open(full_file_name, "r")
        last_line = (list(player_data)[-1])

        if last_line[-1:] == '\n':
            new_line = True
        else:
            new_line = False
        player_data.close()

        player_data = open(full_file_name, "a")
        if not new_line:
            player_data.write('\n')
        player_data.close()

    # Read Data
    player_data = open(full_file_name, "r")

    for player in player_data:
        pos = player.find(' ')
        if player[:pos].lower() == 'top':
            top.append(player[pos + 1: len(player) - 1])
        elif player[:pos].lower() == 'jg':
            jg.append(player[pos + 1: len(player) - 1])
        elif player[:pos].lower() == 'mid':
            mid.append(player[pos + 1: len(player) - 1])
        elif player[:pos].lower() == 'adc':
            adc.append(player[pos + 1: len(player) - 1])
        elif player[:pos].lower() == 'sup':
            sup.append(player[pos + 1: len(player) - 1])

    player_data.close()

    # Menu
    if inp.lower() == 'menu':
        print(menu)

    # Ask for additional input
    elif inp.lower() == 'add':

        player_data = open(full_file_name, "a")

        print('')
        addition = input("Add 'Role Name': ")

        while addition.lower() != "stop":

            # Input Validation
            valid = addition.find(' ')
            if addition[:valid].lower() == 'top':
                player_data.write(addition + "\n")
            elif addition[:valid].lower() == 'jg':
                player_data.write(addition + "\n")
            elif addition[:valid].lower() == 'mid':
                player_data.write(addition + "\n")
            elif addition[:valid].lower() == 'adc':
                player_data.write(addition + "\n")
            elif addition[:valid].lower() == 'sup':
                player_data.write(addition + "\n")
            else:
                print('Invalid Role!')

            addition = input("Add 'Role Name': ")

        player_data.close()

        print('')

    # See TXT File RAW
    elif inp.lower() == 'see':
        player_data = open(full_file_name, "r")
        for line in player_data:
            content = line.strip()
            print(content)
        player_data.close()

    # See TXT File Numbered
    elif inp.lower() == 'number':
        print(numbered_print(full_file_name))

    # TXT Input
    elif inp.lower() == 'txt':
        pass

    # Deleting players
    elif inp.lower() == 'del':
        delete_players = open(full_file_name, "r")

        temp_list = []
        del_list = []

        del_pl = input("Enter player numbers to delete, separated by spaces: ")
        for j in del_pl.split():
            del_list.append(j)
        del_list.sort(reverse=True)

        for line in delete_players:
            temp_list.append(line.strip())

        for i in del_list:
            try:
                temp_list.pop(int(i) - 1)
            except IndexError:
                print('There is no player with number {}'.format(i))

        delete_players.close()

        new_file = open(full_file_name, "w")
        for k in temp_list:
            new_file.write(k + '\n')

        new_file.close()

    # Create Teams W/O AutoFill
    elif inp.lower() == 'start':
        max_team_num = min(len(top), len(jg), len(mid), len(adc), len(sup))
        print('')
        print('Max team number is', max_team_num)
        print('')

        for num in range(1, max_team_num + 1):
            # t = random.randint(0, len(top) - 1)
            t = random.randint(0, len(top) - 1) if len(top) > 1 else 0
            j = random.randint(0, len(jg) - 1) if len(jg) > 1 else 0
            m = random.randint(0, len(mid) - 1) if len(mid) > 1 else 0
            a = random.randint(0, len(adc) - 1) if len(adc) > 1 else 0
            s = random.randint(0, len(sup) - 1) if len(sup) > 1 else 0

            print("Team {}\n"
                  "Top    : {}\n"
                  "Jg     : {}\n"
                  "Mid    : {}\n"
                  "ADC    : {}\n"
                  "Sup    : {}".format(num, top[t], jg[j], mid[m], adc[a], sup[s]))
            print('')

            top.pop(t)
            jg.pop(j)
            mid.pop(m)
            adc.pop(a)
            sup.pop(s)

        print("Left Players: ")

        # Number of roles
        ntop, njg, nmid, nadc, nsup = 0, 0, 0, 0, 0
        for top in top:
            print("Top    : {}".format(top))
            ntop += 1
        for jg in jg:
            print("Jg     : {}".format(jg))
            njg += 1
        for mid in mid:
            print("Mid    : {}".format(mid))
            nmid += 1
        for adc in adc:
            print("ADC    : {}".format(adc))
            nadc += 1
        for sup in sup:
            print("Sup    : {}".format(sup))
            nsup += 1

        # Number of Remaining Roles to Create Perfect Teams
        potential_max = max(ntop, njg, nmid, nadc, nsup)
        rtop, rjg, rmid = potential_max - ntop, potential_max - njg, potential_max - nmid
        radc, rsup = potential_max - nadc, potential_max - nsup

        if (ntop and njg and nmid and nadc and nsup) == 0:
            print('')
            print("{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are not in a team.".format(ntop, njg, nmid,
                                                                                                    nadc, nsup))
            print('')
            print("{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are needed to create {} more teams."
                  .format(rtop, rjg, rmid, radc, rsup, potential_max))
            print('No AutoFills!')
        else:
            print("No leftover players.")

        print('')

    # Create Teams W AutoFill
    elif inp.lower() == 'start autofill':

        max_team_num_w_af = (len(top) + len(jg) + len(mid) + len(adc) + len(sup)) // 5

        ntop, njg, nmid, nadc, nsup = len(top), len(jg), len(mid), len(adc), len(sup)
        rtop, rjg, rmid, radc, rsup = 0, 0, 0, 0, 0
        fit_top, fit_jg, fit_mid, fit_adc, fit_sup = 0, 0, 0, 0, 0

        # Fit number of roles // Number of Remaining additional roles
        if ntop >= max_team_num_w_af:
            fit_top = max_team_num_w_af
            rtop = ntop - fit_top
        else:
            fit_top = ntop
            rtop = 0

        if njg >= max_team_num_w_af:
            fit_jg = max_team_num_w_af
            rjg = njg - fit_jg
        else:
            fit_jg = njg
            rjg = 0

        if nmid >= max_team_num_w_af:
            fit_mid = max_team_num_w_af
            rmid = nmid - fit_mid
        else:
            fit_mid = nmid
            rmid = 0

        if nadc >= max_team_num_w_af:
            fit_adc = max_team_num_w_af
            radc = nadc - fit_adc
        else:
            fit_adc = nadc
            radc = 0

        if nsup >= max_team_num_w_af:
            fit_sup = max_team_num_w_af
            rsup = nsup - fit_sup
        else:
            fit_sup = nsup
            rsup = 0

        players_on_role = fit_top + fit_jg + fit_mid + fit_adc + fit_sup
        players_auto_filled = max_team_num_w_af * 5 - players_on_role
        auto_fills_for_each_game = players_auto_filled / max_team_num_w_af
        out_of_game = rtop + rjg + rmid + radc + rsup - players_auto_filled

        # print(ntop, njg, nmid, nadc, nsup)
        # print(fit_top, fit_jg, fit_mid, fit_adc, fit_sup)
        # print(rtop, rjg, rmid, radc, rsup)

        print('')
        print('Max team number with auto-fills is', max_team_num_w_af)
        print('{} players on role, {} players auto-filled, and {} players out of game'.format(players_on_role,
                                                                                              players_auto_filled,
                                                                                              out_of_game))

        if players_auto_filled % max_team_num_w_af == 0:
            print('{} auto-filled players for each team'.format(int(auto_fills_for_each_game)))
        else:
            print('{} or {} auto-filled players for each team'.format(math.floor(auto_fills_for_each_game),
                                                                      math.ceil(auto_fills_for_each_game)))

        print('')

        auto_fill_list = []

        if rtop != 0:
            for i in range(rtop):
                t = random.randint(0, len(top) - 1) if len(top) > 1 else 0
                auto_fill_list.append("top " + top[t])
                top.pop(t)
        if rjg != 0:
            for i in range(rjg):
                j = random.randint(0, len(jg) - 1) if len(jg) > 1 else 0
                auto_fill_list.append("jg " + jg[j])
                jg.pop(j)
        if rmid != 0:
            for i in range(rmid):
                m = random.randint(0, len(mid) - 1) if len(mid) > 1 else 0
                auto_fill_list.append("mid " + mid[m])
                mid.pop(m)
        if radc != 0:
            for i in range(radc):
                a = random.randint(0, len(adc) - 1) if len(adc) > 1 else 0
                auto_fill_list.append("adc " + adc[a])
                adc.pop(a)
        if rsup != 0:
            for i in range(rsup):
                s = random.randint(0, len(sup) - 1) if len(sup) > 1 else 0
                auto_fill_list.append("sup " + sup[s])
                sup.pop(s)

        print(top, jg, mid, adc, sup, auto_fill_list)


        # kalan 3 yere esit bir sekilde autofill doldur
        # takimlari floor ceil max sayifa autofill olacak sekilde dagit printle
        # autofillden kalanlari leftover players olarak goster

    # Else
    else:
        print('Invalid Command!')
        print('')

    inp = input('Enter Command: ')

print('Good Bye!')

"""
for num in range(1, max_team_num_w_af + 1):
    # t = random.randint(0, len(top) - 1)
    t = random.randint(0, len(top) - 1) if len(top) > 1 else 0
    j = random.randint(0, len(jg) - 1) if len(jg) > 1 else 0
    m = random.randint(0, len(mid) - 1) if len(mid) > 1 else 0
    a = random.randint(0, len(adc) - 1) if len(adc) > 1 else 0
    s = random.randint(0, len(sup) - 1) if len(sup) > 1 else 0

    print("Team {}\n"
          "Top    : {}\n"
          "Jg     : {}\n"
          "Mid    : {}\n"
          "ADC    : {}\n"
          "Sup    : {}".format(num, top[t], jg[j], mid[m], adc[a], sup[s]))
    print('')

    top.pop(t)
    jg.pop(j)
    mid.pop(m)
    adc.pop(a)
    sup.pop(s)

print("Left Players: ")

# Number of roles
ntop, njg, nmid, nadc, nsup = 0, 0, 0, 0, 0
for top in top:
    print("Top    : {}".format(top))
    ntop += 1
for jg in jg:
    print("Jg     : {}".format(jg))
    njg += 1
for mid in mid:
    print("Mid    : {}".format(mid))
    nmid += 1
for adc in adc:
    print("ADC    : {}".format(adc))
    nadc += 1
for sup in sup:
    print("Sup    : {}".format(sup))
    nsup += 1

# Number of Remaining Roles to Create Perfect Teams
potential_max = max(ntop, njg, nmid, nadc, nsup)
rtop, rjg, rmid = potential_max - ntop, potential_max - njg, potential_max - nmid
radc, rsup = potential_max - nadc, potential_max - nsup

if (ntop and njg and nmid and nadc and nsup) == 0:
    print('')
    print("{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are not in a team.".format(ntop, njg, nmid,
                                                                                            nadc, nsup))
    print('')
    print("{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are needed to create {} more teams."
          .format(rtop, rjg, rmid, radc, rsup, potential_max))
    print('No AutoFills!')
else:
    print("No leftover players.")

print('')
"""