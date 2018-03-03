#!/usr/bin/env python
import time
import sys
import argparse


class player(object):

    def __init__(self, player_name, IR_rating, OR_rating, SP_rating, LP_rating):
        self.Name = str(player_name)
        self.IR_rating = int(IR_rating)
        self.OR_rating = int(OR_rating)
        self.SP_rating = int(SP_rating)
        self.LP_rating = int(LP_rating)

    def rating(self, PlayType):
        if PlayType == 'IR':
            return self.IR_rating
        if PlayType == 'OR':
            return self.OR_rating
        if PlayType == 'SP':
            return self.SP_rating
        if PlayType == 'LP':
            return self.LP_rating


class play(object):

    def __init__(self, Name, Type, Yard, Recharge, Players, Chance):
        self.Name = str(Name)
        self.Type = str(Type)
        self.Yard = float(Yard)
        self.Recharge = int(Recharge)
        self.Player = Players.split(';')
        self.Chance = float(Chance)


class top8_play(object):

    def __init__(self, PlayName, PlayScore, PlayEnum):
        self.PlayName = str(PlayName)
        self.PlayScore = int(PlayScore)
        self.PlayEnum = int(PlayEnum)


# update_progress() : Displays or updates a console progress bar
# Accepts a float between 0 and 1. Any int will be converted to a float.
# A value under 0 represents a 'halt'.
# A value at 1 or bigger represents 100%
def update_progress(progress):
    ''' Displays or updates a console progress bar
        Accepts a float between 0 and 1. Any int will be converted to a float.
        A value under 0 represents a 'halt'.
        A value at 1 or bigger represents 100% '''

    barLength = 50  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = "\rPercent: [{0}] {1:.2f}% {2}".format("#" * block + "-" * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def create_parser():

    parser = argparse.ArgumentParser(description='get fuse value from a specific fuse file release area')
    parser.add_argument('-PlayerFile', help='path to the Player csv file', required=True)
    parser.add_argument('-PlayBookFile', help='path to the PlayBook csv file', required=True)

    return parser

def analyzer(PlayerCSVFilePath,PlaybookCSVFilePath):
    start_time = time.time()


    dict_Players = {}
    dict_Players['QB'] = []
    dict_Players['RB'] = []
    dict_Players['WR'] = []
    dict_Players['TE'] = []
    dict_Players['C'] = []

    dict_num_play_limit = {}
    dict_num_play_limit['IR'] = 0
    dict_num_play_limit['OR'] = 6
    dict_num_play_limit['SP'] = 0
    dict_num_play_limit['LP'] = 2

    list_Plays = []

    dict_bookkeeping = {}
    dict_totalscore = {}

    int_line_number = 0
    with open(PlayerCSVFilePath, 'r') as PlayerCSVFile:
        for line in PlayerCSVFile:
            line = line.strip()
            if line.startswith("#"):
                continue
            dict_Players[line.split(',')[1]].append(
                player(line.split(',')[0], line.split(',')[3], line.split(',')[4], line.split(',')[5],
                       line.split(',')[6]))
            # print (dict_Players[line.split(',')[1]][-1].Name,dict_Players[line.split(',')[1]][-1].rating('OR'))

    with open(PlaybookCSVFilePath, 'r') as PlaybookCSVFile:
        for line in PlaybookCSVFile:
            line = line.strip()
            if line.startswith("#"):
                continue
            list_Plays.append(
                play(line.split(',')[0], line.split(',')[1], line.split(',')[2], line.split(',')[3], line.split(',')[4],
                     line.split(',')[5]))

    float_total_progress = float(
        len(dict_Players['QB']) * len(dict_Players['RB']) * len(dict_Players['WR']) * len(dict_Players['TE']) * len(
            dict_Players['C']) * len(list_Plays))
    float_current_progress = 0.0

    # this will be a 6 level for loop to generate all possible player combination to calculate the score for all the
    # plays and rank by the top 8 score
    for each_QB in dict_Players['QB']:
        for each_RB in dict_Players['RB']:
            for each_WR in dict_Players['WR']:
                for each_TE in dict_Players['TE']:
                    for each_C in dict_Players['C']:
                        list_top8_plays = []  # keep track of the top 8 plays
                        dict_top8_plays = {}
                        dict_top8_plays['IR'] = []
                        dict_top8_plays['OR'] = []
                        dict_top8_plays['SP'] = []
                        dict_top8_plays['LP'] = []

                        str_all_players_name = each_QB.Name + ';' + each_RB.Name + ';' + each_WR.Name + ';' + each_TE.Name + ';' + each_C.Name
                        if not str_all_players_name in dict_bookkeeping:
                            dict_bookkeeping[str_all_players_name] = {}
                            dict_bookkeeping[str_all_players_name]['Top8 Plays'] = []
                            dict_bookkeeping[str_all_players_name]['Total Score'] = 0
                        int_play_enum = -1
                        for each_play in list_Plays:
                            int_play_enum += 1
                            current_scoring = 0
                            for each_required_player in each_play.Player:
                                if each_required_player == 'QB':
                                    current_scoring = current_scoring + each_QB.rating(each_play.Type)
                                if each_required_player == 'RB':
                                    current_scoring = current_scoring + each_RB.rating(each_play.Type)
                                if each_required_player == 'WR':
                                    current_scoring = current_scoring + each_WR.rating(each_play.Type)
                                if each_required_player == 'TE':
                                    current_scoring = current_scoring + each_TE.rating(each_play.Type)
                                if each_required_player == 'C':
                                    current_scoring = current_scoring + each_C.rating(each_play.Type)

                                    # scale it based on chance
                            # current_scoring = current_scoring * each_play.Chance

                            if (not dict_top8_plays[each_play.Type]) and (
                                    dict_num_play_limit[each_play.Type] != 0):  # the list is empty
                                dict_top8_plays[each_play.Type].append(
                                    top8_play(each_play.Name, current_scoring, int_play_enum))
                            else:
                                int_index = 0
                                bool_inserted = False
                                for each_top_playscore in dict_top8_plays[each_play.Type]:
                                    if current_scoring > each_top_playscore.PlayScore:
                                        bool_inserted = True
                                        dict_top8_plays[each_play.Type].insert(int_index, top8_play(each_play.Name,
                                                                                                    current_scoring,
                                                                                                    int_play_enum))
                                        break
                                    int_index = int_index + 1
                                if not (bool_inserted) and len(dict_top8_plays[each_play.Type]) < dict_num_play_limit[
                                    each_play.Type]:
                                    dict_top8_plays[each_play.Type].append(
                                        top8_play(each_play.Name, current_scoring, int_play_enum))

                            if len(dict_top8_plays[each_play.Type]) > dict_num_play_limit[each_play.Type]:
                                dict_top8_plays[each_play.Type] = dict_top8_plays[each_play.Type][:-1]

                            float_current_progress = float_current_progress + 1.0
                            update_progress(float_current_progress / float_total_progress)

                        for each_playtype in dict_top8_plays:
                            for index in range(0, len(dict_top8_plays[each_playtype])):
                                dict_bookkeeping[str_all_players_name]['Top8 Plays'].append(
                                    dict_top8_plays[each_playtype][index])
                                dict_bookkeeping[str_all_players_name]['Total Score'] += dict_top8_plays[each_playtype][
                                    index].PlayScore

    int_show_number_of_choice = 5
    int_number_of_choice_shown = 0

    for each_playercombo, each_top8_list in sorted(dict_bookkeeping.iteritems(), key=lambda kv: kv[1]['Total Score'],
                                                   reverse=True):
        print (each_playercombo, each_top8_list['Total Score'])
        for each_list in each_top8_list['Top8 Plays']:
            print (each_list.PlayName, each_list.PlayScore, list_Plays[each_list.PlayEnum].Type,
                   list_Plays[each_list.PlayEnum].Recharge, list_Plays[each_list.PlayEnum].Yard,
                   list_Plays[each_list.PlayEnum].Chance, list_Plays[each_list.PlayEnum].Player)
            # for each_position in list_Plays[each_list.PlayEnum].Player:
            #     for each_player_name in each_playercombo.split(';'):
            #          for each_player in dict_Players[each_position]:
            #               if each_player_name == each_player.Name:
            #                    print (each_player.Name, each_player.rating(list_Plays[each_list.PlayEnum].Type))

        print ('\n')
        int_number_of_choice_shown += 1
        if int_show_number_of_choice == int_number_of_choice_shown:
            break

    stop_time = time.time()

    print('total execution time: ' + str(stop_time - start_time))


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    analyzer(args.PlayerFile, args.PlayBookFile)


