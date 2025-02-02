from abc import ABC

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt


class abstract_window(ABC):
    def __init__(self, title, layout, finalize=True):
        self.win = sg.Window(title, layout, finalize=finalize, resizable=True)

    def Notifica(self):
        pass

    def Update(self):
        pass

    def GetStato(self):
        pass

    def GetWin(self):
        return self.win

    def close(self):
        self.win.close()


class Utente_window(abstract_window):
    def __init__(self):
        self.layout = [[sg.Text('Github Rest analyser'), sg.Text(size=(15, 2), key='-LINE1-')],
                       [sg.Multiline(size=(90, 20), auto_refresh=True, reroute_stdout=True, reroute_cprint=True,
                                     write_only=True, key='-OUT-')],
                       [sg.Text('Inserisci un Token Github per eseguire'), sg.Text(size=(20, 1), key='-LINE2-')],
                       [sg.Input(key='-TOKEN-', size=(90, 1))],
                       [sg.Text('Scrivi la tua query o carica un db compatibile'),
                        sg.Text(size=(20, 1), key='-LINE3-')],
                       [sg.Input(key='-IN-', size=(90, 1))],
                       [sg.Text('Operazioni dati')],
                       [sg.Button('Do Query'), sg.FileBrowse('Load Data', file_types=(("File DB", "*.db"),)),
                        sg.Button('Salva Dati')],
                       [sg.Text('Elaborazioni'), sg.Text(size=(20, 1), key='-LINE4-')],
                       [sg.Button('Repos'), sg.Button('Cloc'), sg.Button('Densità')],
                       [sg.Text('Grafici'), sg.Text(size=(20, 1), key='-LINE5-')],
                       [sg.Button('Documentazione/Modificabilità'), sg.Button('Documentazione/Popolarità')], ]

        super(Utente_window, self).__init__(title='Github Analyzer', layout=self.layout)
        self.stato = {
            "token": None,
            "db": None,
            "query": None,
        }

    def Notifica(self):
        event, values = self.win.read()

        if values['-TOKEN-']:
            self.stato['token'] = values['-TOKEN-']
        if values['-IN-']:
            self.stato['query'] = values['-IN-']
        if values['Load Data']:
            self.stato['db'] = values['Load Data']

        return event

    def GetStato(self):
        return self.stato

    def GetWin(self):
        return self.win


class Salva_window(abstract_window):
    def __init__(self, title):
        self.layout = [[sg.Input(key='-IN SALVA-'), sg.Button('Submit_salva')]]
        super(Salva_window, self).__init__(title=title, layout=self.layout)
        self.stato = {
            'backup': None
        }

    def Notifica(self):
        event, values = self.win.read(timeout=100)
        if values['-IN SALVA-']:
            if values['-IN SALVA-'] != ' ' and values['-IN SALVA-'] is not None:
                self.stato['backup'] = values['-IN SALVA-']

        return event

    def GetStato(self):
        return self.stato


class graph_window(abstract_window):
    def __init__(self, tipo, title, desc_x, desc_y, x, y):
        self.tipo = tipo
        self.layout = [[sg.Canvas(key="-CANVAS-")],
                       [sg.Button('Salva Graph')], ]

        super(graph_window, self).__init__(layout=self.layout, title=title, finalize=True)

        num_list_x = list()
        num_list_y = list()

        for i,j in zip(x,y):
            num_list_x.append(float(i))
            num_list_y.append(float(j))

        num_list_x.sort()
        num_list_y.sort()

        # make fig and plot
        plt.figure(1, figsize=(7, 6), dpi=100)

        plt.plot(num_list_x, num_list_y, 'o', color='tab:red')
        # Instead of plt.show
        plt.xlabel(desc_x)
        plt.ylabel(desc_y)
        self.fig = plt.gcf()
        self.fig.autofmt_xdate()
        self.__draw_figure(self.win['-CANVAS-'].TKCanvas, self.fig)

    def __draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def Notifica(self):
        event, values = self.win.read(timeout=100)
        return event

    def GetFig(self):
        return self.fig
