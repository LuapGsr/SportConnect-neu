import sys
import os
import pytest
import customtkinter as ctk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
import data

@pytest.fixture(scope="module")
def app():
    # Make sure we don't start the mainloop
    application = main.SportConnectApp()
    application.update() # Process all pending events
    yield application
    application.destroy()

def find_button_and_invoke(parent, text_contains):
    # Recursively find a button whose text contains the given string and invoke its command
    for widget in parent.winfo_children():
        # Using cget to get the text, falling back to empty string
        widget_text = ""
        try:
            widget_text = widget.cget("text")
        except:
            pass
        if isinstance(widget, ctk.CTkButton) and text_contains in widget_text:
            command = widget.cget("command")
            if command:
                command()
            return True
        # Recursion for frames
        if hasattr(widget, "winfo_children"):
            if find_button_and_invoke(widget, text_contains):
                return True
    return False

def test_app_initialization(app):
    assert "LoginView" in app.frames
    assert "MainView" in app.frames

def test_login_failure(app):
    login_view = app.frames["LoginView"]
    
    # Try with wrong data
    login_view.username_entry.delete(0, 'end')
    login_view.username_entry.insert(0, "WrongUser")
    login_view.password_entry.delete(0, 'end')
    login_view.password_entry.insert(0, "wrongpass")
    
    login_view.login()
    app.update()
    
    assert "Falscher Benutzername" in login_view.error_label.cget("text")

def test_login_success(app):
    login_view = app.frames["LoginView"]
    
    # Reset to correct data
    login_view.username_entry.delete(0, 'end')
    login_view.username_entry.insert(0, data.current_user["username"])
    login_view.password_entry.delete(0, 'end')
    login_view.password_entry.insert(0, data.current_user["password"])
    
    login_view.login()
    app.update()
    assert login_view.error_label.cget("text") == ""

def test_main_view_tabs(app):
    main_view = app.frames["MainView"]
    app.show_frame("MainView")
    app.update()
    
    tabs = [("Feed", "📰 FEED"), ("Kalender", "📅 KALENDER"), ("Chats", "💬 CHATS"), ("Profil", "👤 PROFIL")]
    for tab_name, tab_text in tabs:
        main_view.switch_tab(tab_name, tab_text)
        app.update()
        assert main_view.current_tab == tab_name

def test_feed_filters(app):
    main_view = app.frames["MainView"]
    main_view.switch_tab("Feed", "📰 FEED")
    main_view.filter_sport = "Volleyball"
    main_view.filter_location = "München"
    main_view.update_view()
    app.update()

def test_create_event_dialog(app):
    main_view = app.frames["MainView"]
    main_view.switch_tab("Feed", "📰 FEED")
    
    existing_toplevels = [w for w in app.winfo_children() if isinstance(w, ctk.CTkToplevel)]
    
    main_view.create_event_dialog()
    app.update()
    
    current_toplevels = [w for w in app.winfo_children() if isinstance(w, ctk.CTkToplevel)]
    new_toplevels = [w for w in current_toplevels if w not in existing_toplevels]
    
    if new_toplevels:
        dialog = new_toplevels[0]
        # Find the "Erstellen" button and invoke it to test the save() nested function
        find_button_and_invoke(dialog, "Erstellen")
        app.update()

def test_open_event(app):
    main_view = app.frames["MainView"]
    main_view.switch_tab("Feed", "📰 FEED")
    
    # Test join function inside open_event
    event = data.events[0]  # Take an event that is not joined
    event["is_joined"] = False 
    main_view.open_event(event)
    app.update()
    
    # Click "Teilnehmen"
    find_button_and_invoke(main_view.content_frame, "Teilnehmen")
    app.update()
    assert event["is_joined"] == True
    
def test_open_chat(app):
    main_view = app.frames["MainView"]
    main_view.switch_tab("Chats", "💬 CHATS")
    
    chat = data.chats[0]
    main_view.open_chat(chat)
    app.update()
    
    # Find the entry and send a message
    for widget in main_view.content_frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkEntry):
                    child.insert(0, "Hello Pytest!")
    
    find_button_and_invoke(main_view.content_frame, "Senden")
    app.update()
    assert chat["messages"][-1]["text"] == "Hello Pytest!"

def test_profile_render(app):
    main_view = app.frames["MainView"]
    # Make sure user is "Free" first to test the buy_premium function
    data.current_user["status"] = "Free"
    main_view.switch_tab("Profil", "👤 PROFIL")
    app.update()
    
    find_button_and_invoke(main_view.content_frame, "Upgrade")
    app.update()
    assert data.current_user["status"] == "Premium"
