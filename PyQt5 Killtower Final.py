import sys
import requests, json
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QWidget, QHeaderView
from PyQt5.QtGui import QColor, QBrush, QIcon, QPalette, QPixmap
from PyQt5.QtCore import QTimer, Qt

class KillTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setStyleSheet("background-image: url(PATH TO PHOTOS//transparency.png); background:transparent;")
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.update_data()
        # Set the font for the application
        font = QtGui.QFont("Bebas Neue", 16)
        app = QApplication.instance()
        app.setFont(font)
        padding = 2  # set the padding to 2 pixels
        self.table.setMinimumHeight(self.table.verticalHeader().length() + padding)
        self.table.setMinimumWidth(self.table.horizontalHeader().length() + 10)
        self.table.setMaximumWidth(self.table.width())
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        # Disable automatic resizing of the table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Set the size of the table based on the content
        self.table.setFixedSize(self.table.horizontalHeader().length() + padding, self.table.verticalHeader().length() + padding)
        self.setCentralWidget(self.table)
        self.setWindowTitle("KillTower")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.last_update_times = {}
        self.table.setShowGrid(False)

        #no window just frame
        #self.setWindowFlags(Qt.FramelessWindowHint)


    def update_data(self):
        # take data from local mockup file
#        with open("PATH TO LOCAL FILE//MOCK_DATA.json", "r") as f:
#            self.data = json.load(f)
#       players = self.data["allinfo"]["TotalPlayerList"]

        #take data from url
        url = "URL GOES HERE"
        response = requests.get(url)
        self.data = response.json()
        players = self.data["allinfo"]["TotalPlayerList"]

        teams = {}
        for player in players:
            if player["teamName"] not in teams:
                teams[player["teamName"]] = {
                    "logo": f"PATH TO LOGOS//{player['teamName']}.png",
                    "liveState": [],
                }
            teams[player["teamName"]]["liveState"].append(player["liveState"])

            # Check if the "timestamp" key exists in the player dictionary
            if "timestamp" in player:
                self.last_update_times[player["playerName"]] = player["timestamp"]

        teams_sorted = sorted(teams.items(),key=lambda x: len([p for p in x[1]["liveState"] if p in [0, 1, 2, 3]]),reverse=True,)


        self.table.setRowCount(len(teams_sorted))
        for i, (team_name, team_data) in enumerate(teams_sorted):
            logo_label = QLabel()
            logo_pixmap = QPixmap(team_data["logo"]).scaledToHeight(30)
            logo_label.setPixmap(logo_pixmap)
            self.table.setCellWidget(i, 0, logo_label)

            team_name_item = QTableWidgetItem(str(team_name))
            self.table.setItem(i, 1, team_name_item)

            live_state_widget = QWidget()
            live_state_widget.setLayout(QHBoxLayout())

            for live_state in team_data["liveState"]:
                if live_state == 0 or live_state == 1 or live_state == 2 or live_state == 3:
                    icon = QIcon("PATH TO IMAGES//alive.png")
                elif live_state == 4:
                    icon = QIcon("PATH TO IMAGES//knock.png")
                else:
                    icon = QIcon("PATH TO IMAGES//dead.png")

                player_icon = QIcon(icon)
                player_label = QLabel()
                player_label.setPixmap(player_icon.pixmap(25, 25))
                live_state_widget.layout().addWidget(player_label)

            self.table.setCellWidget(i, 2, live_state_widget)

        self.table.setRowCount(len(teams_sorted))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KillTracker()
    window.show()
    sys.exit(app.exec_())
