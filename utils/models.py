from .db import Database
from datetime import datetime


class AllAttempts:
    def __init__(self):
        with Database() as db:
            success, results = db.select(
                """
                SELECT * 
                FROM experiment;
                """
            )
            self.all: list = []
            if success:
                for res in results:
                    result_model = Attempt.init_from_dict(
                        {
                            'attempt': res[0],
                            'changed': res[1],
                            'win': res[2],
                            'number_of_doors': res[3]
                        }
                    )
                    self.all.append(result_model)

    def move_conclusion_to_db(self, date_start):
        attempts = 0
        times_changed = 0
        wins = 0
        wins_when_changed = 0
        wins_when_not_changed = 0
        loses = 0
        loses_when_changed = 0
        loses_when_not_changed = 0

        for mes in self.all:
            attempts += 1
            
            if mes.changed == 1:
                times_changed += 1
            
            if mes.win == 1:
                wins += 1

                if mes.changed:
                    wins_when_changed += 1
                else:
                    wins_when_not_changed += 1

            else:
                loses += 1

                if mes.changed:
                    loses_when_changed += 1
                else:
                    loses_when_not_changed +=1
        date_end = datetime.now().strftime("%d.%m.%Y %H:%M")
        with Database() as db:
            db.insert(
            f"""
                INSERT INTO result
                VALUES ({attempts}, {times_changed}, 
                        {wins}, {mes.number_of_doors}, 
                        {loses}, "{date_start}", 
                        "{date_end}", {wins_when_changed}, 
                        {loses_when_changed}, {wins_when_not_changed}, 
                        {loses_when_not_changed});
            """
            )
            db.delete("""
                DELETE FROM experiment;
            """)

class Attempt:
    
    @classmethod
    def init_from_dict(cls, 
                       data: dict):
        inst = cls()
        inst.__dict__ = data
        return inst

    def move_to_db(self):
        query = f"""
            INSERT INTO experiment
            VALUES({self.attempt}, {self.changed}, 
                   {self.win}, {self.number_of_doors})
        """
        with Database() as db:
            print(query)
            db.insert(query)


class AllExpResults:
    def __init__(self):
        self.all: list = []
        query = """
            SELECT *
            FROM result;
        """
        with Database() as db:
            success, results = db.select(query)
        if success:
            for res in results:
                result_model = ExpResult.init_from_dict(
                    {
                        'attempts': res[0],
                        'times_changed': res[1],
                        'wins': res[2],
                        'loses': res[4],
                        'number_of_doors': res[3],
                        'date_start': res[5],
                        'date_end': res[6],
                        'wins_when_changed': res[7],
                        'wins_when_not_changed': res[9],
                        'loses_when_changed': res[8],
                        'loses_when_not_changed': res[10]
                    }
                )
                self.all.append(result_model)

    def make_conclusion(self):
        self.conclusion: str = ''
        if self.all:
            counter = 1
            for exp_res in self.all:
                self.conclusion += exp_res.make_conclusion(counter) + '\n\n'
                counter += 1
        return self.conclusion


class ExpResult:
    
    @classmethod
    def init_from_dict(cls,
                       data: dict):
        inst = cls()
        inst.__dict__ = data
        inst.__count_percents()
        return inst

    def __count_percents(self):
        self.__count_win_percents()
        self.__count_lose_percents()

    def __count_win_percents(self):
        if self.times_changed > 0:
            self.win_percent_when_changed = round(
                self.wins_when_changed / self.times_changed * 100, 
                3
            )
        
        else:
            self.win_percent_when_changed = 0
        
        self.win_percent_when_not_changed = round(
            self.wins_when_not_changed / (self.attempts - self.times_changed) * 100, 
            3
        )

    def __count_lose_percents(self):
        if self.win_percent_when_changed > 0:
            self.lose_percent_when_changed = 100 - self.win_percent_when_changed
        else:
            self.lose_percent_when_changed = 0
        self.lose_percent_when_not_changed = 100 - self.win_percent_when_not_changed

    def make_conclusion(self, num) -> str:
        conclusion = f"""
            Experiment N{num}. 
            From {self.date_start} to {self.date_end}.
            attempts          -->> {self.attempts}
            number of doors   -->> {self.number_of_doors}
            
            \twins   -->> {self.wins}
            
            \t\twins when choice was NOT changed:
            \t\t\tvalue      -->> {self.wins_when_not_changed}
            \t\t\tpercents   -->> {self.win_percent_when_not_changed}
            
            \t\twins when choice WAS changed     -->> {self.wins_when_changed}
            \t\t\tvalue      -->> {self.wins_when_changed}
            \t\t\tpercents   -->> {self.win_percent_when_changed}
            ------------------------------------------------------------------
            \tloses  -->> {self.loses}
            
            \t\tloses when choice was NOT changed:
            \t\t\tvalue      -->> {self.loses_when_not_changed}
            \t\t\tpercent    -->> {self.lose_percent_when_not_changed}
            
            \t\tloses when choice WAS changed:
            \t\t\tvalue      -->> {self.loses_when_changed}
            \t\t\tpercents   -->> {self.lose_percent_when_changed}
        """
        return conclusion
