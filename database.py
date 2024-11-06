# database

import sqlite3

class Database:

    def __init__(self, colors=["red", "green", "blue"]):
        self.conn = sqlite3.connect('example.db')
        self.cursor = self.conn.cursor()

        # Drop the 'buttons' table if it exists
        self.cursor.execute('DROP TABLE IF EXISTS buttons')

        # Step 1: Create the 'buttons' table
        self.cursor.execute('''
            CREATE TABLE buttons (
                id TEXT PRIMARY KEY,    -- Each button has a unique name, used as the primary key
                color TEXT                -- Each button has a color indicating its current state
            )
        ''')

        # Step 2: Insert the initial data into the 'buttons' table
        for i, color in enumerate(colors):
            self.cursor.execute('''
                INSERT INTO buttons (id, color)
                VALUES (?, ?)
            ''', (str(i), color))

        self.conn.commit()

    def get_number_of_buttons(self):
        self.cursor.execute('SELECT COUNT(*) FROM buttons')
        return self.cursor.fetchone()[0]

    def get_schema_description (self):
        out = """The database has the following schema:
        Table: buttons
        - name (TEXT): The unique name of each button, typically a number in text form (e.g., '0', '1', '2').
        - color (TEXT): The current color of the button (e.g., 'red', 'green', 'blue').
        
        Use this schema to generate SQL queries as needed."""
        return out

    def get_button_colors(self):
        """ get a list of just the colors of the buttons so you get something like ["red", "green", "blue"] """
        self.cursor.execute('SELECT color FROM buttons')
        out = [row[0] for row in self.cursor.fetchall()]
        return out

def main():
    db = Database()
    # print the contents of the 'buttons' table
    db.cursor.execute('SELECT * FROM buttons')
    print(db.cursor.fetchall())

    # print the number of buttons
    print(db.get_number_of_buttons())

    # close the connection
    db.conn.close()

# run the main
if __name__ == "__main__":
    main()