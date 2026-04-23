import customtkinter as ctk
import tkinter as tk
import random
import math

# Setup CustomTkinter styling
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# State
state = {
    "playerScore": 0,
    "cpuScore": 0,
    "round": 1
}

CHOICES = ['rock', 'paper', 'scissors']
EMOJIS = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
BEATS = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

# Modern Dark Theme Colors
BG_PRIMARY = "#121212"
BG_CARD = "#1e1e1e"
TEXT_PRIMARY = "#f3f4f6"
TEXT_SECONDARY = "#9ca3af"
WIN_COLOR = "#10b981"  # Neon Green
LOSE_COLOR = "#ef4444" # Neon Red
TIE_COLOR = "#f59e0b"  # Neon Orange
ACCENT = "#3b82f6"     # Modern Blue

class RPSModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors — Modern Arena")
        self.geometry("1000x750")
        self.resizable(False, False)
        
        self.particles = []
        self.anim_objects = []
        
        self.setup_ui()
        self.update_loop()

    def setup_ui(self):
        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # LEFT PANEL
        left_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # RIGHT PANEL (Logs)
        right_panel = ctk.CTkFrame(self.main_container, corner_radius=15)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        # --- Right Panel ---
        ctk.CTkLabel(right_panel, text="📜 BATTLE LOG", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=TEXT_SECONDARY).pack(pady=15)
        
        self.history_text = ctk.CTkTextbox(right_panel, width=300, font=ctk.CTkFont(family="Segoe UI", size=12), fg_color="#2b2b2b", corner_radius=10)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Setup tags for normal tk.Text methods (CTkTextbox wraps tk.Text)
        self.history_text.tag_config('win', foreground=WIN_COLOR)
        self.history_text.tag_config('lose', foreground=LOSE_COLOR)
        self.history_text.tag_config('tie', foreground=TIE_COLOR)
        self.history_text.tag_config('round', foreground=TEXT_SECONDARY)
        self.history_text.configure(state=tk.DISABLED)

        # --- Left Panel ---
        # Header
        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.pack(pady=5)
        ctk.CTkLabel(header_frame, text="⚔️", font=ctk.CTkFont(size=36)).pack(side=tk.LEFT, padx=10)
        ctk.CTkLabel(header_frame, text="Battle Arena", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color=TEXT_PRIMARY).pack(side=tk.LEFT)

        # Scoreboard
        score_frame = ctk.CTkFrame(left_panel, corner_radius=15)
        score_frame.pack(pady=10, fill=tk.X)
        
        # You
        p_frame = ctk.CTkFrame(score_frame, fg_color="transparent")
        p_frame.pack(side=tk.LEFT, expand=True, pady=15)
        ctk.CTkLabel(p_frame, text="YOU", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=TEXT_SECONDARY).pack()
        self.player_score_lbl = ctk.CTkLabel(p_frame, text="0", font=ctk.CTkFont(family="Segoe UI", size=48, weight="bold"), text_color=WIN_COLOR)
        self.player_score_lbl.pack()

        # VS / Round
        mid_frame = ctk.CTkFrame(score_frame, fg_color="transparent")
        mid_frame.pack(side=tk.LEFT, expand=True)
        ctk.CTkLabel(mid_frame, text="VS", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color=TEXT_SECONDARY).pack()
        self.round_lbl = ctk.CTkLabel(mid_frame, text="ROUND 1", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=ACCENT)
        self.round_lbl.pack()

        # CPU
        c_frame = ctk.CTkFrame(score_frame, fg_color="transparent")
        c_frame.pack(side=tk.LEFT, expand=True, pady=15)
        ctk.CTkLabel(c_frame, text="CPU", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=TEXT_SECONDARY).pack()
        self.cpu_score_lbl = ctk.CTkLabel(c_frame, text="0", font=ctk.CTkFont(family="Segoe UI", size=48, weight="bold"), text_color=LOSE_COLOR)
        self.cpu_score_lbl.pack()

        # Canvas Arena
        arena_bg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1] # Get dark mode card color
        self.arena = tk.Canvas(left_panel, width=540, height=300, bg=arena_bg, highlightthickness=0, bd=0)
        self.arena.pack(pady=15)
        
        # Soft border for canvas
        self.arena.create_rectangle(1, 1, 539, 299, outline="#333333", width=2)
        
        self.p_emoji_id = self.arena.create_text(130, 150, text="❓", font=("Segoe UI", 70))
        self.c_emoji_id = self.arena.create_text(410, 150, text="❓", font=("Segoe UI", 70))
        
        self.p_name_id = self.arena.create_text(130, 240, text="Your Choice", font=("Segoe UI", 14, "bold"), fill=TEXT_SECONDARY)
        self.c_name_id = self.arena.create_text(410, 240, text="CPU Choice", font=("Segoe UI", 14, "bold"), fill=TEXT_SECONDARY)
        
        self.result_id = self.arena.create_text(270, 45, text="Choose your weapon!", font=("Segoe UI", 18, "bold"), fill=TEXT_SECONDARY)

        # Ambient background particles
        for _ in range(15):
            self.spawn_particle(ambient=True)

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        btn_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        
        self.btn_rock = ctk.CTkButton(self.btn_frame, text="🪨\nROCK", font=btn_font, fg_color="#374151", hover_color="#4b5563", width=120, height=60, corner_radius=15, command=lambda: self.play("rock"))
        self.btn_rock.pack(side=tk.LEFT, padx=15)

        self.btn_paper = ctk.CTkButton(self.btn_frame, text="📄\nPAPER", font=btn_font, fg_color="#374151", hover_color="#4b5563", width=120, height=60, corner_radius=15, command=lambda: self.play("paper"))
        self.btn_paper.pack(side=tk.LEFT, padx=15)

        self.btn_scissors = ctk.CTkButton(self.btn_frame, text="✂️\nSCISSORS", font=btn_font, fg_color="#374151", hover_color="#4b5563", width=120, height=60, corner_radius=15, command=lambda: self.play("scissors"))
        self.btn_scissors.pack(side=tk.LEFT, padx=15)

        # Actions Frame
        self.actions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        
        self.btn_play_again = ctk.CTkButton(self.actions_frame, text="🔄 Play Again", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), fg_color=ACCENT, hover_color="#2563eb", corner_radius=10, height=40, command=self.play_again)
        self.btn_play_again.pack(side=tk.LEFT, padx=10)

        self.btn_reset = ctk.CTkButton(self.actions_frame, text="🗑️ Reset", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), fg_color="#4b5563", hover_color="#374151", corner_radius=10, height=40, command=self.reset_game)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

    def spawn_particle(self, ambient=False, x=None, y=None, color=None):
        if ambient:
            px = random.randint(0, 540)
            py = random.randint(0, 300)
            r = random.randint(2, 5)
            c = random.choice(["#333333", "#444444", "#222222"])
            dx = random.uniform(-0.4, 0.4)
            dy = random.uniform(-0.4, 0.4)
            life = 9999
        else:
            px = x + random.randint(-10, 10)
            py = y + random.randint(-10, 10)
            r = random.randint(4, 9)
            c = color
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            life = random.randint(20, 40)
            
        pid = self.arena.create_oval(px-r, py-r, px+r, py+r, fill=c, outline="")
        self.particles.append({"id": pid, "x": px, "y": py, "dx": dx, "dy": dy, "life": life, "ambient": ambient})

    def trigger_burst(self, color):
        for _ in range(40):
            self.spawn_particle(ambient=False, x=270, y=150, color=color)

    def update_loop(self):
        for p in self.particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            
            if p['ambient']:
                if p['x'] < 0 or p['x'] > 540: p['dx'] *= -1
                if p['y'] < 0 or p['y'] > 300: p['dy'] *= -1
            else:
                p['dy'] += 0.3 # Gravity
                p['life'] -= 1
                if p['life'] <= 0:
                    self.arena.delete(p['id'])
                    self.particles.remove(p)
                    continue
                    
            r = 3
            self.arena.coords(p['id'], p['x']-r, p['y']-r, p['x']+r, p['y']+r)
            
        for obj in self.anim_objects:
            if obj['type'] == 'bounce':
                obj['tick'] += 0.25
                dy = math.sin(obj['tick']) * 8
                self.arena.coords(obj['id'], obj['base_x'], obj['base_y'] + dy)
            elif obj['type'] == 'clash':
                curr_x, curr_y = self.arena.coords(obj['id'])
                dx = (obj['target_x'] - curr_x) * 0.12
                self.arena.coords(obj['id'], curr_x + dx, curr_y)
            elif obj['type'] == 'scale':
                obj['tick'] += 0.1
                if obj['tick'] <= 1.0:
                    size = int(70 + (obj['target_size'] - 70) * math.sin(obj['tick'] * math.pi / 2))
                    self.arena.itemconfigure(obj['id'], font=("Segoe UI", size))

        self.after(16, self.update_loop)

    def play(self, player_choice):
        self.btn_rock.configure(state="disabled")
        self.btn_paper.configure(state="disabled")
        self.btn_scissors.configure(state="disabled")
        self.actions_frame.pack_forget()

        self.arena.itemconfigure(self.p_emoji_id, text=EMOJIS[player_choice], font=("Segoe UI", 70))
        self.arena.itemconfigure(self.p_name_id, text=player_choice.upper())
        self.arena.coords(self.p_emoji_id, 130, 150)

        self.arena.itemconfigure(self.c_emoji_id, text="🎲", font=("Segoe UI", 70))
        self.arena.itemconfigure(self.c_name_id, text="...")
        self.arena.coords(self.c_emoji_id, 410, 150)
        
        self.arena.itemconfigure(self.result_id, text="CPU is thinking...", fill=TEXT_SECONDARY)

        self.anim_objects = [{"id": self.c_emoji_id, "type": "bounce", "tick": 0, "base_x": 410, "base_y": 150}]
        self.think_ticks = 0
        self.think_loop(player_choice)

    def think_loop(self, player_choice):
        self.think_ticks += 1
        self.arena.itemconfigure(self.c_emoji_id, text=random.choice(list(EMOJIS.values())))
        if self.think_ticks < 15:
            self.after(80, lambda: self.think_loop(player_choice))
        else:
            self.reveal_result(player_choice)

    def reveal_result(self, player_choice):
        cpu_choice = random.choice(CHOICES)

        self.arena.itemconfigure(self.c_emoji_id, text=EMOJIS[cpu_choice])
        self.arena.itemconfigure(self.c_name_id, text=cpu_choice.upper())

        self.anim_objects = [
            {"id": self.p_emoji_id, "type": "clash", "target_x": 210},
            {"id": self.c_emoji_id, "type": "clash", "target_x": 330}
        ]

        self.after(500, lambda: self.show_winner(player_choice, cpu_choice))

    def show_winner(self, player_choice, cpu_choice):
        if player_choice == cpu_choice:
            outcome = "tie"
        elif BEATS[player_choice] == cpu_choice:
            outcome = "win"
        else:
            outcome = "lose"

        self.anim_objects = []

        if outcome == "win":
            state["playerScore"] += 1
            msg = f"{player_choice.capitalize()} beats {cpu_choice} — YOU WIN! 🎉"
            col = WIN_COLOR
            self.anim_objects = [
                {"id": self.p_emoji_id, "type": "scale", "tick": 0, "target_size": 110},
                {"id": self.c_emoji_id, "type": "scale", "tick": 0, "target_size": 40}
            ]
            self.trigger_burst(WIN_COLOR)
        elif outcome == "lose":
            state["cpuScore"] += 1
            msg = f"{cpu_choice.capitalize()} beats {player_choice} — CPU WINS! 😞"
            col = LOSE_COLOR
            self.anim_objects = [
                {"id": self.c_emoji_id, "type": "scale", "tick": 0, "target_size": 110},
                {"id": self.p_emoji_id, "type": "scale", "tick": 0, "target_size": 40}
            ]
            self.trigger_burst(LOSE_COLOR)
        else:
            msg = "Great minds think alike! It's a TIE! 🤝"
            col = TIE_COLOR
            self.trigger_burst(TIE_COLOR)

        self.arena.itemconfigure(self.result_id, text=msg, fill=col)

        self.player_score_lbl.configure(text=str(state["playerScore"]))
        self.cpu_score_lbl.configure(text=str(state["cpuScore"]))
        
        self.add_history(player_choice, cpu_choice, outcome)
        
        state["round"] += 1
        self.round_lbl.configure(text=f"ROUND {state['round']}")

        self.actions_frame.pack(pady=15)

    def add_history(self, p, c, outcome):
        self.history_text.configure(state=tk.NORMAL)
        
        round_txt = f"Round {state['round']}\n"
        self.history_text.insert("1.0", round_txt, "round")
        
        if outcome == "win":
            res, tag = f"{EMOJIS[p]} beats {EMOJIS[c]} -> WIN\n\n", "win"
        elif outcome == "lose":
            res, tag = f"{EMOJIS[p]} loses to {EMOJIS[c]} -> LOSE\n\n", "lose"
        else:
            res, tag = f"{EMOJIS[p]} ties {EMOJIS[c]} -> TIE\n\n", "tie"
            
        self.history_text.insert("2.0", res, tag)
        self.history_text.configure(state=tk.DISABLED)

    def play_again(self):
        self.anim_objects = []
        self.arena.itemconfigure(self.p_emoji_id, text="❓", font=("Segoe UI", 70))
        self.arena.itemconfigure(self.c_emoji_id, text="❓", font=("Segoe UI", 70))
        self.arena.coords(self.p_emoji_id, 130, 150)
        self.arena.coords(self.c_emoji_id, 410, 150)
        
        self.arena.itemconfigure(self.p_name_id, text="Your Choice")
        self.arena.itemconfigure(self.c_name_id, text="CPU Choice")
        self.arena.itemconfigure(self.result_id, text="Choose your weapon!", fill=TEXT_SECONDARY)
        
        self.actions_frame.pack_forget()
        self.btn_rock.configure(state="normal")
        self.btn_paper.configure(state="normal")
        self.btn_scissors.configure(state="normal")

    def reset_game(self):
        state["playerScore"] = 0
        state["cpuScore"] = 0
        state["round"] = 1
        
        self.player_score_lbl.configure(text="0")
        self.cpu_score_lbl.configure(text="0")
        self.round_lbl.configure(text="ROUND 1")
        
        self.history_text.configure(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        self.history_text.configure(state=tk.DISABLED)
        
        self.play_again()

if __name__ == "__main__":
    app = RPSModernApp()
    app.mainloop()
