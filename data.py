# ==============================================================================
# DATENHALTUNG (Dummy-Daten)
# ==============================================================================
# In dieser Datei speichern wir alle Daten der App (Benutzer, Events, Chats).
# Da die App beim Neustart alles vergessen darf, nutzen wir hierfür einfache
# Python-Listen und Dictionaries (Wörterbücher). Das macht den Code extrem
# simpel und auch ohne Datenbank-Kenntnisse verständlich.

# Aktueller (Test-)Benutzer
# Dieser User ist direkt beim Start eingeloggt.
current_user = {
    "username": "Paul",
    "password": "1234",
    "status": "Free",     # Status bestimmt, ob man Werbung sieht
    "applications": 3     # Limitierte Bewerbungen für Gratis-Nutzer
}

# Dummy-Werbung
# Diese Liste enthält fiktive Werbeanzeigen, die später in den Feed eingestreut werden.
ads = [
    {
        "title": "FitX München",
        "description": "Dein Gym um die Ecke. Jetzt den 1. Monat gratis trainieren!",
        "type": "ad"
    },
    {
        "title": "SportScheck",
        "description": "Neue Laufschuhe gesucht? 20% Rabatt auf alle Artikel mit Code SPORT20.",
        "type": "ad"
    },
    {
        "title": "Boulderkurs für Anfänger",
        "description": "Lerne Bouldern mit unseren Profis. Jetzt Platz sichern!",
        "type": "ad"
    }
]

# Dummy-Events (Zukünftig & Vergangen)
# Hier sind die Sportveranstaltungen definiert. Einige sind bereits in der Vergangenheit,
# bei manchen ist der Test-Benutzer ("is_joined": True) schon dabei.
events = [
    {
        "id": 1,
        "title": "Volleyball an der Isar",
        "sport": "Volleyball",
        "location": "München",
        "date": "Heute, 17:00",
        "max_participants": 8,
        "participants": ["Peter", "Linus", "Nick"],
        "is_joined": False,  
        "is_past": False,
        "type": "event"
    },
    {
        "id": 2,
        "title": "Rennrad Feierabendrunde",
        "sport": "Radsport",
        "location": "München (Süd)",
        "date": "Heute, 18:30",
        "max_participants": 5,
        "participants": ["Paul", "Dieter"],
        "is_joined": True,
        "is_past": False,
        "type": "event"
    },
    {
        "id": 3,
        "title": "Yoga im Englischen Garten",
        "sport": "Yoga",
        "location": "München",
        "date": "Morgen, 10:00",
        "max_participants": 15,
        "participants": ["Anna", "Mia"],
        "is_joined": False,
        "is_past": False,
        "type": "event"
    },
    {
        "id": 4,
        "title": "Spontanes Fussball-Match",
        "sport": "Fussball",
        "location": "Olympiapark",
        "date": "Sonntag, 14:00",
        "max_participants": 22,
        "participants": ["Paul", "Amir", "Dastin"],
        "is_joined": True,
        "is_past": False,
        "type": "event"
    },
    {
        "id": 5,
        "title": "Bouldern für Einsteiger",
        "sport": "Bouldern",
        "location": "Boulderwelt München",
        "date": "Letzten Samstag",
        "max_participants": 10,
        "participants": ["Paul", "Linus", "Max"],
        "is_joined": True,
        "is_past": True,
        "type": "event"
    }
]

# Dummy-Chats
# Hier speichern wir die Nachrichtenverläufe. Es gibt private Chats und Gruppenchats (für Events).
chats = [
    {
        "id": 101,
        "title": "Rennrad Feierabendrunde (Event-Chat)",
        "type": "group",
        "messages": [
            {"sender": "Dieter", "text": "Hi zusammen, wo genau treffen wir uns?"},
            {"sender": "Paul", "text": "Lass uns direkt am Tierpark treffen!"},
            {"sender": "Dieter", "text": "Alles klar, bis später."}
        ]
    },
    {
        "id": 102,
        "title": "Linus",
        "type": "private",
        "messages": [
            {"sender": "Linus", "text": "Hey, bist du morgen beim Volleyball am Start?"},
            {"sender": "Paul", "text": "Weiß ich noch nicht genau. Sag dir heute Abend bescheid."}
        ]
    },
    {
        "id": 103,
        "title": "Spontanes Fussball-Match (Event-Chat)",
        "type": "group",
        "messages": [
            {"sender": "Amir", "text": "Wer bringt einen Ball mit?"},
            {"sender": "Dastin", "text": "Ich hab einen!"}
        ]
    }
]

# Hilfsfunktion: Gibt die Liste für den Home-Feed zurück
def get_feed_items(user_status, filter_sport="", filter_location=""):
    items = []
    
    # 1. Wir filtern erstmal alle vergangenen Events heraus
    feed_events = [e for e in events if not e["is_past"]]
    
    # 2. Such-Filter anwenden (wenn der Nutzer was eingetippt hat)
    if filter_sport:
        feed_events = [e for e in feed_events if filter_sport.lower() in e["sport"].lower()]
    if filter_location:
        feed_events = [e for e in feed_events if filter_location.lower() in e["location"].lower()]
        
    # 3. Werbung untermischen (falls der User Gratis-Mitglied ist)
    ad_index = 0
    for i, event in enumerate(feed_events):
        items.append(event) # Event hinzufügen
        
        # Alle 2 Events streuen wir eine Werbekarte ein
        if user_status == "Free" and (i + 1) % 2 == 0 and ad_index < len(ads):
            items.append(ads[ad_index])
            ad_index += 1
            
    return items

# Hilfsfunktion: Gibt Events zurück, für die der User angemeldet ist
def get_user_events():
    future_events = [e for e in events if e["is_joined"] and not e["is_past"]]
    past_events = [e for e in events if e["is_joined"] and e["is_past"]]
    return future_events, past_events
