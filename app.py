import sys,os,csv,psutil,datetime,json,tzlocal

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QWidget, QGridLayout, QLabel, QTabWidget,QDialog,QLineEdit
from plyer.utils import platform
from plyer import notification
from datetime import datetime,timedelta
from apscheduler.schedulers.qt import QtScheduler

weekly_allowed_time = 7*60
daily_allowed_time = 2*60

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Time Mng')
        layout = QGridLayout()
        tabWidget = QTabWidget()
        tabWidget.addTab(TimerTab(), "Set timer")
        tabWidget.addTab(AddGameTab(),'AddGame')
        layout.addWidget(tabWidget)
        self.setLayout(layout)

class TimerTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QGridLayout()

        games_combo = QComboBox()
        with open('games', 'r', encoding='utf-8') as games_csv:
            games_reader = csv.reader(games_csv)
            for row in games_reader:
                games_combo.addItem(str(row).strip('[').strip(']').strip("'"))
        layout.addWidget(games_combo, 0, 0, 1, 3)
        
        
        set_timer_button = QPushButton(('Set Timer'),clicked = lambda: start_timer())
        layout.addWidget(set_timer_button, 2,0,1,1)

        timer_line = QLineEdit()
        timer_line.setPlaceholderText("Введите время в минутах")
        layout.addWidget(timer_line, 2,1,1,1)

        status_line = QLabel('Выберете процесс и задайте время таймера')
        layout.addWidget(status_line ,3,0,1,3)

        def alert():
            notification.notify(
            title='Time Mng',
            message='Через 15 минут процесс умрет, сохраняйся!',
            app_name='Here is the application name',
            #TODO
            #app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
            )
            #time.sleep(15*60)
            kill_process()

        def kill_process():
            os.system(f'taskkill /f /im {games_combo.currentText()} ')


        def start_timer():
            timer = int(timer_line.text())
            timer_end = (datetime.now() + timedelta(minutes=timer)).strftime("%Y-%m-%d %H:%M:%S.%f")
            print(timer_end)
            print(type(timer_end))

            status_line.setText(f'Таймер выставлен на {timer} минут')
            scheduler = QtScheduler(timezone=str(tzlocal.get_localzone()))
            print(str(tzlocal.get_localzone()))
            # def alert():
            #     # notification.notify(
            #     # title='Time Mng',
            #     # message='Через 15 минут процесс умрет, сохраняйся!',
            #     # app_name='Here is the application name',
            #     # #TODO
            #     # #app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
            #     # )
            #     # #time.sleep(15*60)
            #     # kill_process()
            #     print('text')
            scheduler.add_job(alert, 'date', run_date=timer_end)
            scheduler.start()

            #TODO
            # week_number = datetime.now().isocalendar()[1]
            # day_of_the_week = timer, datetime.now().isocalendar()[2]
            # data = {week_number:timer, day_of_the_week:timer}
            # with open('time_played.json', 'w', encoding='utf-8') as file:
            #     json.dumps(data)
            # with open('time_played.json', 'r', encoding='utf-8') as file:
            #     reader_json = json.load(file)
            #     if reader_json[week_number] >= weekly_allowed_time:
            #         status_line.setText('На этой неделе больше гамацать нельзя')
            #     elif reader_json[week_number] < weekly_allowed_time and reader_json[day_of_the_week] >= daily_allowed_time:
            #         status_line.setText('Сегодня больше гамацать нельзя, но можно завтра')
            #     else:
            #         status_line.setText('Все нормас,еще можно гамацать')
            #time.sleep(int(timer)*60)






        self.setLayout(layout)

class AddGameTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QGridLayout()

        add_button = QPushButton(('Добавить игру в список'),clicked = lambda: add_game())
        layout.addWidget(add_button, 1, 0 , 1, 3)

        add_button = QPushButton(('Удалить из списка'),clicked = lambda: remove_game())
        layout.addWidget(add_button, 2, 0 , 1, 3)

        all_processes_combo = QComboBox()
        for proc in psutil.process_iter():
            all_processes_combo.addItem(proc.name())
        layout.addWidget(all_processes_combo, 0, 0, 1, 3)

        def add_game():
            with open('games', 'a', encoding='utf-8', newline='') as games_csv:
                writer = csv.writer(games_csv)
                writer.writerow([all_processes_combo.currentText()])
        #TODO
        def remove_game():
            pass

        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    tabDialog = MainWindow()
    tabDialog.show()
    sys.exit(app.exec())


