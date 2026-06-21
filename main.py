import customtkinter as ctk
import data

# ==============================================================================
# GRUNDEINSTELLUNGEN DER APP
# ==============================================================================
# Wir nutzen customtkinter. Es sieht modern aus, der Code funktioniert aber
# wie beim klassischen Tkinter, was es für Anfänger sehr leicht verständlich macht.
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Seriöses Farb-Theme (Professionell / Dunkelblau) ---
COLOR_BG = "#0b101e"            # Sehr dunkles Nachtblau für den Hintergrund
COLOR_CARD = "#151e32"          # Etwas helleres Marineblau für Kacheln (Events/Chats)
COLOR_PRIMARY = "#2563eb"       # Seriöses, vertrauensvolles "Trust Blue"
COLOR_PRIMARY_HOVER = "#1d4ed8" # Dunkleres Blau beim Drüberfahren
COLOR_SUCCESS = "#059669"       # Ruhiges, klassisches Grün für Zusagen
COLOR_SUCCESS_HOVER = "#047857" 
COLOR_TEXT_DIM = "#94a3b8"      # Blaugrauer Text für Nebeninfos
COLOR_PREMIUM = "#d97706"       # Seriöses Gold/Bronze für Premium

# ==============================================================================
# HAUPTKLASSE DER ANWENDUNG
# ==============================================================================
class SportConnectApp(ctk.CTk):
    """Dies ist das Hauptfenster der App. Es steuert, welche Ansicht gerade gezeigt wird."""
    
    def __init__(self):
        super().__init__()
        
        # Fenster konfigurieren (Hochformat wie eine Handy-App)
        self.title("SportConnect")
        self.geometry("400x750")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)
        
        # Ein Container, in dem die verschiedenen Bildschirme (Screens) liegen
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        # Speichert alle unsere Bildschirme
        self.frames = {}
        self.init_views()
        
        # Zeige als allererstes den Login-Screen
        self.show_frame("LoginView")
        
    def init_views(self):
        """Erstellt die Bildschirme (Login und Hauptapp) und legt sie übereinander."""
        for F in (LoginView, MainView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
    def show_frame(self, page_name):
        """Holt den gewünschten Bildschirm in den Vordergrund."""
        frame = self.frames[page_name]
        if page_name == "MainView":
            # Wenn wir zur Hauptansicht wechseln, laden wir die Inhalte neu
            frame.update_view()
        frame.tkraise()

# ==============================================================================
# LOGIN-BILDSCHIRM
# ==============================================================================
class LoginView(ctk.CTkFrame):
    """Hier kann sich der Nutzer einloggen."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_BG)
        self.controller = controller
        
        # Elemente zentrieren
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="SportConnect", font=ctk.CTkFont(size=38, weight="bold"), text_color=COLOR_PRIMARY)
        title.grid(row=1, column=0, pady=(0, 10))
        
        subtitle = ctk.CTkLabel(self, text="Gemeinsam mehr erreichen.", font=ctk.CTkFont(size=14, weight="normal"), text_color="white")
        subtitle.grid(row=2, column=0, pady=(0, 40))
        
        # Eingabefelder mit Dummy-Daten vorausgefüllt (für schnelles Testen in der Präsentation)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Benutzername", width=250, height=45, corner_radius=8, border_width=1, border_color=COLOR_PRIMARY, fg_color=COLOR_CARD)
        self.username_entry.grid(row=3, column=0, pady=10)
        self.username_entry.insert(0, "Paul")
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", show="*", width=250, height=45, corner_radius=8, border_width=1, border_color=COLOR_PRIMARY, fg_color=COLOR_CARD)
        self.password_entry.grid(row=4, column=0, pady=10)
        self.password_entry.insert(0, "1234")
        
        login_btn = ctk.CTkButton(self, text="Einloggen", width=250, height=45, corner_radius=8, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold"), command=self.login)
        login_btn.grid(row=5, column=0, pady=20, sticky="n")
        
        hint = ctk.CTkLabel(self, text="(Mit Test-Daten anmelden)", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_DIM)
        hint.grid(row=6, column=0, pady=(0, 20))
        
    def login(self):
        """Prüft die Logindaten mit den Daten aus der data.py"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == data.current_user["username"] and password == data.current_user["password"]:
            self.controller.show_frame("MainView")
        else:
            print("Falsche Logindaten")

# ==============================================================================
# HAUPT-APP (Nach dem Login)
# ==============================================================================
class MainView(ctk.CTkFrame):
    """Das ist das Herzstück der App. Es beinhaltet die Navigation und den Scrollbereich."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_BG)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # --- Top Header (Leiste oben) ---
        self.header_frame = ctk.CTkFrame(self, height=65, corner_radius=0, fg_color=COLOR_CARD)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_propagate(False)
        self.header_label = ctk.CTkLabel(self.header_frame, text="📰 FEED", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        self.header_label.pack(pady=20)
        
        # --- Content Container (Hier werden die Tab-Inhalte reingeladen) ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # --- Bottom Navigation (Leiste unten) ---
        self.bottom_nav = ctk.CTkFrame(self, height=65, corner_radius=0, fg_color=COLOR_CARD)
        self.bottom_nav.grid(row=2, column=0, sticky="ew")
        self.bottom_nav.grid_propagate(False)
        
        # Buttons für die Tabs unten erstellen
        self.nav_buttons = {}
        tabs = [("Feed", "📰 FEED"), ("Kalender", "📅 KALENDER"), ("Chats", "💬 CHATS"), ("Profil", "👤 PROFIL")]
        for i, (tab, text) in enumerate(tabs):
            self.bottom_nav.grid_columnconfigure(i, weight=1)
            btn = ctk.CTkButton(self.bottom_nav, text=text, fg_color="transparent", text_color="white", hover_color="#1e293b", corner_radius=8, font=ctk.CTkFont(weight="bold", size=11), command=lambda t=tab, txt=text: self.switch_tab(t, txt))
            btn.grid(row=0, column=i, sticky="nsew", pady=8, padx=2)
            self.nav_buttons[tab] = btn
            
        self.current_tab = "Feed"
        self.filter_sport = ""
        self.filter_location = ""
        self.update_nav_colors()
        
    def switch_tab(self, tab_name, tab_text):
        """Wechselt den angezeigten Tab"""
        self.current_tab = tab_name
        self.header_label.configure(text=tab_text)
        self.update_nav_colors()
        self.update_view()
        
    def update_nav_colors(self):
        """Färbt den aktuell aktiven Button in der unteren Leiste farbig"""
        for tab, btn in self.nav_buttons.items():
            if tab == self.current_tab:
                btn.configure(text_color=COLOR_PRIMARY)
            else:
                btn.configure(text_color="white")
                
    def update_view(self):
        """Löscht den alten Inhalt und lädt den neuen (je nach aktivem Tab)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if self.current_tab == "Feed":
            self.render_feed()
        elif self.current_tab == "Kalender":
            self.render_calendar()
        elif self.current_tab == "Chats":
            self.render_chats()
        elif self.current_tab == "Profil":
            self.render_profile()
            
    # ==========================================================================
    # TAB 1: FEED
    # ==========================================================================
    def render_feed(self):
        """Baut den Feed auf (Suchleiste, Events und Werbung)"""
        
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(5, 10))
        
        sport_entry = ctk.CTkEntry(filter_frame, placeholder_text="🔍 Sportart...", height=35, corner_radius=8, border_width=1, border_color=COLOR_TEXT_DIM, fg_color=COLOR_CARD)
        sport_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        if self.filter_sport: sport_entry.insert(0, self.filter_sport)
        
        loc_entry = ctk.CTkEntry(filter_frame, placeholder_text="📍 Ort...", height=35, corner_radius=8, border_width=1, border_color=COLOR_TEXT_DIM, fg_color=COLOR_CARD)
        loc_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        if self.filter_location: loc_entry.insert(0, self.filter_location)
        
        def apply_filters():
            self.filter_sport = sport_entry.get()
            self.filter_location = loc_entry.get()
            self.update_view() # Feed mit neuen Filtern neu laden
            
        filter_btn = ctk.CTkButton(filter_frame, text="Suchen", width=60, height=35, corner_radius=8, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold", size=11), command=apply_filters)
        filter_btn.pack(side="left")
        
        create_btn = ctk.CTkButton(self.content_frame, text="➕ Neues Event", height=40, fg_color="transparent", border_width=1, border_color=COLOR_PRIMARY, text_color=COLOR_PRIMARY, hover_color="#1e293b", font=ctk.CTkFont(weight="bold"), command=self.create_event_dialog)
        create_btn.pack(fill="x", pady=(0, 10))
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        feed_items = data.get_feed_items(data.current_user["status"], self.filter_sport, self.filter_location)
        
        for item in feed_items:
            if item.get("type") == "event":
                self.create_event_card(scroll_frame, item)
            elif item.get("type") == "ad":
                self.create_ad_card(scroll_frame, item)
                
    def create_event_card(self, parent, event):
        """Erstellt das kleine Info-Kästchen für ein einzelnes Sportevent im Feed"""
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color="#1e293b")
        card.pack(fill="x", pady=8, padx=2)
        
        title = ctk.CTkLabel(card, text=event["title"], font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        title.pack(anchor="w", padx=15, pady=(15, 0))
        
        info = ctk.CTkLabel(card, text=f"📍 {event['location']}  |  🕒 {event['date']}", text_color=COLOR_TEXT_DIM, font=ctk.CTkFont(size=12))
        info.pack(anchor="w", padx=15, pady=(2, 0))
        
        sport_badge = ctk.CTkLabel(card, text=f" {event['sport']} ", fg_color="#1e293b", corner_radius=5, font=ctk.CTkFont(size=10, weight="bold"))
        sport_badge.pack(anchor="w", padx=15, pady=(8, 0))
        
        places = ctk.CTkLabel(card, text=f"👥 Teilnehmer: {len(event['participants'])}/{event['max_participants']}", font=ctk.CTkFont(size=12))
        places.pack(anchor="w", padx=15, pady=(10, 5))
        
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(anchor="e", padx=15, pady=(0, 15), fill="x")
        
        info_btn = ctk.CTkButton(btn_frame, text="ℹ️ Info", width=80, fg_color="#334155", hover_color="#475569", text_color="white", corner_radius=6, font=ctk.CTkFont(weight="bold"), command=lambda ev=event: self.open_event(ev))
        info_btn.pack(side="left")
        
        def join_event(ev=event):
            if ev["is_joined"]: return
            if data.current_user["status"] == "Free":
                if data.current_user["applications"] <= 0:
                    error = ctk.CTkLabel(card, text="Limit erreicht! Gehe auf Profil für Premium.", text_color=COLOR_PRIMARY)
                    error.pack(anchor="w", padx=15, pady=5)
                    return
                else:
                    data.current_user["applications"] -= 1
                    
            ev["is_joined"] = True
            ev["participants"].append(data.current_user["username"])
            
            chat_exists = any(c["title"] == f"{ev['title']} (Event)" for c in data.chats)
            if not chat_exists:
                data.chats.append({
                    "id": len(data.chats)+100,
                    "title": f"{ev['title']} (Event)",
                    "type": "group",
                    "messages": [{"sender": "System", "text": "Willkommen im Chat! Triff dich hier mit deinem Team."}]
                })
                
            self.update_view() 
            
        if event["is_joined"]:
            btn = ctk.CTkButton(btn_frame, text="✔️ Angemeldet", state="disabled", fg_color="#1e293b", text_color=COLOR_TEXT_DIM, corner_radius=6, font=ctk.CTkFont(weight="bold"))
        else:
            btn = ctk.CTkButton(btn_frame, text="Teilnehmen", fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, text_color="white", corner_radius=6, font=ctk.CTkFont(weight="bold"), command=join_event)
            
        btn.pack(side="right")
        
    def create_ad_card(self, parent, ad):
        """Erstellt die Werbekarte (Anzeige), die sich optisch abhebt"""
        card = ctk.CTkFrame(parent, fg_color="#1f2937", corner_radius=10, border_width=1, border_color=COLOR_PREMIUM)
        card.pack(fill="x", pady=12, padx=2)
        
        ad_badge = ctk.CTkLabel(card, text=" 📢 ANZEIGE ", fg_color=COLOR_PREMIUM, text_color="white", corner_radius=4, font=ctk.CTkFont(size=10, weight="bold"))
        ad_badge.pack(anchor="e", padx=15, pady=(10, 0))
        
        title = ctk.CTkLabel(card, text=ad["title"], font=ctk.CTkFont(size=14, weight="bold"))
        title.pack(anchor="w", padx=15)
        
        desc = ctk.CTkLabel(card, text=ad["description"], wraplength=320, justify="left", text_color=COLOR_TEXT_DIM)
        desc.pack(anchor="w", padx=15, pady=(5, 15))
        
    def create_event_dialog(self):
        """Öffnet ein kleines Pop-up-Fenster, um ein neues Event anzulegen"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Neues Event")
        dialog.geometry("350x550")
        dialog.configure(fg_color=COLOR_BG)
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(scroll_frame, text="Event Titel", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        title_e = ctk.CTkEntry(scroll_frame, fg_color=COLOR_CARD, border_width=1, border_color=COLOR_TEXT_DIM, corner_radius=6, height=35)
        title_e.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(scroll_frame, text="Sportart", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        sport_e = ctk.CTkEntry(scroll_frame, fg_color=COLOR_CARD, border_width=1, border_color=COLOR_TEXT_DIM, corner_radius=6, height=35)
        sport_e.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(scroll_frame, text="Ort", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        location_e = ctk.CTkEntry(scroll_frame, fg_color=COLOR_CARD, border_width=1, border_color=COLOR_TEXT_DIM, corner_radius=6, height=35)
        location_e.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(scroll_frame, text="Datum & Uhrzeit", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        date_e = ctk.CTkEntry(scroll_frame, fg_color=COLOR_CARD, border_width=1, border_color=COLOR_TEXT_DIM, corner_radius=6, height=35)
        date_e.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(scroll_frame, text="Max. Teilnehmer", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 0))
        max_p_e = ctk.CTkEntry(scroll_frame, fg_color=COLOR_CARD, border_width=1, border_color=COLOR_TEXT_DIM, corner_radius=6, height=35)
        max_p_e.pack(pady=5, padx=20, fill="x")
        
        def save():
            try:
                max_p = int(max_p_e.get())
            except ValueError:
                max_p = 10
                
            data.events.insert(0, {
                "id": len(data.events)+1,
                "title": title_e.get() or "Mein Event",
                "sport": sport_e.get() or "Diverses",
                "location": location_e.get() or "Nicht angegeben",
                "date": date_e.get() or "Bald",
                "max_participants": max_p,
                "participants": [data.current_user["username"]],
                "is_joined": True,
                "is_past": False,
                "type": "event"
            })
            dialog.destroy()
            self.update_view()
            
        ctk.CTkButton(scroll_frame, text="Erstellen", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, corner_radius=6, height=40, font=ctk.CTkFont(weight="bold"), command=save).pack(pady=20, padx=20, fill="x")

    def open_event(self, event):
        """Öffnet die Detailansicht eines Events (wenn man auf Info klickt)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))
        
        btn_back = ctk.CTkButton(top_bar, text="⬅ Zurück", width=60, fg_color="transparent", text_color="white", font=ctk.CTkFont(weight="bold"), command=self.update_view)
        btn_back.pack(side="left")
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(scroll_frame, text=event["title"], font=ctk.CTkFont(size=22, weight="bold"), text_color=COLOR_PRIMARY, wraplength=350, justify="left").pack(anchor="w", pady=(10, 5), padx=10)
        
        ctk.CTkLabel(scroll_frame, text="Details", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5), padx=10)
        
        details_frame = ctk.CTkFrame(scroll_frame, fg_color=COLOR_CARD, corner_radius=8)
        details_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(details_frame, text=f"⚽ Sportart: {event['sport']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(details_frame, text=f"📍 Ort: {event['location']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(details_frame, text=f"🕒 Datum: {event['date']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=(5, 10))
        
        ctk.CTkLabel(scroll_frame, text="Teilnehmer", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(25, 5), padx=10)
        
        participants_frame = ctk.CTkFrame(scroll_frame, fg_color=COLOR_CARD, corner_radius=8)
        participants_frame.pack(fill="x", padx=10, pady=5)
        
        for person in event["participants"]:
            ctk.CTkLabel(participants_frame, text=f"👤 {person}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=5)
            
        if not event["is_joined"]:
            def join():
                if data.current_user["status"] == "Free":
                    if data.current_user["applications"] <= 0:
                        error = ctk.CTkLabel(scroll_frame, text="Limit erreicht! Gehe auf Profil für Premium.", text_color=COLOR_PRIMARY)
                        error.pack(fill="x", padx=10, pady=5)
                        return
                    data.current_user["applications"] -= 1
                event["is_joined"] = True
                event["participants"].append(data.current_user["username"])
                
                chat_exists = any(c["title"] == f"{event['title']} (Event)" for c in data.chats)
                if not chat_exists:
                    data.chats.append({"id": len(data.chats)+100, "title": f"{event['title']} (Event)", "type": "group", "messages": [{"sender": "System", "text": "Willkommen im Chat!"}]})
                self.open_event(event)
                
            btn_join = ctk.CTkButton(scroll_frame, text="Teilnehmen", height=45, fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, text_color="white", corner_radius=8, font=ctk.CTkFont(weight="bold", size=14), command=join)
            btn_join.pack(fill="x", padx=10, pady=25)
        else:
            btn_joined = ctk.CTkButton(scroll_frame, text="✔️ Bereits angemeldet", state="disabled", height=45, fg_color="#1e293b", text_color=COLOR_TEXT_DIM, corner_radius=8, font=ctk.CTkFont(weight="bold", size=14))
            btn_joined.pack(fill="x", padx=10, pady=25)

    # ==========================================================================
    # TAB 2: KALENDER
    # ==========================================================================
    def render_calendar(self):
        """Zeigt die eigenen zukünftigen und vergangenen Events an"""
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        future, past = data.get_user_events()
        
        ctk.CTkLabel(scroll_frame, text="Anstehende Events", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_SUCCESS).pack(anchor="w", pady=(10, 5), padx=5)
        if not future:
            ctk.CTkLabel(scroll_frame, text="Keine zukünftigen Events.", text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=5)
        for e in future:
            self.create_event_card(scroll_frame, e)
            
        ctk.CTkLabel(scroll_frame, text="Vergangen", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w", pady=(25, 5), padx=5)
        if not past:
            ctk.CTkLabel(scroll_frame, text="Keine vergangenen Events.", text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=5)
        for e in past:
            self.create_event_card(scroll_frame, e)

    # ==========================================================================
    # TAB 3: CHATS
    # ==========================================================================
    def render_chats(self):
        """Zeigt die Liste aller Chats an"""
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        for chat in data.chats:
            card = ctk.CTkFrame(scroll_frame, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color="#1e293b")
            card.pack(fill="x", pady=5, padx=2)
            
            last_msg = chat["messages"][-1]["text"] if chat["messages"] else "..."
            icon = "💬" if chat["type"] == "group" else "👤"
            
            title = ctk.CTkLabel(card, text=f"{icon} {chat['title']}", font=ctk.CTkFont(size=15, weight="bold"))
            title.pack(anchor="w", padx=15, pady=(15, 2))
            
            msg_lbl = ctk.CTkLabel(card, text=last_msg, text_color=COLOR_TEXT_DIM, wraplength=300, justify="left")
            msg_lbl.pack(anchor="w", padx=15, pady=(0, 5))
            
            btn_open = ctk.CTkButton(card, text="Öffnen ➔", width=80, height=25, fg_color="transparent", text_color=COLOR_PRIMARY, font=ctk.CTkFont(weight="bold"), command=lambda c=chat: self.open_chat(c))
            btn_open.pack(anchor="e", padx=10, pady=(0, 10))

    def open_chat(self, chat):
        """Öffnet den Nachrichtenverlauf eines einzelnen Chats"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))
        
        btn_back = ctk.CTkButton(top_bar, text="⬅ Zurück", width=60, fg_color="transparent", text_color="white", font=ctk.CTkFont(weight="bold"), command=self.update_view)
        btn_back.pack(side="left")
        
        chat_title = ctk.CTkLabel(top_bar, text=chat["title"], font=ctk.CTkFont(size=16, weight="bold"), wraplength=230, justify="left", anchor="w")
        chat_title.pack(side="left", padx=10, fill="x", expand=True)
        
        msg_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color=COLOR_CARD, corner_radius=10)
        msg_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        def render_messages():
            for widget in msg_frame.winfo_children():
                widget.destroy()
            for msg in chat["messages"]:
                is_me = msg["sender"] == data.current_user["username"]
                anchor = "e" if is_me else "w"                  
                bg_color = COLOR_PRIMARY if is_me else "#1e293b" 
                text_color = "white"
                
                msg_bubble = ctk.CTkFrame(msg_frame, fg_color=bg_color, corner_radius=10)
                msg_bubble.pack(anchor=anchor, pady=5, padx=10)
                
                sender_lbl = ctk.CTkLabel(msg_bubble, text=msg["sender"], text_color="#d1d5db" if is_me else "#94a3b8", font=ctk.CTkFont(size=10, weight="bold"))
                sender_lbl.pack(anchor="w", padx=10, pady=(5, 0))
                
                txt_lbl = ctk.CTkLabel(msg_bubble, text=msg["text"], text_color=text_color, wraplength=200, justify="left")
                txt_lbl.pack(anchor="w", padx=10, pady=(0, 5))
                
        render_messages()
        
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 5))
        
        entry = ctk.CTkEntry(input_frame, placeholder_text="Nachricht...", height=40, corner_radius=8, border_width=1, border_color=COLOR_TEXT_DIM, fg_color=COLOR_CARD)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        def send_message():
            text = entry.get()
            if text.strip():
                chat["messages"].append({"sender": data.current_user["username"], "text": text})
                entry.delete(0, 'end') 
                render_messages()      
                
        btn_send = ctk.CTkButton(input_frame, text="Senden", width=60, height=40, corner_radius=8, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold"), command=send_message)
        btn_send.pack(side="right")

    # ==========================================================================
    # TAB 4: PROFIL / ABO
    # ==========================================================================
    def render_profile(self):
        """Zeigt die Profil-Seite an, wo man sich das Premium-Abo kaufen kann"""
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, pady=20)
        
        icon = ctk.CTkLabel(frame, text="🏅", font=ctk.CTkFont(size=70))
        icon.pack()
        
        name = ctk.CTkLabel(frame, text=data.current_user["username"].upper(), font=ctk.CTkFont(size=26, weight="bold"))
        name.pack(pady=(10,0))
        
        status_color = COLOR_PREMIUM if data.current_user["status"] == "Premium" else "white"
        status = ctk.CTkLabel(frame, text=f"Status: {data.current_user['status']}", text_color=status_color, font=ctk.CTkFont(weight="bold", size=16))
        status.pack(pady=(5, 20))
        
        if data.current_user["status"] == "Free":
            info = ctk.CTkLabel(frame, text=f"Verbleibende Bewerbungen: {data.current_user['applications']}", font=ctk.CTkFont(size=14))
            info.pack(pady=5)
            
            premium_frame = ctk.CTkFrame(frame, fg_color="#1e180d", corner_radius=10, border_width=1, border_color=COLOR_PREMIUM)
            premium_frame.pack(fill="x", pady=30, padx=10)
            
            ctk.CTkLabel(premium_frame, text="Premium Mitgliedschaft", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLOR_PREMIUM).pack(pady=(20, 5))
            ctk.CTkLabel(premium_frame, text="✔️ Keine Werbung mehr\n✔️ Unbegrenzte Anmeldungen\n✔️ Exklusive Events", justify="left", font=ctk.CTkFont(size=14)).pack(pady=10)
            
            def buy_premium():
                data.current_user["status"] = "Premium"
                self.update_view() 
                
            ctk.CTkButton(premium_frame, text="Upgrade für 3,49 € / Monat", height=45, fg_color=COLOR_PREMIUM, hover_color="#b45309", text_color="white", font=ctk.CTkFont(weight="bold", size=14), corner_radius=6, command=buy_premium).pack(pady=20, padx=20, fill="x")
        else:
            ctk.CTkLabel(frame, text="Du bist Premium-Mitglied!", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLOR_PREMIUM).pack(pady=30)
            ctk.CTkLabel(frame, text="✔️ Unbegrenzte Anmeldungen\n✔️ Keine Werbung", justify="center", font=ctk.CTkFont(size=16)).pack()

# ==============================================================================
# APP START
# ==============================================================================
if __name__ == "__main__":
    app = SportConnectApp()
    app.mainloop()
