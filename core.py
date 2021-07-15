import random
from datetime import datetime
from utils.config import Config
from utils.models import Attempt, AllAttempts, AllExpResults


class Core:

    def start(self):
        self.__start_game()

    def __start_game(self):
        self.__prepare_variables()
        self.date_start = datetime.now().strftime("%d.%m.%Y %H:%M")
        for game in range(1, self.config.attempts+1):
            self.attempt = game
            self.__prepare_doors()
            self.__make_first_choice()


            if self.config.change == 0:
                self.switch = random.randint(0, 1)
            elif self.config.change == 1:
                self.switch = 1
            elif self.config.change == 2:
                self.switch = 0
            else:
                self.switch = 1

            self.__open_doors()
            if self.switch == 1:
                self.choice = self.second_door
            else:
                pass

            if self.choice == self.win_door:
                self.win = 1
            else:
                self.win = 0

            self.__move_attempt_to_db()
        AllAttempts().move_conclusion_to_db(self.date_start)
        print(AllExpResults().make_conclusion())

    def __prepare_doors(self):
        self.doors: list = []
        self.win_door = random.randint(0, self.config.doors - 1)

        for door in range(self.config.doors):
            if door == self.win_door:
                self.doors.append(1)
            else:
                self.doors.append(0)

    def __make_first_choice(self):
        self.choice = random.randint(0, self.config.doors - 1)

    def __open_doors(self):
        if self.choice == self.win_door:
            self.second_door = random.choice(
                [i for i in range(self.config.doors) if i not in [self.win_door, self.choice]]
            )
        else:
            self.second_door = self.win_door

    def __prepare_variables(self):
        start = input(
            "Please, enter 'Y' to start with default config,"
            "or enter 'N' to setup yours"
        )

        if start.lower() == 'y':
            self.__setup_config()

    def __setup_config(self):
        self.config = Config().default

    def __move_attempt_to_db(self):
        attempt = Attempt.init_from_dict(
            {
                'attempt': self.attempt,
                'changed': self.switch,
                'win': self.win,
                'number_of_doors': self.config.doors
            }
        )
        attempt.move_to_db()