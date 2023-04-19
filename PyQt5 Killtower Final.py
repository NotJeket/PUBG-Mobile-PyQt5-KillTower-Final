import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt, QTimer

class KillTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["TeamName", "Players"])

        self.setCentralWidget(self.table)
        self.setWindowTitle("Kill Tracker")
        self.setGeometry(100, 100, 400, 300)

        self.update_data()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        response = requests.get("http://127.0.0.1:5000/data1")
        teams = response.json()['allinfo']['TeamInfoList']
        teams_sorted = sorted(teams, key=lambda t: t["liveMemberNum"], reverse=True)

        self.table.setRowCount(len(teams_sorted))
        for i, team in enumerate(teams_sorted):
            team_name = QTableWidgetItem(str(team["teamName"]))
            self.table.setItem(i, 0, team_name)

            players = ""
            for j in range(team["liveMemberNum"]):
                players += "A "
            for j in range(4 - team["liveMemberNum"]):
                players += "D "
            players_item = QTableWidgetItem(players.strip())

            # Set background color based on player status
            if team["liveMemberNum"] == 0:
                players_item.setBackground(QBrush(QColor(255, 0, 0)))
            elif team["liveMemberNum"] == 4:
                players_item.setBackground(QBrush(QColor(0, 255, 0)))
            else:
                players_item.setBackground(QBrush(QColor(255, 255, 0)))

            self.table.setItem(i, 1, players_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KillTracker()
    window.show()
    sys.exit(app.exec_())
