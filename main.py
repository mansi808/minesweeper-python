from Game import Game
import sqlite3


# TO DO: delete older values of score if number of rows goies over 10 delete res of the rows
class Database:

    def __init__(self):
        self.connection = sqlite3.connect("game.db")
        self.cursor = self.connection.cursor()

    def create_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playerName TEXT
            )
        """)

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS score (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playerId INTEGER,
                    score INTEGER,
                    FOREIGN KEY (playerId) REFERENCES Player(id)
                    )
            """)

    def get_curr_playr_id(self):
        self.cursor.execute('SELECT id FROM player ORDER BY id desc LIMIT 1')
        return self.cursor.fetchone()[0]

    def add_player(self,name):
        self.cursor.execute('INSERT INTO player(playerName) VALUES (?)', (name,))
        self.cursor.execute('SELECT * FROM player')
        self.connection.commit()

    def add_score(self,id, scr):
        command = "INSERT INTO score(playerId,score) VALUES (?,?)"
        self.cursor.execute(command, (id, scr))
        self.cursor.execute("SELECT * FROM score")
        self.connection.commit()

    def get_leaderboard(self):
        self.cursor.execute("SELECT p.playerName,s.score "
                            "FROM score s INNER JOIN player p "
                            "ON p.id=s.playerId "
                            "ORDER BY s.score asc "
                            "LIMIT 10")
        return self.cursor.fetchall()

if __name__ == "__main__":

    db = Database()
    x = 2
    y = 2
    # if game ended show a pay again button
    game = Game(x ,y,db)
    game.window.mainloop()


