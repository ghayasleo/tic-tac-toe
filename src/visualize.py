import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pylab as pylab

class Figure:
  def __init__(self, csv_url: str, img_url: str) -> None:
    self.csv = csv_url
    self.img = img_url
    self.palette = "rocket"

  def create_figure(self):
    self.df = pd.read_csv(self.csv)

    # plt.figure(figsize=(10, 8))

    # plt.subplot(2, 2, 1)
    # self.bar_chart()

    # plt.subplot(2, 2, 2)
    # self.pie_chart()

    # plt.subplot(2, 2, (3, 4))
    # self.heatmap()

    # Adjust layout for better spacing
    # plt.tight_layout()
    # self.show_fig()

    self.bar_chart("./src/assets/img/wins.png")
    self.pie_chart("./src/assets/img/first-move.png")
    self.heatmap("./src/assets/img/head-to-head.png")

  # 1. Bar chart of wins by each player
  def bar_chart(self, img = ""):
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 5))
    win_counts = self.df['winner'].value_counts()
    sns.barplot(x=win_counts.index, y=win_counts.values, palette=self.palette, hue=win_counts.index)
    plt.title('Number of Wins by Each Player')
    plt.xlabel('Player')
    plt.ylabel('Number of Wins')
    # plt.tight_layout()
    self.save_fig(img)
    # self.show_fig()

  # 2. Pie chart of first moves distribution
  def pie_chart(self, img = ""):
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 5))
    first_move_counts = self.df['first_move'].value_counts()
    plt.pie(first_move_counts, labels=first_move_counts.index, autopct='%1.1f%%', colors=sns.color_palette(self.palette, len(first_move_counts)))
    plt.title('Distribution of First Moves')
    # plt.tight_layout()
    self.save_fig(img)
    # self.show_fig()

  # 3. Heatmap of head-to-head wins
  def heatmap(self, img = ""):
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 5))
    head_to_head = pd.crosstab(self.df['first_move'], self.df['second_move'], values=self.df['winner'] == self.df['first_move'], aggfunc='sum', normalize='index')
    sns.heatmap(head_to_head, annot=True, cmap=self.palette, cbar_kws={'label': 'Win Rate'})
    plt.title('Head-to-Head Win Rates')
    plt.xlabel('Player Two')
    plt.ylabel('Player One')
    # plt.tight_layout()
    self.save_fig(img)
    # self.show_fig()

  def save_fig(self, img):
    plt.savefig(img)

  def show_fig(self):
    plt.show()

dataset = "src/assets/dataset.csv"
img_url = "./src/assets/img/plot.png"
figure = Figure(dataset, img_url)
figure.create_figure()