import datetime
import time
import json
import base64

from flask import render_template, redirect, request
import requests
from app import app

from bc.node import Node
from bc.account import Account
from bc.blockchain import Blockchain
from bc.block import Block
from user import User

import random # Zufallsgenerator für "Simulation" der Nodes ("wer zuerst einen gültigen Hash berechnet hat")

print("----------- views.py started")

# eingeloggter Nutzer der Anwendung (Account via Hashgenerator)
# wir gehen einmal davon aus, unser Nutzer hat ein Abo, was ihn 100 Transaktionen ermöglicht
user = User("Banksy", Account("2f0e3b1787b4ea6094f954ff485c3f14b18af24c51678821e320bf8f3db203f3"), "12345")
user.account.coins += 100

# 3 Nodes erzeugen mit jeweils eigenem Wallet
# zur Info: per https://hashgenerator.de einen zufälligen Hash als Dummy generieren
nodes = [
    Node("127.0.0.1/8000", Account("fea82e10e894419fe2bea7d96296a6d46f50f93f9eeda954ec461b2ed2950b62")), # Hash vom String "Node1"
    Node("127.0.0.1/8001", Account("1ac8aece2a18ced660fef8694b61aac3af08ba875ce3026a160acbc3a3af35fc")),
    Node("127.0.0.1/8002", Account("7e9f355dffa78ed24668f0e0e369fd8c224076571c51e2ea8be5f26479edebe4"))
]

# unsere blockchain
blockchain = Blockchain()
blockchain.create_genesis_block()


# f----- Funktion um das Datum ordentlich auszugeben (Nur wenn wir etwas im template ausgeben)
def timestamp_to_string(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')


# f----- Funktion um Bild in base64 String umzuwandeln
def imageToBase64(img):
    return base64.b64encode(img.read()).decode()


# Test Variable um etwas im Template auszugeben
my_variable = ''



# Die Index Route bzw. unsere Formular Seite
'''
Eigentlich müsste im POST Request noch eine Prüfung auf Fehler und Dateien stattfinden
Auch müssten die Bilder eines Multiplen Upload Feldes in einem for in loop eingefügt werden o.ä.
'''                
@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        
        # assign values from input fields to transaction object
        transaction = json.dumps({
            "art_title":                request.form["art-title"],
            "artist_name":              request.form["artist"],
            "main_image":               imageToBase64(request.files["main-image"]),
            #
            # später via loop aus multiple input >> request.files.getlist("main-image")
            # "images":   {                
            #     "detail_01":        block.index,
            #     "detail_02":      block.transactions
            #     },
            # "image_artist_and_work":    request.files["artist-in-image"],
            #
            "copyright_time":           time.time()
        })
        doCopyrighting(transaction)

        return redirect(request.url)
    
    '''
    Schön wäre natürlich ein komplexeres Layout z.B. Darstellung aller bereits gesicherten Urheberschaften o.ä.
    Nur dann ist man ja schnell bei der kompletten Anwendung (Login Screen, Einstellungen, Abos, usw.)
    '''
    return render_template("index.html", my_var=my_variable)



# Funktion welche die Urheberschaft bzw. die entsprechenden Daten in die Blockchain schreibt
# ebenso werden dem Nutzer Kosten und den Nodes ein Gewinn überwiesen
'''
Hierbei ist die Entlohnung der Nodes sowie die Kosten für den Nutzer noch nicht ganz klar.
Auch wodurch genau und an welcher Stelle, die Anwendung mitverdient. 
Da sind verschiedenste Möglichkeiten denkbar. Sowas müsste erst einmal analysiert werden.
'''
def doCopyrighting(trx):
    print(f"----- doCopyrighting -------")
    
    # schreibe die aktuelle Transaktion in die Trasnaktionsliste
    blockchain.add_new_transaction(trx)
    
    # Bezahlung für mining nach Transaktionen in Liste (ist das finanziell sinnvoll?)
    reward = len(blockchain.unconfirmed_transactions)
    
    # mining (fügt neuen Block zur Blockchain) 
    '''
    wir müssen davon ausgehen, dass normalerweise mehrere Nutzer, teilweise
    zeitgleich Transaktionen vornehmen und die Transaktionsliste dann wahrscheinlich 
    in einem zeitlichen Intervall als neuer Block hinzugefügt werden müsste
    '''    
    blockchain.mine()
    # kurze Überprüfung, ob es geklappt hat 
    for block in blockchain.chain:
        print(f"-- block {block.index}: {block.__dict__}")
    
    # wir simulieren hier den "Gewinner" Node des mining bzw proof of work
    random_node = random.choice(nodes)
    
    # Node bekommt einen Coin für jede Transaktion
    random_node.account.coins += reward
    
      
    # Nutzer wird ein Coin abgezogen
    '''
    Die Überprüfung des Guthabens müsste real natürlich schon weitab vorher passieren.
    Entsprechende Hinweise an den Nutzer in Form von angepassten Templates und z.B.
    das Eingabeformular gar nicht erst anzeigen.
    '''        
    if user.account.coins > 0 :
        user.account.coins -= 1
    
    
    print(f"----- end doCopyrighting -------")