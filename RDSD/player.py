"""
File for Rune Age's RDSD - Résurgence du Seigneur Dragon
"""

import random


# TODO : add Cataclysm scenario mode
# Currently Enemies either attack a specific player or all players
# Feature where players can choose which player will defend against an Enemy
# has been implemented but has not been tested yet
# It can be used in Cataclysm

# TODO : add graphics !!


class GoldCard:
    def __init__(
        self,
        name_given,
        gold_value_given,
        cost_given,
    ):
        self.name = name_given
        self.type = "Gold"
        self.gold = gold_value_given
        self.cost = cost_given

    def __str__(self):
        return (
            self.name
            + "\t\t\tGold value : "
            + str(self.gold)
            + "\t\tCost to purchase : "
            + str(self.cost)
            + " Influence point(s)\n"
        )


class Player:
    def __init__(
        self, name_given, nation_name_given, deck_given, shop_given, game_given
    ):
        self.name = name_given
        self.life_points = 20
        self.nation_name = nation_name_given
        self.gold_points = 0
        self.influence_points = 0
        self.strength_points = 0
        self.bonus_in_def = 0
        self.can_reroll_death_dice = False
        self.nb_battle_roar_activated = 0
        self.personal_cities_acquired = 0
        self.cities_acquired = []
        self.hand = []
        self.max_nb_cards_in_hand = 5
        self.deck = deck_given
        random.shuffle(self.deck)
        self.graveyard = []
        self.rewards = []
        self.shop = shop_given
        self.game = game_given

        for _ in range(5):
            self.draw()

    def draw(self):
        if len(self.deck) == 0:
            self.convert_graveyard_into_deck()

        self.hand.append(self.deck.pop())

        print("\n", self.name, " has just drawn following card :")
        print(self.hand[-1], "\n")

    def discard_a_card(self, must_display_hand=True):
        if len(self.hand) > 0:
            if must_display_hand:
                self.display_hand(must_keep_playing=False)
            print("\nWhich card do you want to discard ?")
            answer_tmp = str(input("\n> "))
            while answer_tmp not in [
                str(index_tmp) for index_tmp in range(len(self.hand))
            ]:
                answer_tmp = str(input("\n> "))
            self.discard(index_card_to_discard=int(answer_tmp), must_print=True)

    def discard(self, index_card_to_discard=0, must_print=True):
        if len(self.hand) > 0:
            self.graveyard.append(self.hand.pop(index_card_to_discard))

            if must_print:
                print("\nFollowing card has been discarded :")
                print(self.graveyard[-1], "\n")

    def retrieve_a_card_from_graveyard(self):
        for index_card_tmp in range(len(self.graveyard)):
            print(self.graveyard[index_card_tmp].name, " = ", index_card_tmp)

        print("\nWhich card do you want to retrieve ?")
        answer_tmp = str(input("\n> "))
        while answer_tmp not in [str(index_tmp) for index_tmp in range(len(self.hand))]:
            answer_tmp = str(input("\n> "))

        self.hand.append(self.graveyard.pop(int(answer_tmp)))

    def convert_graveyard_into_deck(self):
        self.deck = [card_tmp for card_tmp in self.graveyard]
        self.graveyard = []
        random.shuffle(self.deck)

        print("\nYour deck has been shuffled and your Graveyard is now empty.\n")

    def display_hand(self, must_keep_playing=True):
        if len(self.hand) > 0:
            print("\nHere is your hand :")
            for index_card in range(len(self.hand)):
                print(self.hand[index_card].name, " = ", index_card)
        else:
            print("\nYour hand is empty.")

        print("\n")

        if must_keep_playing:
            self.play_a_turn()

    def get_info_from_card_in_hand(self):
        print("\nPlease enter the index of the card you want to get info from : ")
        answer_tmp = str(input("\n> "))
        while answer_tmp not in [str(index_tmp) for index_tmp in range(len(self.hand))]:
            answer_tmp = str(input("\n> "))
        print("\n\nInfo of selected card : ")
        print(self.hand[int(answer_tmp)], "\n")

        self.play_a_turn()

    def play_spell_card(self, must_keep_playing=True):
        self.display_hand(must_keep_playing=False)
        print("\nTo cancel, enter 99 in the following input.")
        print("Which spell card do you want to play ?")

        answer_tmp = str(input("\n> "))
        while answer_tmp not in ["99"] + [
            str(index_tmp) for index_tmp in range(len(self.hand))
        ]:
            answer_tmp = str(input("\n> "))

        if answer_tmp != "99":
            spell_card_to_play = self.hand[int(answer_tmp)]

            if isinstance(spell_card_to_play, SpellCard):
                print("\nActivation of the spell ", spell_card_to_play.name, " !")
                self.graveyard.append(self.hand.pop(int(answer_tmp)))

                if spell_card_to_play.name == "Battle Roar":
                    self.nb_battle_roar_activated += 1
                elif spell_card_to_play.name == "Forced March":
                    forced_march(self)

            else:
                print("\nPlease play a spell card !")

        else:
            print("\nCancelling...")

        if must_keep_playing:
            self.play_a_turn()

    def buy_a_personal_city(self):
        if self.personal_cities_acquired < 3:
            list_of_spent_cards = []
            must_continue = len(self.hand) > 0
            must_cancel = False

            if must_continue:
                print(
                    "\nA Personal City costs 4 Gold and makes you gain 1 Influence point per turn."
                )
                print(
                    "If you want to buy one, please select Gold cards to spend in your hand."
                )
                print("If you want to cancel, enter 99 in any of your inputs.")
                print(
                    "If you choose to cancel, all previously chosen cards"
                    + " will be moved back in your hand.\n"
                )
            else:
                print("\nYour hand is empty !")

            while must_continue:
                self.display_hand(must_keep_playing=False)
                print("\nWhich card do you want to spend ?")
                answer_tmp = str(input("\n> "))
                while answer_tmp not in ["99"] + [
                    str(index_tmp) for index_tmp in range(len(self.hand))
                ]:
                    answer_tmp = str(input("\n> "))

                if answer_tmp == "99":
                    must_continue = False
                    must_cancel = True

                if must_continue:
                    if isinstance(self.hand[int(answer_tmp)], GoldCard):
                        list_of_spent_cards.append(self.hand.pop(int(answer_tmp)))
                        print(
                            "\nThe selected card has been added to the list of cards to spend."
                        )
                    else:
                        print("\nPlease select a Gold card !")

                    if len(self.hand) > 0:
                        print(
                            "Do you want to continue spending cards ?\nOui = 0\nNon = 1"
                        )
                        answer_tmp = str(input("\n> "))
                        while not answer_tmp in ["0", "1"]:
                            answer_tmp = str(input("\n> "))
                    else:
                        answer_tmp = "1"

                if answer_tmp == "99":
                    must_continue = False
                    must_cancel = True
                elif answer_tmp == "1":
                    must_continue = False

                if must_cancel:
                    while len(list_of_spent_cards) > 0:
                        self.hand.append(list_of_spent_cards.pop(0))
                    print("\nAction successfully cancelled.")

            if not must_cancel:
                total_of_money = sum(
                    [card_tmp.gold for card_tmp in list_of_spent_cards]
                )
                print("\nYour total of money currently is ", total_of_money)
                if self.gold_points > 0 and total_of_money < 4:
                    print(
                        "Do you want to use gold from your Rewards ?\nOui = 0\nNon = 1"
                    )
                    answer_tmp = str(input("\n> "))
                    while not answer_tmp in ["0", "1"]:
                        answer_tmp = str(input("\n> "))

                    if answer_tmp == "0":
                        total_of_money += self.gold_points
                        self.gold_points = 0

                        print("\nYour new total of money is ", total_of_money)

                if total_of_money >= 4:
                    print("\nYou successfully bought a Personal City !")
                    self.personal_cities_acquired += 1
                    self.influence_points += 1
                else:
                    print("\nInsufficient money to buy a Personal City...")
                    if len(list_of_spent_cards) > 0:
                        print(
                            "Trying to scam me ? I'll keep your money as a punishment !"
                        )

                for gold_card_tmp in list_of_spent_cards:
                    self.graveyard.append(gold_card_tmp)

        else:
            print("\nYou already have acquired all of your Personal Cities !")

        self.play_a_turn()

    def buy_a_unit(
        self,
        add_unit_to_hand_instead=False,
        must_keep_playing=True,
        can_purchase_many_units=True,
    ):
        list_of_spent_cards = []
        must_continue = len(self.hand) > 0 or self.gold_points > 0
        must_cancel = False

        list_of_unit_costs = [unit_tmp.cost for unit_tmp in self.shop.units]

        if must_continue:
            print("\nUnits you can buy have prices as follow :")
            for index_unit_tmp in range(len(self.shop.units)):
                if self.shop.nb_remaining_units[index_unit_tmp] > 0:
                    print(
                        self.shop.units[index_unit_tmp].name,
                        " (cost : ",
                        self.shop.units[index_unit_tmp].cost,
                        ", strength : ",
                        self.shop.units[index_unit_tmp].strength,
                        ")\t\tRemaining Units in shop : ",
                        self.shop.nb_remaining_units[index_unit_tmp],
                    )

            if len(self.hand) > 0:
                print(
                    "If you want to buy one, please select Gold cards to spend in your hand."
                )
                print("If you want to cancel, enter 99 in any of your inputs.")
                print(
                    "If you choose to cancel, all previously chosen cards"
                    + " will be moved back in your hand.\n"
                )
        else:
            print("\nYour hand is empty and you have no Rewards that give you Gold !")
            must_cancel = True

        while must_continue:
            if len(self.hand) > 0:
                self.display_hand(must_keep_playing=False)
                print("\nIf you want to cancel, enter 99 in any of your inputs.")
                print("Which card do you want to spend ?")
                answer_tmp = str(input("\n> "))
                while answer_tmp not in ["99"] + [
                    str(index_tmp) for index_tmp in range(len(self.hand))
                ]:
                    answer_tmp = str(input("\n> "))

                if answer_tmp == "99":
                    must_continue = False
                    must_cancel = True

                if must_continue:
                    if isinstance(self.hand[int(answer_tmp)], GoldCard):
                        list_of_spent_cards.append(self.hand.pop(int(answer_tmp)))
                        print(
                            "\nThe selected card has been added to the list of cards to spend."
                        )
                    else:
                        print("\nPlease select a Gold card !")

                    if len(self.hand) > 0:
                        print(
                            "Do you want to continue spending cards ?\nOui = 0\nNon = 1"
                        )
                        answer_tmp = str(input("\n> "))
                        while not answer_tmp in ["0", "1"]:
                            answer_tmp = str(input("\n> "))
                    else:
                        answer_tmp = "1"

                if answer_tmp == "99":
                    must_continue = False
                    must_cancel = True
                elif answer_tmp == "1":
                    must_continue = False

                if must_cancel:
                    while len(list_of_spent_cards) > 0:
                        self.hand.append(list_of_spent_cards.pop(0))
                    print("\nAction successfully cancelled.")

            else:
                must_continue = False

        if not must_cancel:
            total_of_money = sum([card_tmp.gold for card_tmp in list_of_spent_cards])
            print("\nYour total of money currently is ", total_of_money)

            if self.gold_points > 0:
                print("Do you want to use gold from your Rewards ?\nOui = 0\nNon = 1")
                answer_tmp = str(input("\n> "))
                while not answer_tmp in ["0", "1"]:
                    answer_tmp = str(input("\n> "))

                if answer_tmp == "0":
                    total_of_money += self.gold_points
                    self.gold_points = 0

                    print("\nYour new total of money is ", total_of_money)

            if can_purchase_many_units:
                # then buy a unit until there is no more money
                # with possibility of cancelling
                for gold_card_tmp in list_of_spent_cards:
                    self.graveyard.append(gold_card_tmp)

                while total_of_money > 0:
                    print(
                        "\nPlease select a Unit card to buy among following possible choices :"
                    )
                    list_of_indices_purchasable_units = []
                    for index_unit_tmp in range(len(self.shop.units)):
                        if (
                            self.shop.nb_remaining_units[index_unit_tmp] > 0
                            and self.shop.units[index_unit_tmp].cost <= total_of_money
                        ):
                            print(
                                self.shop.units[index_unit_tmp].name,
                                " = ",
                                index_unit_tmp,
                            )
                            list_of_indices_purchasable_units.append(
                                str(index_unit_tmp)
                            )

                    print("To cancel, enter 99 in the following input.")
                    list_of_indices_purchasable_units.append("99")

                    print("\nWhich card do you want to buy ?")
                    answer_tmp = str(input("\n> "))
                    while not answer_tmp in list_of_indices_purchasable_units:
                        answer_tmp = str(input("\n> "))

                    if answer_tmp != "99":
                        unit_to_append_tmp = self.shop.units[int(answer_tmp)]

                        # TODO : continuously update here !

                        if isinstance(unit_to_append_tmp, Ravageur):
                            unit_to_append = Ravageur()
                        elif isinstance(unit_to_append_tmp, Spiritiste):
                            unit_to_append = Spiritiste()
                        elif isinstance(unit_to_append_tmp, ChefDeGuerre):
                            unit_to_append = ChefDeGuerre()

                        elif isinstance(unit_to_append_tmp, Fantassin):
                            unit_to_append = Fantassin()
                        elif isinstance(unit_to_append_tmp, Chevalier):
                            unit_to_append = Chevalier()
                        elif isinstance(unit_to_append_tmp, MageNovice):
                            unit_to_append = MageNovice()
                        elif isinstance(unit_to_append_tmp, MachineDeSiege):
                            unit_to_append = MachineDeSiege()
                        elif isinstance(unit_to_append_tmp, GuerrierRoc):
                            unit_to_append = GuerrierRoc()

                        elif isinstance(unit_to_append_tmp, Ranime):
                            unit_to_append = Ranime()
                        elif isinstance(unit_to_append_tmp, Necromancien):
                            unit_to_append = Necromancien()
                        elif isinstance(unit_to_append_tmp, Vampire):
                            unit_to_append = Vampire()
                        elif isinstance(unit_to_append_tmp, ChevalierNoir):
                            unit_to_append = ChevalierNoir()
                        elif isinstance(unit_to_append_tmp, Wyrm):
                            unit_to_append = Wyrm()

                        else:
                            unit_to_append = Unit(
                                unit_to_append_tmp.name,
                                unit_to_append_tmp.strength,
                                unit_to_append_tmp.cost,
                            )

                        print(
                            "\n\nYou successfully bought : ",
                            unit_to_append.name,
                            " !",
                        )
                        # create a copy so that all units are independant from each other
                        # python .append does not create a copy of the appened object
                        if add_unit_to_hand_instead:
                            self.hand.append(unit_to_append)
                            print("The Unit has been put into your hand.\n")
                        else:
                            self.graveyard.append(unit_to_append)
                            print("The Unit has been put into your Graveyard.\n")

                        self.shop.nb_remaining_units[int(answer_tmp)] -= 1

                        total_of_money -= unit_to_append.cost

                    else:
                        # if we cancel at this stage, then all remaining money
                        # is wasted
                        total_of_money = 0

                    print("\n")

            elif total_of_money > 0:
                # else, buy a single unit and stop
                print(
                    "\nPlease select a Unit card to buy among following possible choices :"
                )
                list_of_indices_purchasable_units = []
                for index_unit_tmp in range(len(self.shop.units)):
                    if (
                        self.shop.nb_remaining_units[index_unit_tmp] > 0
                        and self.shop.units[index_unit_tmp].cost <= total_of_money
                    ):
                        print(
                            self.shop.units[index_unit_tmp].name, " = ", index_unit_tmp
                        )
                        list_of_indices_purchasable_units.append(str(index_unit_tmp))

                print("To cancel, enter 99 in the following input.")
                list_of_indices_purchasable_units.append("99")

                print("\nWhich card do you want to buy ?")
                answer_tmp = str(input("\n> "))
                while not answer_tmp in list_of_indices_purchasable_units:
                    answer_tmp = str(input("\n> "))

                if answer_tmp != "99":
                    unit_to_append_tmp = self.shop.units[int(answer_tmp)]

                    # TODO : continuously update here !

                    if isinstance(unit_to_append_tmp, Ravageur):
                        unit_to_append = Ravageur()
                    elif isinstance(unit_to_append_tmp, Spiritiste):
                        unit_to_append = Spiritiste()
                    elif isinstance(unit_to_append_tmp, ChefDeGuerre):
                        unit_to_append = ChefDeGuerre()

                    elif isinstance(unit_to_append_tmp, Fantassin):
                        unit_to_append = Fantassin()
                    elif isinstance(unit_to_append_tmp, Chevalier):
                        unit_to_append = Chevalier()
                    elif isinstance(unit_to_append_tmp, MageNovice):
                        unit_to_append = MageNovice()
                    elif isinstance(unit_to_append_tmp, MachineDeSiege):
                        unit_to_append = MachineDeSiege()
                    elif isinstance(unit_to_append_tmp, GuerrierRoc):
                        unit_to_append = GuerrierRoc()

                    elif isinstance(unit_to_append_tmp, Ranime):
                        unit_to_append = Ranime()
                    elif isinstance(unit_to_append_tmp, Necromancien):
                        unit_to_append = Necromancien()
                    elif isinstance(unit_to_append_tmp, Vampire):
                        unit_to_append = Vampire()
                    elif isinstance(unit_to_append_tmp, ChevalierNoir):
                        unit_to_append = ChevalierNoir()
                    elif isinstance(unit_to_append_tmp, Wyrm):
                        unit_to_append = Wyrm()

                    else:
                        unit_to_append = Unit(
                            unit_to_append_tmp.name,
                            unit_to_append_tmp.strength,
                            unit_to_append_tmp.cost,
                        )

                    print(
                        "\n\nYou successfully bought : ",
                        unit_to_append.name,
                        " !",
                    )
                    # create a copy so that all units are independant from each other
                    # python .append does not create a copy of the appened object
                    if add_unit_to_hand_instead:
                        self.hand.append(unit_to_append)
                        print("The Unit has been put into your hand.\n")
                    else:
                        self.graveyard.append(unit_to_append)
                        print("The Unit has been put into your Graveyard.\n")

                    self.shop.nb_remaining_units[int(answer_tmp)] -= 1

                    for gold_card_tmp in list_of_spent_cards:
                        self.graveyard.append(gold_card_tmp)

                    for index_unit in range(len(self.shop.units)):
                        print(
                            "You still have ",
                            self.shop.nb_remaining_units[index_unit],
                            " units ",
                            self.shop.units[index_unit].name,
                            " in your Shop.",
                        )
                    print("\n")

        if must_keep_playing:
            self.play_a_turn()

    def buy_spell_card_or_neutral_unit_with_influence(self):
        if self.influence_points > 0:
            print("\nYou currently have ", self.influence_points, " influence points.")
            print("\nWhich neutral card do you want to buy ?")
            list_of_possibilities = ["99"]

            index_neutral_card = 0
            while index_neutral_card < len(self.game.available_spell_cards):
                if (
                    self.game.available_spell_cards[index_neutral_card].influence
                    <= self.influence_points
                    and self.game.nb_available_spell_cards[index_neutral_card] > 0
                ):
                    print(
                        self.game.available_spell_cards[index_neutral_card].name,
                        " = ",
                        index_neutral_card,
                    )
                    list_of_possibilities.append(str(index_neutral_card))
                index_neutral_card += 1

            index_neutral_card = 0
            while index_neutral_card < len(self.game.available_neutral_units):
                # yeah it's not influence attribute here
                # a unit has a cost, while spells have not cost attribute
                # they have an influence attribute to resolve some effects
                # may be changed in the future
                if (
                    self.game.available_neutral_units[index_neutral_card].cost
                    <= self.influence_points
                    and self.game.nb_available_neutral_units[index_neutral_card] > 0
                ):
                    print(
                        self.game.available_neutral_units[index_neutral_card].name,
                        " = ",
                        index_neutral_card + len(self.game.available_spell_cards),
                    )
                    list_of_possibilities.append(
                        str(index_neutral_card + len(self.game.available_spell_cards))
                    )
                index_neutral_card += 1

            print("\nTo cancel, enter 99 in the following input.")
            print("Which neutral card do you want to buy ?")
            answer_tmp = str(input("\n> "))
            while answer_tmp not in list_of_possibilities:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "99":
                print("\nCancelling purchase...")
            else:
                index_neutral_card = int(answer_tmp)
                if index_neutral_card < len(self.game.available_spell_cards):
                    neutral_card_to_buy = self.game.available_spell_cards[
                        index_neutral_card
                    ]
                    self.game.nb_available_spell_cards[index_neutral_card] -= 1
                    self.influence_points -= neutral_card_to_buy.influence

                    self.graveyard.append(
                        SpellCard(
                            neutral_card_to_buy.name,
                            neutral_card_to_buy.influence,
                            neutral_card_to_buy.effect,
                        )
                    )

                else:
                    index_neutral_card -= len(self.game.available_spell_cards)
                    if index_neutral_card < len(self.game.available_neutral_units):
                        neutral_card_to_buy = self.game.available_neutral_units[
                            index_neutral_card
                        ]
                        self.game.nb_available_neutral_units[index_neutral_card] -= 1
                        self.influence_points -= neutral_card_to_buy.cost

                        self.graveyard.append(
                            Unit(
                                neutral_card_to_buy.name,
                                neutral_card_to_buy.strength,
                                neutral_card_to_buy.cost,
                            )
                        )

                print("\nYou successfully bought : ")
                print(self.graveyard[-1])
                print("This neutral card has been added to your graveyard.")
        else:
            print("\nYou have no more influence points...")
            print("Please come back later !")

        self.play_a_turn()

    def buy_a_gold_card_with_influence(self):
        if self.influence_points > 0:
            print("\nYou currently have ", self.influence_points, " influence points.")
            print("\nWhich Gold card do you want to buy ?")
            list_of_possibilities = ["99"]
            if self.game.nb_gold_1_cards > 0 and self.influence_points >= 1:
                print(
                    "Gold card of 1 Gold\t\tCost to purchase : 1 Influence point\t\t= 0"
                )
                list_of_possibilities.append("0")
            if self.game.nb_gold_2_cards > 0 and self.influence_points >= 3:
                print(
                    "Gold card of 2 Gold\t\tCost to purchase : 3 Influence points\t\t= 1"
                )
                list_of_possibilities.append("1")
            if self.game.nb_gold_3_cards > 0 and self.influence_points >= 5:
                print(
                    "Gold card of 3 Gold\t\tCost to purchase : 5 Influence points\t\t= 2"
                )
                list_of_possibilities.append("2")

            print("\nTo cancel, enter 99 in the following input.")
            print("Which Gold card do you want to buy ?")
            answer_tmp = str(input("\n> "))
            while answer_tmp not in list_of_possibilities:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "99":
                print("\nCancelling purchase...")
            else:
                if answer_tmp == "0":
                    print("\nYou successfully bought a Gold card 1 !")
                    self.graveyard.append(GoldCard("Gold Card 1", 1, 1))
                    self.game.nb_gold_1_cards -= 1
                    self.influence_points -= 1
                elif answer_tmp == "1":
                    print("\nYou successfully bought a Gold card 2 !")
                    self.graveyard.append(GoldCard("Gold Card 2", 2, 3))
                    self.game.nb_gold_2_cards -= 1
                    self.influence_points -= 3
                elif answer_tmp == "2":
                    print("\nYou successfully bought a Gold card 3 !")
                    self.graveyard.append(GoldCard("Gold Card 3", 3, 5))
                    self.game.nb_gold_3_cards -= 1
                    self.influence_points -= 5
                print("This gold card has been added to your graveyard.")
        else:
            print("\nYou have no more influence points...")
            print("Please come back later !")

        self.play_a_turn()

    def get_summary(self):
        print(
            "\nYou have acquired ", self.personal_cities_acquired, " personal cities."
        )
        print("\nYou still have ", self.influence_points, " influence points.")
        print("\nAvailable neutral cities :")
        list_of_cities_that_can_be_attacked = []
        for city_tmp in self.game.available_neutral_cities:
            if not city_tmp.is_bought:
                list_of_cities_that_can_be_attacked.append(city_tmp)
        for city_tmp in list_of_cities_that_can_be_attacked:
            print(city_tmp)

        print("\nAcquired cities : ")
        for city_tmp in self.cities_acquired:
            print(city_tmp)

        print("\nAll remaining enemies to slain : \n")
        for enemy_tmp in self.game.spawned_enemies:
            print(enemy_tmp)

        print("\nYou still have ", len(self.deck), " cards in your deck.\n")
        for index_unit in range(len(self.shop.units)):
            print(
                "You still have ",
                self.shop.nb_remaining_units[index_unit],
                " units ",
                self.shop.units[index_unit].name,
                " in your Shop.",
            )

        print("\n")
        for index_spell_card in range(len(self.game.available_spell_cards)):
            print(
                "You still have ",
                self.game.nb_available_spell_cards[index_spell_card],
                " spell cards ",
                self.game.available_spell_cards[index_spell_card].name,
                " in your Influence Shop.",
            )
        for index_neutral_unit in range(len(self.game.available_neutral_units)):
            print(
                "You still have ",
                self.game.nb_available_neutral_units[index_neutral_unit],
                " neutral units ",
                self.game.available_neutral_units[index_neutral_unit].name,
                " in your Influence Shop.",
            )

        print("\nYou have ", len(self.graveyard), " card(s) in your Graveyard.")

        if len(self.rewards) > 0:
            print("\nYou have won following Rewards :")
            for reward_tmp in self.rewards:
                print(reward_tmp)
        else:
            print("\nYou have not won any Reward...")

        print("\nTo skip this step, enter 0.\nTo see other players hand, enter 1.\n")
        list_of_possibilities = ["0", "1"]

        print("What do you want to do ?")
        answer_tmp = str(input("\n> "))
        while answer_tmp not in list_of_possibilities:
            answer_tmp = str(input("\n> "))

        if answer_tmp == "1":
            for other_player_tmp in self.game.players:
                # assuming a player's name is unique
                if other_player_tmp.name != self.name:
                    print("\nDisplaying hand of player ", other_player_tmp.name, " : ")
                    other_player_tmp.display_hand(must_keep_playing=False)

            print("\n")

        self.play_a_turn()

    def show_graveyard(self, must_keep_playing=True):
        print("\nHere is the content of your graveyard :")
        for card_tmp in self.graveyard:
            print(card_tmp)
        print("\n")

        if must_keep_playing:
            self.play_a_turn()

    def attack_a_personal_city(self):
        if self.personal_cities_acquired < 3:
            list_of_played_cards = []
            must_continue = len(self.hand) > 0
            must_cancel = len(self.hand) == 0

            while must_continue:
                print("\nA personal city has a strength of 2.")
                print("Choose units from your hand to attack the city !\n")

                self.display_hand(must_keep_playing=False)
                answer_tmp = str(input("\n> "))
                while answer_tmp not in [
                    str(index_tmp) for index_tmp in range(len(self.hand))
                ]:
                    answer_tmp = str(input("\n> "))

                if isinstance(self.hand[int(answer_tmp)], Unit):
                    list_of_played_cards.append(self.hand.pop(int(answer_tmp)))
                    print(
                        "\nFollowing card has been added to the list of "
                        + "participating units !"
                    )
                    print(list_of_played_cards[-1])

                    if list_of_played_cards[-1].effect_type == "When played":
                        if isinstance(list_of_played_cards[-1], GuerrierRoc):
                            list_of_played_cards[-1].apply_effect(
                                self, list_of_played_cards[:-1]
                            )
                        elif isinstance(list_of_played_cards[-1], Ranime):
                            returned_card = list_of_played_cards[-1].apply_effect(self)
                            if returned_card is not None:
                                list_of_played_cards.append(returned_card)
                        else:
                            list_of_played_cards[-1].apply_effect(self)

                else:
                    print("Please add only Unit cards to the fight !")

                if len(self.hand) > 0:
                    print("\nDo you want to continue adding units to the fight ?")
                    print("Oui = 0\nNon = 1")
                    answer_tmp = str(input("\n> "))
                    while answer_tmp not in ["0", "1"]:
                        answer_tmp = str(input("\n> "))
                else:
                    answer_tmp = "1"

                if answer_tmp == "1":
                    must_continue = False

            if not must_cancel:
                for played_card_tmp in list_of_played_cards:
                    if played_card_tmp.effect_type == "Resolution":
                        played_card_tmp.apply_effect(self)

                total_strength = sum(
                    [unit_tmp.strength for unit_tmp in list_of_played_cards]
                ) + self.nb_battle_roar_activated * len(list_of_played_cards)
                if self.nb_battle_roar_activated > 0:
                    self.nb_battle_roar_activated = 0
                print("\nTotal strength of your army : ", total_strength)
                print("Targeted city strength : 2")
                if total_strength >= 2:
                    print("\nYou have acquired a personal city !")
                    self.personal_cities_acquired += 1
                    self.influence_points += 1
                    print(
                        "You now have ",
                        self.personal_cities_acquired,
                        " acquired personal cities !\n",
                    )
                else:
                    print(
                        "\nYour army is not strong enough to acquire a personal city...\n"
                    )

                for unit_tmp in list_of_played_cards:
                    unit_tmp.strength = unit_tmp.initial_strength
                    self.graveyard.append(unit_tmp)

            else:
                print("\nYour hand is empty !")

        else:
            print("\nYou already have acquired all of your personal cities...\n")

        self.play_a_turn()

    def attack_a_neutral_city(self):
        list_of_cities_that_can_be_attacked = []
        for city_tmp in self.game.available_neutral_cities:
            if not city_tmp.is_bought:
                list_of_cities_that_can_be_attacked.append(city_tmp)

        if len(list_of_cities_that_can_be_attacked) > 0 and len(self.hand) > 0:
            list_of_possibilities = []
            print("\nYou can attack one of following neutral cities :")
            for index_city in range(len(list_of_cities_that_can_be_attacked)):
                print(
                    index_city, " = ", list_of_cities_that_can_be_attacked[index_city]
                )
                list_of_possibilities.append(str(index_city))

            print("\nWhich neutral city do you want to attack ?")
            answer_tmp = str(input("\n> "))
            while answer_tmp not in list_of_possibilities:
                answer_tmp = str(input("\n> "))

            targeted_city = list_of_cities_that_can_be_attacked[int(answer_tmp)]
            print("\nOk, you're now attacking following city :")
            print(targeted_city, "\n")

            list_of_played_cards = []
            must_continue = True

            while must_continue:
                print("Choose units from your hand to attack the city !")

                self.display_hand(must_keep_playing=False)
                answer_tmp = str(input("\n> "))
                while answer_tmp not in [
                    str(index_tmp) for index_tmp in range(len(self.hand))
                ]:
                    answer_tmp = str(input("\n> "))

                if isinstance(self.hand[int(answer_tmp)], Unit):
                    list_of_played_cards.append(self.hand.pop(int(answer_tmp)))
                    print(
                        "\nFollowing card has been added to the list of "
                        + "participating units !"
                    )
                    print(list_of_played_cards[-1])

                    if list_of_played_cards[-1].effect_type == "When played":
                        if isinstance(list_of_played_cards[-1], GuerrierRoc):
                            list_of_played_cards[-1].apply_effect(
                                self, list_of_played_cards[:-1]
                            )
                        elif isinstance(list_of_played_cards[-1], Ranime):
                            returned_card = list_of_played_cards[-1].apply_effect(self)
                            if returned_card is not None:
                                list_of_played_cards.append(returned_card)
                        else:
                            list_of_played_cards[-1].apply_effect(self)

                else:
                    print("Please add only Unit cards to the fight !")

                if len(self.hand) > 0:
                    print("\nDo you want to continue adding units to the fight ?")
                    print("Oui = 0\nNon = 1")
                    answer_tmp = str(input("\n> "))
                    while answer_tmp not in ["0", "1"]:
                        answer_tmp = str(input("\n> "))
                else:
                    answer_tmp = "1"

                if answer_tmp == "1":
                    must_continue = False

            for played_card_tmp in list_of_played_cards:
                if played_card_tmp.effect_type == "Resolution":
                    played_card_tmp.apply_effect(self)

            total_strength = sum(
                [unit_tmp.strength for unit_tmp in list_of_played_cards]
            ) + self.nb_battle_roar_activated * len(list_of_played_cards)
            if self.nb_battle_roar_activated > 0:
                self.nb_battle_roar_activated = 0
            print("\nTotal strength of your army : ", total_strength)
            print("Targeted city strength : ", targeted_city.strength)
            if total_strength >= targeted_city.strength:
                print("\nYou have acquired the city ", targeted_city.name, " !")
                targeted_city.is_bought = True
                self.cities_acquired.append(targeted_city)
                self.influence_points += targeted_city.influence
            else:
                print(
                    "\nYour army is not strong enough to acquire the city ",
                    targeted_city.name,
                    "...",
                )

            for unit_tmp in list_of_played_cards:
                unit_tmp.strength = unit_tmp.initial_strength
                self.graveyard.append(unit_tmp)

        elif len(list_of_cities_that_can_be_attacked) == 0:
            print("\nThere is no more neutral cities to attack...")

        elif len(self.hand) == 0:
            print("\nYour hand is empty! ")

        self.play_a_turn()

    def attack_an_enemy(self):
        list_of_enemies_that_can_be_attacked = [
            enemy_tmp for enemy_tmp in self.game.spawned_enemies
        ]

        bonus_in_strength_for_targeted_enemy = (
            2
            if "Seigneur Dragon Choyo"
            in [enemy_tmp.name for enemy_tmp in self.game.spawned_enemies]
            else 0
        )

        if len(list_of_enemies_that_can_be_attacked) > 0 and len(self.hand) > 0:
            list_of_possibilities = []
            print("\nYou can attack one of following enemies :")
            for index_enemy in range(len(list_of_enemies_that_can_be_attacked)):
                print(
                    index_enemy,
                    " = ",
                    list_of_enemies_that_can_be_attacked[index_enemy],
                )
                list_of_possibilities.append(str(index_enemy))

            print("\nWhich enemy do you want to attack ?")
            answer_tmp = str(input("\n> "))
            while answer_tmp not in list_of_possibilities:
                answer_tmp = str(input("\n> "))

            targeted_enemy = list_of_enemies_that_can_be_attacked[int(answer_tmp)]
            print("\nOk, you're now attacking following enemy :")
            print(targeted_enemy, "\n")

            list_of_played_cards = []
            must_continue = True

            while must_continue:
                print("Choose units from your hand to attack the enemy !")

                self.display_hand(must_keep_playing=False)
                answer_tmp = str(input("\n> "))
                while answer_tmp not in [
                    str(index_tmp) for index_tmp in range(len(self.hand))
                ]:
                    answer_tmp = str(input("\n> "))

                if isinstance(self.hand[int(answer_tmp)], Unit):
                    list_of_played_cards.append(self.hand.pop(int(answer_tmp)))
                    print(
                        "\nFollowing card has been added to the list of "
                        + "participating units !"
                    )
                    print(list_of_played_cards[-1])

                    if list_of_played_cards[-1].effect_type == "When played":
                        if isinstance(list_of_played_cards[-1], GuerrierRoc):
                            list_of_played_cards[-1].apply_effect(
                                self, list_of_played_cards[:-1]
                            )
                        elif isinstance(list_of_played_cards[-1], Ranime):
                            returned_card = list_of_played_cards[-1].apply_effect(self)
                            if returned_card is not None:
                                list_of_played_cards.append(returned_card)
                        else:
                            list_of_played_cards[-1].apply_effect(self)

                else:
                    print("Please add only Unit cards to the fight !")

                if len(self.hand) > 0:
                    print("\nDo you want to continue adding units to the fight ?")
                    print("Oui = 0\nNon = 1")
                    answer_tmp = str(input("\n> "))
                    while answer_tmp not in ["0", "1"]:
                        answer_tmp = str(input("\n> "))
                else:
                    answer_tmp = "1"

                if answer_tmp == "1":
                    must_continue = False

            for played_card_tmp in list_of_played_cards:
                if played_card_tmp.effect_type == "Resolution":
                    played_card_tmp.apply_effect(self)

            total_strength = sum(
                [unit_tmp.strength for unit_tmp in list_of_played_cards]
            ) + self.nb_battle_roar_activated * len(list_of_played_cards)

            if targeted_enemy.is_final_boss and self.strength_points > 0:
                total_strength += self.strength_points
                print(
                    "\nYour bonus in strength provided by your Rewards has been "
                    + "added to the total strength of your army."
                )
            print("\nTotal strength of your army : ", total_strength)
            print(
                "Targeted enemy strength : ",
                targeted_enemy.strength + bonus_in_strength_for_targeted_enemy,
            )
            print(
                "\nEnemy has an attridtion dice to roll : ",
                "Yes" if targeted_enemy.has_death_dice else "No",
            )

            if targeted_enemy.has_death_dice:
                nb_of_units_to_kill = roll_death_dice()
                if self.can_reroll_death_dice:
                    nb_of_units_to_kill_2 = roll_death_dice()
                    nb_of_units_to_kill = min(
                        nb_of_units_to_kill, nb_of_units_to_kill_2
                    )

                print(
                    "Result of the death dice roll : ",
                    nb_of_units_to_kill,
                    "\nBeginning of death dice tribute...",
                )

                # only destroy destroyable units
                nb_destroyable_units = 0
                for card_tmp in list_of_played_cards:
                    if card_tmp.is_destroyable:
                        nb_destroyable_units += 1

                # we cannot destroy more units than the number of destroyable units
                if nb_destroyable_units < nb_of_units_to_kill:
                    nb_of_units_to_kill = nb_destroyable_units

                index_enemy_to_kill = 0
                while index_enemy_to_kill < nb_of_units_to_kill:

                    if len(list_of_played_cards) > 0 and nb_destroyable_units > 0:
                        print("\nHere is your army :\n")
                        for index_card_tmp in range(len(list_of_played_cards)):
                            print(
                                list_of_played_cards[index_card_tmp],
                                " = ",
                                index_card_tmp,
                            )
                        print("\nPlease select a destroyable Unit ot Destroy : ")
                        answer_tmp = str(input("\n> "))
                        while answer_tmp not in [
                            str(index_tmp)
                            for index_tmp in range(len(list_of_played_cards))
                        ]:
                            answer_tmp = str(input("\n> "))

                        unit_to_destroy = list_of_played_cards[int(answer_tmp)]

                        if unit_to_destroy.is_destroyable:
                            unit_name = unit_to_destroy.name

                            if unit_to_destroy.is_a_neutral_unit:
                                neutral_unit_names = [
                                    unit_tmp.name in self.game.available_neutral_units
                                ]
                                self.game.nb_available_neutral_units[
                                    neutral_unit_names.index(unit_name)
                                ] += 1
                            else:
                                unit_names_in_shop = [
                                    unit_tmp.name for unit_tmp in self.shop.units
                                ]
                                self.shop.nb_remaining_units[
                                    unit_names_in_shop.index(unit_name)
                                ] += 1

                            list_of_played_cards.pop(int(answer_tmp))

                            index_enemy_to_kill += 1

                        else:
                            print("\nPlease select a destroyable Unit !")

                    else:
                        index_enemy_to_kill += nb_of_units_to_kill

                print("\nEnd of death dice tribute. Here is your final army :\n")
                for index_card_tmp in range(len(list_of_played_cards)):
                    print(list_of_played_cards[index_card_tmp], " = ", index_card_tmp)

                total_strength = sum(
                    [unit_tmp.strength for unit_tmp in list_of_played_cards]
                ) + self.nb_battle_roar_activated * len(list_of_played_cards)

                if targeted_enemy.is_final_boss and self.strength_points > 0:
                    total_strength += self.strength_points
                    print(
                        "\nYour bonus in strength provided by your Rewards has been "
                        + "added to the total strength of your army."
                    )
                print("\nTotal strength of your army : ", total_strength)
                print(
                    "Targeted enemy strength : ",
                    targeted_enemy.strength + bonus_in_strength_for_targeted_enemy,
                )

            if self.nb_battle_roar_activated > 0:
                self.nb_battle_roar_activated = 0

            if (
                total_strength
                >= targeted_enemy.strength + bonus_in_strength_for_targeted_enemy
            ):
                print("\nYou have slained the enemy ", targeted_enemy.name, " !")
                targeted_enemy.has_been_defeated = True
                targeted_enemy.life_points = 0

                if targeted_enemy.must_become_a_reward:
                    self.rewards.append(targeted_enemy)
                    self.influence_points += targeted_enemy.influence
                    self.gold_points += targeted_enemy.gold
                    self.strength_points += targeted_enemy.special_caracteristic
                    if targeted_enemy.name == "Seigneur Dragon Kalladra":
                        self.can_reroll_death_dice = True
                    if targeted_enemy.is_final_boss:
                        self.game.final_boss.life_points = 0

                    self.game.spawned_enemies.pop(
                        self.game.spawned_enemies.index(targeted_enemy)
                    )
                else:
                    self.game.defeated_enemies.append(
                        self.game.spawned_enemies.pop(
                            self.game.spawned_enemies.index(targeted_enemy)
                        )
                    )
            else:
                print(
                    "\nYour army is not strong enough to slain the enemy ",
                    targeted_enemy.name,
                    "...",
                )

            for unit_tmp in list_of_played_cards:
                unit_tmp.strength = unit_tmp.initial_strength
                self.graveyard.append(unit_tmp)

        elif len(list_of_enemies_that_can_be_attacked) == 0:
            print("\nThere is no more alive enemies to attack...")

        elif len(self.hand) > 0:
            print("\nYour hand is empty !")

        self.play_a_turn()

    def defend_against_an_enemy(self, attacking_enemy):
        bonus_in_strength_for_attacking_enemy = (
            2
            if "Seigneur Dragon Choyo"
            in [enemy_tmp.name for enemy_tmp in self.game.spawned_enemies]
            else 0
        )

        print("\nThe following enemy is attacking you :")
        print(attacking_enemy, "\nDefend yourself !\n")

        list_of_played_cards = []
        must_continue = True

        while must_continue:
            print("\nActivate your spell cards now !")
            print("Do you want to activate a spell card from your hand ?")
            print("Oui = 0\nNon = 1")
            answer_tmp = str(input("\n> "))
            while answer_tmp not in ["0", "1"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                self.play_spell_card(must_keep_playing=False)
            elif answer_tmp == "1":
                must_continue = False

        must_continue = True

        while must_continue:
            print("Choose units from your hand to defend against the enemy !")

            self.display_hand(must_keep_playing=False)
            answer_tmp = str(input("\n> "))
            while answer_tmp not in [
                str(index_tmp) for index_tmp in range(len(self.hand))
            ]:
                answer_tmp = str(input("\n> "))

            if isinstance(self.hand[int(answer_tmp)], Unit):
                list_of_played_cards.append(self.hand.pop(int(answer_tmp)))
                print(
                    "\nFollowing card has been added to the list of "
                    + "participating units !"
                )
                print(list_of_played_cards[-1])

                if list_of_played_cards[-1].effect_type == "When played":
                    if isinstance(list_of_played_cards[-1], GuerrierRoc):
                        list_of_played_cards[-1].apply_effect(
                            self, list_of_played_cards[:-1]
                        )
                    elif isinstance(list_of_played_cards[-1], Ranime):
                        returned_card = list_of_played_cards[-1].apply_effect(self)
                        if returned_card is not None:
                            list_of_played_cards.append(returned_card)
                    else:
                        list_of_played_cards[-1].apply_effect(self)

            else:
                print("Please add only Unit cards to the fight !")

            if len(self.hand) > 0:
                print("\nDo you want to continue adding units to the fight ?")
                print("Oui = 0\nNon = 1")
                answer_tmp = str(input("\n> "))
                while answer_tmp not in ["0", "1"]:
                    answer_tmp = str(input("\n> "))
            else:
                answer_tmp = "1"

            if answer_tmp == "1":
                must_continue = False

        for played_card_tmp in list_of_played_cards:
            if played_card_tmp.effect_type == "Resolution":
                played_card_tmp.apply_effect(self)

        total_strength = sum(
            [unit_tmp.strength for unit_tmp in list_of_played_cards]
        ) + self.nb_battle_roar_activated * len(list_of_played_cards)

        print("\nTotal strength of your army : ", total_strength)
        print(
            "Attacking enemy strength : ",
            attacking_enemy.strength + bonus_in_strength_for_attacking_enemy,
        )
        print(
            "\nEnemy has an attridtion dice to roll : ",
            "Yes" if attacking_enemy.has_death_dice else "No",
        )

        if attacking_enemy.has_death_dice:
            nb_of_units_to_kill = roll_death_dice()
            if self.can_reroll_death_dice:
                nb_of_units_to_kill_2 = roll_death_dice()
                nb_of_units_to_kill = min(nb_of_units_to_kill, nb_of_units_to_kill_2)

            print(
                "Result of the death dice roll : ",
                nb_of_units_to_kill,
                "\nBeginning of death dice tribute...",
            )

            index_enemy_to_kill = 0
            while index_enemy_to_kill < nb_of_units_to_kill:
                # only destroy destroyable units
                nb_destroyable_units = 0
                for card_tmp in list_of_played_cards:
                    if card_tmp.is_destroyable:
                        nb_destroyable_units += 1

                if len(list_of_played_cards) > 0 and nb_destroyable_units > 0:
                    print("\nHere is your army :\n")
                    for index_card_tmp in range(len(list_of_played_cards)):
                        print(
                            list_of_played_cards[index_card_tmp],
                            " = ",
                            index_card_tmp,
                        )
                    print("\nPlease select a destroyable Unit ot Destroy : ")
                    answer_tmp = str(input("\n> "))
                    while answer_tmp not in [
                        str(index_tmp) for index_tmp in range(len(list_of_played_cards))
                    ]:
                        answer_tmp = str(input("\n> "))

                    unit_to_destroy = list_of_played_cards[int(answer_tmp)]

                    if unit_to_destroy.is_destroyable:
                        unit_name = unit_to_destroy.name
                        unit_names_in_shop = [
                            unit_tmp.name for unit_tmp in self.shop.units
                        ]
                        self.shop.nb_remaining_units[
                            unit_names_in_shop.index(unit_name)
                        ] += 1

                        list_of_played_cards.pop(int(answer_tmp))

                        index_enemy_to_kill += 1

                    else:
                        print("\nPlease select a destroyable Unit !")

                else:
                    index_enemy_to_kill += nb_of_units_to_kill

            print("\nEnd of death dice tribute. Here is your final army :\n")
            for index_card_tmp in range(len(list_of_played_cards)):
                print(list_of_played_cards[index_card_tmp], " = ", index_card_tmp)

            total_strength = sum(
                [unit_tmp.strength for unit_tmp in list_of_played_cards]
            ) + self.nb_battle_roar_activated * len(list_of_played_cards)

            print("\nTotal strength of your army : ", total_strength)
            print(
                "Attacking enemy strength : ",
                attacking_enemy.strength + bonus_in_strength_for_attacking_enemy,
            )

        if self.nb_battle_roar_activated > 0:
            self.nb_battle_roar_activated = 0

        if (
            total_strength
            >= attacking_enemy.strength + bonus_in_strength_for_attacking_enemy
        ):
            print(
                "\nYou have completely defended yourself against the enemy ",
                attacking_enemy.name,
                " !",
            )
        else:
            diff_in_strength = (
                attacking_enemy.strength
                + bonus_in_strength_for_attacking_enemy
                - total_strength
            )
            print(
                "\nYour army is missing ",
                diff_in_strength,
                " strength points to completely defend yourself against the enemy...",
            )
            print("You kingdom is receiving ", diff_in_strength, " damage points !")
            self.life_points -= diff_in_strength

        for unit_tmp in list_of_played_cards:
            unit_tmp.strength = unit_tmp.initial_strength
            self.graveyard.append(unit_tmp)

        while len(self.hand) < self.max_nb_cards_in_hand:
            self.draw()

        print("\nYour new hand is :")
        self.display_hand(must_keep_playing=False)

    def smite_final_boss(self):
        self.game.final_boss.life_points = 0

        print(
            "Final boss remaining life points : ",
            self.game.final_boss.life_points,
        )

    def change_name(self):
        print("\n", self.name, " wants to change name !")
        print(
            "Note that you cannot rename yourself 99.\nTo cancel, enter 99 in next input."
        )
        print(
            "Also, note that the next input will be taken as is. "
            + "Although most inputs are safe, it is your responsibility "
            + "not to break the game with a bad input."
        )
        print("\nHow do you want to rename yourself ?\n")

        new_name = str(input("\n> "))

        self.name = new_name

        print("\nFrom now on, your new name will be", self.name, "!\n")

    def begin_turn(self):
        self.influence_points = (
            self.personal_cities_acquired
            + sum([city_tmp.influence for city_tmp in self.cities_acquired])
            + sum([reward_tmp.influence for reward_tmp in self.rewards])
        )
        self.gold_points = sum([reward_tmp.gold for reward_tmp in self.rewards])
        self.strength_points = sum(
            [reward_tmp.bonus_in_strength for reward_tmp in self.rewards]
        )

    def play_a_turn(self):
        if self.life_points > 0:
            print("\n\t\t\t\t\t*** It's " + self.name + "'s turn ! ***\n")
            print("You currently have ", self.life_points, " life points.")
            print("You currently have ", self.influence_points, " influence points.")
            self.display_hand(must_keep_playing=False)
            print("\nYou can make one of the following action : ")
            print("0 :\tDisplay hand")
            print("1 :\tGet info regarding a Card in the hand")
            print("2 :\tPlay a Spell card")
            print("3 :\tBuy a Unit from Shop")
            print("4 :\tBuy a Personal City with Gold")
            print("5 :\tBuy a Spell card or a Neutral Unit with Influence Points")
            print("6 :\tBuy a Gold card with Influence Points")
            print("7 :\tGet a summary of useful info")
            print("8 :\tAttack a Personal City")
            print("9 :\tAttack a Neutral City")
            print("10 :\tAttack an Enemy")
            print("No, you can't attack another player in this mode !")
            print("11 :\tDisplay graveyard")
            print("12 :\tEnd turn")
            print("20 :\tChange your Player's name")

            print(
                "\nIF YOU KNOW WHAT YOU ARE DOING AND IF YOU ARE NOT CHEATING, "
                + "you can perform following actions as well :"
            )
            print("13 :\tDraw one card")
            print("14 :\tDiscard one card")
            print("15 :\tAdd a card from the Graveyard to the hand")
            print("16 :\tAdd a Unit card from the Shop to the hand")
            print("17 :\tGains Influence points")
            print("18 :\tGains Gold points")
            print("19 :\tSmite Final Boss to End Game")

            print("\nWhat do you want to do ?")
            answer_tmp = str(input("\n> "))
            while not answer_tmp in [str(index_tmp) for index_tmp in range(19)]:
                answer_tmp = str(input("\n> "))
            print("\n\n")

            if answer_tmp == "0":
                self.display_hand()

            elif answer_tmp == "1":
                self.get_info_from_card_in_hand()

            elif answer_tmp == "2":
                self.play_spell_card()

            elif answer_tmp == "3":
                self.buy_a_unit()

            elif answer_tmp == "4":
                self.buy_a_personal_city()

            elif answer_tmp == "5":
                self.buy_spell_card_or_neutral_unit_with_influence()

            elif answer_tmp == "6":
                self.buy_a_gold_card_with_influence()

            elif answer_tmp == "7":
                self.get_summary()

            elif answer_tmp == "8":
                self.attack_a_personal_city()

            elif answer_tmp == "9":
                self.attack_a_neutral_city()

            elif answer_tmp == "10":
                self.attack_an_enemy()

            elif answer_tmp == "11":
                self.show_graveyard()

            # if answer_tmp == "12" then it will end the turn
            # so we don't do anything

            elif answer_tmp == "13":
                self.draw()
                self.play_a_turn()

            elif answer_tmp == "14":
                self.discard_a_card()
                self.play_a_turn()

            elif answer_tmp == "15":
                self.play_a_turn()

            elif answer_tmp == "16":
                self.play_a_turn()

            elif answer_tmp == "17":
                self.influence_points += 999
                self.play_a_turn()

            elif answer_tmp == "18":
                for _ in range(10):
                    self.hand.append(GoldCard("Gold Card 3", 3, 5))
                self.play_a_turn()

            elif answer_tmp == "19":
                self.smite_final_boss()
                self.play_a_turn()

            elif answer_tmp == "20":
                self.change_name()
                self.play_a_turn()

    def end_turn(self):
        # in case the player has activated one but
        # has not attacked this turn
        self.nb_battle_roar_activated = 0

        if self.game.final_boss.life_points > 0 and self.life_points > 0:
            # si le joueur a encore des points d'influence
            # faire choisir si oui ou non le joueur veut garder des cartes
            # si oui, faire choisir lesquelles juqu'à ce qu'il ne veuille plus
            # ou qu'il ait épuisé ses points d'influence
            index_cards_to_keep = []
            if self.influence_points > 0 and len(self.hand) > 0:
                print("\nYou still have ", self.influence_points, " influence points.")
                print(
                    "\nOui = 0\nNon = 1\n"
                    + "Do you want to keep one or more card(s) in your hand ?"
                )
                answer_tmp = str(input("\n> "))
                while not answer_tmp in ["0", "1"]:
                    answer_tmp = str(input("\n> "))
                print("\n\n")

                while answer_tmp == "0" and self.influence_points > 0:
                    self.display_hand(must_keep_playing=False)
                    print(
                        "\nYou still have ", self.influence_points, " influence points."
                    )
                    print("Which card do you want to keep ? ")
                    answer_tmp = str(input("\n> "))
                    while not answer_tmp in [
                        str(index_tmp) for index_tmp in range(len(self.hand))
                    ]:
                        answer_tmp = str(input("\n> "))

                    index_cards_to_keep.append(int(answer_tmp))
                    self.influence_points -= 1

                    if self.influence_points > 0:
                        print("\nOui = 0\nNon = 1\nDo you want to continue ?")
                        answer_tmp = str(input("\n> "))
                        while not answer_tmp in ["0", "1"]:
                            answer_tmp = str(input("\n> "))
                        print("\n\n")

                # reverse order of the range so that
                # there is no problem with the .pop function
                for index_card in range(len(self.hand))[::-1]:
                    if index_card not in index_cards_to_keep:
                        self.discard(index_card_to_discard=index_card)

            elif len(self.hand) > 0:
                while len(self.hand) > 0:
                    self.discard()

            while len(self.hand) < self.max_nb_cards_in_hand:
                self.draw()

            print("\nYour new hand is :")
            self.display_hand(must_keep_playing=False)


class City:
    def __init__(
        self,
        name_given,
        strength_given,
        bonus_in_def_strength_given,
        influence_points_given,
    ):
        self.name = name_given
        self.type = "City"
        self.strength = strength_given
        self.bonus_in_def_strength = bonus_in_def_strength_given
        self.influence = influence_points_given
        self.is_bought = False

    def __str__(self):
        return (
            self.name
            + "\t\tStrength : "
            + str(self.strength)
            + "\t\tInfluence : "
            + str(self.influence)
            + "\nBonus of defense provided when attacked : "
            + str(self.bonus_in_def_strength)
            + "\n"
        )


class Enemy:
    def __init__(
        self,
        name_given,
        type_given,
        rank_given,
        strength_given,
        effect_given,
        life_points_given=0,
        has_death_dice_given=True,
        must_become_a_reward_given=False,
        gold_given=0,
        influence_given=0,
        special_caracteristic_given=0,
        bonus_in_strength_given=0,
        is_final_boss_given=False,
    ):
        self.name = name_given
        self.type = type_given
        self.rank = rank_given
        self.strength = strength_given
        self.life_points = life_points_given
        self.effect = effect_given
        self.has_been_defeated = False
        self.has_death_dice = has_death_dice_given
        self.must_become_a_reward = must_become_a_reward_given

        self.gold = gold_given
        self.influence = influence_given
        self.special_caracteristic = special_caracteristic_given
        self.bonus_in_strength = bonus_in_strength_given

        self.is_final_boss = is_final_boss_given

    def __str__(self):
        return (
            self.type
            + " "
            + self.name
            + "\t\tStrength : "
            + str(self.strength)
            + "\t\tLife points : "
            + str(self.life_points)
            + "\nIs final boss : "
            + ("Yes" if self.is_final_boss else "No")
            + "\nMust roll death dice to fight it : "
            + ("Yes" if self.has_death_dice else "No")
            + "\nEffect : "
            + self.effect
            + "\n"
        )


class Shop:
    def __init__(self):
        self.units = []
        self.nb_remaining_units = []

    def add_purchasable_unit_to_shop(self, unit_to_add, nb_of_units_to_add):
        self.units.append(unit_to_add)
        self.nb_remaining_units.append(nb_of_units_to_add)


class Unit:
    def __init__(
        self,
        name_given,
        strength_given,
        cost_given,
        is_destroyable_given=True,
        is_a_central_unit_given=False,
    ):
        self.name = name_given
        self.initial_strength = strength_given
        self.strength = strength_given
        self.cost = cost_given
        self.effect_type = "None"
        self.is_destroyable = is_destroyable_given
        self.is_a_central_unit = is_a_central_unit_given

    def __str__(self):
        return (
            self.name
            + "\t\tStrength : "
            + str(self.strength)
            + "\t\tCost to purchase : "
            + str(self.cost)
            + "\n"
        )


class Ravageur(Unit):
    def __init__(self):
        Unit.__init__(self, "Ravageur", 1, 1)
        self.effect_type = "Resolution"

    def apply_effect(self, player):
        if len(player.hand) == 0:
            print("\nYour hand is empty. Ravageur's strength increases !")
            self.strength += 1


class Spiritiste(Unit):
    def __init__(self):
        Unit.__init__(self, "Spiritiste Orque", 3, 3)
        self.effect_type = "When played"

    def apply_effect(self, player):
        if len(player.hand) == 0:
            two_following_cards = []
            while len(two_following_cards) < 2:
                if len(player.deck) == 0:
                    player.convert_graveyard_into_deck()
                two_following_cards.append(player.deck.pop())

            print("\nThe next two cards in your deck are :")
            print(two_following_cards[0], "\t\t= 0")
            print(two_following_cards[1], "\t\t= 1")

            if isinstance(two_following_cards[0], Unit) and isinstance(
                two_following_cards[1], Unit
            ):
                print("\nPlease chose one card beween the two drawn cards !")
                answer_tmp = str(input("\n> "))
                while not answer_tmp in ["0", "1"]:
                    answer_tmp = str(input("\n> "))

                if answer_tmp == "0":
                    player.hand.append(two_following_cards[0])
                    player.graveyard.append(two_following_cards[1])
                elif answer_tmp == "1":
                    player.hand.append(two_following_cards[1])
                    player.graveyard.append(two_following_cards[0])

            elif isinstance(two_following_cards[0], Unit):
                print("\nYou draw the following Unit :")
                print(two_following_cards[0], "\n")
                player.hand.append(two_following_cards[0])
                player.graveyard.append(two_following_cards[1])

            elif isinstance(two_following_cards[1], Unit):
                print("\nYou draw the following Unit :")
                print(two_following_cards[1], "\n")
                player.hand.append(two_following_cards[1])
                player.graveyard.append(two_following_cards[0])

            else:
                print("\nThere was no Unit card in the two drawn cards...")
                print("The two drawn cards have been put into the Graveyard.\n")
                player.graveyard.append(two_following_cards[0])
                player.graveyard.append(two_following_cards[1])


class ChefDeGuerre(Unit):
    def __init__(self):
        Unit.__init__(self, "Chef de Guerre", 4, 5)
        self.effect_type = "When played"

    def apply_effect(self, player):
        player.buy_a_unit(
            add_unit_to_hand_instead=True,
            must_keep_playing=False,
            can_purchase_many_units=False,
        )


class Fantassin(Unit):
    def __init__(self):
        Unit.__init__(self, "Fantassin", 1, 1)
        self.effect_type = "When played"

    def apply_effect(self, player):
        if len(player.deck) == 0:
            player.convert_graveyard_into_deck()

        top_card = player.deck.pop()
        print("\nThe top card of your deck is : ")
        print(top_card)

        if top_card.name == "Fantassin":
            player.hand.append(top_card)
            print("The Fantassin has been added to your hand.\n")
        else:
            print("Discard it = 0")
            print("Put it back at the top of your deck = 1")
            print("What do you want to do with this card ?")
            answer_tmp = str(input("\n> "))
            while not answer_tmp in ["0", "1"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                player.graveyard.append(top_card)
                print("The card has been discarded.\n")
            elif answer_tmp == "1":
                player.deck.append(top_card)
                print("The card has been put back at the top of your deck.\n")


class Chevalier(Unit):
    def __init__(self):
        Unit.__init__(self, "Chevalier", 3, 3)
        self.effect_type = "When played"

    def apply_effect(self, player):
        print("\nThis card has following effect :")
        print(
            "You can display the card at the top of your deck."
            + "\nIf this card is a Unit with strength 1 or 2, or if it is not a Unit,"
            + " add it to your hand."
            + "\nOtherwise, discard it."
        )
        print("\nOui = 0\nNon = 1\nDo you want to activate this card's effect ?")
        answer_tmp = str(input("\n> "))
        while not answer_tmp in ["0", "1"]:
            answer_tmp = str(input("\n> "))

        if answer_tmp == "0":
            if len(player.deck) == 0:
                player.convert_graveyard_into_deck()

            top_card = player.deck.pop()
            print("\nThe top card of your deck is : ")
            print(top_card)

            if (
                isinstance(top_card, Unit)
                and top_card.strength < 3
                or not isinstance(top_card, Unit)
            ):
                player.hand.append(top_card)
                print("The card has been added to your hand.\n")
            else:
                player.graveyard.append(top_card)
                print("The card has a strength greater or equal to 3.")
                print("It has been put into your graveyard.\n")


class MageNovice(Unit):
    def __init__(self):
        Unit.__init__(self, "Mage Novice", 2, 3)
        self.effect_type = "When played"

    def apply_effect(self, player):
        if len(player.hand) > 0:
            print("\nThis card has following effect :")
            print("You can discard one card from your hand to draw one card.")
            print("\nOui = 0\nNon = 1\nDo you want to activate this card's effect ?")
            answer_tmp = str(input("\n> "))
            while not answer_tmp in ["0", "1"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                player.discard_a_card()
                player.draw()


class MachineDeSiege(Unit):
    def __init__(self):
        Unit.__init__(self, "Machine de Siège", 4, 5)
        self.effect_type = "Resolution"

    def apply_effect(self, player):
        if len(player.hand) > 0:
            print("\nThis card has following effect :")
            print(
                "You can discard one card from your hand to increase this card's strength by 2."
            )
            print("\nOui = 0\nNon = 1\nDo you want to activate this card's effect ?")
            answer_tmp = str(input("\n> "))
            while not answer_tmp in ["0", "1"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                player.discard_a_card()
                self.strength += 2


class GuerrierRoc(Unit):
    def __init__(self):
        Unit.__init__(self, "Guerrier Roc", 5, 6)
        self.effect_type = "When played"

    def apply_effect(self, player, list_of_played_units):
        if len(list_of_played_units) > 0:
            print("\nThis card has following effect :")
            print(
                "You can retrieve an already played unit into your hand to "
                + "reactivate its 'When played' effect."
            )
            print("\nOui = 0\nNon = 1\nDo you want to activate this card's effect ?")
            answer_tmp = str(input("\n> "))
            while not answer_tmp in ["0", "1"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                for index_card in range(len(list_of_played_units)):
                    print(list_of_played_units[index_card].name, " = ", index_card)

                print("\nWhich card do you want to retrieve in your hand ?")
                answer_tmp = str(input("\n> "))
                while answer_tmp not in [
                    str(index_tmp) for index_tmp in range(len(list_of_played_units))
                ]:
                    answer_tmp = str(input("\n> "))

                player.hand.append(list_of_played_units.pop(int(answer_tmp)))


class Ranime(Unit):
    def __init__(self):
        Unit.__init__(self, "Ranimé", 1, 1)
        self.effect_type = "When played"

    def apply_effect(self, player):
        list_of_card_names_in_graveyard = [
            card_tmp.name for card_tmp in player.graveyard
        ]

        if "Ranimé" in list_of_card_names_in_graveyard:
            index_ranime = list_of_card_names_in_graveyard.index("Ranimé")
            print("A Ranimé has been added from your Graveyard to the fight !")

            return player.graveyard.pop(index_ranime)


class Necromancien(Unit):
    def __init__(self):
        Unit.__init__(self, "Nécromancien", 3, 3)
        self.effect_type = "When played"

    def apply_effect(self, player):
        two_following_cards = []
        while len(two_following_cards) < 2:
            if len(player.deck) == 0:
                player.convert_graveyard_into_deck()
            two_following_cards.append(player.deck.pop())

        print("\nThe next two cards in your deck are :")
        print(two_following_cards[0], "\t\t= 0")
        print(two_following_cards[1], "\t\t= 1")

        if (
            two_following_cards[0].name
            in [
                "Ranimé",
                "Archer Squelette",
            ]
            and two_following_cards[1].name in ["Ranimé", "Archer Squelette"]
        ):
            print("\nPlease choose one card beween the two drawn cards !")
            answer_tmp = str(input("\n> "))
            while not answer_tmp in ["0", "1"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                player.hand.append(two_following_cards[0])
                player.graveyard.append(two_following_cards[1])
            elif answer_tmp == "1":
                player.hand.append(two_following_cards[1])
                player.graveyard.append(two_following_cards[0])

        elif two_following_cards[0].name in ["Ranimé", "Archer Squelette"]:
            print("\nYou draw the following Unit :")
            print(two_following_cards[0], "\n")
            player.hand.append(two_following_cards[0])
            player.graveyard.append(two_following_cards[1])

        elif two_following_cards[1].name in ["Ranimé", "Archer Squelette"]:
            print("\nYou draw the following Unit :")
            print(two_following_cards[1], "\n")
            player.hand.append(two_following_cards[1])
            player.graveyard.append(two_following_cards[0])

        else:
            print(
                "\nThere was neither Ranimé nor Archer Squelette cards in the two drawn cards..."
            )
            print("The two drawn cards have been put into the Graveyard.\n")
            player.graveyard.append(two_following_cards[0])
            player.graveyard.append(two_following_cards[1])


class Vampire(Unit):
    def __init__(self):
        Unit.__init__(self, "Vampire", 3, 3)
        self.effect_type = "When played"

    def apply_effect(self, player):
        four_following_cards = []
        while len(four_following_cards) < 4:
            if len(player.deck) == 0:
                player.convert_graveyard_into_deck()
            four_following_cards.append(player.deck.pop())

        print("\nThe next four cards in your deck are :")
        for card_tmp in four_following_cards:
            print(card_tmp)

        # ajouter au cimetière
        # ajouter immédiatement au deck
        # ajouter au deck mais plus tard
        while len(four_following_cards) > 0:
            print("\nDiscard to graveyard = 0")
            print("Add card to top of deck now = 1")
            print("Add card to top of deck later = 2")
            print(
                "What do you want to do with the card ",
                four_following_cards[0].name,
                "?",
            )
            answer_tmp = str(input("\n> "))
            while not answer_tmp in ["0", "1", "2"]:
                answer_tmp = str(input("\n> "))

            if answer_tmp == "0":
                player.graveyard.append(four_following_cards.pop(0))
            elif answer_tmp == "1":
                player.deck.append(four_following_cards.pop(0))
            elif answer_tmp == "2":
                four_following_cards.append(four_following_cards.pop(0))


class ChevalierNoir(Unit):
    def __init__(self):
        Unit.__init__(self, "Chevalier Noir", 3, 5)
        self.effect_type = "Resolution"

    def apply_effect(self, player):
        self.strength -= 1
        player.nb_battle_roar_activated += 1


class Wyrm(Unit):
    def __init__(self):
        Unit.__init__(self, "Wyrm", 4, 6)
        self.effect_type = "When played"

    def apply_effect(self, player):
        player.retrieve_a_card_from_graveyard()


class SpellCard:
    def __init__(self, name_given, influence_cost_given, effect_given):
        self.name = name_given
        self.type = "Spell"
        self.influence = influence_cost_given
        self.effect = effect_given

    def __str__(self):
        return "Spell " + self.name + " : \n" + self.effect + "\n"


def roll_death_dice():
    return [0, 0, 0, 1, 1, 2][random.randint(0, 5)]


def remove_duplicates_from(list_to_remove_duplicates_from):
    to_return = []
    for element_tmp in list_to_remove_duplicates_from:
        if element_tmp not in to_return:
            to_return.append(element_tmp)

    return to_return


class Game:
    def __init__(self, list_of_player_names):
        if len(list_of_player_names) == 1:
            self.nb_gold_1_cards = 9
            self.nb_gold_2_cards = 8
            self.nb_gold_3_cards = 4
            self.nb_neutral_cities = 2
            self.nb_neutral_cards_per_card_type = 2
        elif len(list_of_player_names) == 2:
            self.nb_gold_1_cards = 14
            self.nb_gold_2_cards = 10
            self.nb_gold_3_cards = 6
            self.nb_neutral_cities = 3
            self.nb_neutral_cards_per_card_type = 3
        elif len(list_of_player_names) == 3:
            self.nb_gold_1_cards = 19
            self.nb_gold_2_cards = 12
            self.nb_gold_3_cards = 8
            self.nb_neutral_cities = 4
            self.nb_neutral_cards_per_card_type = 4
        elif len(list_of_player_names) == 4:
            self.nb_gold_1_cards = 24
            self.nb_gold_2_cards = 14
            self.nb_gold_3_cards = 10
            self.nb_neutral_cities = 5
            self.nb_neutral_cards_per_card_type = 5

        self.all_neutral_cities = [
            City("Forge", 9, 2, 3),
            City("Greyhaven", 6, 2, 2),
            City("Tamalir", 8, 1, 3),
            City("Nerekhall", 5, 1, 2),
            City("Vynelvale", 6, 2, 2),
            City("Riverwatch", 7, 0, 3),
            City("Frostgate", 5, 1, 2),
            City("Dawnsmoor", 4, 0, 2),
        ]

        self.available_neutral_cities = remove_duplicates_from(
            [
                self.all_neutral_cities[
                    random.randint(0, len(self.all_neutral_cities) - 1)
                ]
                for _ in range(self.nb_neutral_cities)
            ]
        )

        while len(self.available_neutral_cities) < self.nb_neutral_cities:
            self.available_neutral_cities = remove_duplicates_from(
                [
                    self.all_neutral_cities[
                        random.randint(0, len(self.all_neutral_cities) - 1)
                    ]
                    for _ in range(self.nb_neutral_cities)
                ]
            )

        self.available_spell_cards = [
            SpellCard(
                "Forced March", 4, "Destroy one card in your hand to draw two cards."
            ),
            SpellCard(
                "Battle Roar",
                2,
                "Add 1 to your total battle strength per participating unit.",
            ),
        ]
        self.nb_available_spell_cards = [
            self.nb_neutral_cards_per_card_type for _ in self.available_spell_cards
        ]
        self.available_neutral_units = [
            Unit(
                "Démon", 5, 6, is_destroyable_given=False, is_a_central_unit_given=True
            )
        ]
        self.nb_available_neutral_units = [
            self.nb_neutral_cards_per_card_type for _ in self.available_neutral_units
        ]

        # name, type, rank_given,
        # strength_given, effect_given,
        # life_points_given=0,
        # has_death_dice_given=True,
        # gold_given=0, influence_given=0,
        # special_caracteristic_given=0,

        self.list_of_enemies = [
            Enemy(
                "Seigneur Dragon Margath",
                "Enemy",
                2,
                12,
                "The player that defeats this Enemy takes it as a Reward with "
                + "following effect : gains +3 Strength when attacking the Ultimate Goal",
                life_points_given=12,
                bonus_in_strength_given=3,
                must_become_a_reward_given=True,
            ),
            Enemy(
                "Seigneur Dragon Ghox",
                "Enemy",
                2,
                8,
                "At the beginning of each Event Phase : inflicts 2 damage points "
                + "to each player's kingdom.",
                life_points_given=8,
                special_caracteristic_given=2,
            ),
            Enemy(
                "Seigneur Dragon Khorgard",
                "Instantaneous",
                2,
                12,
                "This card attacks the kingdom of the player that has the highest life points."
                + "\nIn case of equality, this card attacks the kingdom of all "
                + "players with highest life points.",
                has_death_dice_given=False,
            ),
            Enemy(
                "Seigneur Dragon Phrylenex",
                "Instantaneous",
                2,
                0,
                "Inflicts 3 points of damage to the kingdom of all players.",
                special_caracteristic_given=3,
                has_death_dice_given=False,
            ),
            Enemy(
                "Résurgence des Seigneurs Dragon",
                "Enemy",
                0,
                18,
                "This carte is considered as the Ultimate Goal. "
                + "\nThe player thats defeats this card wins the game.",
                life_points_given=18,
                is_final_boss_given=True,
            ),
            Enemy(
                "Seigneur Dragon Choyo",
                "Enemy",
                10,
                2,
                "All other enemies' strength increase by 2 while this card is on the field.",
                life_points_given=10,
                special_caracteristic_given=2,
            ),
            Enemy(
                "Seigneur Dragon Kalladra",
                "Enemy",
                2,
                10,
                "The player that defeats this Enemy takes it as a Reward with "
                + "following effect : when attacking the Ultimate Goal, you can "
                + "reroll the Death Dice once.",
                life_points_given=10,
                must_become_a_reward_given=True,
            ),
            Enemy(
                "Seigneur Dragon Baraxis",
                "Instantaneous",
                2,
                0,
                "Each player's kingdom takes damage equal to twice the number of Enemies "
                + "that are still alive (Instantaneous are not included)."
                + "\nEach player can Destroy cards from his hand that have a value "
                + "of 2 or more to reduce received damage by 2 per card.",
                has_death_dice_given=False,
            ),
            Enemy(
                "Seigneur Dragon Tzeitz",
                "Instantaneous",
                2,
                9,
                "This card attacks kingdom of all players that have at least one Reward, "
                + "excepted the 'Rallier des Soutiens' Reward.",
                has_death_dice_given=False,
            ),
            Enemy(
                "Rallier des Soutiens",
                "Reward",
                1,
                0,
                "The first player gives this card to another player that takes it as a Reward."
                + "\nThis player gains 1 Influence point.",
                has_death_dice_given=False,
                influence_given=1,
                must_become_a_reward_given=True,
            ),
            Enemy(
                "Seigneur Dragon Mithrilim",
                "Enemy",
                1,
                6,
                "The player that defeats this card takes it as a Reward."
                + "\nThis player gains 1 Gold.",
                life_points_given=6,
                gold_given=1,
                must_become_a_reward_given=True,
            ),
            Enemy(
                "Seigneur Dragon Endormi",
                "Enemy",
                1,
                5,
                "The player that defeats this card takes it as a Reward."
                + "\nThis player gains 1 Influence Point.",
                life_points_given=5,
                influence_given=1,
                must_become_a_reward_given=True,
            ),
        ]

        self.list_of_enemies_of_rank_1 = []
        self.list_of_enemies_of_rank_2 = []
        self.list_of_enemies_of_rank_3 = []
        for enemy_tmp in self.list_of_enemies:
            if enemy_tmp.rank == 1:
                self.list_of_enemies_of_rank_1.append(enemy_tmp)
            elif enemy_tmp.rank == 2:
                self.list_of_enemies_of_rank_2.append(enemy_tmp)
            elif enemy_tmp.rank == 3:
                self.list_of_enemies_of_rank_3.append(enemy_tmp)
            elif enemy_tmp.rank == 0:
                self.final_boss = enemy_tmp

        self.spawned_enemies = [self.final_boss]
        self.defeated_enemies = []

        if "Bambouman" in list_of_player_names:
            # name_given, strength_given, cost_given
            unit_1 = Unit("Petit Esprit du Bambou", 1, 1)
            unit_2 = Unit("Esprit du Bambou", 2, 2)
            unit_3 = Unit("Grand Esprit du Bambou", 3, 3)
            unit_4 = Unit("Dryade", 4, 4)
            unit_5 = Unit("Reine Dryade", 5, 5)

            shop = Shop()
            shop.add_purchasable_unit_to_shop(unit_1, 5)
            shop.add_purchasable_unit_to_shop(unit_2, 5)
            shop.add_purchasable_unit_to_shop(unit_3, 5)
            shop.add_purchasable_unit_to_shop(unit_4, 4)
            shop.add_purchasable_unit_to_shop(unit_5, 3)

            # name_given, nation_name_given, deck_given, shop_given, game_given
            player_0 = Player(
                "Bambouman",
                "Spirits of the Bambou Forest",
                [Unit("Petit Esprit du Bambou", 1, 1) for _ in range(3)]
                + [GoldCard("Gold Card 1", 1, 1) for _ in range(5)],
                shop,
                self,
            )

        else:
            player_0 = None

        if "Orcs Duellist" in list_of_player_names:
            # name_given, strength_given, cost_given
            unit_1 = Ravageur()
            unit_2 = Unit("Maître des Bêtes", 2, 2)
            unit_3 = Spiritiste()
            unit_4 = Unit("Chevaucheur de Lézard", 3, 3)
            unit_5 = ChefDeGuerre()
            unit_6 = Unit("Troll Géant", 6, 6)

            shop = Shop()
            shop.add_purchasable_unit_to_shop(unit_1, 5)
            shop.add_purchasable_unit_to_shop(unit_2, 5)
            shop.add_purchasable_unit_to_shop(unit_3, 5)
            shop.add_purchasable_unit_to_shop(unit_4, 5)
            shop.add_purchasable_unit_to_shop(unit_5, 4)
            shop.add_purchasable_unit_to_shop(unit_6, 3)

            # name_given, nation_name_given, deck_given, shop_given, game_given
            player_1 = Player(
                "Orcs Duellist",
                "Orcs of the Broken Lands",
                [Ravageur() for _ in range(3)]
                + [GoldCard("Gold Card 1", 1, 1) for _ in range(5)],
                shop,
                self,
            )

        else:
            player_1 = None

        if "Humen Duellist" in list_of_player_names:
            # name_given, strength_given, cost_given
            unit_1 = Fantassin()
            unit_2 = Unit("Archer", 2, 2)
            unit_3 = Chevalier()
            unit_4 = MageNovice()
            unit_5 = MachineDeSiege()
            unit_6 = GuerrierRoc()

            shop = Shop()
            shop.add_purchasable_unit_to_shop(unit_1, 5)
            shop.add_purchasable_unit_to_shop(unit_2, 5)
            shop.add_purchasable_unit_to_shop(unit_3, 5)
            shop.add_purchasable_unit_to_shop(unit_4, 5)
            shop.add_purchasable_unit_to_shop(unit_5, 4)
            shop.add_purchasable_unit_to_shop(unit_6, 3)

            # name_given, nation_name_given, deck_given, shop_given, game_given
            player_2 = Player(
                "Humen Duellist",
                "Daqan Lords",
                [Fantassin() for _ in range(3)]
                + [GoldCard("Gold Card 1", 1, 1) for _ in range(5)],
                shop,
                self,
            )

        else:
            player_2 = None

        if "Undeads Duelllist" in list_of_player_names:
            # name_given, strength_given, cost_given
            unit_1 = Ranime()
            unit_2 = Unit("Archer Squelette", 2, 2)
            unit_3 = Necromancien()
            unit_4 = Vampire()
            unit_5 = ChevalierNoir()
            unit_6 = Wyrm()

            shop = Shop()
            shop.add_purchasable_unit_to_shop(unit_1, 5)
            shop.add_purchasable_unit_to_shop(unit_2, 5)
            shop.add_purchasable_unit_to_shop(unit_3, 5)
            shop.add_purchasable_unit_to_shop(unit_4, 5)
            shop.add_purchasable_unit_to_shop(unit_5, 4)
            shop.add_purchasable_unit_to_shop(unit_6, 3)

            # name_given, nation_name_given, deck_given, shop_given, game_given
            player_3 = Player(
                "Undeads Duellist",
                "Waiqar the Undying",
                [Ranime() for _ in range(3)]
                + [GoldCard("Gold Card 1", 1, 1) for _ in range(5)],
                shop,
                self,
            )

        else:
            player_3 = None

        self.players = [player_0, player_1, player_2, player_3]
        while None in self.players:
            self.players.pop(self.players.index(None))

    def display_all_hands(self):
        for player_tmp in self.players:
            if len(player_tmp.hand) > 0:
                print("\nHere is ", player_tmp.name, "'s hand :")
                for index_card in range(len(self.hand)):
                    print(player_tmp.hand[index_card].name, " = ", index_card)
            else:
                print("\n", player_tmp.name, "'s hand is empty.")

            print("\n")

    def choose_a_player(
        self, must_use_default_string=True, list_of_strings_to_use_instead=None
    ):
        # lists_of_strings_to_use_instead must be a list of two strings
        # first one is a global message to print beforehand
        # second one is the messgae to print right before the str input
        print(
            "\nPlease choose one player among all game's players : "
            if must_use_default_string
            else string_to_use_instead[0]
        )
        list_of_possibilities = []
        for index_player_tmp in self.players:
            print(
                self.players[index_player_tmp].name,
                " = ",
                index_player_tmp,
            )
            list_of_possibilities.append(str(index_player_tmp))

        print(
            "\nWhich player do you want to choose ?"
            if must_use_default_string
            else list_of_strings_to_use_instead[1]
        )
        answer_tmp = str(input("\n> "))
        while answer_tmp not in list_of_possibilities:
            answer_tmp = str(input("\n> "))

        return int(answer_tmp)

    def play_game(self):
        is_game_finished = False
        while not is_game_finished:
            for player_tmp in self.players:
                if not is_game_finished:
                    player_tmp.begin_turn()
                    player_tmp.play_a_turn()
                    player_tmp.end_turn()

                    is_game_finished = self.final_boss.life_points <= 0 or True not in [
                        player_tmp.life_points > 0 for player_tmp in self.players
                    ]
                    print(
                        "Final boss remaining life points in game : ",
                        self.final_boss.life_points,
                    )
                    print(
                        "Player ",
                        player_tmp.name,
                        " remaining life points : ",
                        player_tmp.life_points,
                    )

                    x = str(input("\n> "))

            if not is_game_finished:
                list_to_use_for_enemy_spawn = self.list_of_enemies_of_rank_1
                if len(self.list_of_enemies_of_rank_1) == 0:
                    list_to_use_for_enemy_spawn = self.list_of_enemies_of_rank_2
                if len(self.list_of_enemies_of_rank_2) == 0:
                    # for cataclysm only
                    # list_to_use_for_enemy_spawn = self.list_of_enemies_of_rank_3
                    self.list_of_enemies_of_rank_2 = []
                    for defeated_enemy_tmp in self.defeated_enemies:
                        if defeated_enemy_tmp.rank == 2:
                            self.list_of_enemies_of_rank_2.append(defeated_enemy_tmp)

                    list_to_use_for_enemy_spawn = self.list_of_enemies_of_rank_2

                if "Seigneur Dragon Ghox" in [
                    enemy_tmp.name for enemy_tmp in self.spawned_enemies
                ]:
                    for player_tmp in self.players:
                        player_tmp.life_points -= 2

                index_monster_to_spawn = random.randint(
                    0, len(list_to_use_for_enemy_spawn) - 1
                )
                spawned_enemy_tmp = list_to_use_for_enemy_spawn.pop(
                    index_monster_to_spawn
                )
                print("\nA new enemy appeared !")
                print(spawned_enemy_tmp, "\n")

                if spawned_enemy_tmp.name == "Seigneur Dragon Phrylenex":
                    for player_tmp in self.players:
                        player_tmp.life_points -= 3

                    self.defeated_enemies.append(spawned_enemy_tmp)

                elif spawned_enemy_tmp.name == "Rallier des Soutiens":
                    print(
                        "\nChosen player will receive the Rallier des Soutiens Reward card."
                    )
                    print(
                        "This card gives one additional Gold point per turn to this player.\n"
                    )

                    index_chosen_player = self.choose_a_player()
                    self.players[index_chosen_player].rewards.append(spawned_enemy_tmp)
                    print("\n")

                elif spawned_enemy_tmp.name == "Seigneur Dragon Baraxis":
                    for player_tmp in self.players:
                        player_tmp.life_points -= 2 * len(self.spawned_enemies)

                    self.defeated_enemies.append(spawned_enemy_tmp)

                elif spawned_enemy_tmp.name == "Seigneur Dragon Tzeitz":
                    for player_tmp in self.players:
                        nb_rewards = len(player_tmp.rewards)
                        if "Rallier des Soutiens" in [
                            reward_tmp.name for reward_tmp in player_tmp.rewards
                        ]:
                            nb_rewards -= 1

                        if nb_rewards > 0:
                            player_tmp.defend_against_an_enemy(
                                Enemy(
                                    "Seigneur Dragon Tzeitz",
                                    "Instantaneous",
                                    2,
                                    9,
                                    "This card attacks kingdom of all players that have at least one Reward, "
                                    + "excepted the 'Rallier des Soutiens' Reward.",
                                    has_death_dice_given=False,
                                )
                            )

                    self.defeated_enemies.append(spawned_enemy_tmp)

                elif spawned_enemy_tmp.name == "Seigneur Dragon Khorgard":
                    max_life_points = max(
                        [player_tmp.life_points for player_tmp in self.players]
                    )
                    for player_tmp in self.players:
                        if player_tmp.life_points == max_life_points:
                            player_tmp.defend_against_an_enemy(
                                Enemy(
                                    "Seigneur Dragon Khorgard",
                                    "Instantaneous",
                                    2,
                                    12,
                                    "This card attacks the kingdom of the player that has the highest life points."
                                    + "\nIn case of equality, this card attacks the kingdom of all "
                                    + "players with highest life points.",
                                    has_death_dice_given=False,
                                )
                            )

                else:
                    self.spawned_enemies.append(spawned_enemy_tmp)

                print("\nAll remaining enemies to slain : \n")
                for enemy_tmp in self.spawned_enemies:
                    print(enemy_tmp)
                print("\n")

                x = str(input("\n> "))

        if self.final_boss.life_points > 0 and True not in [
            player_tmp.life_points > 0 for player_tmp in self.players
        ]:
            print("\nYou've lost...\n\n")
        else:
            print("\nCongratulations ! You won !!\n\n")


def forced_march(player):
    list_of_played_cards = []
    must_continue = True

    print("\nChoose a card to Destroy from your hand to activate the Forced March !")
    print("It will make you draw two cards, but the chosen card will be Destroyed.")
    print("\nWhich card do you want to destroy ?")

    player.display_hand(must_keep_playing=False)
    answer_tmp = str(input("\n> "))
    while answer_tmp not in [str(index_tmp) for index_tmp in range(len(player.hand))]:
        answer_tmp = str(input("\n> "))

    removed_card = player.hand.pop(int(answer_tmp))
    print("\nFollowing card has been destroyed !")
    print(removed_card)

    if isinstance(removed_card, GoldCard):
        if removed_card.gold == 1:
            player.game.nb_gold_1_cards += 1
        elif removed_card.gold == 2:
            player.game.nb_gold_2_cards += 1
        elif removed_card.gold == 3:
            player.game.nb_gold_3_cards += 1

    elif isinstance(removed_card, SpellCard):
        spell_card_names = [
            spell_card_tmp.name for spell_card_tmp in player.game.available_spell_cards
        ]
        player.game.nb_available_spell_cards[
            spell_card_names.index(removed_card.name)
        ] += 1

    elif isinstance(removed_card, Unit):
        neutral_units_names = [
            neutral_unit_tmp.name
            for neutral_unit_tmp in player.game.available_neutral_units
        ]

        if removed_card.name in neutral_units_names:
            player.game.nb_available_neutral_units[
                neutral_units_names.index(removed_card.name)
            ] += 1

        else:
            player_unit_names = [unit_tmp.name for unit_tmp in player.shop.units]
            player.shop.nb_remaining_units[
                player_unit_names.index(removed_card.name)
            ] += 1

    player.draw()
    player.draw()


def play():
    game = Game(["Orcs Duellist", "Humen Duellist"])

    game.play_game()


if __name__ == "__main__":
    play()
