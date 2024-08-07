import sqlite3

con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute("CREATE TABLE all_shortened (original_url VARCHAR(4096), shortened_hash VARCHAR(256), email_creator VARCHAR(512), expiry VARCHAR(16), authenticated INTEGER);")
con.close()

os.system("pip install -r requirements.txt --ignore-installed")

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

print("""

 ____ _________________  ___
|    |   \______   \   \/  /
|    |   /|       _/\     / 
|    |  / |    |   \/     \ 
|______/  |____|_  /___/\  \
                 \/      \_/

""")
print("Successfully installed all requirements and setup the database. Please setup the configurations for email files yourself")
