from Game import Game
import sqlite3

# create the databse
# add values to the database from the game

# TO DO: add a timer for the game as soon as the game starts and the main game window appears start timer

# only add to the table if win

def create_database():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            playerName TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY,
            playerName TEXT,
            score INTEGER,
            FOREIGN KEY (playerName) REFERENCES playerName
            )
    """)

def getCurrPlayerId():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY,
                playerName TEXT,
            )
        """)

def addPlayer(playerName):
    command = "INSERT INTO player(id,playerName) VALUES (lower(hex(randomblob(4))),?)"
    cursor.execute(command,(playerName))
    connection.commit()

def addScore(scr, playerName):
    command = "INSERT INTO score(id,playerName,score) VALUES (lower(hex(randomblob(4))),?,?)"
    cursor.execute(command, (playerName,scr))
    connection.commit()



if __name__ == "__main__":
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    create_database()
    x = 5
    y = 10
    game = Game(x ,y)
    game.window.mainloop()

    connection.commit()
    connection.close()


