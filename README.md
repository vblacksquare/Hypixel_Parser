### Hello:
    This is a hypixel auctions parser. I`am poop programmer so my code is poop too.

# Idea:
    1)Get all orders from hypixel auctions
    2)Save them to db
    3)Get it from db to analyze
    4)Configure program to run it in Terminal

### Description:
    1) Getting orders from hypixel auctions:
        a) To do this, I found official hypixel api(https://api.hypixel.net/). 
        b) We can request api with https://api.hypixel.net/skyblock/auctions?page=1&key=your_key
        c) To get your own api key, you have to join offical hypixel minecraft server and type command /api
    
    2) Saving them into db:
        a) I chose sqlite3 coz it is very simple and fast enough.
        b) The response from hypixel api is in json format, so I had to use json parser (base library)
        c) I created a class DbHandler to work with db, and created copy of the class in the settings.py
        c) Saving them into db by method upload_order_to_db of class DbHandler that I created
    
    3) Getting orders from db:
        a) I created method get_orders_by_keys in class DbHandler to get orders or certain order data.
        b) After you got needed data, analyze it.
    
    4) Configuring it to run throw Terminal or Cmd:
        I imported library argparse to parse arguments

### How to use:
    1) You need to check if you have Python 3.x on your, just download it by link https://www.python.org/
    2) Also program needs some additional libraries, so you need to run in terminal pip install -r requirements.txt
    3) And finally run python3 main.py -h, to know avaible commands
    4) If you are running it at first time, run python3 main.py -func update
