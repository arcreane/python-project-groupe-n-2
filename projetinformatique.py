import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random


fenetre = None
frame_principal = None
zone_jeu = None
zone_statut = None
label_score = None
label_temps = None
label_meilleur_score = None
progression = None
parties_sauvegardees = {}
meilleur_score = 0



questions = [
    {"question": "Quel est le nom du vaisseau spatial de Han Solo ?",
     "reponses": ["Faucon Millenium", "Étoile Noire", "Destroyer Stellaire", "X-Wing"],
     "correcte": 0, "difficulte": 1},
    {"question": "Qui est le père de Luke Skywalker ?",
     "reponses": ["Obi-Wan Kenobi", "Darth Vader", "Yoda", "Boba Fett"],
     "correcte": 1, "difficulte": 2},
    {"question": "Quel robot de Star Wars communique uniquement par bips ?",
     "reponses": ["C-3PO", "BB-8", "R2-D2", "IG-11"],
     "correcte": 2, "difficulte": 1},
    {"question": "Quelle planète est connue pour être le lieu de naissance de la Princesse Leia ?",
     "reponses": ["Tatooine", "Alderaan", "Naboo", "Hoth"],
     "correcte": 1, "difficulte": 3},
    {"question": "Quel est le nom du chasseur de Darth Vader ?",
     "reponses": ["Dark Vador", "Darth Sidious", "Darth Maul", "Darth Plagueis"],
     "correcte": 0, "difficulte": 2},
    {"question": "Quel est le nom du virus qui a compromis les systèmes ?",
     "reponses": ["DarkShadow", "CyberStorm", "BlackOut", "DigitalPlague"],
     "correcte": 0, "difficulte": 4},
    {"question": "Quel est le mot de passe administrateur ?",
     "reponses": ["admin123", "blackoutcity", "cyberpunk90", "darknet404"],
     "correcte": 1, "difficulte": 5}
]

sequences_coffre = [
    {'sequence': [2, 4, 8, 16], 'reponse': 32, 'regle': 'Doublement des nombres'},
    {'sequence': [3, 6, 11, 18], 'reponse': 27, 'regle': 'Différence croissante (+3, +5, +7, ...)'},
    {'sequence': [1, 2, 4, 8], 'reponse': 16, 'regle': 'Doublement des nombres'},
    {'sequence': [2, 6, 12, 20], 'reponse': 30, 'regle': 'Différence croissante (+4, +6, +8, ...)'},
    {'sequence': [1, 3, 6, 10], 'reponse': 15, 'regle': 'Somme des nombres de 1 à n'},
    {'sequence': [4, 9, 16, 25], 'reponse': 36, 'regle': 'Carrés des nombres'},
    {'sequence': [1, 4, 9, 16], 'reponse': 25, 'regle': 'Carrés des nombres'},
    {'sequence': [2, 6, 12, 20], 'reponse': 30, 'regle': 'Différence croissante (+4, +6, +8, ...)'},
    {'sequence': [1, 2, 4, 7], 'reponse': 11, 'regle': 'Fibonacci modifié'},
    {'sequence': [3, 5, 8, 12], 'reponse': 17, 'regle': 'Différence croissante (+2, +3, +4, ...)'}
]

codes_ascenseur = [
    '7462', '938271', '842135', '219874', '463728',
    '982134', '753219', '627384', '198473', '742935',
    '842135', '219874', '463728', '982134', '753219'
]


def initialiser_jeu():
    global fenetre, frame_principal, zone_jeu, zone_statut, label_score, label_temps, label_meilleur_score, progression
    global parties_sauvegardees, meilleur_score

    fenetre = tk.Tk()
    fenetre.title("BLACKOUT CITY - Escape Game")
    fenetre.geometry("800x600")
    fenetre.configure(bg='#000000')

    style = ttk.Style()
    style.configure('Cyber.TFrame', background='#000000')
    style.configure('Cyber.TLabel', background='#000000', foreground='#00ff00')
    style.configure('Cyber.TButton', background='#1a1a1a', foreground='#00ff00')
    style.configure('Cyber.TEntry', background='#1a1a1a', foreground='#00ff00')

    progression = {
        'niveau_actuel': 1,
        'manche_actuelle': 1,
        'questions_restantes': 5,
        'reponses_correctes': 0,
        'score': 0,
        'temps_restant': 300,
        'nom_partie': ''
    }

    try:
        with open('parties_sauvegardees.json', 'r') as f:
            parties_sauvegardees = json.load(f)
    except FileNotFoundError:
        parties_sauvegardees = {}

    try:
        with open('meilleur_score.json', 'r') as f:
            meilleur_score = json.load(f)
    except FileNotFoundError:
        meilleur_score = 0

    frame_principal = ttk.Frame(fenetre, style='Cyber.TFrame')
    frame_principal.pack(fill='both', expand=True)

    zone_jeu = ttk.Frame(frame_principal, style='Cyber.TFrame')
    zone_jeu.pack(fill='both', expand=True, padx=10, pady=5)

    zone_statut = ttk.Frame(frame_principal, style='Cyber.TFrame')
    zone_statut.pack(fill='x', padx=10, pady=5)
    label_score = ttk.Label(zone_statut, text="Score: 0", style='Cyber.TLabel')
    label_score.pack(side='left', padx=5)
    label_temps = ttk.Label(zone_statut, text="Temps: 5:00", style='Cyber.TLabel')
    label_temps.pack(side='right', padx=5)
    label_meilleur_score = ttk.Label(zone_statut, text=f"Meilleur Score: {meilleur_score}", style='Cyber.TLabel')
    label_meilleur_score.pack(side='left', padx=5)
    demarrer_compteur()
    afficher_intro()


def afficher_intro():
    for widget in zone_jeu.winfo_children():
        widget.destroy()
    messages = [
        "Une nuit comme les autres...",
        "jusqu'à ce que tout s'éteigne.",
        "Plongé dans le noir après une cyberattaque massive,",
        "vous vous réveillez seul dans un immeuble high-tech",
        "dont tous les systèmes sont verrouillés.",
        "Un mystérieux hacker a coupé l'électricité."
    ]
    for ligne in messages:
        ttk.Label(zone_jeu, text=ligne, style='Cyber.TLabel', font=('Courier', 16)).pack(pady=5)
    ttk.Button(zone_jeu, text="Commencer l'aventure", style='Cyber.TButton',
               command=afficher_menu_principal).pack(pady=20)
    afficher_bouton_retour()


def afficher_menu_principal():
    for widget in zone_jeu.winfo_children():


        widget.destroy()
    ttk.Label(zone_jeu, text="BLACKOUT CITY", style='Cyber.TLabel',
              font=('Arial', 24)).pack(pady=20)
    if parties_sauvegardees:
        ttk.Label(zone_jeu, text="Parties Sauvegardées:",
                  style='Cyber.TLabel').pack(pady=10)
        for nom_partie in parties_sauvegardees:
            partie = parties_sauvegardees[nom_partie]
            ttk.Button(zone_jeu,
                       text=f"Continuer: {nom_partie} (Niveau {partie['niveau_actuel']}, Score: {partie['score']})",
                       style='Cyber.TButton',
                       command=lambda p=nom_partie: charger_partie(p)).pack(pady=5)
    ttk.Button(zone_jeu, text="Nouvelle Partie", style='Cyber.TButton',
               command=nouvelle_partie).pack(pady=10)
    ttk.Button(zone_jeu, text="Quitter", style='Cyber.TButton',
               command=fenetre.quit).pack(pady=10)


def afficher_bouton_retour():
    global bouton_retour
    if 'bouton_retour' in globals():
        bouton_retour.destroy()
    bouton_retour = ttk.Button(zone_jeu,
                               text="Accueil",
                               style='Cyber.TButton',
                               command=afficher_menu_principal)
    bouton_retour.pack(pady=10)


def mettre_a_jour_score():
    global label_score, meilleur_score
    label_score.config(text=f"Score: {progression['score']}")
    if progression['score'] > 1000:
        label_score.configure(foreground='#ff3333')
    else:
        label_score.configure(foreground='#00ff00')
    if progression['score'] > meilleur_score:
        meilleur_score = progression['score']
        with open('meilleur_score.json', 'w') as f:
            json.dump(meilleur_score, f)
        label_meilleur_score.config(text=f"Meilleur Score: {meilleur_score}")


def demarrer_compteur():
    def mettre_a_jour():
        global progression
        if progression['temps_restant'] > 0:
            minutes = progression['temps_restant'] // 60
            secondes = progression['temps_restant'] % 60
            label_temps.config(text=f"Temps: {minutes}:{secondes:02d}")
            progression['temps_restant'] -= 1
            fenetre.after(1000, mettre_a_jour)
        else:
            game_over()

    mettre_a_jour()

def game_over():
    messagebox.showinfo("Game Over",
                        f"Temps écoulé! Score: {progression['score']}")
    mettre_a_jour_score()
    fenetre.quit()
def afficher_niveau_actuel():
    global progression
    for widget in zone_jeu.winfo_children():
        widget.destroy()

    if progression['niveau_actuel'] <= 4:
        if progression['niveau_actuel'] == 1:
            jeu_wifi()
        elif progression['niveau_actuel'] == 2:
            jeu_coffre()
        elif progression['niveau_actuel'] == 3:
            jeu_ascenseur()
        elif progression['niveau_actuel'] == 4:
            jeu_wifi_difficile()
        elif progression['niveau_actuel'] == 5:
            jeu_coffre_avance()
        elif progression['niveau_actuel'] == 6:
            jeu_ascenseur_expert()
        elif progression['niveau_actuel'] == 7:
            jeu_final()
        elif progression['niveau_actuel'] == 8:
            jeu_puzzle_connexion()
    else:
        victoire()


def jeu_wifi():
    global progression
    question = random.choice(questions)
    ttk.Label(zone_jeu, text="🔒 Rétablir le Wi-Fi", style='Cyber.TLabel',
              font=('Arial', 16)).pack(pady=10)
    ttk.Label(zone_jeu, text=f"Question {6 - progression['questions_restantes']}/5",
              style='Cyber.TLabel').pack(pady=5)
    ttk.Label(zone_jeu, text=f"Réponses correctes: {progression['reponses_correctes']}/3",
              style='Cyber.TLabel').pack(pady=5)
    ttk.Label(zone_jeu, text=question['question'], style='Cyber.TLabel',
              wraplength=600).pack(pady=10)
    for reponse in question['reponses']:
        ttk.Button(zone_jeu, text=reponse, style='Cyber.TButton',
                   command=lambda r=reponse, q=question: verifier_reponse_wifi(r, q)).pack(pady=5)
    afficher_bouton_retour()


def verifier_reponse_wifi(reponse, question):
    global progression
    progression['questions_restantes'] -= 1
    if reponse == question['reponses'][question['correcte']]:
        bonus = 20 * progression['niveau_actuel']
        progression['score'] += bonus
        progression['reponses_correctes'] += 1
        messagebox.showinfo("Succès!", f"Réponse correcte! +{bonus} points!")
        mettre_a_jour_score()
        sauvegarder_partie_automatique()
    else:
        messagebox.showinfo("Échec", "Réponse incorrecte!")
    if progression['questions_restantes'] > 0:
        afficher_niveau_actuel()
    else:
        if progression['reponses_correctes'] >= 3:
            progression['niveau_actuel'] += 1
            progression['questions_restantes'] = 5
            progression['reponses_correctes'] = 0
            afficher_niveau_actuel()
        else:
            messagebox.showinfo("Échec",
                                "Vous n'avez pas obtenu assez de bonnes réponses. Recommencez!")
            progression['questions_restantes'] = 5
            progression['reponses_correctes'] = 0
            afficher_niveau_actuel()


def jeu_coffre():
    global progression, entree_reponse
    sequence = random.choice(sequences_coffre)
    ttk.Label(zone_jeu, text="🔐 Pirater le coffre", style='Cyber.TLabel',
              font=('Arial', 16)).pack(pady=10)
    ttk.Label(zone_jeu, text=f"Question {6 - progression['questions_restantes']}/5",
              style='Cyber.TLabel').pack(pady=5)
    ttk.Label(zone_jeu, text=f"Réponses correctes: {progression['reponses_correctes']}/3",
              style='Cyber.TLabel').pack(pady=5)
    ttk.Label(zone_jeu, text=f"Séquence: {' '.join(map(str, sequence['sequence']))}",
              style='Cyber.TLabel').pack(pady=10)
    ttk.Label(zone_jeu, text=f"Regle: {sequence.get('regle', 'Pas de règle spécifique')}", style='Cyber.TLabel').pack(
        pady=10)
    entree_reponse = ttk.Entry(zone_jeu, style='Cyber.TEntry')
    entree_reponse.pack(pady=10)
    ttk.Button(zone_jeu, text="Vérifier", style='Cyber.TButton',
               command=lambda: verifier_sequence(sequence, entree_reponse)).pack(pady=5)
    afficher_bouton_retour()


def verifier_sequence(sequence, entree_reponse):
    global progression
    reponse_utilisateur = entree_reponse.get().strip()
    if not reponse_utilisateur.isdigit():
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide!")
        afficher_niveau_actuel()
        return

    try:
        reponse = int(reponse_utilisateur)
        progression['questions_restantes'] -= 1
        if reponse == sequence['reponse']:
            bonus = 20 * progression['niveau_actuel']
            progression['score'] += bonus
            progression['reponses_correctes'] += 1
            messagebox.showinfo("Succès!", f"Séquence correcte! +{bonus} points!")
            mettre_a_jour_score()
            sauvegarder_partie_automatique()
        else:
            messagebox.showinfo("Échec", "Séquence incorrecte!")

        if progression['questions_restantes'] > 0:
            afficher_niveau_actuel()
        else:
            if progression['reponses_correctes'] >= 3:
                progression['niveau_actuel'] += 1
                progression['questions_restantes'] = 5
                progression['reponses_correctes'] = 0
                afficher_niveau_actuel()
            else:
                messagebox.showinfo("Échec",
                                    "Vous n'avez pas obtenu assez de bonnes réponses. Recommencez!")
                progression['questions_restantes'] = 5
                progression['reponses_correctes'] = 0
                afficher_niveau_actuel()
    except Exception as e:
        messagebox.showerror("Erreur inattendue", f"Une erreur s'est produite : {e}")
        afficher_niveau_actuel()


def jeu_ascenseur():
    global progression, entree_code
    code = random.choice(codes_ascenseur)
    ttk.Label(zone_jeu, text="🚨 Déverrouiller l'ascenseur", style='Cyber.TLabel',
              font=('Arial', 16)).pack(pady=10)
    ttk.Label(zone_jeu, text=f"Question {6 - progression['questions_restantes']}/5",
              style='Cyber.TLabel').pack(pady=5)
    ttk.Label(zone_jeu, text=f"Réponses correctes: {progression['reponses_correctes']}/3",
              style='Cyber.TLabel').pack(pady=5)
    afficher_code_distordu(code)
    entree_code = ttk.Entry(zone_jeu, style='Cyber.TEntry')
    entree_code.pack(pady=10)
    ttk.Button(zone_jeu, text="Vérifier", style='Cyber.TButton',
               command=lambda: verifier_code(code, entree_code)).pack(pady=5)
    afficher_bouton_retour()


def afficher_code_distordu(code):
    couleurs = ['#33ff33', '#66ff66', '#99ff99', '#ff3333', '#ff6666']
    vitesse = 1
    tremblement = [0, 3,-4, 2, 0, -3, 2, 1, 4, -2]
    label_code = ttk.Label(
        zone_jeu,
        text=code,
        style='Cyber.TLabel',
        font=('Arial', 24),
        foreground='#33ff33'
    )

    def appliquer_effet():
        def changer():
            label_code.configure(
                foreground=random.choice(couleurs),
                padding=(random.choice(tremblement), random.choice(tremblement))
            )
            fenetre.after(vitesse, changer)

        changer()

    appliquer_effet()
    label_code.pack(pady=10)
    fenetre.after(3000, lambda: label_code.pack_forget())


def verifier_code(code_attendu, entree_code):
    global progression
    code_saisi = entree_code.get()
    progression['questions_restantes'] -= 1
    if code_saisi == code_attendu:
        bonus = 20 * progression['niveau_actuel']
        progression['score'] += bonus
        progression['reponses_correctes'] += 1
        messagebox.showinfo("Succès!", f"Code correct! +{bonus} points!")
        mettre_a_jour_score()
        sauvegarder_partie_automatique()
    else:
        messagebox.showinfo("Échec", "Code incorrect!")
    if progression['questions_restantes'] > 0:
        afficher_niveau_actuel()
    else:
        if progression['reponses_correctes'] >= 3:
            progression['niveau_actuel'] += 1
            progression['questions_restantes'] = 5
            progression['reponses_correctes'] = 0
            afficher_niveau_actuel()
        else:
            messagebox.showinfo("Échec",
                                "Vous n'avez pas obtenu assez de bonnes réponses. Recommencez!")
            progression['questions_restantes'] = 5
            progression['reponses_correctes'] = 0
            afficher_niveau_actuel()

def victoire():
    messagebox.showinfo("Victoire!",
                        f"Félicitations! Vous avez réussi à pirater tous les systèmes avec un score de {progression['score']}!")
    mettre_a_jour_score()
    fenetre.quit()


def nouvelle_partie():
    global progression
    nom_partie = simpledialog.askstring("Nouvelle Partie",
                                        "Entrez un nom pour votre nouvelle partie:")
    if nom_partie and nom_partie not in parties_sauvegardees:
        progression = {
            'niveau_actuel': 1,
            'manche_actuelle': 1,
            'questions_restantes': 5,
            'reponses_correctes': 0,
            'score': 0,
            'temps_restant': 300,
            'nom_partie': nom_partie
        }
        sauvegarder_partie()  # Sauvegarde immédiate
        afficher_niveau_actuel()


def charger_partie(nom_partie):
    global progression
    if nom_partie in parties_sauvegardees:
        progression = parties_sauvegardees[nom_partie].copy()
        progression['temps_restant'] = 300  # Temps par défaut
        mettre_a_jour_score()
        afficher_niveau_actuel()
    else:
        messagebox.showerror("Erreur", "Impossible de charger cette partie")


def sauvegarder_partie():
    global progression, parties_sauvegardees
    if not progression['nom_partie']:
        progression['nom_partie'] = simpledialog.askstring(
            "Nom de la partie",
            "Entrez un nom pour votre partie:"
        )
    if progression['nom_partie']:
        parties_sauvegardees[progression['nom_partie']] = progression.copy()
        with open('parties_sauvegardees.json', 'w') as f:
            json.dump(parties_sauvegardees, f)
        messagebox.showinfo("Sauvegarde",
                            f"Partie sauvegardée avec succès sous le nom: {progression['nom_partie']}")


def sauvegarder_partie_automatique():
    global progression, parties_sauvegardees
    if progression['nom_partie']:
        parties_sauvegardees[progression['nom_partie']] = progression.copy()
        with open('parties_sauvegardees.json', 'w') as f:
            json.dump(parties_sauvegardees, f)


def demarrer():
    initialiser_jeu()
    fenetre.mainloop()


if __name__ == "__main__":
    demarrer()