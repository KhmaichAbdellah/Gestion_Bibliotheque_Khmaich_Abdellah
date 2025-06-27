import json
import matplotlib.pyplot as plt
from collections import Counter
import csv
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib import dates as mdates

# Fonction utilitaire pour tronquer les noms trop longs
def truncate_labels(labels, max_len=15):
    return [label if len(label) <= max_len else label[:max_len-3] + '...' for label in labels]

# Couleurs et polices cohérentes
color_pie = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
color_bar = '#2a9d8f'
color_line = '#f4a261'
font_family = 'Segoe UI'

# 📊 1. Diagramme circulaire : % des livres par genre
def genre_pie_chart_figure():
    with open("data/livres.json", "r", encoding="utf-8") as f:
        livres = json.load(f)
    genres = [livre.get("genre", "Inconnu") for livre in livres.values()]
    genre_counts = Counter(genres)

    fig = Figure(figsize=(6, 6), facecolor='none')
    ax = fig.add_subplot(111)
    ax.pie(
        genre_counts.values(),
        labels=genre_counts.keys(),
        autopct='%1.1f%%',
        startangle=140,
        colors=color_pie,
        textprops={'fontsize': 11, 'fontname': font_family, 'color': "#e1e6e6"}
    )
    ax.set_title("Répartition des livres par genre", fontsize=16, fontweight='bold', fontname=font_family, color="#2CD0C0", pad=20)
    return fig

# 📊 2. Histogramme : Top 10 des auteurs
def top_auteurs_bar_figure():
    with open("data/livres.json", "r", encoding="utf-8") as f:
        livres = json.load(f)
    auteurs = [livre.get("auteur", "Inconnu") for livre in livres.values()]
    auteur_counts = Counter(auteurs).most_common(10)
    if auteur_counts:
        noms, nb = zip(*auteur_counts)
        noms = truncate_labels(noms, max_len=15)
    else:
        noms, nb = [], []

    fig, ax = plt.subplots(figsize=(10, 4), facecolor='none')
    ax.set_facecolor('none')

    ax.bar(noms, nb, color=color_bar)
    ax.set_xticks(range(len(noms)))  # Fixe les positions des ticks
    ax.set_xticklabels(noms, rotation=90, fontsize=10, fontname=font_family, color="#EFF3F4")


    ax.tick_params(axis='y', labelsize=10, labelcolor="#2B9DCA")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_title("Top 10 des auteurs les plus populaires", fontsize=16, fontweight='bold', fontname=font_family, color='#264653', pad=20)
    ax.set_ylabel("Nombre de livres", fontsize=12, fontname=font_family, color="#2B9DCA")
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    return fig

# 📊 3. Courbe d'activité : nombre d'emprunts sur les 30 derniers jours
def activite_emprunts_courbe_figure():
    dates = []
    with open("data/historique.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 4:
                continue
            date_str, _, _, action = row
            if action == "emprunt":
                try:
                    date_obj = datetime.fromisoformat(date_str)
                    if datetime.now() - date_obj <= timedelta(days=30):
                        dates.append(date_obj.date())
                except Exception:
                    continue

    date_counts = Counter(dates)
    jours = [datetime.now().date() - timedelta(days=i) for i in range(29, -1, -1)]
    valeurs = [date_counts.get(j, 0) for j in jours]

    fig, ax = plt.subplots(figsize=(12, 6), facecolor='none')
    ax.set_facecolor('none')

    ax.plot(jours, valeurs, marker='o', linestyle='-', color=color_line, linewidth=2)

    # ✅ Appliquer les styles cohérents
    ax.set_title("Emprunts - 30 derniers jours", fontsize=18, fontweight='bold', fontname=font_family, color="#27B3EB", pad=25)
    ax.set_xlabel("Date", fontsize=14, fontname=font_family, color='#264653')
    ax.set_ylabel("Nombre d'emprunts", fontsize=14, fontname=font_family, color='#264653')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    
    ax.set_xticks(jours)
    ax.tick_params(axis='x', labelrotation=90, labelsize=11, labelcolor="#F2F5F6")
    ax.tick_params(axis='y', labelsize=11, labelcolor="#F5F8FA")

    # ✅ Forcer les entiers uniquement sur l’axe Y
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.grid(True, linestyle='--', alpha=0.4)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    return fig
