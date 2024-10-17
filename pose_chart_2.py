import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QScreen, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from tqdm import tqdm

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.df = pd.read_csv('file name.csv_with_metrics.csv')
        self.weight = 70  # default weigth

        self.initUI()
        self.idx = 0
        self.is_playing = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

    def initUI(self):
        # monitor dimension
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        screen_width = screen.width()
        screen_height = screen.height()

        # hegth and width of the plot
        plot_width = screen_width * 0.8 / 100
        plot_height = screen_height * 0.6 / 100

        self.canvas = MplCanvas(self, width=plot_width, height=plot_height, dpi=200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        plot_layout = QVBoxLayout()
        stats_layout = QVBoxLayout()
        control_layout = QVBoxLayout()
        
        plot_layout.addWidget(self.canvas)

        label_font = QFont('Times font')
        label_font.setPointSize(15)  # set character dimension
        
        self.stats_velocity = QLabel(self)
        self.stats_velocity.setFont(label_font)
        self.stats_acceleration = QLabel(self)
        self.stats_acceleration.setFont(label_font)
        self.stats_displacement = QLabel(self)
        self.stats_displacement.setFont(label_font)
        self.stats_power = QLabel(self)
        self.stats_power.setFont(label_font)
        self.weight_input = QLineEdit(self)
        self.weight_input.setFont(label_font)

        label_velocity = QLabel("Velocity (hand):", self)
        label_velocity.setFont(label_font)
        stats_layout.addWidget(label_velocity)
        stats_layout.addWidget(self.stats_velocity)

        label_acceleration = QLabel("Acceleration (hand):", self)
        label_acceleration.setFont(label_font)
        stats_layout.addWidget(label_acceleration)
        stats_layout.addWidget(self.stats_acceleration)

        label_displacement = QLabel("Displacement (hand):", self)
        label_displacement.setFont(label_font)
        stats_layout.addWidget(label_displacement)
        stats_layout.addWidget(self.stats_displacement)

        label_weight = QLabel("Weight (kg):", self)
        label_weight.setFont(label_font)
        stats_layout.addWidget(label_weight)
        stats_layout.addWidget(self.weight_input)

        label_power = QLabel("Power (hand):", self)
        label_power.setFont(label_font)
        stats_layout.addWidget(label_power)
        stats_layout.addWidget(self.stats_power)

        button_font_size = 20
        
        self.next_button = QPushButton('Next', self)
        self.next_button.setFixedSize(150, 150)
        self.next_button.clicked.connect(self.next_frame)
        self.next_button.setFont(QFont('Times font', button_font_size))

        self.prev_button = QPushButton('Previous', self)
        self.prev_button.setFixedSize(150, 150)
        self.prev_button.clicked.connect(self.prev_frame)
        self.prev_button.setFont(QFont('Times font', button_font_size))

        self.play_button = QPushButton('Play', self)
        self.play_button.setFixedSize(150, 150)
        self.play_button.clicked.connect(self.play)
        self.play_button.setFont(QFont('Times font', button_font_size))

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.setFixedSize(150, 150)
        self.pause_button.clicked.connect(self.pause)
        self.pause_button.setFont(QFont('Times font', button_font_size))

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setFixedSize(150, 150)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setFont(QFont('Times font', button_font_size))

        control_layout.addWidget(self.next_button)
        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)

        main_layout.addLayout(plot_layout)
        main_layout.addLayout(stats_layout)
        main_layout.addLayout(control_layout)

    def timerEvent(self, event):
        self.update_plot()

    def next_frame(self):
        self.idx += 1
        if self.idx >= len(self.df):
            self.idx = 0
        self.update_plot()

    def prev_frame(self):
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.df) - 1
        self.update_plot()

    def play(self):
        self.is_playing = True
        self.timer.start(100)  # Start timer to update every 100 ms

    def pause(self):
        self.is_playing = False
        self.timer.stop()

    def stop(self):
        self.is_playing = False
        self.timer.stop()
        self.idx = 0
        self.update_plot()

    def update_plot(self):
        self.canvas.ax.clear()
        connections = [
            (11, 12), (12, 14), (14, 16), (11, 13), (13, 15),  # Upper body
            (12, 24), (24, 26), (26, 28), (28, 32), (11, 23), (23, 25), (25, 27), (27, 31), (28, 30), (27,29),  # Lower body
            (23, 24),  # Hip
            (8, 0), (0, 7), # Head
            (15, 16) # barbell
        ]
        
        for connection in connections:
            x_coords = [self.df[f'lm_{connection[0]}_x'][self.idx], self.df[f'lm_{connection[1]}_x'][self.idx]]
            y_coords = [self.df[f'lm_{connection[0]}_y'][self.idx], self.df[f'lm_{connection[1]}_y'][self.idx]]
            self.canvas.ax.plot(x_coords, [-y for y in y_coords], 'k-')  # Linee nere
        
        # red dot
        for i in range(33):
            if i not in [15, 16]:
                self.canvas.ax.plot(self.df[f'lm_{i}_x'][self.idx], -self.df[f'lm_{i}_y'][self.idx], 'ro')
        
        # green line to connect 15 and 16 landmarks (hand)
        self.canvas.ax.plot([self.df[f'lm_15_x'][self.idx], self.df[f'lm_16_x'][self.idx]],
                            [-self.df[f'lm_15_y'][self.idx], -self.df[f'lm_16_y'][self.idx]], 'g-')
        self.canvas.ax.plot(self.df[f'lm_15_x'][self.idx], -self.df[f'lm_15_y'][self.idx], 'go')
        self.canvas.ax.plot(self.df[f'lm_16_x'][self.idx], -self.df[f'lm_16_y'][self.idx], 'go')
        
        # limit of the axis
        x_min = self.df[[f'lm_{i}_x' for i in range(33)]].min().min()
        x_max = self.df[[f'lm_{i}_x' for i in range(33)]].max().max()
        y_min = self.df[[f'lm_{i}_y' for i in range(33)]].min().min()
        y_max = self.df[[f'lm_{i}_y' for i in range(33)]].max().max()

        self.canvas.ax.set_xlim(x_min - 50, x_max + 50)
        self.canvas.ax.set_ylim(-(y_max + 50), -(y_min - 50))  # invert y axis

        self.canvas.draw()

        self.update_stats()

    def update_stats(self):
        try:
            self.weight = float(self.weight_input.text())
        except ValueError:
            self.weight = 70  # Default weight if invalid input

        # velcity (min, mavgedia, max) for current frame
        speed_15 = self.df['speed_15'].iloc[self.idx]
        speed_16 = self.df['speed_16'].iloc[self.idx]

        mean_speed_15 = self.df['mean_speed_15'].iloc[self.idx]
        max_speed_15 = self.df['max_speed_15'].iloc[self.idx]
        mean_speed_16 = self.df['mean_speed_16'].iloc[self.idx]
        max_speed_16 = self.df['max_speed_16'].iloc[self.idx]

        self.stats_velocity.setText(f"15: current={speed_15:.2f}, mean={mean_speed_15:.2f}, max={max_speed_15:.2f}\n"
                                    f"16: current={speed_16:.2f}, mean={mean_speed_16:.2f}, max={max_speed_16:.2f}")

        # acceleration (min, avg, max) for current frame
        acc_15 = self.df['acc_15'].iloc[self.idx]
        acc_16 = self.df['acc_16'].iloc[self.idx]

        mean_acc_15 = self.df['mean_acc_15'].iloc[self.idx]
        max_acc_15 = self.df['max_acc_15'].iloc[self.idx]
        mean_acc_16 = self.df['mean_acc_16'].iloc[self.idx]
        max_acc_16 = self.df['max_acc_16'].iloc[self.idx]

        self.stats_acceleration.setText(f"15: current={acc_15:.2f}, mean={mean_acc_15:.2f}, max={max_acc_15:.2f}\n"
                                        f"16: current={acc_16:.2f}, mean={mean_acc_16:.2f}, max={max_acc_16:.2f}")

        # dislocation 
        disp_15_frame = self.df['disp_15_frame'].iloc[self.idx]
        total_disp_15 = self.df['total_disp_15'].iloc[self.idx]
        disp_16_frame = self.df['disp_16_frame'].iloc[self.idx]
        total_disp_16 = self.df['total_disp_16'].iloc[self.idx]

        self.stats_displacement.setText(f"15: frame={disp_15_frame:.2f}, total={total_disp_15:.2f}\n"
                                        f"16: frame={disp_16_frame:.2f}, total={total_disp_16:.2f}")

        # power (min, avg, max) for current frame
        power_15 = self.df['power_15'].iloc[self.idx]
        mean_power_15 = self.df['mean_power_15'].iloc[self.idx]
        max_power_15 = self.df['max_power_15'].iloc[self.idx]
        power_16 = self.df['power_16'].iloc[self.idx]
        mean_power_16 = self.df['mean_power_16'].iloc[self.idx]
        max_power_16 = self.df['max_power_16'].iloc[self.idx]

        self.stats_power.setText(f"15: current={power_15:.2f}, mean={mean_power_15:.2f}, max={max_power_15:.2f}\n"
                                f"16: current={power_16:.2f}, mean={mean_power_16:.2f}, max={max_power_16:.2f}")

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
