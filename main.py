import sys
from PySide6.QtWidgets import QApplication
import numpy as np
from MplWidget import *
from gui import *
import matplotlib.ticker as tkr

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MMMUi()
        self.ui.setupUi(self)
        self.ui.SimulateButton.clicked.connect(self.plot_data)
        self.ui.Plot1 = MplWidget(self.ui.Plots1)
        self.ui.Plot1.canvas.draw()
        self.ui.Plot2_2 = MplWidget(self.ui.Plot2)
        self.ui.Plot2_2.canvas.draw()

    def vect_add(self,U, V, N):
        W = np.zeros(N)
        W = U + V
        return W

    def vect_scalar_multiply(self,U, d, N):
        W = np.zeros(N)
        for i in range(N):
            W[i] = U[i] * d
        return W

    def matr_vect_multiply(self,A, V, N):
        W = np.zeros(N)
        for i in range(N):
            W[i] = np.dot(A[i], V)
        return W

    def vect_dot_product(self,U, V):
        return np.dot(U, V)

    def plot_data(self):
        h = 0.001  # krok obliczeń
        T = 50.0  # czas
        L1=self.ui.FrequencyInput_2.text().replace(',', '.')
        L = float(L1)  # liczba przebiegów sygnału w przedziale T
        M1=self.ui.AmplitudeInput.text().replace(',', '.')
        M = float(M1) # amplituda
        w = 2.0 * np.pi * L / T  # częstotliwość
        total = int(1.0 * T / h) + 1
        us = np.zeros(total)
        uf = np.zeros(total)
        ug = np.zeros(total)

        for i in range(total):
            us[i] = M * np.sin(w * i * h)  # harmoniczny
            uf[i] = M if us[i] > 0 else -M # prostokątny
            ug[i] = (M * np.abs((2 / np.pi) * np.arcsin(np.sin(w * i * h/2))))-M/2 #trójkątny



        self.ui.Plot1.canvas.ax.clear()
        yw=[]
        if self.ui.InputSignalChoice_2.currentIndex() == 0: #sprawdzanie wybranego sygnału wejsciowego
            yw = uf
            self.integrating(total,h,uf)
            self.ui.Plot1.canvas.ax.set_title("Sygnał prostokątny")
        elif self.ui.InputSignalChoice_2.currentIndex() == 1:
            yw = ug
            self.integrating(total, h, ug)
            self.ui.Plot1.canvas.ax.set_title("Sygnał trójkątny")
        elif self.ui.InputSignalChoice_2.currentIndex() == 2:
            yw = us
            self.integrating(total, h, us)
            self.ui.Plot1.canvas.ax.set_title("Sygnał harmoniczny")

        if self.stabilnosc == True:
            self.ui.Plot1.canvas.ax.set_xlabel("Czas")
            self.ui.Plot1.canvas.ax.set_ylabel("Amplituda")
            self.ui.Plot1.canvas.ax.plot(self.wektor_czas, yw)
            self.ui.Plot1.canvas.ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, pos: f'{x / 10000:.2f}'))
            self.ui.Plot1.canvas.draw()
            self.ui.Plot2_2.canvas.ax.clear()
            self._line = self.ui.Plot2_2.canvas.ax.plot(self.wektor_czas, self.wktor_y)

            self.ui.Plot2_2.canvas.ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, pos: f'{x / 10000:.2f}'))
            self.ui.Plot2_2.canvas.ax.set_title("Wyjście")
            self.ui.Plot2_2.canvas.ax.set_xlabel("Czas")
            self.ui.Plot2_2.canvas.ax.set_ylabel("Amplituda")
            # display canvasa
            self.ui.Plot2_2.canvas.draw()
        else: self.ui.dialog.exec()

    def integrating(self, total, h , signal):
        wzmocnienie1=self.ui.Kinput.text().replace(',', '.')
        wzmocnienie = float(wzmocnienie1)
        czas_zdwojenia1=self.ui.TimeInput_2.text().replace(',', '.')
        czas_zdwojenia =float(czas_zdwojenia1)
        A3=0
        A2=0
        A11=self.ui.a0Input.text().replace(',', '.')
        A1=float(A11)
        A00=self.ui.a1Input.text().replace(',', '.')
        A0=float(A00)
        B3=0
        B22=self.ui.b2Input.text().replace(',', '.')
        B2=float(B22)
        B11=self.ui.b1Input.text().replace(',', '.')
        B1=float(B11)
        B00=self.ui.b0Input.text().replace(',', '.')
        B0=float(B00)
        b3 = 0
        b2 = wzmocnienie*A1*czas_zdwojenia
        b1 = wzmocnienie*A1 + wzmocnienie*A0*czas_zdwojenia
        b0 = A0*wzmocnienie
        a3 = B2*czas_zdwojenia
        a2 = B1*czas_zdwojenia + wzmocnienie*A1*czas_zdwojenia
        a1 = B0*czas_zdwojenia + wzmocnienie*A1 + wzmocnienie*A0*czas_zdwojenia
        a0 = A0*wzmocnienie
        #sprawdzenie stopnia ukladu
        if (a3, a2,a1,a0 != 0):
            N=4
        if a3==0 and (a2, a1, a0 != 0):
            N=3
        if a3 == 0 and a2 == 0 and (a1, a0 != 0):
            N=2

        #sprawdzenie stabilnosci ukladu
        if (a3 * a2 * a1 - a3 * a3 * a0 - a1 * a1) > 0 and a3 > 0 and a2 > 0 and a1 > 0 and a0 > 0 and N==4:
            self.stabilnosc = True
        elif -a0 / a1 < 0 and N==2:
            self.stabilnosc = True
        elif a2 > 0 and a1 > 0 and a0 > 0 and N==3:
            self.stabilnosc = True
        else:
            self.stabilnosc = False

        if N==4:
            A = np.zeros((N, N))
            A[0] = [0, 1, 0, 0]
            A[1] = [0, 0, 1, 0]
            A[2] = [0, 0, 0, 1]
            A[3] = [-a0, -a1, -a2, -a3]

            B = np.zeros(N)
            B = [0, 0, 0, 1]

            C = np.zeros(N)
            C = [b0, b1, b2, b3]

            D = 0
        if N==3:
            A = np.zeros((N, N))
            A[0] = [0, 1, 0]
            A[1] = [0, 0, 1]
            A[2] = [-a0, -a1, -a2]

            B = np.zeros(N)
            B = [0, 0, 1]

            C = np.zeros(N)
            C = [b0, b1, b2]

            D = 0
        elif N==2:
            A = np.zeros((N, N))
            A[0] = [0, 1]
            A[1] = [-a0, -a1]

            B = np.zeros(N)
            B = [0, 1]

            C = np.zeros(N)
            C = [b0, b1]

            D = 0

        # zerowe warunki początkowe
        xi_1 = np.zeros(N)
        self.wektor_czas = []
        self.wktor_y = []
        y = np.zeros(total)
        # główna pętla obliczeń
        for i in range(total):
            Ax = self.matr_vect_multiply(A, xi_1, N)
            Bu = self.vect_scalar_multiply(B, signal[i], N)
            Cx = self.vect_dot_product(C, xi_1)
            Du = D * signal[i]

            xi = self.vect_add(Ax, Bu, N)
            xi = self.vect_scalar_multiply(xi, h, N)
            xi = self.vect_add(xi_1, xi, N)
            xi_1 = xi
            y[i] = Cx + Du
            self.wektor_czas.append([i])
            self.wktor_y.append(y[i])


if __name__ == "__main__":
        app = QApplication(sys.argv)
        widget = Widget()
        widget.show()
        sys.exit(app.exec())
