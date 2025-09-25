from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import json
import os
from datetime import datetime
import threading
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

class GoogleSelfBot:
    def __init__(self, config_file="googler_config.json"):
        """Initialisiert den Google Self-Bot mit erweiterten Features"""
        self.driver = None
        self.config = self.load_config(config_file)
        self.stats = {
            "total_searches": 0,
            "successful_searches": 0,
            "start_time": datetime.now(),
            "errors": []
        }
        self.running = False
        self.setup_driver()
    
    def load_config(self, config_file):
        """Lädt die Konfiguration aus einer JSON-Datei"""
        default_config = {
            "search_terms": [
                "Google", "google", "GOOGLE", "Google Search", "Google.com",
                "Was ist Google?", "Google Deutschland", "Google News",
                "YouTube", "Gmail", "Google Maps", "Android"
            ],
            "delay_range": [2, 5],
            "headless": False,
            "stealth_mode": True,
            "enable_scrolling": True,
            "enable_clicks": True,
            "max_iterations": None,
            "save_screenshots": False
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                return default_config
        except Exception as e:
            print(f"Fehler beim Laden der Config: {e}")
            return default_config
    
    def setup_driver(self):
        """Richtet den Chrome WebDriver mit erweiterten Stealth-Features ein"""
        try:
            chrome_options = webdriver.ChromeOptions()
            
            if self.config.get("headless", False):
                chrome_options.add_argument("--headless")

            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en', 'de']})")
            
            self.driver.set_window_size(1920, 1080)
            
            self.print_colored("Chrome WebDriver mit Stealth-Mode erfolgreich initialisiert!", "green")
            
        except Exception as e:
            self.print_colored(f"Fehler beim Initialisieren des WebDrivers: {e}", "red")
            self.print_colored("Stelle sicher, dass ChromeDriver installiert ist!", "yellow")
    
    def print_colored(self, text, color="white"):
        """Druckt farbigen Text (Fallback ohne colorama)"""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m"
        }
        reset = "\033[0m"
        print(f"{colors.get(color, colors['white'])}{text}{reset}")
    
    def open_google(self):
        """Öffnet Google mit erweiterten Features"""
        try:
            google_domains = [
                "https://www.google.com",
                "https://www.google.de", 
                "https://google.com",
                "https://www.google.com/search"
            ]
            
            chosen_domain = random.choice(google_domains)
            self.driver.get(chosen_domain)
            
            time.sleep(random.uniform(1.0, 2.5))
            
            self.handle_cookie_banner()
            
            if self.config.get("enable_scrolling", True) and random.random() < 0.3:
                self.random_scroll()
            
            self.print_colored(f"Google geöffnet: {chosen_domain}", "green")
            return True
            
        except Exception as e:
            self.print_colored(f"Fehler beim Öffnen von Google: {e}", "red")
            self.stats["errors"].append(f"Google öffnen: {e}")
            return False
    
    def handle_cookie_banner(self):
        """Behandelt Cookie-Banner automatisch"""
        try:
            cookie_selectors = [
                "button[id*='accept']",
                "button[id*='cookie']",
                "button[aria-label*='Accept']",
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'Akzeptieren')]",
                "//div[contains(@class, 'cookie')]//button"
            ]
            
            for selector in cookie_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        time.sleep(random.uniform(0.5, 1.0))
                        self.print_colored("Cookie-Banner akzeptiert", "cyan")
                        break
                except:
                    continue
        except:
            pass
    
    def random_scroll(self):
        """Führt zufälliges Scrollen aus für natürliches Verhalten"""
        try:
            scroll_amount = random.randint(100, 500)
            direction = random.choice(["down", "up"])
            
            if direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            else:
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            
            time.sleep(random.uniform(0.3, 0.8))
        except:
            pass
    
    def search_google(self, search_term="Google"):
        """Sucht nach dem gegebenen Begriff mit erweiterten Features"""
        try:
            search_selectors = [
                (By.NAME, "q"),
                (By.CSS_SELECTOR, "input[title='Search']"),
                (By.CSS_SELECTOR, "input[role='combobox']"),
                (By.XPATH, "//input[@name='q']")
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    break
                except:
                    continue
            
            if not search_box:
                raise Exception("Suchfeld nicht gefunden")
            
            search_box.click()
            time.sleep(random.uniform(0.2, 0.5))
            
            search_box.clear()
            time.sleep(random.uniform(0.3, 0.7))
            
            self.type_like_human(search_box, search_term)
            
            if random.random() < 0.2:
                time.sleep(random.uniform(1.0, 2.0))
                if self.try_use_suggestion():
                    self.stats["total_searches"] += 1
                    self.stats["successful_searches"] += 1
                    return True
            
            if random.random() < 0.7:
                search_box.send_keys(Keys.RETURN)
            else:
                self.click_search_button()
            
            time.sleep(random.uniform(1.0, 2.0))
            
            if self.config.get("enable_clicks", True) and random.random() < 0.4:
                self.interact_with_results()
            
            self.print_colored(f"Gesucht nach: '{search_term}'", "blue")
            self.stats["total_searches"] += 1
            self.stats["successful_searches"] += 1
            
            if self.config.get("save_screenshots", False):
                self.save_screenshot(search_term)
            
            return True
            
        except Exception as e:
            self.print_colored(f"Fehler beim Suchen: {e}", "red")
            self.stats["errors"].append(f"Suche '{search_term}': {e}")
            return False
    
    def type_like_human(self, element, text):
        """Simuliert menschliches Tippen mit Variationen"""
        for i, char in enumerate(text):
            element.send_keys(char)
            
            base_delay = random.uniform(0.05, 0.15)
            
            if char == ' ':
                base_delay += random.uniform(0.1, 0.3)
            
            if random.random() < 0.1:
                base_delay += random.uniform(0.2, 0.5)
            
            if random.random() < 0.05 and i < len(text) - 1:
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.2))
            
            time.sleep(base_delay)
    
    def try_use_suggestion(self):
        """Versucht, einen Suchvorschlag zu verwenden"""
        try:
            suggestions = self.driver.find_elements(By.CSS_SELECTOR, "[role='option'], .sbct")
            if suggestions and len(suggestions) > 1:
                suggestion = random.choice(suggestions[1:4])
                if suggestion.is_displayed():
                    suggestion.click()
                    self.print_colored("Suchvorschlag verwendet", "cyan")
                    return True
        except:
            pass
        return False
    
    def click_search_button(self):
        """Klickt auf den Such-Button"""
        try:
            button_selectors = [
                "input[value='Google Search']",
                "input[name='btnK']",
                "button[aria-label='Google Search']"
            ]
            
            for selector in button_selectors:
                try:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if button.is_displayed():
                        button.click()
                        return True
                except:
                    continue
        except:
            pass
        return False
    
    def interact_with_results(self):
        """Interagiert mit Suchergebnissen für natürliches Verhalten"""
        try:
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(random.uniform(0.5, 1.0))
            
            if random.random() < 0.3:
                results = self.driver.find_elements(By.CSS_SELECTOR, "h3, .LC20lb")
                if results:
                    result = random.choice(results[:5]) 
                    if result.is_displayed():
                        result.click()
                        time.sleep(random.uniform(2.0, 4.0))
                        self.driver.back()
                        self.print_colored("Mit Suchergebnis interagiert", "purple")
            
            scroll_amount = random.randint(200, 800)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
            
        except:
            pass
    
    def save_screenshot(self, search_term):
        """Speichert einen Screenshot der aktuellen Seite"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}_{search_term.replace(' ', '_')}.png"
            
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            self.driver.save_screenshot(f"screenshots/{filename}")
            self.print_colored(f"Screenshot gespeichert: {filename}", "yellow")
        except Exception as e:
            self.print_colored(f"Screenshot-Fehler: {e}", "yellow")

    def run_loop(self, iterations=None, delay_range=None):
        """Führt die Google-Suche in einer erweiterten Schleife aus"""
        if not self.driver:
            self.print_colored("WebDriver nicht initialisiert!", "red")
            return
        
        if delay_range is None:
            delay_range = self.config.get("delay_range", [2, 5])
        
        if iterations is None:
            iterations = self.config.get("max_iterations", None)
        
        counter = 0
        self.running = True
        search_terms = self.config.get("search_terms", ["Google"])
        
        stats_thread = threading.Thread(target=self.live_stats_display, daemon=True)
        stats_thread.start()
        
        try:
            self.print_colored("\nGOOGLE SUPER-BOT GESTARTET!", "green")
            self.print_colored("=" * 50, "cyan")
            
            while self.running:
                counter += 1
                
                if iterations and counter > iterations:
                    self.print_colored(f"Erreichte maximale Anzahl von {iterations} Iterationen.", "green")
                    break
                
                self.print_colored(f"\n=== ITERATION {counter} ===", "yellow")
                
                if not self.open_google():
                    self.adaptive_delay(5, 10) 
                    continue
                
               
                search_term = self.get_smart_search_term(search_terms, counter)
                
                
                if not self.search_google(search_term):
                    self.adaptive_delay(3, 7)
                    continue
                
                wait_time = self.adaptive_delay(delay_range[0], delay_range[1])
                
                if counter % 10 == 0:
                    extra_wait = random.uniform(10, 20)
                    self.print_colored(f"Längere Pause für Realismus: {extra_wait:.1f}s", "purple")
                    time.sleep(extra_wait)
                
        except KeyboardInterrupt:
            self.print_colored("\nBot durch Benutzer gestoppt (Ctrl+C)", "yellow")
        except Exception as e:
            self.print_colored(f"Unerwarteter Fehler: {e}", "red")
            self.stats["errors"].append(f"Hauptschleife: {e}")
        finally:
            self.running = False
            self.close()
    
    def get_smart_search_term(self, search_terms, iteration):
        """Wählt intelligente Suchbegriffe basierend auf der Iteration"""
        if iteration <= 5:
            return random.choice(search_terms[:5])
        elif iteration % 7 == 0:
            special_terms = ["How to use Google", "Google tips", "Google tricks"]
            return random.choice(special_terms)
        else:
            return random.choice(search_terms)
    
    def adaptive_delay(self, min_delay, max_delay):
        """Adaptive Wartezeit basierend auf Performance"""
        base_wait = random.uniform(min_delay, max_delay)
        
        error_count = len(self.stats["errors"])
        if error_count > 5:
            base_wait *= 1.5
            self.print_colored(" Erhöhte Wartezeit wegen Fehlern", "yellow")

        self.print_colored(f" Warte {base_wait:.1f} Sekunden...", "cyan")
        time.sleep(base_wait)
        return base_wait
    
    def live_stats_display(self):
        """Zeigt Live-Statistiken an"""
        while self.running:
            time.sleep(30)
            if self.running:
                self.print_stats()
    
    def print_stats(self):
        """Druckt ausführliche Statistiken"""
        runtime = datetime.now() - self.stats["start_time"]
        success_rate = (self.stats["successful_searches"] / max(self.stats["total_searches"], 1)) * 100
        
        self.print_colored("\n === LIVE STATISTIKEN === ", "green")
        self.print_colored(f" Laufzeit: {str(runtime).split('.')[0]}", "cyan")
        self.print_colored(f" Gesamte Suchen: {self.stats['total_searches']}", "blue")
        self.print_colored(f" Erfolgreiche Suchen: {self.stats['successful_searches']}", "green")
        self.print_colored(f" Erfolgsrate: {success_rate:.1f}%", "purple")
        self.print_colored(f" Fehler: {len(self.stats['errors'])}", "red")
        
        if self.stats["total_searches"] > 0:
            searches_per_minute = self.stats["total_searches"] / (runtime.total_seconds() / 60)
            self.print_colored(f" Suchen/Minute: {searches_per_minute:.1f}", "yellow")

        self.print_colored("=" * 40, "cyan")
    
    def close(self):
        """Schließt den WebDriver und zeigt finale Statistiken"""
        self.running = False
        
        if self.driver:
            try:
                self.driver.quit()
                self.print_colored(" WebDriver erfolgreich geschlossen!", "green")
            except:
                self.print_colored(" WebDriver-Schließung mit Problemen", "yellow")

        self.print_colored("\n === FINALE STATISTIKEN === ", "green")
        self.print_stats()
        
        self.save_stats_to_file()
    
    def save_stats_to_file(self):
        """Speichert die Statistiken in eine Datei"""
        try:
            stats_data = {
                "session_end": datetime.now().isoformat(),
                "total_runtime": str(datetime.now() - self.stats["start_time"]),
                "stats": self.stats.copy()
            }
            
            stats_data["stats"]["start_time"] = self.stats["start_time"].isoformat()
            
            filename = f"googler_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, ensure_ascii=False)
            
            self.print_colored(f" Statistiken gespeichert: {filename}", "cyan")
            
        except Exception as e:
            self.print_colored(f" Fehler beim Speichern der Stats: {e}", "yellow")

    def emergency_stop(self):
        """Notfall-Stopp für den Bot"""
        self.running = False
        self.print_colored("NOTFALL-STOPP AKTIVIERT!", "red")
        self.close()

def main():
    """Haupt-Funktion mit interaktivem Menü"""
    print("=" * 50)
    print("        GOOGLE SUPER-BOT V2.0         ")
    print("=" * 50)
    print("Features:")
    print("Stealth-Mode mit Anti-Detection")
    print("Intelligente Suchbegriff-Rotation")
    print("Menschliche Interaktions-Simulation")
    print("Live-Statistiken & Analytics")
    print("Screenshot-Funktion")
    print("JSON-Konfiguration")
    print("Bunte Konsolen-Ausgabe")
    print("\nDrücke Ctrl+C um den Bot zu stoppen\n")
    
    print("Wähle deinen Modus:")
    print("1. Standard-Modus (empfohlen)")
    print("2. Turbo-Modus (schnell)")
    print("3. Stealth-Modus (langsam & sicher)")
    print("4. Custom-Modus (eigene Einstellungen)")
    print("5. Config-Datei bearbeiten")
    
    try:
        choice = input("\nDeine Wahl (1-5): ").strip()
        
        if choice == "5":
            show_config_editor()
            return
        
        bot = GoogleSelfBot()
        
        if not bot.driver:
            print("Bot konnte nicht gestartet werden!")
            return
        
        if choice == "1": 
            bot.run_loop(iterations=None, delay_range=(3, 6))
        elif choice == "2": 
            bot.config["delay_range"] = [1, 2]
            bot.config["enable_scrolling"] = False
            bot.config["enable_clicks"] = False
            bot.run_loop(iterations=None, delay_range=(1, 2))
        elif choice == "3":  
            bot.config["delay_range"] = [8, 15]
            bot.config["enable_scrolling"] = True
            bot.config["enable_clicks"] = True
            bot.run_loop(iterations=None, delay_range=(8, 15))
        elif choice == "4": 
            custom_setup(bot)
        else:
            bot.run_loop()
            
    except KeyboardInterrupt:
        print("\nAuf Wiedersehen!")
    except Exception as e:
        print(f"Fehler: {e}")

def show_config_editor():
    """Zeigt die Config-Datei zum Bearbeiten an"""
    config_file = "googler_config.json"
    if os.path.exists(config_file):
        print(f"\nConfig-Datei: {config_file}")
        with open(config_file, 'r', encoding='utf-8') as f:
            print(f.read())
        
        print("\nDu kannst diese Datei mit einem Texteditor bearbeiten.")
        print("   Starte den Bot dann erneut.")
    else:
        print("Config-Datei nicht gefunden. Starte den Bot einmal, um sie zu erstellen.")

def custom_setup(bot):
    """Benutzerdefinierte Einstellungen"""
    try:
        print("\nCUSTOM SETUP")
        
        iterations = input("Anzahl Iterationen (leer = unendlich): ").strip()
        iterations = int(iterations) if iterations else None
        
        min_delay = float(input("Minimale Wartezeit (Sekunden): ") or "2")
        max_delay = float(input("Maximale Wartezeit (Sekunden): ") or "5")
        
        enable_screenshots = input("Screenshots aktivieren? (j/n): ").lower().startswith('j')
        bot.config["save_screenshots"] = enable_screenshots
        
        print(f"\nSetup abgeschlossen!")
        print(f"   Iterationen: {iterations or 'Unendlich'}")
        print(f"   Wartezeit: {min_delay}-{max_delay}s")
        print(f"   Screenshots: {'Ja' if enable_screenshots else 'Nein'}")
        
        input("\nDrücke Enter um zu starten...")
        bot.run_loop(iterations=iterations, delay_range=(min_delay, max_delay))
        
    except ValueError:
        print("Ungültige Eingabe! Verwende Standard-Einstellungen.")
        bot.run_loop()

if __name__ == "__main__":
    main()