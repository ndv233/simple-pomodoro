from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, \
     QLabel, QSpinBox, QLCDNumber, QProgressBar, QVBoxLayout, QPlainTextEdit
from PyQt6.QtCore import QTimer
import winsound
from stats_manager import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


def secondsToMinutesSeconds(seconds: int) -> tuple[int, int]:
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    return minutes, seconds


class MainApplication(QWidget):
    def __init__(self):
        MIN = 40
        MAX = 240
        super().__init__()

        self.timeRemainingSec = 0
        self.work_time = 0
        self.rest_min = 0
        self.completed_sessions = 0
        self.total_sessions = 0

        # Timers
        self.focusTimer = QTimer()
        self.focusTimer.setInterval(1000)  # 1000ms
        self.focusTimer.timeout.connect(self.updateFocus)  # Calls updateFocus function every 1000ms

        self.breakTimer = QTimer()
        self.breakTimer.setInterval(1000)  # 1000ms
        self.breakTimer.timeout.connect(self.updateBreak)  # Calls updateBreak function every 1000ms

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)
        # Widgets setup

        # Input boxes
        self.boxTotalSessions = QSpinBox()
        self.boxTotalSessions.setMinimum(1)
        self.boxTotalSessions.setMaximum(999)
        self.boxTotalSessions.setSuffix(" sessions")
        self.boxTotalSessions.setSingleStep(1)
        self.boxTotalSessions.setMinimumWidth(MIN)
        self.boxTotalSessions.setMaximumWidth(MAX)
        self.boxTotalSessions.setValue(2)

        self.boxFocusTime = QSpinBox()
        self.boxFocusTime.setMinimum(5)
        self.boxFocusTime.setMaximum(999)
        self.boxFocusTime.setSuffix(" min")
        self.boxFocusTime.setSingleStep(5)
        self.boxFocusTime.setMinimumWidth(MIN)
        self.boxFocusTime.setMaximumWidth(MAX)
        self.boxFocusTime.setValue(15)

        self.boxRestTime = QSpinBox()
        self.boxRestTime.setMinimum(5)
        self.boxRestTime.setMaximum(30)
        self.boxRestTime.setSuffix(" min")
        self.boxRestTime.setSingleStep(5)
        self.boxRestTime.setMinimumWidth(MIN)
        self.boxRestTime.setMaximumWidth(MAX)
        self.boxRestTime.setValue(5)

        # Clock
        self.clockDisplay = QLCDNumber()
        self.clockDisplay.setMinimumSize(300, 300)
        self.clockDisplay.setMaximumSize(1000, 500)

        # Buttons
        self.button_play = QPushButton("Start")
        self.button_play.setMaximumWidth(MAX)
        self.button_play.clicked.connect(self.setTimer)
        self.button_pause = QPushButton("Reset")
        self.button_pause.setMaximumWidth(MAX)
        self.button_pause.clicked.connect(self.resetClock)

        # Text fields
        self.system_text = QLabel("")
        tooltip_total_sessions = QLabel("Number of focus sessions")
        tooltip_total_sessions.setStyleSheet('''font-size:1em;''')
        tooltip_focus = QLabel("Focus session duration")
        tooltip_focus.setStyleSheet('''font-size:1em;''')
        tooltip_break = QLabel("Break duration")
        tooltip_break.setStyleSheet('''font-size:1em;''')

        # Progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMinimumWidth(300)

        # Add widgets to layout
        layout.addWidget(self.clockDisplay, 1, 0, 2, 0)
        layout.addWidget(tooltip_total_sessions, 2, 0)
        layout.addWidget(self.boxTotalSessions, 2, 1)
        layout.addWidget(tooltip_focus, 3, 0)
        layout.addWidget(self.boxFocusTime, 3, 1)
        layout.addWidget(tooltip_break, 4, 0)
        layout.addWidget(self.boxRestTime, 4, 1)
        layout.addWidget(self.button_play, 6, 0)
        layout.addWidget(self.button_pause, 6, 1)
        layout.addWidget(self.system_text, 9, 0)
        layout.addWidget(self.progressBar, 10, 0)

        self.resetClock()  # Init values

    def setTimer(self):
        """
        Get values from input boxes and call for the timer to start
        :return:
        """
        # Get values
        self.total_sessions = self.boxTotalSessions.value()
        self.work_time = self.boxFocusTime.value()
        self.rest_min = self.boxRestTime.value()
        self.progressBar.setMaximum(self.total_sessions)

        # Check if values are valid
        if (self.total_sessions == 0) or (self.work_time == 0) or (self.rest_min == 0):
            self.system_text.setText("Invalid Input Values!")
        else:
            self.timerStart()  # Start timer

    def timerStart(self):
        """
        Starts timer
        :return:
        """
        self.startFocus()  # Start from focus period
        self.button_play.setEnabled(False)  # Disable play button while running

    def startFocus(self):
        """
        Starts focus period
        :return:
        """
        self.system_text.setText("Work")  # Change system text
        self.clockDisplay.display(f"{self.work_time:02d}:00")  # Change clock text
        self.timeRemainingSec = self.work_time * 60
        self.focusTimer.start()  # Start timer

    def updateFocus(self):
        """
        Function for handling focus period timer
        :return:
        """
        self.refreshClock()  # Refresh clock display
        if self.timeRemainingSec == 0:  # Check if time remaining
            self.focusTimer.stop()  # Stop focus timer
            self.completed_sessions += 1  # Record session as completed
            self.progressBar.setValue(self.completed_sessions)  # Update progress bar for total sessions
            winsound.PlaySound("Media/Alarm04.wav", winsound.SND_FILENAME)  # Play sound
            self.writeToFile()  # Write stats to stats file
            if self.completed_sessions < self.total_sessions:  # Check if sessions remaining
                self.startBreak()  # Move to break period if sessions remaining
            else:
                # TODO: Implement what happens when you complete all entire session. A daily goal feature?
                self.resetClock()
                self.progressBar.setValue(0)

    def startBreak(self):
        """
        Starts break time
        :return:
        """
        self.system_text.setText("Break")  # Change system text
        self.clockDisplay.display(f"{self.rest_min:02d}:00")
        self.timeRemainingSec = self.rest_min * 60
        self.breakTimer.start()

    def updateBreak(self):
        """
        Function for handling break period timer
        :return:
        """
        self.refreshClock()  # Refresh clock display
        if self.timeRemainingSec == 0:  # Check if time remaining
            self.breakTimer.stop()  # Stop timer
            winsound.PlaySound("Media/Alarm07.wav", winsound.SND_FILENAME)  # Play sound
            self.startFocus()  # Move to focus period

    def refreshClock(self):
        """
        Function for refreshing clock display
        :return:
        """
        self.timeRemainingSec -= 1  # Update time remaining
        minutes, secs = secondsToMinutesSeconds(self.timeRemainingSec)  # Convert time format
        remainingText = f"{minutes:02d}:{secs:02d}"
        self.clockDisplay.display(remainingText)  # Update text

    def resetClock(self):
        """
        Resets clock and system text to initial values
        :return:
        """
        self.button_play.setEnabled(True)  # Enables play button
        self.system_text.setText("Waiting")  # Change system message
        self.focusTimer.stop()  # Stop timers
        self.breakTimer.stop()
        self.clockDisplay.display("00:00")  # Update text

    def writeToFile(self):
        """
        Writes session data to csv file
        :return:
        """
        if not checkData(getDate()):  # Check if current date already exists in stats file
            writeData(self.work_time)  # Write session data into stats file
        else:
            current_value = getDataValue(getDataIndex(getDate()))  # Get current amount of minutes recorded for the day
            override_value = current_value + self.work_time  # Add completed session time
            overrideData(getDataIndex(getDate()), override_value)  # Override old session time


class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Notes")
        self.label.setStyleSheet("""font-size:12px;""")
        self.list = QPlainTextEdit()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list)


class FigureCanvas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        fig = Figure()
        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)


