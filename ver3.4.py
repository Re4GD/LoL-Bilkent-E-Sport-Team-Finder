import random
import math
import csv
import time
# import copy

modes = """
Bilkent LoL E-Sport Team Finder by Can Gürsu and Yunus Özkan!

-This program is created for players to find teams. There are 7 modes to this script:
Mode 1:  Primary Roles, NO Secondary Roles, NO Auto-Fills, and NO Rank Consideration. (start p)
Mode 2:  Primary Roles, NO Secondary Roles,    Auto-Fills, and NO Rank Consideration  (start pa)
Mode 3:  Primary Roles,    Secondary Roles, NO Auto-Fills, and NO Rank Consideration. (start ps)
Mode 4a: Primary Roles,    Secondary Roles,    Auto-Fills, and NO Rank Consideration. (start psa)
Mode 4b: Primary Roles,    Secondary Roles,    Auto-Fills, and NO Rank Consideration. (start psa yunus)
Mode 5a: Primary Roles, NO Secondary Roles, NO Auto-Fills, and    Rank Consideration. (start pr old)
Mode 5b: Primary Roles, NO Secondary Roles, NO Auto-Fills, and    Rank Consideration. (start pr mmr)
Mode 6:  Primary Roles,    Secondary Roles, NO Auto-Fills, and    Rank Consideration. (start psr mmr)
Mode 7:  Primary Roles,    Secondary Roles,    Auto-Fills, and    Rank Consideration. (start psar yunus)
-User can use a formatted text file to create teams, or choose a csv file to convert to 
a formatted text file.
-User can see the 'raw', 'numbered' and 'bilkent numbered' versions of the formatted text file, or Users can search 
by keywords to find mail, nick, fullname, primary and secondary roles of players.
-User can manually add or delete player data.
"""

menu = """
Command List:
-Type 'menu' to bring this command menu.
-Type 'modes' to bring the modes menu.

-Type 'txt' to change/create the text file. Only enter the name of the file, 
not the (.) extension. Ex: not 'players.txt' --> 'players'
-Type 'csv' to select a csv file to use its data. The program will ask to 
create a new text file or add data to existing text file. Only enter the name of the file, 
not the (.) extension. Ex: not 'tourney_input.csv' --> 'tourney_input'

-Type 'see' to see raw text file for all player roles/names.
-Type 'number' to see numbered version of text file for all player roles/names.
-Type 'bilkent number' to see numbered version of text file for players that have Bilkent Mail.
-Type 'mail' to enter keywords to look for player mail. 
-Type 'nick' to enter keywords to look for player nick.
-Type 'fullname' to enter keywords to look for player fullname.
-Type 'primary' to look for players by primary role.
-Type 'secondary' to look for players by secondary role.

-Type 'add' to enter additional players to the player list. Type the player roles and names.
Input Formatting: (Mail,Nick,Fullname,Rank,Primary,Secondary)
-Type 'stop' to exit from player inputting.
-Type 'del' to delete players using the 'number' command and typing their number. --> Ex: '4 16 7' 

-Type 'quit' to save data and exit from program. Program might not work properly if it is not 
exited this way.
"""

add_info = """
Input Format: Mail,Nick,Name_Surname,Rank,Primary,Secondary
Mail has to have '@ug.bilkent.edu.tr' in it.
Players cannot have the same email.
Roles have to be either 'Top' or 'Jg' or 'Mid' or 'Adc' or 'Sup'.
"""

# deleted_info = """
# -Type 'start' to create teams. Players are put only on their primary roles.
# NO Secondary Roles, NO Auto-Fills, NO Rank Consideration.
#
# -Type 'start autofill' to create teams. Maximum number of players are put on their primary roles,
# left over players are auto-filled randomly.
# NO Secondary Roles, Random Auto-Fills, NO Rank Consideration.
#
# -Type 'start ranked' to create ranked teams. Players are put only on their primary roles. Enter a tolerance
# to determine a rank gap. Lower the tolerance, closer the total team ranks will be/harder for the program to create
# teams if number of competitors is small.
# NO Secondary Roles, NO Auto-Fills, Rank Consideration.
# """


def raw_print(txt_file):
    """
    Take some .txt file and print the players in it.
    """
    result = ""
    with open(txt_file, "r") as file_handler:
        for line_el in file_handler:
            if line_el != "\n":
                result += "{}\n".format(line_el.strip())

    return result


def numbered_print(txt_file):
    """
    Take some .txt file and print the players with numbers next to them.
    """
    result = ""
    with open(txt_file, "r") as file_handler:
        for start_num, el in enumerate(file_handler.readlines(), 1):
            if el != "\n":
                el = el.strip()
                result += "{} {}\n".format(start_num, el)
    return result


def bilkent_numbered_print(txt_file):
    """
    Take some .txt file and print the players that have Bilkent mails with numbers next to them.
    """
    result = ""
    correct_num = 0
    with open(txt_file, "r") as file_handler:
        for start_num, el in enumerate(file_handler.readlines(), 1):
            if el != "\n" and "@ug.bilkent.edu.tr" in el:
                el = el.strip()
                result += "{} {}\n".format(start_num - correct_num, el)
            else:
                correct_num += 1
    return result


def does_file_exist(txt_file):
    """
    Look if the file exists, if it does not exist create one. (Only txt files)
    """
    try:
        txt_data = open(txt_file, "r")
        txt_data.close()
    except FileNotFoundError:
        print("'{}' was not found!".format(txt_file))
        if '.csv' not in txt_file:
            txt_data = open(txt_file, "w")
            txt_data.close()
        return False
    else:
        return True


def convert_to_type_fullname(file_type):
    """
    Take some file 'name', if the file exists make it name.txt or name.csv
    """
    full_name, usr_inp_txt, usr_inp_csv = "", "", ""
    does_exist = False
    while not does_exist:
        if file_type == "txt":
            usr_inp_txt = input("Enter text file name to look player data from!(Ex: 'players'): ")
            if usr_inp_txt.lower() == 'quit':
                return 'quit'
            full_name = str(usr_inp_txt) + ".txt"
            if does_file_exist(full_name):
                print("'{}' will be opened and used.\n".format(full_name))
                does_exist = True
            else:
                print("'{}' will be created and used.\n".format(full_name))
                does_exist = True

        elif file_type == "csv":
            usr_inp_csv = input("Enter a csv file to read roles/nicknames from!(Ex: 'tourney5docs'): ")
            if usr_inp_csv.lower() == 'quit':
                return 'quit'
            full_name = str(usr_inp_csv) + ".csv"
            if does_file_exist(full_name):
                print("'{}' will be opened and its information used.\n".format(full_name))
                does_exist = True

    return full_name


def convert_csv_to_txt(mode):
    """
    Take a csv file name, convert it to name.csv
    Open that csv file and add its content to a txt file.
    During the process, create a new txt file or add to an existing one.
    """
    csv_full_file_name = convert_to_type_fullname("csv")
    if csv_full_file_name == 'quit':
        global converted_to_txt
        converted_to_txt = 'quit'
        return '\nClosing.'
    else:
        usr_inp_txt = input("Enter a text file name to transfer player data from csv file!(Ex: 'tourney5docs'): ")
        full_name = str(usr_inp_txt) + ".txt"
        print("'{}' will be opened!\n".format(full_name))

        result = ""
        with open(csv_full_file_name, "r") as csv_file_player_data:
            csv_file_reader = csv.reader(csv_file_player_data)
            next(csv_file_reader)

            with open(full_name, mode) as output_text:
                csv_counter = 1  # 1=Mail, 2=Nick, 3=Name Surname, 4=Rank, 5=Primary, 6=Secondary
                for line_el in csv_file_reader:
                    if line_el:
                        line_el[csv_counter] = line_el[csv_counter].replace(" ", "_")  # Mail

                        line_el[csv_counter + 1] = line_el[csv_counter + 1].replace(" ", "_")  # Nick

                        line_el[csv_counter + 2] = line_el[csv_counter + 2].replace(" ", "_")  # Name Surname

                        player_info = (line_el[csv_counter] + "," + line_el[csv_counter + 1] + "," +
                                       line_el[csv_counter + 2] + "," + line_el[csv_counter + 3] + "," +
                                       line_el[csv_counter + 4] + "," + line_el[csv_counter + 5] + "\n")

                        # print(player_info)

                        output_text.write(player_info)

            converted_to_txt = full_name

            if mode == "w":
                result = "Player data from {} transferred to {} successfully!\n".format(csv_full_file_name, full_name)
            elif mode == "a":
                result = "Player data from {} added to {} successfully!\n".format(csv_full_file_name, full_name)

        return result


def is_empty(txt_file):
    """
    Check if a txt file is empty
    """
    with open(txt_file, "r") as player_data_content:
        content = player_data_content.read()
        if content == "":
            return True
        return False


def does_end_with_newline(txt_file):
    """
    If an existing file does not end with a newline return False, else return True.
    """
    with open(txt_file, "r") as player_data_newline:
        last_line = (list(player_data_newline)[-1])
        if last_line[-1:] == '\n':
            return True
        else:
            return False


def add_newline(txt_file):
    """
    If does_end_with_newline() == False, add one newline.
    """
    with open(txt_file, "a") as player_data_newline:
        if not does_end_with_newline(txt_file):
            player_data_newline.write('\n')


def end_with_multiple_newline(txt_file):
    """
    If name.txt ends with multiple newlines, leave one newline.
    """
    found_char = False
    char_counter = -1
    with open(txt_file, "r") as player_data_newline:
        newline_data = player_data_newline.read()

        while not found_char:
            if newline_data[char_counter - 1: char_counter] == "\n":
                char_counter -= 1
            else:
                found_char = True

    if char_counter != -1:
        with open(txt_file, "w") as player_data_newline:
            # NEWLINE_COUNT = abs(char_counter)
            newline_data = newline_data[:char_counter + 1]
            player_data_newline.write(newline_data)


def is_output_wanted():
    """
    Ask if user wants a text output .
    """
    ask_output_text_bool = input('Write the results to a text file? (yes or no): ')
    while True:
        if ask_output_text_bool.lower() == 'yes':
            return True
        elif ask_output_text_bool.lower() == 'no':
            return False
        else:
            print('Invalid input!')
            ask_output_text_bool = input('Write the results to a text file? (yes or no): ')


def take_output_name():
    """
    Get output text file name.
    """
    output_text_name = input("Enter a file name to output team data (Ex: 'output'): ")
    output_text_fullname = output_text_name + ".txt"
    print("'{}' will be created/opened and team data will be written on it.\n"
          .format(output_text_fullname))
    return output_text_fullname


def find_from_mail(p_dict, inp):
    """
    Find player data by mail.
    """
    result = ""
    for key in p_dict:
        if inp in key.lower():
            result += "{:35s}\t--> {}\n".format(key, p_dict[key])
    if result != "":
        return result
    else:
        return "This Mail Does Not Exist In The List!\n"


def find_from_nick(p_dict, inp):
    """
    Find player data by nick.
    """
    result = ""
    for key in p_dict:
        if inp in p_dict[key][0].lower():
            result += "{:35s}\t--> {}\n".format(key, p_dict[key])
    if result != "":
        return result
    else:
        return "This Nick Does Not Exist In The List!\n"


def find_from_fullname(p_dict, inp):
    """
    Find player data by fullname.
    """
    result = ""
    for key in p_dict:
        if inp in p_dict[key][1].lower():
            result += "{:35s}\t--> {}\n".format(key, p_dict[key])
    if result != "":
        return result
    else:
        return "This Name Does Not Exist In The List!\n"


def find_from_primary(p_dict, inp):
    """
    Find player data by primary role.
    """
    result = ""
    if inp.lower() != "top" and inp.lower() != "jg" and inp.lower() != "mid" and inp.lower() != "adc" \
            and inp.lower() != "sup":
        return "This Role Does Not Exist!\n"

    for key in p_dict:
        if inp.lower() == p_dict[key][3].lower():
            result += "{:35s}\t--> {}\n".format(key, p_dict[key])
    if result != "":
        return result
    else:
        return "There are no players with this primary role!\n"


def find_from_secondary(p_dict, inp):
    """
    Find player data by secondary role.
    """
    result = ""
    if inp.lower() != "top" and inp.lower() != "jg" and inp.lower() != "mid" and inp.lower() != "adc" \
            and inp.lower() != "sup":
        return "This Role Does Not Exist!\n"

    for key in p_dict:
        if inp.lower() == p_dict[key][4].lower():
            result += "{:35s}\t--> {}\n".format(key, p_dict[key])
    if result != "":
        return result
    else:
        return "There are no players with this secondary role!\n"


def change_mail(txt_file, old, new):
    """
    Change player mail.
    """
    result = ""
    with open(txt_file, "r") as ch_mail:
        mail_data = ch_mail.read()
        if old in mail_data:
            mail_data = mail_data.replace(old, new)
            result += "The old mail: '{}' changed to the new mail: '{}'\n".format(old, new)
        else:
            return "There is no player with this old mail!\n"

    with open(txt_file, "w") as ch_mail:
        ch_mail.write(mail_data)

    return result


print(modes)
print(menu)

full_file_name = ""
txt_or_csv = input("Start with txt or csv file? ").lower()

# Beginning TXT or CSV question
while txt_or_csv != 'quit':
    if txt_or_csv.strip() == "txt":
        full_file_name = convert_to_type_fullname("txt")
        break

    elif txt_or_csv.strip() == "csv":

        csv_add_create = input(
            "Create a new text file or add information to an existing text file?('create' or 'add') ")
        while csv_add_create != "quit":
            if csv_add_create.lower() == "create":
                print()
                print(convert_csv_to_txt("w"))
                full_file_name = converted_to_txt
                break

            elif csv_add_create.lower() == "add":
                print()
                print(convert_csv_to_txt("a"))
                full_file_name = converted_to_txt
                break

            else:
                print('Invalid input type!\n')
                csv_add_create = input("Create a new text file or add information to an existing text file? ")
        break

    else:
        print('Invalid input type!\n')
        txt_or_csv = input("Start with txt or csv file? ").lower()

# If beginning TXT or CSV question is QUIT
main_loop_inp = ""
first_time = True
if txt_or_csv == full_file_name == 'quit':
    main_loop_inp = 'quit'

# Main While Loop
while main_loop_inp != 'quit':

    # Primary Role Lists
    top, jg, mid, adc, sup = [], [], [], [], []
    # Secondary Role Lists
    sec_top, sec_jg, sec_mid, sec_adc, sec_sup = [], [], [], [], []
    # Primary Role Lists With Ranks
    rank_top, rank_jg, rank_mid, rank_adc, rank_sup = [0], [0], [0], [0], [0]
    # Secondary Role Lists With Ranks
    rank_sec_top, rank_sec_jg, rank_sec_mid, rank_sec_adc, rank_sec_sup = [0], [0], [0], [0], [0]

    if main_loop_inp.strip() == 'txt':
        full_file_name = convert_to_type_fullname("txt")

    # Create TXT File with new name if there is none
    try:
        with open(full_file_name, "r") as player_data:
            pass
    except FileNotFoundError:
        with open(full_file_name, "w") as player_data:
            pass

    # Check if file is empty and Make Sure TXT ends with \n in an old file
    if not is_empty(full_file_name):
        if does_end_with_newline(full_file_name):
            end_with_multiple_newline(full_file_name)
        else:
            add_newline(full_file_name)

    # Read Data
    with open(full_file_name, "r") as player_data_read:

        rank_point = 0
        player_dict = {}
        data = ""

        for line in player_data_read:
            # Create Player Dictionary
            data = line.strip().split(",")
            if "@ug.bilkent.edu.tr" in data[0]:
                player_dict[data[0]] = [data[1], data[2], data[3], data[4], data[5]]

                # Append to Primary Roles
                if player_dict[data[0]][3].lower() == 'top':
                    top.append(data[0])
                elif player_dict[data[0]][3].lower() == 'jg':
                    jg.append(data[0])
                elif player_dict[data[0]][3].lower() == 'mid':
                    mid.append(data[0])
                elif player_dict[data[0]][3].lower() == 'adc':
                    adc.append(data[0])
                elif player_dict[data[0]][3].lower() == 'sup':
                    sup.append(data[0])

                # Append to Secondary Roles
                if player_dict[data[0]][4].lower() == 'top':
                    sec_top.append(data[0])
                elif player_dict[data[0]][4].lower() == 'jg':
                    sec_jg.append(data[0])
                elif player_dict[data[0]][4].lower() == 'mid':
                    sec_mid.append(data[0])
                elif player_dict[data[0]][4].lower() == 'adc':
                    sec_adc.append(data[0])
                elif player_dict[data[0]][4].lower() == 'sup':
                    sec_sup.append(data[0])

                # Calculate Rank
                if player_dict[data[0]][2].lower() == 'iron':
                    rank_point = 1
                elif player_dict[data[0]][2].lower() == 'bronze':
                    rank_point = 2
                elif player_dict[data[0]][2].lower() == 'silver':
                    rank_point = 3
                elif player_dict[data[0]][2].lower() == 'gold':
                    rank_point = 4
                elif player_dict[data[0]][2].lower() == 'platinum':
                    rank_point = 5
                elif player_dict[data[0]][2].lower() == 'diamond':
                    rank_point = 6
                elif player_dict[data[0]][2].lower() == 'master':
                    rank_point = 7
                elif player_dict[data[0]][2].lower() == 'grandmaster':
                    rank_point = 8
                elif player_dict[data[0]][2].lower() == 'challenger':
                    rank_point = 9

                # Append To Rank Primary
                if player_dict[data[0]][3].lower() == 'top':
                    rank_top.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][3].lower() == 'jg':
                    rank_jg.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][3].lower() == 'mid':
                    rank_mid.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][3].lower() == 'adc':
                    rank_adc.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][3].lower() == 'sup':
                    rank_sup.append(data[0] + " " + str(rank_point))

                # Append To Rank Secondary
                if player_dict[data[0]][4].lower() == 'top':
                    rank_sec_top.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][4].lower() == 'jg':
                    rank_sec_jg.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][4].lower() == 'mid':
                    rank_sec_mid.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][4].lower() == 'adc':
                    rank_sec_adc.append(data[0] + " " + str(rank_point))
                elif player_dict[data[0]][4].lower() == 'sup':
                    rank_sec_sup.append(data[0] + " " + str(rank_point))

        # print(player_dict)
        # print()
        # print(top, jg, mid, adc, sup)
        # print(sec_top, sec_jg, sec_mid, sec_adc, sec_sup)
        # print(rank_top, rank_jg, rank_mid, rank_adc, rank_sup)
        # print(rank_sec_top, rank_sec_jg, rank_sec_mid, rank_sec_adc, rank_sec_sup)

    # Menu
    if main_loop_inp.strip() == 'menu':
        print(menu)

    # Modes
    elif main_loop_inp.strip() == 'modes':
        print(modes)

    # See TXT File RAW
    elif main_loop_inp.strip() == 'see':
        print(raw_print(full_file_name))

    # See TXT File Numbered
    elif main_loop_inp.strip() == 'number':
        print(numbered_print(full_file_name))

    # See TXT File Numbered WITH Bilkent Mails
    elif main_loop_inp.strip() == 'bilkent number':
        print(bilkent_numbered_print(full_file_name))

    # Ask for additional input
    elif main_loop_inp.strip() == 'add':

        with open(full_file_name, "a") as player_data:

            print(add_info)
            addition = input("Add Player Data(Type 'stop' to stop inputting): ")

            while addition.lower() != "stop":
                # Input Validation
                usr_info = addition.split(",")

                # Data length has to be 6
                if len(usr_info) != 6:
                    print('Invalid Player Data Amount!\n')

                # Email has to contain "@ug.bilkent.edu.tr"
                elif "@ug.bilkent.edu.tr" not in usr_info[0]:
                    print('Invalid Player Mail! Not a Bilkent Mail!\n')

                # Primary Role Inputs
                elif not (usr_info[4].lower() == 'top' or
                          usr_info[4].lower() == 'jg' or
                          usr_info[4].lower() == 'mid' or
                          usr_info[4].lower() == 'adc' or
                          usr_info[4].lower() == 'sup'):
                    print('Invalid Player Primary Role!\n')

                # Secondary Role Inputs
                elif not (usr_info[5].lower() == 'top' or
                          usr_info[5].lower() == 'jg' or
                          usr_info[5].lower() == 'mid' or
                          usr_info[5].lower() == 'adc' or
                          usr_info[5].lower() == 'sup'):
                    print('Invalid Player Secondary Role!\n')

                # Look for same mails
                elif usr_info[0] in player_dict.keys():
                    print('Invalid Player Mail! This Player Is Already On The List!\n')

                # Add to txt
                else:
                    # Mail Can Not have spaces
                    if " " in usr_info[0]:
                        usr_info[0] = usr_info[0].replace(" ", "_")

                    # Nick Can Not have spaces
                    if " " in usr_info[1]:
                        usr_info[1] = usr_info[1].replace(" ", "_")

                    # Fullname Can Not have spaces
                    if " " in usr_info[2]:
                        usr_info[2] = usr_info[2].replace(" ", "_")

                    print("--> Player Added!\n")
                    player_data.write("{},{},{},{},{},{}\n".format(usr_info[0], usr_info[1], usr_info[2],
                                                                   usr_info[3], usr_info[4], usr_info[5]))

                addition = input("Add Player Data(Type 'stop' to stop inputting): ")

        print('')

    # Find From Mail
    elif main_loop_inp.strip() == 'mail':
        mail = input("Enter keywords to look for in the player mail: ")
        print(find_from_mail(player_dict, mail))

    # Find From Nick
    elif main_loop_inp.strip() == 'nick':
        nick = input("Enter keywords to look for in the player nick: ")
        print(find_from_nick(player_dict, nick))

    # Find From Fullname
    elif main_loop_inp.strip() == 'fullname':
        fullname = input("Enter keywords to look for in the player fullname: ")
        print(find_from_fullname(player_dict, fullname))

    # Find From Primary Role
    elif main_loop_inp.strip() == 'primary':
        primary = input("Enter primary role to look for: ")
        print(find_from_primary(player_dict, primary))

    # Find From Secondary Role
    elif main_loop_inp.strip() == 'secondary':
        secondary = input("Enter secondary role to look for: ")
        print(find_from_secondary(player_dict, secondary))

    # Change Player Mail
    elif main_loop_inp.strip() == 'change mail':
        old_mail = input("Enter the old mail of the player: ")
        new_mail = input("Enter the new mail of the player: ")
        print(change_mail(full_file_name, old_mail, new_mail))

    # TXT Input
    elif main_loop_inp.strip() == 'txt':
        pass

    # CSV File
    elif main_loop_inp.strip() == 'csv':

        csv_add_create = input(
            "Create a new text file or add information to an existing text file?('create' or 'add') ")
        while csv_add_create != "quit":
            if csv_add_create.lower() == "create":
                print(convert_csv_to_txt("w"))
                break

            elif csv_add_create.lower() == "add":
                print(convert_csv_to_txt("a"))
                break

            else:
                print('Invalid input type!')
                csv_add_create = input("Create a new text file or add information to an existing text file? ")

    # Deleting players
    elif main_loop_inp.strip() == 'del':
        with open(full_file_name, "r") as delete_players:
            temp_list, del_list = [], []

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

        with open(full_file_name, "w") as new_file:
            for k in temp_list:
                new_file.write(k + '\n')

    # Create Teams Primary
    elif main_loop_inp.strip() == 'start p':

        result_text = ""
        max_team_num = min(len(top), len(jg), len(mid), len(adc), len(sup))
        players_on_role = max_team_num * 5
        out_of_game = len(top) + len(jg) + len(mid) + len(adc) + len(sup) - players_on_role

        result_text += "\nMax team number is {}\n".format(max_team_num)
        result_text += "{} players on role, and {} players out of game\n\n".format(players_on_role, out_of_game)

        for num in range(1, max_team_num + 1):
            # t = random.randint(0, len(top) - 1)
            t = random.randint(0, len(top) - 1) if len(top) > 1 else 0
            j = random.randint(0, len(jg) - 1) if len(jg) > 1 else 0
            m = random.randint(0, len(mid) - 1) if len(mid) > 1 else 0
            a = random.randint(0, len(adc) - 1) if len(adc) > 1 else 0
            s = random.randint(0, len(sup) - 1) if len(sup) > 1 else 0

            display_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[top[t]][0], player_dict[top[t]][1], top[t])
            display_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[jg[j]][0], player_dict[jg[j]][1], jg[j])
            display_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[mid[m]][0], player_dict[mid[m]][1], mid[m])
            display_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[adc[a]][0], player_dict[adc[a]][1], adc[a])
            display_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[sup[s]][0], player_dict[sup[s]][1], sup[s])

            result_text += "Team {}\nTop    : {}\nJg     : {}\nMid    : {}\nADC    : {}\nSup    : {} \n\n"\
                .format(num, display_top, display_jg, display_mid, display_adc, display_sup)

            top.pop(t)
            jg.pop(j)
            mid.pop(m)
            adc.pop(a)
            sup.pop(s)

        result_text += "Left Players: \n"

        # Number of roles
        number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup = 0, 0, 0, 0, 0
        for top in top:
            leftover_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[top][0], player_dict[top][1], top)
            result_text += "Top    : {}\n".format(leftover_top)
            number_of_top += 1
        for jg in jg:
            leftover_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[jg][0], player_dict[jg][1], jg)
            result_text += "Jg     : {}\n".format(leftover_jg)
            number_of_jg += 1
        for mid in mid:
            leftover_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[mid][0], player_dict[mid][1], mid)
            result_text += "Mid    : {}\n".format(leftover_mid)
            number_of_mid += 1
        for adc in adc:
            leftover_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[adc][0], player_dict[adc][1], adc)
            result_text += "ADC    : {}\n".format(leftover_adc)
            number_of_adc += 1
        for sup in sup:
            leftover_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[sup][0], player_dict[sup][1], sup)
            result_text += "Sup    : {}\n".format(leftover_sup)
            number_of_sup += 1

        # Number of Remaining Roles to Create Perfect Teams
        potential_max = max(number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup)
        remaining_top, remaining_jg, remaining_mid, remaining_adc, remaining_sup = potential_max - number_of_top, \
            potential_max - number_of_jg, potential_max - number_of_mid, potential_max - number_of_adc, \
            potential_max - number_of_sup

        if (number_of_top and number_of_jg and number_of_mid and number_of_adc and number_of_sup) == 0:

            result_text += "\n{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are not in a team.\n".format(
                number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup)

            result_text += "{} Top, {} Jungle, {} Mid, {} ADC, {} Support players are needed to create perfect " \
                           "amount of teams.\n".format(remaining_top, remaining_jg, remaining_mid,
                                                       remaining_adc, remaining_sup)

            result_text += '\nNO Auto-Fills! NO Secondary Roles! NO Ranks!\nAll players are in their primary roles!'

        else:
            result_text += "\nNo leftover players.\nNo Auto-Fills! All players are in their primary roles!"

        print(result_text)
        print('')

        if is_output_wanted():
            output_file_name = take_output_name()
            with open(output_file_name, "w") as result_output_file:
                result_output_file.write(result_text)
        else:
            print('No output file.\n')

    # Create Teams Primary AutoFill
    elif main_loop_inp == 'start pa':

        result_text = ""
        max_team_num_w_af = (len(top) + len(jg) + len(mid) + len(adc) + len(sup)) // 5

        number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup = len(top), len(jg), len(mid), \
            len(adc), len(sup)
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
        out_of_game = len(top) + len(jg) + len(mid) + len(adc) + len(sup) - players_on_role - players_auto_filled
        # out_of_game = remaining_top + remaining_jg + remaining_mid + remaining_adc + remaining_sup -
        #       players_auto_filled

        # print(number_of_top, number_of_jg, number_of_mid, number_of_adc, number_of_sup)
        # print(fit_top, fit_jg, fit_mid, fit_adc, fit_sup)
        # print(remaining_top, remaining_jg, remaining_mid, remaining_adc, remaining_sup)

        result_text += "\nMax team number with auto-fills is {}\n{} players on role, {} players auto-filled, " \
                       "and {} players out of game\n".format(max_team_num_w_af, players_on_role, players_auto_filled,
                                                             out_of_game)

        af_floor = math.floor(auto_fills_for_each_game)
        af_ceil = math.ceil(auto_fills_for_each_game)

        if players_auto_filled % max_team_num_w_af == 0:
            result_text += "{} auto-filled players for each team\n\n".format(int(auto_fills_for_each_game))
        else:
            result_text += "{} or {} auto-filled players for each team\n\n".format(af_floor, af_ceil)

        auto_fill_list = []

        # print(top, jg, mid, adc, sup)

        if remaining_top != 0:
            for i in range(remaining_top):
                t = random.randint(0, len(top) - 1) if len(top) > 1 else 0
                auto_fill_list.append(top[t])
                top.pop(t)
        if remaining_jg != 0:
            for i in range(remaining_jg):
                j = random.randint(0, len(jg) - 1) if len(jg) > 1 else 0
                auto_fill_list.append(jg[j])
                jg.pop(j)
        if remaining_mid != 0:
            for i in range(remaining_mid):
                m = random.randint(0, len(mid) - 1) if len(mid) > 1 else 0
                auto_fill_list.append(mid[m])
                mid.pop(m)
        if remaining_adc != 0:
            for i in range(remaining_adc):
                a = random.randint(0, len(adc) - 1) if len(adc) > 1 else 0
                auto_fill_list.append(adc[a])
                adc.pop(a)
        if remaining_sup != 0:
            for i in range(remaining_sup):
                s = random.randint(0, len(sup) - 1) if len(sup) > 1 else 0
                auto_fill_list.append(sup[s])
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
        if max_team_num_w_af == fit_jg:
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

        # print(top, jg, mid, adc, sup)
        # print(teams)
        # print(auto_fill_list)
        # print(max_team_num_w_af)

        for k in range(0, max_team_num_w_af):
            player1, player2, player3, player4, player5 = teams[k][1], teams[k][2], teams[k][3], teams[k][4], \
                                                          teams[k][5]

            nick_disp_top, nick_disp_jg, nick_disp_mid, nick_disp_adc, nick_disp_sup = player_dict[player1][0], \
                player_dict[player2][0], player_dict[player3][0], player_dict[player4][0], player_dict[player5][0]

            if player_dict[player1][3].lower() != 'top':
                nick_disp_top = "{} (Auto-Fill {})".format(player_dict[player1][0], player_dict[player1][3])
            elif player_dict[player2][3].lower() != 'jg':
                nick_disp_jg = "{} (Auto-Fill {})".format(player_dict[player2][0], player_dict[player2][3])
            elif player_dict[player3][3].lower() != 'mid':
                nick_disp_mid = "{} (Auto-Fill {})".format(player_dict[player3][0], player_dict[player3][3])
            elif player_dict[player4][3].lower() != 'adc':
                nick_disp_adc = "{} (Auto-Fill {})".format(player_dict[player4][0], player_dict[player4][3])
            elif player_dict[player5][3].lower() != 'sup':
                nick_disp_sup = "{} (Auto-Fill {})".format(player_dict[player5][0], player_dict[player5][3])

            display_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(nick_disp_top, player_dict[player1][1], player1)
            display_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(nick_disp_jg, player_dict[player2][1], player2)
            display_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(nick_disp_mid, player_dict[player3][1], player3)
            display_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(nick_disp_adc, player_dict[player4][1], player4)
            display_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(nick_disp_sup, player_dict[player5][1], player5)

            result_text += "Team {}\nTop    : {}\nJg     : {}\nMid    : {}\nADC    : {}\nSup    : {}\n\n"\
                .format(k + 1, display_top, display_jg, display_mid, display_adc, display_sup)

        if len(auto_fill_list) > 0:
            result_text += "Leftover players:\n"
            for keys in auto_fill_list:
                if player_dict[keys][3].lower() == "top":
                    leftover_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Top    : {}\n".format(leftover_top)
                elif player_dict[keys][3].lower() == "jg":
                    leftover_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Jg     : {}\n".format(leftover_jg)
                elif player_dict[keys][3].lower() == "mid":
                    leftover_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Mid    : {}\n".format(leftover_mid)
                elif player_dict[keys][3].lower() == "adc":
                    leftover_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "ADC    : {}\n".format(leftover_adc)
                elif player_dict[keys][3].lower() == "sup":
                    leftover_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Sup    : {}\n".format(leftover_sup)

        print(result_text)

        if is_output_wanted():
            output_file_name = take_output_name()
            with open(output_file_name, "w") as result_output_file:
                result_output_file.write(result_text)
        else:
            print('No output file.\n')

    # Create Teams Primary Secondary
    elif main_loop_inp.strip() == 'start ps':
        top_main = [0, [], [], [], []]
        jg_main = [0, [], [], [], []]
        mid_main = [0, [], [], [], []]
        adc_main = [0, [], [], [], []]
        sup_main = [0, [], [], [], []]

        for player in player_dict:
            if player_dict[player][3].lower() == 'top':
                if player_dict[player][4].lower() == 'jg':
                    top_main[1].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    top_main[2].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    top_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    top_main[4].append(player)
                top_main[0] += 1
            elif player_dict[player][3].lower() == 'jg':

                if player_dict[player][4].lower() == 'top':
                    jg_main[1].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    jg_main[2].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    jg_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    jg_main[4].append(player)
                jg_main[0] += 1
            elif player_dict[player][3].lower() == 'mid':

                if player_dict[player][4].lower() == 'top':
                    mid_main[1].append(player)
                elif player_dict[player][4].lower() == 'jg':
                    mid_main[2].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    mid_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    mid_main[4].append(player)
                mid_main[0] += 1
            elif player_dict[player][3].lower() == 'adc':

                if player_dict[player][4].lower() == 'top':
                    adc_main[1].append(player)
                elif player_dict[player][4].lower() == 'jg':
                    adc_main[2].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    adc_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    adc_main[4].append(player)
                adc_main[0] += 1
            elif player_dict[player][3].lower() == 'sup':

                if player_dict[player][4].lower() == 'top':
                    sup_main[1].append(player)
                elif player_dict[player][4].lower() == 'jg':
                    sup_main[2].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    sup_main[3].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    sup_main[4].append(player)
                sup_main[0] += 1

        result_text = ""
        pot_max_team_num = len(player_dict.keys()) // 5
        unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup = [], [], [], [], []
        spare_top, spare_jg, spare_mid, spare_adc, spare_sup = 0, 0, 0, 0, 0
        needed_top, needed_jg, needed_mid, needed_adc, needed_sup = 0, 0, 0, 0, 0
        top_constant, jg_constant, mid_constant, adc_constant, sup_constant = 0, 0, 0, 0, 0

        found = False
        while not found:

            if 0 < top_main[0] <= pot_max_team_num:
                for player in top_main[1]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[1].clear()
                for player in top_main[2]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[2].clear()
                for player in top_main[3]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[3].clear()
                for player in top_main[4]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[4].clear()
            if 0 < jg_main[0] <= pot_max_team_num:
                for player in jg_main[1]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[1].clear()
                for player in jg_main[2]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[2].clear()
                for player in jg_main[3]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[3].clear()
                for player in jg_main[4]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[4].clear()
            if 0 < mid_main[0] <= pot_max_team_num:
                for player in mid_main[1]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[1].clear()
                for player in mid_main[2]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[2].clear()
                for player in mid_main[3]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[3].clear()
                for player in mid_main[4]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[4].clear()
            if 0 < adc_main[0] <= pot_max_team_num:
                for player in adc_main[1]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[1].clear()
                for player in adc_main[2]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[2].clear()
                for player in adc_main[3]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[3].clear()
                for player in adc_main[4]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[4].clear()
            if 0 < sup_main[0] <= pot_max_team_num:
                for player in sup_main[1]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[1].clear()
                for player in sup_main[2]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[2].clear()
                for player in sup_main[3]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[3].clear()
                for player in sup_main[4]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[4].clear()

            if top_main[0] != 0:
                spare_top = top_main[0] - pot_max_team_num
            else:
                needed_top = pot_max_team_num - len(unordered_top) - top_constant

            if jg_main[0] != 0:
                spare_jg = jg_main[0] - pot_max_team_num
            else:
                needed_jg = pot_max_team_num - len(unordered_jg) - jg_constant

            if mid_main[0] != 0:
                spare_mid = mid_main[0] - pot_max_team_num
            else:
                needed_mid = pot_max_team_num - len(unordered_mid) - mid_constant

            if adc_main[0] != 0:
                spare_adc = adc_main[0] - pot_max_team_num
            else:
                needed_adc = pot_max_team_num - len(unordered_adc) - adc_constant

            if sup_main[0] != 0:
                spare_sup = sup_main[0] - pot_max_team_num
            else:
                needed_sup = pot_max_team_num - len(unordered_sup) - sup_constant

            # print('-------------------------------------------------------')
            # print(top_main, jg_main, mid_main, adc_main, sup_main, sep='\n')
            # print()
            # print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, sep='\n')
            # print(len(unordered_top), len(unordered_jg), len(unordered_mid), len(unordered_adc), len(unordered_sup))
            # print()
            # print(spare_top, spare_jg, spare_mid, spare_adc, spare_sup)
            # print(needed_top, needed_jg, needed_mid, needed_adc, needed_sup)
            # print('-------------------------------------------------------')
            # print('needed part')

            if needed_top > 0:
                # print('needed top')
                temp_top = set()
                temp_top.update(jg_main[1], mid_main[1], adc_main[1], sup_main[1])
                temp_top = list(temp_top)
                transferred_top = needed_top if len(temp_top) >= needed_top else spare_top

                if temp_top:
                    for _ in range(transferred_top):
                        t = random.randint(0, len(temp_top) - 1) if len(temp_top) > 1 else 0
                        unordered_top.append(temp_top[t])
                        if temp_top[t] in jg_main[1]:
                            jg_main[1].remove(temp_top[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_top[t] in mid_main[1]:
                            mid_main[1].remove(temp_top[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_top[t] in adc_main[1]:
                            adc_main[1].remove(temp_top[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        elif temp_top[t] in sup_main[1]:
                            sup_main[1].remove(temp_top[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_top.pop(t)
                        needed_top -= 1
                        break
                    continue
                else:
                    top_constant = pot_max_team_num - len(unordered_top)
                    continue
            elif needed_jg > 0:
                # print('needed jg')
                temp_jg = set()
                temp_jg.update(top_main[1], mid_main[2], adc_main[2], sup_main[2])
                temp_jg = list(temp_jg)
                transferred_jg = needed_jg if len(temp_jg) >= needed_jg else spare_jg

                if temp_jg:
                    for _ in range(transferred_jg):
                        t = random.randint(0, len(temp_jg) - 1) if len(temp_jg) > 1 else 0
                        unordered_jg.append(temp_jg[t])
                        if temp_jg[t] in top_main[1]:
                            top_main[1].remove(temp_jg[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_jg[t] in mid_main[2]:
                            mid_main[2].remove(temp_jg[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_jg[t] in adc_main[2]:
                            adc_main[2].remove(temp_jg[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        elif temp_jg[t] in sup_main[2]:
                            sup_main[2].remove(temp_jg[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_jg.pop(t)
                        needed_jg -= 1
                        break
                    continue
                else:
                    jg_constant = pot_max_team_num - len(unordered_jg)
                    continue
            elif needed_mid > 0:
                # print('needed mid')
                temp_mid = set()
                temp_mid.update(top_main[2], jg_main[2], adc_main[3], sup_main[3])
                temp_mid = list(temp_mid)
                transferred_mid = needed_mid if len(temp_mid) >= needed_mid else spare_mid

                if temp_mid:
                    for _ in range(transferred_mid):
                        t = random.randint(0, len(temp_mid) - 1) if len(temp_mid) > 1 else 0
                        unordered_mid.append(temp_mid[t])
                        if temp_mid[t] in top_main[2]:
                            top_main[2].remove(temp_mid[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_mid[t] in jg_main[2]:
                            jg_main[2].remove(temp_mid[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_mid[t] in adc_main[3]:
                            adc_main[3].remove(temp_mid[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        elif temp_mid[t] in sup_main[3]:
                            sup_main[3].remove(temp_mid[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_mid.pop(t)
                        needed_mid -= 1
                        break
                    continue
                else:
                    mid_constant = pot_max_team_num - len(unordered_mid)
                    continue
            elif needed_adc > 0:
                # print('needed adc')
                temp_adc = set()
                temp_adc.update(top_main[3], jg_main[3], mid_main[3], sup_main[4])
                temp_adc = list(temp_adc)
                transferred_adc = needed_adc if len(temp_adc) >= needed_adc else spare_adc

                if temp_adc:
                    for _ in range(transferred_adc):
                        t = random.randint(0, len(temp_adc) - 1) if len(temp_adc) > 1 else 0
                        unordered_adc.append(temp_adc[t])
                        if temp_adc[t] in top_main[3]:
                            top_main[3].remove(temp_adc[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_adc[t] in jg_main[3]:
                            jg_main[3].remove(temp_adc[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_adc[t] in mid_main[3]:
                            mid_main[3].remove(temp_adc[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_adc[t] in sup_main[4]:
                            sup_main[4].remove(temp_adc[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_adc.pop(t)
                        needed_adc -= 1
                        break
                    continue
                else:
                    adc_constant = pot_max_team_num - len(unordered_adc)
                    continue
            elif needed_sup > 0:
                # print('needed sup')
                temp_sup = set()
                temp_sup.update(top_main[4], jg_main[4], mid_main[4], adc_main[4])
                temp_sup = list(temp_sup)
                transferred_sup = needed_sup if len(temp_sup) >= needed_sup else spare_sup
                if temp_sup:
                    for _ in range(transferred_sup):
                        t = random.randint(0, len(temp_sup) - 1) if len(temp_sup) > 1 else 0
                        unordered_sup.append(temp_sup[t])
                        if temp_sup[t] in top_main[4]:
                            top_main[4].remove(temp_sup[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_sup[t] in jg_main[4]:
                            jg_main[4].remove(temp_sup[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_sup[t] in mid_main[4]:
                            mid_main[4].remove(temp_sup[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_sup[t] in adc_main[4]:
                            adc_main[4].remove(temp_sup[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        temp_sup.pop(t)
                        needed_sup -= 1
                        break
                    continue
                else:
                    sup_constant = pot_max_team_num - len(unordered_sup)
                    continue
            else:
                # print('else')
                if top_main[0] != 0:
                    temp_top = set()
                    temp_top.update(top_main[1], top_main[2], top_main[3], top_main[4])
                    temp_top = list(temp_top)
                    unordered_top += temp_top
                if jg_main[0] != 0:
                    temp_jg = set()
                    temp_jg.update(jg_main[1], jg_main[2], jg_main[3], jg_main[4])
                    temp_jg = list(temp_jg)
                    unordered_jg += temp_jg
                if mid_main[0] != 0:
                    temp_mid = set()
                    temp_mid.update(mid_main[1], mid_main[2], mid_main[3], mid_main[4])
                    temp_mid = list(temp_mid)
                    unordered_mid += temp_mid
                if adc_main[0] != 0:
                    temp_adc = set()
                    temp_adc.update(adc_main[1], adc_main[2], adc_main[3], adc_main[4])
                    temp_adc = list(temp_adc)
                    unordered_adc += temp_adc
                if sup_main[0] != 0:
                    temp_sup = set()
                    temp_sup.update(sup_main[1], sup_main[2], sup_main[3], sup_main[4])
                    temp_sup = list(temp_sup)
                    unordered_sup += temp_sup
                found = True

        print()
        print(top_main, jg_main, mid_main, adc_main, sup_main, sep='\n')
        print()
        print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, sep='\n')
        print(len(unordered_top), len(unordered_jg), len(unordered_mid), len(unordered_adc), len(unordered_sup))
        print()
        print(spare_top, spare_jg, spare_mid, spare_adc, spare_sup)
        print(needed_top, needed_jg, needed_mid, needed_adc, needed_sup)
        print()

        # AUTOFILL CAN BE ADDED FROM NOW ON, BALANCING THE TEAMS OUT

        real_max_team_num = min(len(unordered_top), len(unordered_jg), len(unordered_mid), len(unordered_adc),
                                len(unordered_sup))
        additional_top, additional_jg, additional_mid, additional_adc, additional_sup = [], [], [], [], []
        out_of_game = (len(player_dict.keys()) % 5) + (pot_max_team_num - real_max_team_num) * 5

        result_text += "\nMax team number is {}\n".format(real_max_team_num)
        result_text += "{} players on role, and {} players out of game\n\n".format(real_max_team_num * 5, out_of_game)

        # Get Rid Of Additional Players
        if len(unordered_top) > real_max_team_num:
            for num in range(len(unordered_top) - real_max_team_num):
                t = random.randint(1, len(unordered_top) - 1) if len(unordered_top) > 1 else 0
                additional_top.append(unordered_top[t])
                unordered_top.pop(t)
        if len(unordered_jg) > real_max_team_num:
            for num in range(len(unordered_jg) - real_max_team_num):
                j = random.randint(1, len(unordered_jg) - 1) if len(unordered_jg) > 1 else 0
                additional_jg.append(unordered_jg[j])
                unordered_jg.pop(j)
        if len(unordered_mid) > real_max_team_num:
            for num in range(len(unordered_mid) - real_max_team_num):
                m = random.randint(1, len(unordered_mid) - 1) if len(unordered_mid) > 1 else 0
                additional_mid.append(unordered_mid[m])
                unordered_mid.pop(m)
        if len(unordered_adc) > real_max_team_num:
            for num in range(len(unordered_adc) - real_max_team_num):
                a = random.randint(1, len(unordered_adc) - 1) if len(unordered_adc) > 1 else 0
                additional_adc.append(unordered_adc[a])
                unordered_adc.pop(a)
        if len(unordered_sup) > real_max_team_num:
            for num in range(len(unordered_sup) - real_max_team_num):
                s = random.randint(1, len(unordered_sup) - 1) if len(unordered_sup) > 1 else 0
                additional_sup.append(unordered_sup[s])
                unordered_sup.pop(s)

        print(additional_top, additional_jg, additional_mid, additional_adc, additional_sup, sep='\n')

        # What Is The Player Roles
        secondary_count = 0
        for i in range(len(unordered_top)):
            if player_dict[unordered_top[i]][3].lower() == 'top':
                unordered_top[i] += ' p'
            else:
                unordered_top[i] += ' s'
                secondary_count += 1
        for i in range(len(unordered_jg)):
            if player_dict[unordered_jg[i]][3].lower() == 'jg':
                unordered_jg[i] += ' p'
            else:
                unordered_jg[i] += ' s'
                secondary_count += 1
        for i in range(len(unordered_mid)):
            if player_dict[unordered_mid[i]][3].lower() == 'mid':
                unordered_mid[i] += ' p'
            else:
                unordered_mid[i] += ' s'
                secondary_count += 1
        for i in range(len(unordered_adc)):
            if player_dict[unordered_adc[i]][3].lower() == 'adc':
                unordered_adc[i] += ' p'
            else:
                unordered_adc[i] += ' s'
                secondary_count += 1
        for i in range(len(unordered_sup)):
            if player_dict[unordered_sup[i]][3].lower() == 'sup':
                unordered_sup[i] += ' p'
            else:
                unordered_sup[i] += ' s'
                secondary_count += 1

        # print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, sep='\n')

        teams = [[0] for _ in range(real_max_team_num)]

        for num in range(1, real_max_team_num + 1):
            t = random.randint(0, len(unordered_top) - 1) if len(unordered_top) > 1 else 0
            j = random.randint(0, len(unordered_jg) - 1) if len(unordered_jg) > 1 else 0
            m = random.randint(0, len(unordered_mid) - 1) if len(unordered_mid) > 1 else 0
            a = random.randint(0, len(unordered_adc) - 1) if len(unordered_adc) > 1 else 0
            s = random.randint(0, len(unordered_sup) - 1) if len(unordered_sup) > 1 else 0

            top_role = 'Primary  ' if unordered_top[t][-1:] == 'p' else 'Secondary'
            jg_role = 'Primary  ' if unordered_jg[j][-1:] == 'p' else 'Secondary'
            mid_role = 'Primary  ' if unordered_mid[m][-1:] == 'p' else 'Secondary'
            adc_role = 'Primary  ' if unordered_adc[a][-1:] == 'p' else 'Secondary'
            sup_role = 'Primary  ' if unordered_sup[s][-1:] == 'p' else 'Secondary'

            display_top = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_top[t][:-2]][0], top_role,
                                                                  player_dict[unordered_top[t][:-2]][1],
                                                                  unordered_top[t][:-2])
            display_jg = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_jg[j][:-2]][0], jg_role,
                                                                 player_dict[unordered_jg[j][:-2]][1],
                                                                 unordered_jg[j][:-2])
            display_mid = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_mid[m][:-2]][0], mid_role,
                                                                  player_dict[unordered_mid[m][:-2]][1],
                                                                  unordered_mid[m][:-2])
            display_adc = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_adc[a][:-2]][0], adc_role,
                                                                  player_dict[unordered_adc[a][:-2]][1],
                                                                  unordered_adc[a][:-2])
            display_sup = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_sup[s][:-2]][0], sup_role,
                                                                  player_dict[unordered_sup[s][:-2]][1],
                                                                  unordered_sup[s][:-2])

            result_text += "Team {}\nTop    : {}\nJg     : {}\nMid    : {}\nADC    : {}\nSup    : {} \n\n"\
                .format(num, display_top, display_jg, display_mid, display_adc, display_sup)

            unordered_top.pop(t)
            unordered_jg.pop(j)
            unordered_mid.pop(m)
            unordered_adc.pop(a)
            unordered_sup.pop(s)

        result_text += "{} players on their primary roles, and {} players on their secondary roles.\n"\
            .format(real_max_team_num * 5 - secondary_count, secondary_count)

        result_text += "\nLeftover players:\n"

        # print(additional_top, additional_jg, additional_mid, additional_adc, additional_sup, sep='\n')

        if additional_top:
            for top in additional_top:
                display_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[top][0],
                                                                  player_dict[top][1],
                                                                  top)
                result_text += "Top    : {}\n".format(display_top)
        if additional_jg:
            for jg in additional_jg:
                display_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[jg][0],
                                                                 player_dict[jg][1],
                                                                 jg)
                result_text += "Jg     : {}\n".format(display_jg)
        if additional_mid:
            for mid in additional_mid:
                display_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[mid][0],
                                                                  player_dict[mid][1],
                                                                  mid)
                result_text += "Mid    : {}\n".format(display_mid)
        if additional_adc:
            for adc in additional_adc:
                display_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[adc][0],
                                                                  player_dict[adc][1],
                                                                  adc)
                result_text += "ADC    : {}\n".format(display_adc)
        if additional_sup:
            for sup in additional_sup:
                display_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[sup][0],
                                                                  player_dict[sup][1],
                                                                  sup)
                result_text += "Sup    : {}\n".format(display_sup)

        print(result_text)

        if is_output_wanted():
            output_file_name = take_output_name()
            with open(output_file_name, "w") as result_output_file:
                result_output_file.write(result_text)
        else:
            print('No output file.\n')

    # Create Teams Primary Secondary AutoFill
    elif main_loop_inp.strip() == 'start psa':
        top_main = [0, [], [], [], []]
        jg_main = [0, [], [], [], []]
        mid_main = [0, [], [], [], []]
        adc_main = [0, [], [], [], []]
        sup_main = [0, [], [], [], []]

        for player in player_dict:
            if player_dict[player][3].lower() == 'top':
                if player_dict[player][4].lower() == 'jg':
                    top_main[1].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    top_main[2].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    top_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    top_main[4].append(player)
                top_main[0] += 1
            elif player_dict[player][3].lower() == 'jg':

                if player_dict[player][4].lower() == 'top':
                    jg_main[1].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    jg_main[2].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    jg_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    jg_main[4].append(player)
                jg_main[0] += 1
            elif player_dict[player][3].lower() == 'mid':

                if player_dict[player][4].lower() == 'top':
                    mid_main[1].append(player)
                elif player_dict[player][4].lower() == 'jg':
                    mid_main[2].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    mid_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    mid_main[4].append(player)
                mid_main[0] += 1
            elif player_dict[player][3].lower() == 'adc':

                if player_dict[player][4].lower() == 'top':
                    adc_main[1].append(player)
                elif player_dict[player][4].lower() == 'jg':
                    adc_main[2].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    adc_main[3].append(player)
                elif player_dict[player][4].lower() == 'sup':
                    adc_main[4].append(player)
                adc_main[0] += 1
            elif player_dict[player][3].lower() == 'sup':

                if player_dict[player][4].lower() == 'top':
                    sup_main[1].append(player)
                elif player_dict[player][4].lower() == 'jg':
                    sup_main[2].append(player)
                elif player_dict[player][4].lower() == 'mid':
                    sup_main[3].append(player)
                elif player_dict[player][4].lower() == 'adc':
                    sup_main[4].append(player)
                sup_main[0] += 1

        result_text = ""
        pot_max_team_num = len(player_dict.keys()) // 5
        unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup = [], [], [], [], []
        spare_top, spare_jg, spare_mid, spare_adc, spare_sup = 0, 0, 0, 0, 0
        needed_top, needed_jg, needed_mid, needed_adc, needed_sup = 0, 0, 0, 0, 0
        top_constant, jg_constant, mid_constant, adc_constant, sup_constant = 0, 0, 0, 0, 0

        found = False
        while not found:

            if 0 < top_main[0] <= pot_max_team_num:
                for player in top_main[1]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[1].clear()
                for player in top_main[2]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[2].clear()
                for player in top_main[3]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[3].clear()
                for player in top_main[4]:
                    unordered_top.append(player)
                    top_main[0] -= 1
                top_main[4].clear()
            if 0 < jg_main[0] <= pot_max_team_num:
                for player in jg_main[1]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[1].clear()
                for player in jg_main[2]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[2].clear()
                for player in jg_main[3]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[3].clear()
                for player in jg_main[4]:
                    unordered_jg.append(player)
                    jg_main[0] -= 1
                jg_main[4].clear()
            if 0 < mid_main[0] <= pot_max_team_num:
                for player in mid_main[1]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[1].clear()
                for player in mid_main[2]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[2].clear()
                for player in mid_main[3]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[3].clear()
                for player in mid_main[4]:
                    unordered_mid.append(player)
                    mid_main[0] -= 1
                mid_main[4].clear()
            if 0 < adc_main[0] <= pot_max_team_num:
                for player in adc_main[1]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[1].clear()
                for player in adc_main[2]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[2].clear()
                for player in adc_main[3]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[3].clear()
                for player in adc_main[4]:
                    unordered_adc.append(player)
                    adc_main[0] -= 1
                adc_main[4].clear()
            if 0 < sup_main[0] <= pot_max_team_num:
                for player in sup_main[1]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[1].clear()
                for player in sup_main[2]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[2].clear()
                for player in sup_main[3]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[3].clear()
                for player in sup_main[4]:
                    unordered_sup.append(player)
                    sup_main[0] -= 1
                sup_main[4].clear()

            if top_main[0] != 0:
                spare_top = top_main[0] - pot_max_team_num
            else:
                needed_top = pot_max_team_num - len(unordered_top) - top_constant

            if jg_main[0] != 0:
                spare_jg = jg_main[0] - pot_max_team_num
            else:
                needed_jg = pot_max_team_num - len(unordered_jg) - jg_constant

            if mid_main[0] != 0:
                spare_mid = mid_main[0] - pot_max_team_num
            else:
                needed_mid = pot_max_team_num - len(unordered_mid) - mid_constant

            if adc_main[0] != 0:
                spare_adc = adc_main[0] - pot_max_team_num
            else:
                needed_adc = pot_max_team_num - len(unordered_adc) - adc_constant

            if sup_main[0] != 0:
                spare_sup = sup_main[0] - pot_max_team_num
            else:
                needed_sup = pot_max_team_num - len(unordered_sup) - sup_constant

            # print('-------------------------------------------------------')
            # print(top_main, jg_main, mid_main, adc_main, sup_main, sep='\n')
            # print()
            # print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, sep='\n')
            # print(len(unordered_top), len(unordered_jg), len(unordered_mid), len(unordered_adc), len(unordered_sup))
            # print()
            # print(spare_top, spare_jg, spare_mid, spare_adc, spare_sup)
            # print(needed_top, needed_jg, needed_mid, needed_adc, needed_sup)
            # print('-------------------------------------------------------')
            # print('needed part')

            if needed_top > 0:
                # print('needed top')
                temp_top = set()
                temp_top.update(jg_main[1], mid_main[1], adc_main[1], sup_main[1])
                temp_top = list(temp_top)
                transferred_top = needed_top if len(temp_top) >= needed_top else spare_top

                if temp_top:
                    for _ in range(transferred_top):
                        t = random.randint(0, len(temp_top) - 1) if len(temp_top) > 1 else 0
                        unordered_top.append(temp_top[t])
                        if temp_top[t] in jg_main[1]:
                            jg_main[1].remove(temp_top[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_top[t] in mid_main[1]:
                            mid_main[1].remove(temp_top[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_top[t] in adc_main[1]:
                            adc_main[1].remove(temp_top[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        elif temp_top[t] in sup_main[1]:
                            sup_main[1].remove(temp_top[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_top.pop(t)
                        needed_top -= 1
                        break
                    continue
                else:
                    top_constant = pot_max_team_num - len(unordered_top)
                    continue
            elif needed_jg > 0:
                # print('needed jg')
                temp_jg = set()
                temp_jg.update(top_main[1], mid_main[2], adc_main[2], sup_main[2])
                temp_jg = list(temp_jg)
                transferred_jg = needed_jg if len(temp_jg) >= needed_jg else spare_jg

                if temp_jg:
                    for _ in range(transferred_jg):
                        t = random.randint(0, len(temp_jg) - 1) if len(temp_jg) > 1 else 0
                        unordered_jg.append(temp_jg[t])
                        if temp_jg[t] in top_main[1]:
                            top_main[1].remove(temp_jg[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_jg[t] in mid_main[2]:
                            mid_main[2].remove(temp_jg[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_jg[t] in adc_main[2]:
                            adc_main[2].remove(temp_jg[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        elif temp_jg[t] in sup_main[2]:
                            sup_main[2].remove(temp_jg[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_jg.pop(t)
                        needed_jg -= 1
                        break
                    continue
                else:
                    jg_constant = pot_max_team_num - len(unordered_jg)
                    continue
            elif needed_mid > 0:
                # print('needed mid')
                temp_mid = set()
                temp_mid.update(top_main[2], jg_main[2], adc_main[3], sup_main[3])
                temp_mid = list(temp_mid)
                transferred_mid = needed_mid if len(temp_mid) >= needed_mid else spare_mid

                if temp_mid:
                    for _ in range(transferred_mid):
                        t = random.randint(0, len(temp_mid) - 1) if len(temp_mid) > 1 else 0
                        unordered_mid.append(temp_mid[t])
                        if temp_mid[t] in top_main[2]:
                            top_main[2].remove(temp_mid[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_mid[t] in jg_main[2]:
                            jg_main[2].remove(temp_mid[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_mid[t] in adc_main[3]:
                            adc_main[3].remove(temp_mid[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        elif temp_mid[t] in sup_main[3]:
                            sup_main[3].remove(temp_mid[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_mid.pop(t)
                        needed_mid -= 1
                        break
                    continue
                else:
                    mid_constant = pot_max_team_num - len(unordered_mid)
                    continue
            elif needed_adc > 0:
                # print('needed adc')
                temp_adc = set()
                temp_adc.update(top_main[3], jg_main[3], mid_main[3], sup_main[4])
                temp_adc = list(temp_adc)
                transferred_adc = needed_adc if len(temp_adc) >= needed_adc else spare_adc

                if temp_adc:
                    for _ in range(transferred_adc):
                        t = random.randint(0, len(temp_adc) - 1) if len(temp_adc) > 1 else 0
                        unordered_adc.append(temp_adc[t])
                        if temp_adc[t] in top_main[3]:
                            top_main[3].remove(temp_adc[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_adc[t] in jg_main[3]:
                            jg_main[3].remove(temp_adc[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_adc[t] in mid_main[3]:
                            mid_main[3].remove(temp_adc[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_adc[t] in sup_main[4]:
                            sup_main[4].remove(temp_adc[t])
                            sup_main[0] -= 1
                            spare_sup -= 1
                        temp_adc.pop(t)
                        needed_adc -= 1
                        break
                    continue
                else:
                    adc_constant = pot_max_team_num - len(unordered_adc)
                    continue
            elif needed_sup > 0:
                # print('needed sup')
                temp_sup = set()
                temp_sup.update(top_main[4], jg_main[4], mid_main[4], adc_main[4])
                temp_sup = list(temp_sup)
                transferred_sup = needed_sup if len(temp_sup) >= needed_sup else spare_sup
                if temp_sup:
                    for _ in range(transferred_sup):
                        t = random.randint(0, len(temp_sup) - 1) if len(temp_sup) > 1 else 0
                        unordered_sup.append(temp_sup[t])
                        if temp_sup[t] in top_main[4]:
                            top_main[4].remove(temp_sup[t])
                            top_main[0] -= 1
                            spare_top -= 1
                        elif temp_sup[t] in jg_main[4]:
                            jg_main[4].remove(temp_sup[t])
                            jg_main[0] -= 1
                            spare_jg -= 1
                        elif temp_sup[t] in mid_main[4]:
                            mid_main[4].remove(temp_sup[t])
                            mid_main[0] -= 1
                            spare_mid -= 1
                        elif temp_sup[t] in adc_main[4]:
                            adc_main[4].remove(temp_sup[t])
                            adc_main[0] -= 1
                            spare_adc -= 1
                        temp_sup.pop(t)
                        needed_sup -= 1
                        break
                    continue
                else:
                    sup_constant = pot_max_team_num - len(unordered_sup)
                    continue
            else:
                # print('else')
                if top_main[0] != 0:
                    temp_top = set()
                    temp_top.update(top_main[1], top_main[2], top_main[3], top_main[4])
                    temp_top = list(temp_top)
                    unordered_top += temp_top
                if jg_main[0] != 0:
                    temp_jg = set()
                    temp_jg.update(jg_main[1], jg_main[2], jg_main[3], jg_main[4])
                    temp_jg = list(temp_jg)
                    unordered_jg += temp_jg
                if mid_main[0] != 0:
                    temp_mid = set()
                    temp_mid.update(mid_main[1], mid_main[2], mid_main[3], mid_main[4])
                    temp_mid = list(temp_mid)
                    unordered_mid += temp_mid
                if adc_main[0] != 0:
                    temp_adc = set()
                    temp_adc.update(adc_main[1], adc_main[2], adc_main[3], adc_main[4])
                    temp_adc = list(temp_adc)
                    unordered_adc += temp_adc
                if sup_main[0] != 0:
                    temp_sup = set()
                    temp_sup.update(sup_main[1], sup_main[2], sup_main[3], sup_main[4])
                    temp_sup = list(temp_sup)
                    unordered_sup += temp_sup
                found = True

        # print()
        # print(top_main, jg_main, mid_main, adc_main, sup_main, sep='\n')
        # print()
        # print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, sep='\n')
        # print(len(unordered_top), len(unordered_jg), len(unordered_mid), len(unordered_adc), len(unordered_sup))
        # print()
        # print(spare_top, spare_jg, spare_mid, spare_adc, spare_sup)
        # print(needed_top, needed_jg, needed_mid, needed_adc, needed_sup)
        # print()

        # AUTO FILL CAN BE ADDED FROM NOW ON, BALANCING THE TEAMS OUT

        # additional_top, additional_jg, additional_mid, additional_adc, additional_sup = [], [], [], [], []
        auto_fill_list = []
        out_of_game = (len(player_dict.keys()) % 5)

        result_text += "\nMax team number is {}\n".format(pot_max_team_num)
        result_text += "{} players playing, and {} players out of game\n\n".format(pot_max_team_num * 5, out_of_game)

        # Get Rid Of Additional Players Append Them To a List
        if len(unordered_top) > pot_max_team_num:
            for num in range(len(unordered_top) - pot_max_team_num):
                t = random.randint(1, len(unordered_top) - 1) if len(unordered_top) > 1 else 0
                auto_fill_list.append(unordered_top[t])
                unordered_top.pop(t)
        if len(unordered_jg) > pot_max_team_num:
            for num in range(len(unordered_jg) - pot_max_team_num):
                j = random.randint(1, len(unordered_jg) - 1) if len(unordered_jg) > 1 else 0
                auto_fill_list.append(unordered_jg[j])
                unordered_jg.pop(j)
        if len(unordered_mid) > pot_max_team_num:
            for num in range(len(unordered_mid) - pot_max_team_num):
                m = random.randint(1, len(unordered_mid) - 1) if len(unordered_mid) > 1 else 0
                auto_fill_list.append(unordered_mid[m])
                unordered_mid.pop(m)
        if len(unordered_adc) > pot_max_team_num:
            for num in range(len(unordered_adc) - pot_max_team_num):
                a = random.randint(1, len(unordered_adc) - 1) if len(unordered_adc) > 1 else 0
                auto_fill_list.append(unordered_adc[a])
                unordered_adc.pop(a)
        if len(unordered_sup) > pot_max_team_num:
            for num in range(len(unordered_sup) - pot_max_team_num):
                s = random.randint(1, len(unordered_sup) - 1) if len(unordered_sup) > 1 else 0
                auto_fill_list.append(unordered_sup[s])
                unordered_sup.pop(s)

        # Append Auto-Fill to Teams
        if pot_max_team_num > len(unordered_top):
            for num in range(pot_max_team_num - len(unordered_top)):
                t = random.randint(0, len(auto_fill_list) - 1) if len(auto_fill_list) > 1 else 0
                unordered_top.append(auto_fill_list[t])
                auto_fill_list.pop(t)
        if pot_max_team_num > len(unordered_jg):
            for num in range(pot_max_team_num - len(unordered_jg)):
                t = random.randint(0, len(auto_fill_list) - 1) if len(auto_fill_list) > 1 else 0
                unordered_jg.append(auto_fill_list[t])
                auto_fill_list.pop(t)
        if pot_max_team_num > len(unordered_mid):
            for num in range(pot_max_team_num - len(unordered_mid)):
                t = random.randint(0, len(auto_fill_list) - 1) if len(auto_fill_list) > 1 else 0
                unordered_mid.append(auto_fill_list[t])
                auto_fill_list.pop(t)
        if pot_max_team_num > len(unordered_adc):
            for num in range(pot_max_team_num - len(unordered_adc)):
                t = random.randint(0, len(auto_fill_list) - 1) if len(auto_fill_list) > 1 else 0
                unordered_adc.append(auto_fill_list[t])
                auto_fill_list.pop(t)
        if pot_max_team_num > len(unordered_sup):
            for num in range(pot_max_team_num - len(unordered_sup)):
                t = random.randint(0, len(auto_fill_list) - 1) if len(auto_fill_list) > 1 else 0
                unordered_sup.append(auto_fill_list[t])
                auto_fill_list.pop(t)

        # What Is The Player Roles
        secondary_count = 0
        auto_fill_count = 0
        for i in range(len(unordered_top)):
            if player_dict[unordered_top[i]][3].lower() == 'top':
                unordered_top[i] += ' p'
            elif player_dict[unordered_top[i]][4].lower() == 'top':
                unordered_top[i] += ' s'
                secondary_count += 1
            else:
                unordered_top[i] += ' a'
                auto_fill_count += 1
        for i in range(len(unordered_jg)):
            if player_dict[unordered_jg[i]][3].lower() == 'jg':
                unordered_jg[i] += ' p'
            elif player_dict[unordered_jg[i]][4].lower() == 'jg':
                unordered_jg[i] += ' s'
                secondary_count += 1
            else:
                unordered_jg[i] += ' a'
                auto_fill_count += 1
        for i in range(len(unordered_mid)):
            if player_dict[unordered_mid[i]][3].lower() == 'mid':
                unordered_mid[i] += ' p'
            elif player_dict[unordered_mid[i]][4].lower() == 'mid':
                unordered_mid[i] += ' s'
                secondary_count += 1
            else:
                unordered_mid[i] += ' a'
                auto_fill_count += 1
        for i in range(len(unordered_adc)):
            if player_dict[unordered_adc[i]][3].lower() == 'adc':
                unordered_adc[i] += ' p'
            elif player_dict[unordered_adc[i]][4].lower() == 'adc':
                unordered_adc[i] += ' s'
                secondary_count += 1
            else:
                unordered_adc[i] += ' a'
                auto_fill_count += 1
        for i in range(len(unordered_sup)):
            if player_dict[unordered_sup[i]][3].lower() == 'sup':
                unordered_sup[i] += ' p'
            elif player_dict[unordered_sup[i]][4].lower() == 'sup':
                unordered_sup[i] += ' s'
                secondary_count += 1
            else:
                unordered_sup[i] += ' a'
                auto_fill_count += 1

        # print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, auto_fill_list, sep='\n')

        teams = [[0] for _ in range(pot_max_team_num)]

        for num in range(1, pot_max_team_num + 1):
            t = random.randint(0, len(unordered_top) - 1) if len(unordered_top) > 1 else 0
            j = random.randint(0, len(unordered_jg) - 1) if len(unordered_jg) > 1 else 0
            m = random.randint(0, len(unordered_mid) - 1) if len(unordered_mid) > 1 else 0
            a = random.randint(0, len(unordered_adc) - 1) if len(unordered_adc) > 1 else 0
            s = random.randint(0, len(unordered_sup) - 1) if len(unordered_sup) > 1 else 0

            if unordered_top[t][-1:] == 'p':
                top_role = 'Primary  '
            elif unordered_top[t][-1:] == 's':
                top_role = 'Secondary'
            else:
                top_role = 'Auto-Fill'

            if unordered_jg[j][-1:] == 'p':
                jg_role = 'Primary  '
            elif unordered_jg[j][-1:] == 's':
                jg_role = 'Secondary'
            else:
                jg_role = 'Auto-Fill'

            if unordered_mid[m][-1:] == 'p':
                mid_role = 'Primary  '
            elif unordered_mid[m][-1:] == 's':
                mid_role = 'Secondary'
            else:
                mid_role = 'Auto-Fill'

            if unordered_adc[a][-1:] == 'p':
                adc_role = 'Primary  '
            elif unordered_adc[a][-1:] == 's':
                adc_role = 'Secondary'
            else:
                adc_role = 'Auto-Fill'

            if unordered_sup[s][-1:] == 'p':
                sup_role = 'Primary  '
            elif unordered_sup[s][-1:] == 's':
                sup_role = 'Secondary'
            else:
                sup_role = 'Auto-Fill'

            display_top = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_top[t][:-2]][0], top_role,
                                                                  player_dict[unordered_top[t][:-2]][1],
                                                                  unordered_top[t][:-2])
            display_jg = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_jg[j][:-2]][0], jg_role,
                                                                 player_dict[unordered_jg[j][:-2]][1],
                                                                 unordered_jg[j][:-2])
            display_mid = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_mid[m][:-2]][0], mid_role,
                                                                  player_dict[unordered_mid[m][:-2]][1],
                                                                  unordered_mid[m][:-2])
            display_adc = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_adc[a][:-2]][0], adc_role,
                                                                  player_dict[unordered_adc[a][:-2]][1],
                                                                  unordered_adc[a][:-2])
            display_sup = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_sup[s][:-2]][0], sup_role,
                                                                  player_dict[unordered_sup[s][:-2]][1],
                                                                  unordered_sup[s][:-2])

            result_text += "Team {}\nTop    : {}\nJg     : {}\nMid    : {}\nADC    : {}\nSup    : {} \n\n" \
                .format(num, display_top, display_jg, display_mid, display_adc, display_sup)

            unordered_top.pop(t)
            unordered_jg.pop(j)
            unordered_mid.pop(m)
            unordered_adc.pop(a)
            unordered_sup.pop(s)

        result_text += "{} players on their primary roles, {} players on their secondary roles, " \
                       "and {} players auto-filled.\n".format(pot_max_team_num * 5 - secondary_count - auto_fill_count,
                                                              secondary_count, auto_fill_count)

        if len(auto_fill_list) > 0:
            result_text += "\nLeftover players:\n"
            for keys in auto_fill_list:
                if player_dict[keys][3].lower() == "top":
                    leftover_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Top    : {}\n".format(leftover_top)
                elif player_dict[keys][3].lower() == "jg":
                    leftover_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Jg     : {}\n".format(leftover_jg)
                elif player_dict[keys][3].lower() == "mid":
                    leftover_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Mid    : {}\n".format(leftover_mid)
                elif player_dict[keys][3].lower() == "adc":
                    leftover_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "ADC    : {}\n".format(leftover_adc)
                elif player_dict[keys][3].lower() == "sup":
                    leftover_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                    result_text += "Sup    : {}\n".format(leftover_sup)

        print(result_text)

        if is_output_wanted():
            output_file_name = take_output_name()
            with open(output_file_name, "w") as result_output_file:
                result_output_file.write(result_text)
        else:
            print('No output file.\n')

    # Create Teams Primary Secondary AutoFill Yunus
    elif main_loop_inp.strip() == 'start psa yunus':

        original_dict = player_dict.copy()
        ccc = player_dict.copy()
        # print(player_dict)

        out_of_game_list = []

        if len(ccc.keys()) % 5 != 0:
            additional = len(ccc.keys()) % 5
            for _ in range(additional):
                x = random.choice(list(ccc.keys()))
                del ccc[x]
                del original_dict[x]
                out_of_game_list.append(x)

        # print(len(ccc.keys()))

        mid = []
        adc = []
        jg = []
        sup = []
        top = []

        found = True
        while_count = 0
        while True:
            while_count += 1
            if while_count > 100:
                print('\nCould not find teams!\n')
                found = False
                break

            count_top, count_top1, count_top2 = 0, 0, 0
            for key in original_dict:
                count_top1 += original_dict[key][3].lower().count("top")
                count_top2 += original_dict[key][4].lower().count("top")
            count_top = count_top1 + count_top2

            count_jg, count_jg1, count_jg2 = 0, 0, 0
            for key in original_dict:
                count_jg1 += original_dict[key][3].lower().count("jg")
                count_jg2 += original_dict[key][4].lower().count("jg")
            count_jg = count_jg1 + count_jg2

            count_mid, count_mid1, count_mid2 = 0, 0, 0
            for key in original_dict:
                count_mid1 += original_dict[key][3].lower().count("mid")
                count_mid2 += original_dict[key][4].lower().count("mid")
            count_mid = count_mid1 + count_mid2

            count_adc, count_adc1, count_adc2 = 0, 0, 0
            for key in original_dict:
                count_adc1 += original_dict[key][3].lower().count("adc")
                count_adc2 += original_dict[key][4].lower().count("adc")
            count_adc = count_adc1 + count_adc2

            count_sup, count_sup1, count_sup2 = 0, 0, 0
            for key in original_dict:
                count_sup1 += original_dict[key][3].lower().count("sup")
                count_sup2 += original_dict[key][4].lower().count("sup")
            count_sup = count_sup1 + count_sup2

            listeee = [count_mid, count_jg, count_adc, count_sup, count_top]
            toplam = count_mid + count_jg + count_adc + count_sup + count_top
            listeee.sort()

            xyz, xyz1, xyz2, xyz3, xyz4 = 0, 0, 0, 0, 0
            a, b, c, d, e = 0, 0, 0, 0, 0

            if count_mid == 0 and count_jg == 0 and count_sup == 0 and count_adc == 0 and count_top == 0:
                print("mid {}\njungle {}\nsup {}\ntop {}\nadc {}\n".format(mid, jg, sup, top, adc))
                break
            elif count_mid + count_jg + count_sup + count_top + count_adc == 10:
                for key in ccc:
                    if xyz == 0:
                        mid.append(key)
                        a = key
                        original_dict.pop(key)
                        xyz += 1

                    elif xyz1 == 0:
                        top.append(key)
                        b = key
                        original_dict.pop(key)
                        xyz1 += 1

                    elif xyz2 == 0:
                        jg.append(key)
                        c = key
                        original_dict.pop(key)
                        xyz2 += 1

                    elif xyz3 == 0:
                        sup.append(key)
                        d = key
                        original_dict.pop(key)
                        xyz3 += 1

                    elif xyz4 == 0:
                        adc.append(key)
                        e = key
                        original_dict.pop(key)
                        xyz4 += 1
                ccc.pop(a)
                ccc.pop(b)
                ccc.pop(c)
                ccc.pop(d)
                ccc.pop(e)
                continue

            elif count_mid1 != 0 and count_top1 != 0 and count_sup1 != 0 and count_adc1 != 0 and count_jg1 != 0:
                for key in ccc:
                    if original_dict[key][3].lower() == "mid" and xyz == 0:
                        mid.append(key)
                        a = key
                        original_dict.pop(key)
                        xyz += 1
                    elif original_dict[key][3].lower() == "top" and xyz1 == 0:
                        top.append(key)
                        b = key
                        original_dict.pop(key)
                        xyz1 += 1
                    elif original_dict[key][3].lower() == "jg" and xyz2 == 0:
                        jg.append(key)
                        c = key
                        original_dict.pop(key)
                        xyz2 += 1
                    elif original_dict[key][3].lower() == "sup" and xyz3 == 0:
                        sup.append(key)
                        d = key
                        original_dict.pop(key)
                        xyz3 += 1
                    elif original_dict[key][3].lower() == "adc" and xyz4 == 0:
                        adc.append(key)
                        e = key
                        original_dict.pop(key)
                        xyz4 += 1
                ccc.pop(a)
                ccc.pop(b)
                ccc.pop(c)
                ccc.pop(d)
                ccc.pop(e)
                continue

            # zaten 1 i 0 sa diye giriyor
            elif count_sup == 0:

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1
                continue

            elif count_mid == 0:

                if listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1
                continue

            elif count_top == 0:

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1

                elif listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1
                continue

            elif count_jg == 0:

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1

                elif listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1
                continue

            elif count_adc == 0:

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1

                elif listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1
                continue

            elif count_sup == listeee[0] and (not (
                    listeee[0] == listeee[1] and listeee[1] == listeee[2] and listeee[2] == listeee[3] and listeee[3] ==
                    listeee[4])):

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "sup"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "sup"
                                xyz += 1
                continue

            elif count_mid == listeee[0] and (not (
                    listeee[0] == listeee[1] and listeee[1] == listeee[2] and listeee[2] == listeee[3] and listeee[3] ==
                    listeee[4])):

                if listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "mid"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "mid"
                                xyz += 1
                continue

            elif count_top == listeee[0] and (not (
                    listeee[0] == listeee[1] and listeee[1] == listeee[2] and listeee[2] == listeee[3] and listeee[3] ==
                    listeee[4])):

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1

                elif listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "top"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "top"
                                xyz += 1
                continue

            elif count_jg == listeee[0] and (not (
                    listeee[0] == listeee[1] and listeee[1] == listeee[2] and listeee[2] == listeee[3] and listeee[3] ==
                    listeee[4])):

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1

                elif listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1

                elif listeee[-1] == count_adc:
                    if count_adc2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "adc" and xyz == 0:
                                original_dict[key][4] = "jg"
                                xyz += 1
                    elif count_adc2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "adc" and xyz == 0:
                                original_dict[key][3] = "jg"
                                xyz += 1
                continue

            elif count_adc == listeee[0] and (not (
                    listeee[0] == listeee[1] and listeee[1] == listeee[2] and listeee[2] == listeee[3] and listeee[3] ==
                    listeee[4])):

                if listeee[-1] == count_mid:
                    if count_mid2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "mid" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_mid2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "mid" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1

                elif listeee[-1] == count_top:
                    if count_top2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "top" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_top2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "top" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1

                elif listeee[-1] == count_jg:
                    if count_jg2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "jg" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_jg2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "jg" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1

                elif listeee[-1] == count_sup:
                    if count_sup2 != 0:
                        for key in original_dict:
                            if original_dict[key][4].lower() == "sup" and xyz == 0:
                                original_dict[key][4] = "adc"
                                xyz += 1
                    elif count_sup2 == 0:
                        for key in original_dict:
                            if original_dict[key][3].lower() == "sup" and xyz == 0:
                                original_dict[key][3] = "adc"
                                xyz += 1
                continue

            # Bundan sonrasında supun 2. sinden alıp 1. sine atması yeterli.
            elif count_sup2 != 0:

                for key in original_dict:
                    if original_dict[key][4].lower() == "sup" and xyz == 0:
                        original_dict[key][3] = "sup"
                        xyz += 1
                continue

            elif count_mid2 != 0:

                for key in original_dict:
                    if original_dict[key][4].lower() == "mid" and xyz == 0:
                        original_dict[key][3] = "mid"
                        xyz += 1
                continue

            elif count_top2 != 0:

                for key in original_dict:
                    if original_dict[key][4].lower() == "top" and xyz == 0:
                        original_dict[key][3] = "top"
                        xyz += 1

            elif count_jg2 != 0:

                for key in original_dict:
                    if original_dict[key][4].lower() == "jg" and xyz == 0:
                        original_dict[key][3] = "jg"
                        xyz += 1

            elif count_adc2 != 0:

                for key in original_dict:
                    if original_dict[key][4].lower() == "adc" and xyz == 0:
                        original_dict[key][3] = "adc"
                        xyz += 1

        # Can
        if found:
            result_text = ""

            unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup = top, jg, mid, adc, sup
            pot_max_team_num = min(len(top), len(jg), len(mid), len(adc), len(sup))

            out_of_game = (len(player_dict.keys()) % 5)

            result_text += "\nMax team number is {}\n".format(pot_max_team_num)
            result_text += "{} players playing, and {} players out of game\n\n".format(pot_max_team_num * 5,
                                                                                       out_of_game)

            # What Is The Player Roles
            secondary_count = 0
            auto_fill_count = 0
            for i in range(len(unordered_top)):
                if player_dict[unordered_top[i]][3].lower() == 'top':
                    unordered_top[i] += ' p'
                elif player_dict[unordered_top[i]][4].lower() == 'top':
                    unordered_top[i] += ' s'
                    secondary_count += 1
                else:
                    unordered_top[i] += ' a'
                    auto_fill_count += 1
            for i in range(len(unordered_jg)):
                if player_dict[unordered_jg[i]][3].lower() == 'jg':
                    unordered_jg[i] += ' p'
                elif player_dict[unordered_jg[i]][4].lower() == 'jg':
                    unordered_jg[i] += ' s'
                    secondary_count += 1
                else:
                    unordered_jg[i] += ' a'
                    auto_fill_count += 1
            for i in range(len(unordered_mid)):
                if player_dict[unordered_mid[i]][3].lower() == 'mid':
                    unordered_mid[i] += ' p'
                elif player_dict[unordered_mid[i]][4].lower() == 'mid':
                    unordered_mid[i] += ' s'
                    secondary_count += 1
                else:
                    unordered_mid[i] += ' a'
                    auto_fill_count += 1
            for i in range(len(unordered_adc)):
                if player_dict[unordered_adc[i]][3].lower() == 'adc':
                    unordered_adc[i] += ' p'
                elif player_dict[unordered_adc[i]][4].lower() == 'adc':
                    unordered_adc[i] += ' s'
                    secondary_count += 1
                else:
                    unordered_adc[i] += ' a'
                    auto_fill_count += 1
            for i in range(len(unordered_sup)):
                if player_dict[unordered_sup[i]][3].lower() == 'sup':
                    unordered_sup[i] += ' p'
                elif player_dict[unordered_sup[i]][4].lower() == 'sup':
                    unordered_sup[i] += ' s'
                    secondary_count += 1
                else:
                    unordered_sup[i] += ' a'
                    auto_fill_count += 1

            # print(unordered_top, unordered_jg, unordered_mid, unordered_adc, unordered_sup, auto_fill_list, sep='\n')

            teams = [[0] for _ in range(pot_max_team_num)]

            for num in range(1, pot_max_team_num + 1):
                t = random.randint(0, len(unordered_top) - 1) if len(unordered_top) > 1 else 0
                j = random.randint(0, len(unordered_jg) - 1) if len(unordered_jg) > 1 else 0
                m = random.randint(0, len(unordered_mid) - 1) if len(unordered_mid) > 1 else 0
                a = random.randint(0, len(unordered_adc) - 1) if len(unordered_adc) > 1 else 0
                s = random.randint(0, len(unordered_sup) - 1) if len(unordered_sup) > 1 else 0

                if unordered_top[t][-1:] == 'p':
                    top_role = 'Primary  '
                elif unordered_top[t][-1:] == 's':
                    top_role = 'Secondary'
                else:
                    top_role = 'Auto-Fill'

                if unordered_jg[j][-1:] == 'p':
                    jg_role = 'Primary  '
                elif unordered_jg[j][-1:] == 's':
                    jg_role = 'Secondary'
                else:
                    jg_role = 'Auto-Fill'

                if unordered_mid[m][-1:] == 'p':
                    mid_role = 'Primary  '
                elif unordered_mid[m][-1:] == 's':
                    mid_role = 'Secondary'
                else:
                    mid_role = 'Auto-Fill'

                if unordered_adc[a][-1:] == 'p':
                    adc_role = 'Primary  '
                elif unordered_adc[a][-1:] == 's':
                    adc_role = 'Secondary'
                else:
                    adc_role = 'Auto-Fill'

                if unordered_sup[s][-1:] == 'p':
                    sup_role = 'Primary  '
                elif unordered_sup[s][-1:] == 's':
                    sup_role = 'Secondary'
                else:
                    sup_role = 'Auto-Fill'

                display_top = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_top[t][:-2]][0], top_role,
                                                                      player_dict[unordered_top[t][:-2]][1],
                                                                      unordered_top[t][:-2])
                display_jg = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_jg[j][:-2]][0], jg_role,
                                                                     player_dict[unordered_jg[j][:-2]][1],
                                                                     unordered_jg[j][:-2])
                display_mid = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_mid[m][:-2]][0], mid_role,
                                                                      player_dict[unordered_mid[m][:-2]][1],
                                                                      unordered_mid[m][:-2])
                display_adc = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_adc[a][:-2]][0], adc_role,
                                                                      player_dict[unordered_adc[a][:-2]][1],
                                                                      unordered_adc[a][:-2])
                display_sup = "{:25s}\t{}\t-->\t{:25s}\t-\t{}".format(player_dict[unordered_sup[s][:-2]][0], sup_role,
                                                                      player_dict[unordered_sup[s][:-2]][1],
                                                                      unordered_sup[s][:-2])

                result_text += "Team {}\nTop    : {}\nJg     : {}\nMid    : {}\nADC    : {}\nSup    : {} \n\n" \
                    .format(num, display_top, display_jg, display_mid, display_adc, display_sup)

                unordered_top.pop(t)
                unordered_jg.pop(j)
                unordered_mid.pop(m)
                unordered_adc.pop(a)
                unordered_sup.pop(s)

            result_text += "{} players on their primary roles, {} players on their secondary roles, " \
                           "and {} players auto-filled.\n".format(pot_max_team_num * 5 - secondary_count -
                                                                  auto_fill_count, secondary_count, auto_fill_count)

            if len(out_of_game_list) > 0:
                result_text += "\nLeftover players:\n"
                for keys in out_of_game_list:
                    if player_dict[keys][3].lower() == "top":
                        leftover_top = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                        result_text += "Top    : {}\n".format(leftover_top)
                    elif player_dict[keys][3].lower() == "jg":
                        leftover_jg = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                        result_text += "Jg     : {}\n".format(leftover_jg)
                    elif player_dict[keys][3].lower() == "mid":
                        leftover_mid = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                        result_text += "Mid    : {}\n".format(leftover_mid)
                    elif player_dict[keys][3].lower() == "adc":
                        leftover_adc = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                        result_text += "ADC    : {}\n".format(leftover_adc)
                    elif player_dict[keys][3].lower() == "sup":
                        leftover_sup = "{:25s}\t-->\t{:25s}\t-\t{}".format(player_dict[keys][0], player_dict[keys][1], keys)
                        result_text += "Sup    : {}\n".format(leftover_sup)

            print(result_text)

            if is_output_wanted():
                output_file_name = take_output_name()
                with open(output_file_name, "w") as result_output_file:
                    result_output_file.write(result_text)
            else:
                print('No output file.\n')

    # Create Teams Primary Ranked Old System
    elif main_loop_inp == 'start pr old':

        # print(rank_top, rank_jg, rank_mid, rank_adc, rank_sup)
        additional_top, additional_jg, additional_mid, additional_adc, additional_sup = [], [], [], [], []

        rank_player_sum = len(rank_top) + len(rank_jg) + len(rank_mid) + len(rank_adc) + len(rank_sup) - 5

        print('')

        tolerance = input("Enter a tolerance level between 0-4 (DEFAULT/RECOMMENDED: 2)(Type 'no' to use default): ")
        while tolerance != "no":
            if tolerance == "0":
                break
            elif tolerance == "1":
                break
            elif tolerance == "2":
                break

            elif tolerance == "3":
                break
            elif tolerance == "4":
                break
            else:
                print("Tolerance number not within boundaries!")
                tolerance = input("Enter a tolerance level between 0-4 (DEFAULT/RECOMMENDED: 2)"
                                  "(Type 'no' to use default): ")

        if tolerance == "no":
            tolerance = 2

        tolerance = int(tolerance)

        result_text = ""

        max_team_num = min(len(rank_top), len(rank_jg), len(rank_mid), len(rank_adc), len(rank_sup))
        max_team_num -= 1
        max_player_num = len(rank_top) + len(rank_jg) + len(rank_mid) + len(rank_adc) + len(rank_sup) - 5

        result_text += "\nMax team number is {}\n\n".format(max_team_num)

        # Get Rid Of Additional Players
        if len(rank_top) > max_team_num:
            for num in range(len(rank_top) - max_team_num - 1):
                t = random.randint(1, len(rank_top) - 1) if len(rank_top) > 2 else 1
                additional_top.append(rank_top[t])
                rank_top.pop(t)
        if len(rank_jg) > max_team_num:
            for num in range(len(rank_jg) - max_team_num - 1):
                j = random.randint(1, len(rank_jg) - 1) if len(rank_jg) > 2 else 1
                additional_jg.append(rank_jg[j])
                rank_jg.pop(j)
        if len(rank_mid) > max_team_num:
            for num in range(len(rank_mid) - max_team_num - 1):
                m = random.randint(1, len(rank_mid) - 1) if len(rank_mid) > 2 else 1
                additional_mid.append(rank_mid[m])
                rank_mid.pop(m)
        if len(rank_adc) > max_team_num:
            for num in range(len(rank_adc) - max_team_num - 1):
                a = random.randint(1, len(rank_adc) - 1) if len(rank_adc) > 2 else 1
                additional_adc.append(rank_adc[a])
                rank_adc.pop(a)
        if len(rank_sup) > max_team_num:
            for num in range(len(rank_sup) - max_team_num - 1):
                s = random.randint(1, len(rank_sup) - 1) if len(rank_sup) > 2 else 1
                additional_sup.append(rank_sup[s])
                rank_sup.pop(s)

        # Sum of all Rank points
        sum_rank = 0
        for i in range(1, max_team_num + 1):
            rank_top[0] += int(rank_top[i][-1:])
            rank_jg[0] += int(rank_jg[i][-1:])
            rank_mid[0] += int(rank_mid[i][-1:])
            rank_adc[0] += int(rank_adc[i][-1:])
            rank_sup[0] += int(rank_sup[i][-1:])

        sum_rank = rank_top[0] + rank_jg[0] + rank_mid[0] + rank_adc[0] + rank_sup[0]
        all_player_list = [rank_top, rank_jg, rank_mid, rank_adc, rank_sup]
        avg_rank_per_team = sum_rank / max_team_num

        # tolerance = 2 DEFAULT TOLERANCE
        # print(sum_rank, avg_rank_per_team, tolerance)
        # print(rank_top, rank_jg, rank_mid, rank_adc, rank_sup)

        teams = [[0] for _ in range(max_team_num)]

        found_team = False
        no_possible_count = 0
        max_loop_count = 20
        no_possible_teams = True

        # Main Ranked Loop
        while no_possible_teams and no_possible_count < max_loop_count:

            shuffle_top, shuffle_jg, shuffle_mid, shuffle_adc, shuffle_sup = rank_top[:], rank_jg[:], \
                                                                             rank_mid[:], rank_adc[:], rank_sup[:]

            teams = [[0] for i in range(max_team_num)]
            temp_all_player_list = [shuffle_top, shuffle_jg, shuffle_mid, shuffle_adc, shuffle_sup]
            found_team_count = 0
            left_team_number = max_team_num

            # print(all_player_list)
            # print(temp_all_player_list)
            # print('before for')
            # print()

            no_possible_teams = False

            for k in range(5):
                temp_rank = temp_all_player_list[k][0]
                temp_all_player_list[k].pop(0)
                random.shuffle(temp_all_player_list[k])
                temp_all_player_list[k].insert(0, temp_rank)
                # print(temp_all_player_list[k], temp_rank)

            # print()

            # print('all player')
            # print(all_player_list)
            # print('temp player')
            # print(temp_all_player_list)
            # print()

            no_possible_count += 1
            # print(no_possible_count)
            # print()

            while (found_team_count != max_team_num) and (not no_possible_teams):
                found_team = False
                top_player_counter, jg_player_counter, mid_player_counter, \
                    adc_player_counter, sup_player_counter = 1, 1, 1, 1, 1

                while not found_team and not no_possible_teams:
                    current_rank_sum = 0
                    current_rank_sum += int(temp_all_player_list[0][top_player_counter][-1:]) + \
                        int(temp_all_player_list[1][jg_player_counter][-1:]) + \
                        int(temp_all_player_list[2][mid_player_counter][-1:]) + \
                        int(temp_all_player_list[3][adc_player_counter][-1:]) + \
                        int(temp_all_player_list[4][sup_player_counter][-1:])

                    # print(current_rank_sum)
                    # print(temp_all_player_list)
                    # print(teams)

                    if avg_rank_per_team - tolerance <= current_rank_sum <= avg_rank_per_team + tolerance:
                        found_team = True
                        found_team_count += 1
                        left_team_number -= 1

                        temp_all_player_list[0][0] -= int(temp_all_player_list[0][top_player_counter][-1:])
                        teams[found_team_count - 1].append(temp_all_player_list[0][top_player_counter])
                        teams[found_team_count - 1][0] += int(temp_all_player_list[0][top_player_counter][-1:])
                        temp_all_player_list[0].pop(top_player_counter)

                        temp_all_player_list[1][0] -= int(temp_all_player_list[1][jg_player_counter][-1:])
                        teams[found_team_count - 1].append(temp_all_player_list[1][jg_player_counter])
                        teams[found_team_count - 1][0] += int(temp_all_player_list[1][jg_player_counter][-1:])
                        temp_all_player_list[1].pop(jg_player_counter)

                        temp_all_player_list[2][0] -= int(temp_all_player_list[2][mid_player_counter][-1:])
                        teams[found_team_count - 1].append(temp_all_player_list[2][mid_player_counter])
                        teams[found_team_count - 1][0] += int(temp_all_player_list[2][mid_player_counter][-1:])
                        temp_all_player_list[2].pop(mid_player_counter)

                        temp_all_player_list[3][0] -= int(temp_all_player_list[3][adc_player_counter][-1:])
                        teams[found_team_count - 1].append(temp_all_player_list[3][adc_player_counter])
                        teams[found_team_count - 1][0] += int(temp_all_player_list[3][adc_player_counter][-1:])
                        temp_all_player_list[3].pop(adc_player_counter)

                        temp_all_player_list[4][0] -= int(temp_all_player_list[4][sup_player_counter][-1:])
                        teams[found_team_count - 1].append(temp_all_player_list[4][sup_player_counter])
                        teams[found_team_count - 1][0] += int(temp_all_player_list[4][sup_player_counter][-1:])
                        temp_all_player_list[4].pop(sup_player_counter)

                        # print('found team')

                    else:
                        # print('not found')
                        if top_player_counter == 1 and jg_player_counter == 1 and mid_player_counter == 1 and \
                                adc_player_counter == 1 and sup_player_counter == 1 and \
                                max_team_num - found_team_count == 1:
                            # print('no condition')
                            no_possible_teams = True

                        elif sup_player_counter != left_team_number:
                            sup_player_counter += 1

                        elif adc_player_counter < left_team_number < sup_player_counter + 1:
                            adc_player_counter += 1
                            sup_player_counter = 1

                        elif mid_player_counter < left_team_number < adc_player_counter + 1:
                            mid_player_counter += 1
                            adc_player_counter, sup_player_counter = 1, 1

                        elif jg_player_counter < left_team_number < mid_player_counter + 1:
                            jg_player_counter += 1
                            mid_player_counter, adc_player_counter, sup_player_counter = 1, 1, 1

                        elif top_player_counter < left_team_number < jg_player_counter + 1:
                            top_player_counter += 1
                            jg_player_counter, mid_player_counter, adc_player_counter, sup_player_counter = 1, 1, 1, 1

                        elif top_player_counter + 1 > left_team_number:
                            no_possible_teams = True

                    # print(top_player_counter, jg_player_counter, mid_player_counter, adc_player_counter,
                    # sup_player_counter)

                    # print('sleep for 3 seconds')
                    # print('')
                    # time.sleep(3)

                # print(temp_all_player_list)

        # print(teams)
        # print(temp_all_player_list)
        # print(all_player_list)
        # print(rank_top, rank_adc)

        result_text += "Rankings: Iron:1, Bronze:2, Silver:3, Gold:4, Platinum:5,\n"
        result_text += "Diamond:6, Master:7, Grandmaster:8, Challenger:9.\n\n"
        result_text += "Average Rank Points per team: {:.2f}\n".format(avg_rank_per_team)
        result_text += "All teams are within the tolerance number of: ±{}\n\n".format(tolerance)

        if not no_possible_teams:
            result_text += "All players that will be put on a team: \n"

            for top in range(max_team_num):
                display_top = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[teams[top][1][:-2]][0],
                                                                  teams[top][1][:-2],
                                                                  player_dict[teams[top][1][:-2]][1])
                result_text += "Top    : {}\n".format(display_top)
            for jg in range(max_team_num):
                display_jg = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[teams[jg][2][:-2]][0],
                                                                 teams[jg][2][:-2],
                                                                 player_dict[teams[jg][2][:-2]][1])
                result_text += "Jg     : {}\n".format(display_jg)
            for mid in range(max_team_num):
                display_mid = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[teams[mid][3][:-2]][0],
                                                                  teams[mid][3][:-2],
                                                                  player_dict[teams[mid][3][:-2]][1])
                result_text += "Mid    : {}\n".format(display_mid)
            for adc in range(max_team_num):
                display_adc = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[teams[adc][4][:-2]][0],
                                                                  teams[adc][4][:-2],
                                                                  player_dict[teams[adc][4][:-2]][1])
                result_text += "ADC    : {}\n".format(display_adc)
            for sup in range(max_team_num):
                display_sup = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[teams[sup][5][:-2]][0],
                                                                  teams[sup][5][:-2],
                                                                  player_dict[teams[sup][5][:-2]][1])
                result_text += "Sup    : {}\n".format(display_sup)
            result_text += "\n\n"

            result_text += "All players that will not play: \n"

            # print(additional_top, additional_jg, additional_mid, additional_adc, additional_sup)

            if additional_top:
                for top in additional_top:
                    display_top = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[top[:-2]][0],
                                                                      top[:-2],
                                                                      player_dict[top[:-2]][1])
                    result_text += "Top    : {}\n".format(display_top)
            if additional_jg:
                for jg in additional_jg:
                    display_jg = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[jg[:-2]][0],
                                                                     jg[:-2],
                                                                     player_dict[jg[:-2]][1])
                    result_text += "Jg     : {}\n".format(display_jg)
            if additional_mid:
                for mid in additional_mid:
                    display_mid = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[mid[:-2]][0],
                                                                      mid[:-2],
                                                                      player_dict[mid[:-2]][1])
                    result_text += "Mid    : {}\n".format(display_mid)
            if additional_adc:
                for adc in additional_adc:
                    display_adc = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[adc[:-2]][0],
                                                                      adc[:-2],
                                                                      player_dict[adc[:-2]][1])
                    result_text += "ADC    : {}\n".format(display_adc)
            if additional_sup:
                for sup in additional_sup:
                    display_sup = "{:25s}\t-->\t{:35s}\t-\t{}".format(player_dict[sup[:-2]][0],
                                                                      sup[:-2],
                                                                      player_dict[sup[:-2]][1])
                    result_text += "Sup    : {}\n".format(display_sup)
            result_text += "\n"

        if no_possible_teams:
            result_text += 'Start another queue, program could not find optimal teams!\n\n'
        else:
            for k in range(max_team_num):

                player1, player2, player3, player4, player5 = teams[k][1], teams[k][2], teams[k][3], teams[k][4], \
                                                              teams[k][5]
                player_list = [player1, player2, player3, player4, player5]
                show_list = []

                # print(player_list)

                for player in player_list:

                    player = "{:18s} {}".format(player_dict[player[:-2]][0], player[-1:])
                    # print(player)

                    if player[-1:] == '1':
                        player = player[:-2] + " Iron"
                    elif player[-1:] == '2':
                        player = player[:-2] + " Bronze"
                    elif player[-1:] == '3':
                        player = player[:-2] + " Silver"
                    elif player[-1:] == '4':
                        player = player[:-2] + " Gold"
                    elif player[-1:] == '5':
                        player = player[:-2] + " Platinum"
                    elif player[-1:] == '6':
                        player = player[:-2] + " Diamond"
                    elif player[-1:] == '7':
                        player = player[:-2] + " Master"
                    elif player[-1:] == '8':
                        player = player[:-2] + " Grandmaster"
                    elif player[-1:] == '9':
                        player = player[:-2] + " Challenger"
                    show_list.append(player)

                # print(show_list)

                result_text += "Team {}\nTop    : {}\nJg     : {}\nMid    : {}\nADC    : {}\n" \
                               "Sup    : {}\nTotal Rank Point    : {}\n\n" \
                    .format(k + 1, show_list[0], show_list[1], show_list[2], show_list[3], show_list[4], teams[k][0])

            result_text += "All {} players are on their primary roles, " \
                           "{} players out of game!\n".format(max_team_num * 5, max_player_num - max_team_num * 5)
            result_text += "NO Auto-Fills! NO Secondary Roles!\n"
            result_text += "Most equal teams are created with respect to tolerances and rankings of the players!\n"

        print(result_text)

        if not no_possible_teams:
            if is_output_wanted():
                output_file_name = take_output_name()
                with open(output_file_name, "w") as result_output_file:
                    result_output_file.write(result_text)
            else:
                print('No output file.\n')

    # Create Teams Primary Ranked MMR System
    elif main_loop_inp == 'start pr mmr':
        print("This Module is not available right now!\n")
        pass

    # Create Teams Primary Secondary Ranked MMR
    elif main_loop_inp.strip() == 'start psr mmr':
        print("This Module is not available right now!\n")
        pass

    # Create Teams Primary Secondary AutoFill Ranked
    elif main_loop_inp.strip() == 'start psar yunus':
        print("This Module is not available right now!\n")
        pass

    # Else
    else:
        if first_time:
            first_time = False
            pass
        else:
            print('Invalid Command!')
            print('')

    main_loop_inp = input('Enter Command: ').lower()

# Program Ends
print('Good Bye!')
time.sleep(2)