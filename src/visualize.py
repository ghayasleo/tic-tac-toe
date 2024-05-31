import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Figure:
  def __init__(self, csv_url: str, img_url: str) -> None:
    self.csv = csv_url
    self.img = img_url

  def save_figure(self):
    self.df = pd.read_csv(self.csv)
    self.df["winner_was_first_mover"] = (self.df["winner"] == self.df["first_move"]).astype(int)

    # Count wins for each player from first move and second move
    wins_first_move = self.df[self.df["winner_was_first_mover"] == 1]["winner"].value_counts()
    wins_second_move = self.df[self.df["winner_was_first_mover"] == 0]["winner"].value_counts()
    # Create a new DataFrame with the counts
    df_wins = pd.DataFrame({"First Move": wins_first_move, "Second Move": wins_second_move})

    # Create a new matplotlib style sheet with a dark theme
    plt.style.use("dark_background")

    # Set the size of the figure
    plt.rcParams["figure.figsize"] = (8, 5)
    df_wins.plot(kind="bar")

    # Set the title and labels
    plt.title("Wins for each player from first and second move", color="white")
    plt.xlabel("Player", color="white")
    plt.ylabel("Wins", color="white")

    # Set the legend
    plt.legend(loc="upper left", facecolor="#333333")

    # Set the y-axis limits and ticks
    plt.ylim(0, int(np.ceil(df_wins.max().max())))
    plt.yticks(range(0, int(np.ceil(df_wins.max().max()) + 2), 1), color="white")
    plt.subplots_adjust(bottom=0.3)

    # Set the grid
    # plt.grid(True, linestyle=":", color="#555555")

    # Save the figure
    plt.savefig(self.img)
    # plt.show()
  
# dataset = "src/assets/dataset.csv"
# img_url = "./src/assets/img/plot.png"
# figure = Figure(dataset, img_url)
# figure.save_figure()