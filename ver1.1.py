import random
import math
import csv

# TODO: file ismi degistirebilme secebilme txt dosyasi   DONE
# TODO: delete users from txt                            DONE
# TODO: can read all txt / print txt                     DONE
# TODO: Use w+ mode                                      DONE BUT NOT USED
# TODO: toplam rank puani ile eslsme
# TODO: rastgele eslesme                                 DONE
# TODO: Autofill                                         DONE
# TODO: Rank Siralama
# TODO: takim eslesmeleri
# TODO: secondary roles
# TODO: text output
# TODO: csv create add ekle


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

-Type 'start' to create teams. Players are put only on their primary roles, NO auto-fills.

-Type 'start autofill' to create teams. Maximum number of players are put on their primary roles, 
left over players are auto-filled. (Secondary Role selection will come in the future. With this feature 
players will be auto-filled according to their secondary role.)

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

full_file_name = ""
txt_or_csv = input("Start with txt or csv file? ")
while True:
    if txt_or_csv.lower() == "txt":
        default = input("Enter text file name to begin!(Ex: 'players'): ")
        full_default = str(default) + ".txt"
        full_file_name = full_default
        file_output = "'{}' will be created/opened and used.".format(full_file_name)
        print(file_output)
        print('')
        break

    elif txt_or_csv.lower() == "csv":
        csv_file_name = input("Enter a csv file to read roles/nicknames from!(Ex: 'tourney5docs'): ")
        csv_full_file_name = str(csv_file_name) + ".csv"
        csv_file_print_output = "'{}' will be opened and its information used.".format(csv_full_file_name)
        print(csv_file_print_output)
        print('')

        csv_file = open(csv_full_file_name, "r")
        csv_reader = csv.reader(csv_file)

        next(csv_reader)

        csv_add_create = input("Create a new text file or add information to an existing text file?('create' or 'add') ")
        while True:
            if csv_add_create.lower() == "create":
                output_text_file_name = input(
                    "Enter a text file name to transfer player data from csv file!(Ex: 'tourney5docs'): ")
                output_text_file_full_name = output_text_file_name + ".txt"
                txt_file_print_output = "'{}' will be opened and its information used.".format(
                    output_text_file_full_name)
                print(txt_file_print_output)
                print('')

                output_text_file = open(output_text_file_full_name, "w")
                for line in csv_reader:
                    output_text_file.write(str(line[1]).lower() + " " + line[2] + "\n")
                break

            elif csv_add_create.lower() == "add":
                output_text_file_name = input(
                    "Enter a text file name to add player data to existing file from a csv file!(Ex: 'tourney5docs'): ")
                output_text_file_full_name = output_text_file_name + ".txt"
                txt_file_print_output = "'{}' will be opened and its information used.".format(
                    output_text_file_full_name)
                print(txt_file_print_output)
                print('')

                output_text_file = open(output_text_file_full_name, "a")
                for line in csv_reader:
                    output_text_file.write(str(line[1]).lower() + " " + line[2] + "\n")
                break

            else:
                print('Invalid input type!')
                csv_add_create = input("Create a new text file or add information to an existing text file? ")

        output_text_file.close()
        csv_file.close()
        break

    else:
        print('Invalid input type!')
        txt_or_csv = input("Start with txt or csv file? ")


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

    # CSV File
    elif inp.lower() == 'csv':
        csv_file_name = input("Enter a csv file to read roles/nicknames from!(Ex: 'tourney5docs'): ")
        csv_full_file_name = str(csv_file_name) + ".csv"
        csv_file_print_output = "'{}' will be opened and its information used.".format(csv_full_file_name)
        print(csv_file_print_output)
        print('')

        csv_file = open(csv_full_file_name, "r")
        csv_reader = csv.reader(csv_file)

        next(csv_reader)

        csv_add_create = input(
            "Create a new text file or add information to an existing text file?('create' or 'add') ")
        while True:
            if csv_add_create.lower() == "create":
                output_text_file_name = input(
                    "Enter a text file name to transfer player data from csv file!(Ex: 'tourney5docs'): ")
                output_text_file_full_name = output_text_file_name + ".txt"
                txt_file_print_output = "'{}' will be opened and its information used.".format(
                    output_text_file_full_name)
                print(txt_file_print_output)
                print('')

                output_text_file = open(output_text_file_full_name, "w")
                for line in csv_reader:
                    output_text_file.write(str(line[1]).lower() + " " + line[2] + "\n")
                break

            elif csv_add_create.lower() == "add":
                output_text_file_name = input(
                    "Enter a text file name to add player data to existing file from a csv file!(Ex: 'tourney5docs'): ")
                output_text_file_full_name = output_text_file_name + ".txt"
                txt_file_print_output = "'{}' will be opened and its information used.".format(
                    output_text_file_full_name)
                print(txt_file_print_output)
                print('')

                output_text_file = open(output_text_file_full_name, "a")
                for line in csv_reader:
                    output_text_file.write(str(line[1]).lower() + " " + line[2] + "\n")
                break

            else:
                print('Invalid input type!')
                csv_add_create = input("Create a new text file or add information to an existing text file? ")

        output_text_file.close()
        csv_file.close()
        break

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
        number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup = 0, 0, 0, 0, 0
        for top in top:
            print("Top    : {}".format(top))
            number_of_top += 1
        for jg in jg:
            print("Jg     : {}".format(jg))
            number_of_jg += 1
        for mid in mid:
            print("Mid    : {}".format(mid))
            number_of_mid += 1
        for adc in adc:
            print("ADC    : {}".format(adc))
            number_of_adc += 1
        for sup in sup:
            print("Sup    : {}".format(sup))
            number_of_sup += 1

        # Number of Remaining Roles to Create Perfect Teams
        potential_max = max(number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup)
        remaining_top, remaining_jg, remaining_mid, remaining_adc, remaining_sup = potential_max - number_of_top, \
                                                                                   potential_max - number_of_jg, \
                                                                                   potential_max - number_of_mid, \
                                                                                   potential_max - number_of_adc, \
                                                                                   potential_max - number_of_sup

        if (number_of_top and number_of_jg and number_of_mid and number_of_adc and number_of_sup) == 0:
            print('')
            print("{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are not in a team.".format(number_of_top,
                                                                                                    number_of_jg,
                                                                                                    number_of_mid,
                                                                                                    number_of_adc,
                                                                                                    number_of_sup))
            print('')
            print("{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are needed to create {} more teams."
                  .format(remaining_top, remaining_jg, remaining_mid, remaining_adc, remaining_sup, potential_max))
            print('No Auto-Fills! All players are in their primary roles!')

        else:
            print("No leftover players.")
            print('No Auto-Fills! All players are in their primary roles!')

        print('')

    # Create Teams W AutoFill
    elif inp.lower() == 'start autofill':

        max_team_num_w_af = (len(top) + len(jg) + len(mid) + len(adc) + len(sup)) // 5

        number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup = len(top), len(jg), len(mid), len(adc), len(sup)
        remaining_top, remaining_jg, remaining_mid, remaining_adc, remaining_sup = 0, 0, 0, 0, 0
        fit_top, fit_jg, fit_mid, fit_adc, fit_sup = 0, 0, 0, 0, 0

        # Fit number of roles // Number of Remaining additional roles
        if number_of_top >= max_team_num_w_af:
            fit_top = max_team_num_w_af
            remaining_top = number_of_top - fit_top
        else:
            fit_top = number_of_top
            remaining_top = 0

        if number_of_jg >= max_team_num_w_af:
            fit_jg = max_team_num_w_af
            remaining_jg = number_of_jg - fit_jg
        else:
            fit_jg = number_of_jg
            remaining_jg = 0

        if number_of_mid >= max_team_num_w_af:
            fit_mid = max_team_num_w_af
            remaining_mid = number_of_mid - fit_mid
        else:
            fit_mid = number_of_mid
            remaining_mid = 0

        if number_of_adc >= max_team_num_w_af:
            fit_adc = max_team_num_w_af
            remaining_adc = number_of_adc - fit_adc
        else:
            fit_adc = number_of_adc
            remaining_adc = 0

        if number_of_sup >= max_team_num_w_af:
            fit_sup = max_team_num_w_af
            remaining_sup = number_of_sup - fit_sup
        else:
            fit_sup = number_of_sup
            remaining_sup = 0

        players_on_role = fit_top + fit_jg + fit_mid + fit_adc + fit_sup
        players_auto_filled = max_team_num_w_af * 5 - players_on_role
        auto_fills_for_each_game = players_auto_filled / max_team_num_w_af
        out_of_game = remaining_top + remaining_jg + remaining_mid + remaining_adc + remaining_sup - players_auto_filled

        # print(number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup)
        # print(fit_top, fit_jg, fit_mid, fit_adc, fit_sup)
        # print(remaining_top, remaining_jg, remaining_mid, remaining_adc, remaining_sup)

        print('')
        print('Max team number with auto-fills is', max_team_num_w_af)
        print('{} players on role, {} players auto-filled, and {} players out of game'.format(players_on_role,
                                                                                              players_auto_filled,
                                                                                              out_of_game))

        af_floor = math.floor(auto_fills_for_each_game)
        af_ceil = math.ceil(auto_fills_for_each_game)

        if players_auto_filled % max_team_num_w_af == 0:
            print('{} auto-filled players for each team'.format(int(auto_fills_for_each_game)))
        else:
            print('{} or {} auto-filled players for each team'.format(af_floor, af_ceil))

        print('')

        auto_fill_list = []

        if remaining_top != 0:
            for i in range(remaining_top):
                t = random.randint(0, len(top) - 1) if len(top) > 1 else 0
                auto_fill_list.append("top " + top[t])
                top.pop(t)
        if remaining_jg != 0:
            for i in range(remaining_jg):
                j = random.randint(0, len(jg) - 1) if len(jg) > 1 else 0
                auto_fill_list.append("jg " + jg[j])
                jg.pop(j)
        if remaining_mid != 0:
            for i in range(remaining_mid):
                m = random.randint(0, len(mid) - 1) if len(mid) > 1 else 0
                auto_fill_list.append("mid " + mid[m])
                mid.pop(m)
        if remaining_adc != 0:
            for i in range(remaining_adc):
                a = random.randint(0, len(adc) - 1) if len(adc) > 1 else 0
                auto_fill_list.append("adc " + adc[a])
                adc.pop(a)
        if remaining_sup != 0:
            for i in range(remaining_sup):
                s = random.randint(0, len(sup) - 1) if len(sup) > 1 else 0
                auto_fill_list.append("sup " + sup[s])
                sup.pop(s)

        team_number = max_team_num_w_af
        teams = [[0] for i in range(max_team_num_w_af)]

        # print(top, jg, mid, adc, sup)
        # print(auto_fill_list)
        # print(teams)
        # print('')

        # Role numbers
        fix_top, fix_jg, fix_mid, fix_adc, fix_sup = 1, 2, 3, 4, 5

        # First available list
        first_available = 0
        for i in range(max_team_num_w_af):
            if teams[i][0] < af_ceil:
                first_available = i
                break

        # Top AutoFill
        if max_team_num_w_af == fit_top:
            for i in range(max_team_num_w_af):
                rand_num = random.randint(0, len(top) - 1)
                teams[i].append(top[rand_num])
                top.pop(rand_num)
        elif max_team_num_w_af > fit_top:
            for i in range(first_available, first_available + max_team_num_w_af - fit_top):
                if teams[i][0] < af_ceil:
                    rand_num = random.randint(0, len(auto_fill_list) - 1)
                    teams[i].append(auto_fill_list[rand_num])
                    teams[i][0] = teams[i][0] + 1
                    auto_fill_list.pop(rand_num)
            for j in range(max_team_num_w_af):
                try:
                    hello = teams[j][fix_top]
                except IndexError:
                    rand_num = random.randint(0, len(top) - 1)
                    teams[j].append(top[rand_num])
                    top.pop(rand_num)

        # First available list
        for i in range(max_team_num_w_af):
            if teams[i][0] < af_ceil:
                first_available = i
                break

        # Jungle AutoFill
        if max_team_num_w_af == fit_top:
            for i in range(max_team_num_w_af):
                rand_num = random.randint(0, len(jg) - 1)
                teams[i].append(jg[rand_num])
                jg.pop(rand_num)
        elif max_team_num_w_af > fit_jg:
            for i in range(first_available, first_available + max_team_num_w_af - fit_jg):
                if teams[i][0] < af_ceil:
                    rand_num = random.randint(0, len(auto_fill_list) - 1)
                    teams[i].append(auto_fill_list[rand_num])
                    teams[i][0] = teams[i][0] + 1
                    auto_fill_list.pop(rand_num)
            for j in range(max_team_num_w_af):
                try:
                    hello = teams[j][fix_jg]
                except IndexError:
                    rand_num = random.randint(0, len(jg) - 1)
                    teams[j].append(jg[rand_num])
                    jg.pop(rand_num)

        # First available list
        for i in range(max_team_num_w_af):
            if teams[i][0] < af_ceil:
                first_available = i
                break

        # Middle AutoFill
        if max_team_num_w_af == fit_mid:
            for i in range(max_team_num_w_af):
                rand_num = random.randint(0, len(mid) - 1)
                teams[i].append(mid[rand_num])
                mid.pop(rand_num)
        elif max_team_num_w_af > fit_mid:
            for i in range(first_available, first_available + max_team_num_w_af - fit_mid):
                if teams[i][0] < af_ceil:
                    rand_num = random.randint(0, len(auto_fill_list) - 1)
                    teams[i].append(auto_fill_list[rand_num])
                    teams[i][0] = teams[i][0] + 1
                    auto_fill_list.pop(rand_num)
            for j in range(max_team_num_w_af):
                try:
                    hello = teams[j][fix_mid]
                except IndexError:
                    rand_num = random.randint(0, len(mid) - 1)
                    teams[j].append(mid[rand_num])
                    mid.pop(rand_num)

        # First available list
        for i in range(max_team_num_w_af):
            if teams[i][0] < af_ceil:
                first_available = i
                break

        # ADC AutoFill
        if max_team_num_w_af == fit_adc:
            for i in range(max_team_num_w_af):
                rand_num = random.randint(0, len(adc) - 1)
                teams[i].append(adc[rand_num])
                adc.pop(rand_num)
        elif max_team_num_w_af > fit_adc:
            for i in range(first_available, first_available + max_team_num_w_af - fit_adc):
                if teams[i][0] < af_ceil:
                    rand_num = random.randint(0, len(auto_fill_list) - 1)
                    teams[i].append(auto_fill_list[rand_num])
                    teams[i][0] = teams[i][0] + 1
                    auto_fill_list.pop(rand_num)
            for j in range(max_team_num_w_af):
                try:
                    hello = teams[j][fix_adc]
                except IndexError:
                    rand_num = random.randint(0, len(adc) - 1)
                    teams[j].append(adc[rand_num])
                    adc.pop(rand_num)

        # First available list
        for i in range(max_team_num_w_af):
            if teams[i][0] < af_ceil:
                first_available = i
                break

        # Support AutoFill
        if max_team_num_w_af == fit_sup:
            for i in range(max_team_num_w_af):
                rand_num = random.randint(0, len(sup) - 1)
                teams[i].append(sup[rand_num])
                sup.pop(rand_num)
        elif max_team_num_w_af > fit_sup:
            for i in range(first_available, first_available + max_team_num_w_af - fit_sup):
                if teams[i][0] < af_ceil:
                    rand_num = random.randint(0, len(auto_fill_list) - 1)
                    teams[i].append(auto_fill_list[rand_num])
                    teams[i][0] = teams[i][0] + 1
                    auto_fill_list.pop(rand_num)
            for j in range(max_team_num_w_af):
                try:
                    hello = teams[j][fix_sup]
                except IndexError:
                    rand_num = random.randint(0, len(sup) - 1)
                    teams[j].append(sup[rand_num])
                    sup.pop(rand_num)

        # print(teams)
        # print(auto_fill_list)

        for k in range(0, max_team_num_w_af):
            player1, player2, player3, player4, player5 = teams[k][1], teams[k][2], teams[k][3], teams[k][4], teams[k][5]
            player_list = [player1, player2, player3, player4, player5]
            show_list = []

            for player in player_list:

                player = str(player)
                af_pos = player.find(' ')
                if player[:af_pos].lower() == 'top':
                    player = player[af_pos + 1: len(player)] + " (Auto-Fill Top)"
                elif player[:af_pos].lower() == 'jg':
                    player = player[af_pos + 1: len(player)] + " (Auto-Fill Jungle)"
                elif player[:af_pos].lower() == 'mid':
                    player = player[af_pos + 1: len(player)] + " (Auto-Fill Mid)"
                elif player[:af_pos].lower() == 'adc':
                    player = player[af_pos + 1: len(player)] + " (Auto-Fill ADC)"
                elif player[:af_pos].lower() == 'sup':
                    player = player[af_pos + 1: len(player)] + " (Auto-Fill Support)"
                show_list.append(player)

            print("Team {}\n"
                  "Top    : {}\n"
                  "Jg     : {}\n"
                  "Mid    : {}\n"
                  "ADC    : {}\n"
                  "Sup    : {}".format(k + 1, show_list[0], show_list[1], show_list[2], show_list[3], show_list[4]))
            print('')

        if len(auto_fill_list) > 0:
            print("Leftover players:")
            for i in auto_fill_list:
                print(i)

        print('')

    # Else
    else:
        print('Invalid Command!')
        print('')

    inp = input('Enter Command: ')

print('Good Bye!')