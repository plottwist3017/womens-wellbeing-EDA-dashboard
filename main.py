import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
from matplotlib.widgets import Button
import matplotlib.ticker as ticker

# =========================================================
# WOMEN'S WELLBEING DASHBOARD
# =========================================================

# -----------------------------
# SET WORKING DIRECTORY
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# -----------------------------
# THEME (Soft Pink Aesthetic)
# -----------------------------
mpl.rcParams['font.family'] = 'Times New Roman'

mpl.rcParams['figure.facecolor'] = '#fdf7f9'
mpl.rcParams['axes.facecolor'] = '#ffffff'
mpl.rcParams['axes.edgecolor'] = '#e3c7cf'

mpl.rcParams['text.color'] = '#4a3a3d'
mpl.rcParams['axes.labelcolor'] = '#4a3a3d'
mpl.rcParams['xtick.color'] = '#4a3a3d'
mpl.rcParams['ytick.color'] = '#4a3a3d'

mpl.rcParams['grid.color'] = '#ead5db'
mpl.rcParams['grid.alpha'] = 0.5

# -----------------------------
# LOAD DATA
# -----------------------------
csv_path = os.path.join(BASE_DIR, "livwell.csv")
df = pd.read_csv(csv_path)

# -----------------------------
# VARIABLES
# -----------------------------
columns = {
    "Education Levels": "ED_educ_years_mean",
    "Financial Decision-Making Power": "DP_decide_money_p",
    "Mobile Phone Ownership": "EI_mobile_p",
    "Healthcare Insurance Access": "HL_health_insur_p",
    "Wealth Index": "WL_wealth_mean"
}

# X-axis meaning (IMPORTANT FOR STORYTELLING)
units = {
    "ED_educ_years_mean": "Average Years of Education",
    "DP_decide_money_p": "Women with Financial Decision-Making Power (%)",
    "EI_mobile_p": "Women Owning Mobile Phones (%)",
    "HL_health_insur_p": "Women with Health Insurance Access (%)",
    "WL_wealth_mean": "Wealth Index (Score)"
}

# Clean missing values
df = df.dropna(subset=columns.values())

sorted_columns = dict(sorted(columns.items()))

# =========================================================
# GRAPH FUNCTION
# =========================================================
def open_graph(column_name, graph_title):

    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram (soft pastel pink)
    ax.hist(
        df[column_name],
        bins=20,
        color="#f9c6d3",
        alpha=0.85,
        edgecolor="white"
    )

    # Title
    ax.set_title(
        graph_title,
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    # X-axis (with proper unit label)
    x_label = units.get(column_name, "Value")
    ax.set_xlabel(x_label, fontsize=13)

    # Y-axis
    ax.set_ylabel("Frequency (Number of Countries)", fontsize=13)

    # Fix decimal tick issue
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Grid
    ax.grid(alpha=0.3)

    # Stats
    mean_value = round(df[column_name].mean(), 2)
    median_value = round(df[column_name].median(), 2)

    stats_text = (
        f"Mean: {mean_value}\n"
        f"Median: {median_value}\n"
        f"Data Points: {len(df[column_name])}"
    )

    ax.text(
        0.97, 0.95,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(
            facecolor='#fff0f3',
            edgecolor='#e3c7cf',
            boxstyle='round,pad=0.5'
        )
    )
    
    plt.show()

# =========================================================
# DASHBOARD
# =========================================================
dashboard_fig = plt.figure(figsize=(11, 6))

background_ax = dashboard_fig.add_axes([0, 0, 1, 1])
background_ax.axis("off")

# TITLE
dashboard_fig.text(
    0.5, 0.92,
    "Women's Wellbeing Dashboard",
    ha="center",
    fontsize=24,
    fontweight="bold"
)

# INTRO
intro_text = (
    "This dashboard explores women's wellbeing across 52 countries.\n\n"
    "It analyzes education, healthcare access, financial empowerment, "
    "technology access, and wealth using the LivWell dataset.\n\n"
    "Click any button below to view a visualization."
)

dashboard_fig.text(
    0.5, 0.72,
    intro_text,
    ha="center",
    fontsize=12
)

# IMAGE (larger + centered)
try:
    img_path = os.path.join(BASE_DIR, "women.png")
    img = mpimg.imread(img_path)

    image_ax = dashboard_fig.add_axes([0.30, 0.25, 0.40, 0.40])
    image_ax.imshow(img)
    image_ax.axis("off")

except FileNotFoundError:
    print("women.png not found.")

# =========================================================
# BUTTONS
# =========================================================
button_positions = [
    [0.06, 0.12, 0.16, 0.08],
    [0.25, 0.12, 0.16, 0.08],
    [0.44, 0.12, 0.16, 0.08],
    [0.63, 0.12, 0.16, 0.08],
    [0.82, 0.12, 0.16, 0.08]
]

buttons = []

for (title, column), position in zip(sorted_columns.items(), button_positions):

    ax_button = plt.axes(position)

    button = Button(
        ax_button,
        title.replace(" ", "\n")
    )

    button.color = "#f3e3e8"
    button.hovercolor = "#e7d2d9"

    button.on_clicked(
        lambda event, col=column, t=title:
        open_graph(col, t)
    )

    buttons.append(button)

# FOOTER
dashboard_fig.text(
    0.5, 0.03,
    "EDA Project • Python • Pandas • Matplotlib",
    ha="center",
    fontsize=10,
    alpha=0.7
)

try:
    mngr = plt.get_current_fig_manager()
    mngr.window.wm_geometry("+150+80")
except:
    pass


# RUN
plt.show()