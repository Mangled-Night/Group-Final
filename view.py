from tkinter import *
from tkinter import ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
from model import Model
from newController import AudioController

model = AudioController()
_model = Model()


def open_file():
    filename = filedialog.askopenfilename(
        filetypes=(("Wav Files", "*.wav"), ("Mp3 Files", "*.mp3"), ("Aac Files", "*.aac")))
    #model.load_file(filename)
    _model.LoadFile(filename)
    _file.set(filename)
    _status_msg.set("Loaded file")


def plot(start=0.0, end=0.0, plt=0):
    def draw(fig):
        fig.set_dpi(100)
        fig.set_size_inches(7.77, 3.85)

        canvas = FigureCanvasTkAgg(
            fig, master=_plot_frame)
        canvas.draw()

        canvas.get_tk_widget().grid(
            row=2, column=0, pady=0)

        _status_msg.set("Showing: "+_current_plot.get())

    def de(fig):
        fig.clf()

    #fig = model.show_wav(start, end)

    if start.replace('.', '', 1).isdigit():
        start = float(start)
    else:
        start = 0

    if end.replace('.', '', 1).isdigit() and float(end) > float(start):
        end = float(end)
    else:
        end = 0

    match plt:
        case 0:
            fig = _model.ShowWav(start, end)
            de(fig)
            fig = _model.ShowWav(start, end)
            _current_plot.set("WaveForm")
            draw(fig)
        case 1:
            fig = _model.Frequency(None)[0]
            de(fig)
            fig = _model.Frequency(None)[0]
            _current_plot.set("Spectrograph")
            draw(fig)
        case 2:
            fig = _model.Frequency(None)[1][0]
            de(fig)
            fig = _model.Frequency(None)[1][0]
            _current_plot.set("Channel 1 RT60")
            draw(fig)
        case 3:
            if len(_model.Frequency(None)) == 3:
                fig = _model.Frequency(None)[2][0]
                de(fig)
                fig = _model.Frequency(None)[2][0]
                _current_plot.set("Channel 2 RT60")
                draw(fig)
        case 4:
            if _current_plot.get()[0] == "C":
                _current_channel.set(int(_current_plot.get()[8]))
                channel = _current_channel.get()
            elif _current_channel.get() > 0:
                channel = _current_channel.get()
            else:
                _current_channel.set(0)
                return

            match _current_plot.get()[0]:
                case "L":
                    fig = _model.Frequency(1)[channel][0]
                    de(fig)
                    fig = _model.Frequency(1)[channel][0]
                    _current_plot.set("Medium Freq")
                    draw(fig)
                case "M":
                    fig = _model.Frequency(2)[channel][0]
                    de(fig)
                    fig = _model.Frequency(2)[channel][0]
                    _current_plot.set("High Freq")
                    draw(fig)
                case "H":
                    fig = _model.Frequency(0)[channel][0]
                    de(fig)
                    fig = _model.Frequency(0)[channel][0]
                    _current_plot.set("Low Freq")
                    draw(fig)
                case _:
                    fig = _model.Frequency(0)[channel][0]
                    de(fig)
                    fig = _model.Frequency(0)[channel][0]
                    _current_plot.set("Low Freq")
                    draw(fig)


_root = Tk()  # instantiate instance of Tk class
_root.title('SPIDAM')

_root.geometry("800x600")
_root.minsize(800, 610)
_root.maxsize(800, 610)
_root.resizable(False, False)
_root.grid_rowconfigure(0, weight=1)

_mainframe = ttk.Frame(_root, padding='5 5 5 5')
_mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S"))
_mainframe.grid_columnconfigure((0,1), uniform="1", weight=1)

_file_frame = ttk.LabelFrame(
    _mainframe, text='File', padding="5 1 0 5")
_file_frame.grid(row=0, column=0, sticky=("E", "W"), columnspan=2)
_file_frame.columnconfigure(0, weight=1)
_file_frame.rowconfigure(0, weight=1)

_file = StringVar()
_file.set("File Directory")
_file_entry = ttk.Entry(
    _file_frame, width=111, text=_file)
_file_entry.grid(row=0, column=0, padx=(0, 23))

_file_button = ttk.Button(
    _file_frame, text="Open File", command=open_file)
_file_button.grid(row=0, column=1, padx=0, sticky='W E')

_file_button2 = ttk.Button(
    _file_frame, text="Analyze Audio", command=lambda:
    plot(_start_time.get(), _end_time.get(), 0))
_file_button2.grid(row=1, column=1, sticky='W E')

_current_plot = StringVar()
_current_plot.set("None")
_current_channel = IntVar()
_current_channel.set(0)

_data_frame = ttk.LabelFrame(
    _mainframe, text="Data", padding="5 6 0 13")
_data_frame.grid(row=1, column=0, sticky="W E")

_data_time_label1 = ttk.Label(
    _data_frame, text="Start Time ")
_data_time_label1.grid(row=0, column=0, sticky=("E", "W"))
_data_time_label2 = ttk.Label(
    _data_frame, text="End Time   ")
_data_time_label2.grid(row=1, column=0, sticky=("E", "W"))

_data_time_entry1 = ttk.Entry(
    _data_frame, width=5)
_data_time_entry1.grid(row=0, column=1, sticky=("E", "W"))
_start_time = _data_time_entry1
_data_time_entry2 = ttk.Entry(
    _data_frame, width=5)
_data_time_entry2.grid(row=1, column=1, sticky=("E", "W"))
_end_time = _data_time_entry2

# <editor-fold desc="Data Values">
_data_fq = StringVar()
_data_fq.set("Average Frequency: 0")
_data_label_fq = ttk.Label(
    _data_frame, textvariable=_data_fq)
_data_label_fq.grid(row=0, column=2, sticky=("E", "W"))

_data_amp = StringVar()
_data_amp.set("Peak Amplitude: 0")
_data_label_amp = ttk.Label(
    _data_frame, textvariable=_data_amp)
_data_label_amp.grid(row=1, column=2, sticky=("E", "W"))

_data_len = StringVar()
_data_len.set("Length (in seconds): 0")
_data_label_len = ttk.Label(
    _data_frame, textvariable=_data_len)
_data_label_len.grid(row=2, column=2, sticky=("E", "W"))
# </editor-fold> #

_switch_frame = ttk.LabelFrame(
    _mainframe, text="Switch", padding="5 0 0 5")
_switch_frame.grid(row=1, column=1, sticky="W E")
_switch_frame.columnconfigure((0,1), weight=1)

_switch_button_wav = ttk.Button(
    _switch_frame, text="Wave", command=lambda:
    plot(_start_time.get(), _end_time.get(), 0))
_switch_button_wav.grid(row=0, column=0, sticky="W E")
_switch_button_spec = ttk.Button(
    _switch_frame, text="Spec", command=lambda:
    plot(_start_time.get(), _end_time.get(), 1))
_switch_button_spec.grid(row=1, column=0, sticky="W E")
_switch_button_freq1 = ttk.Button(
    _switch_frame, text="Freq 1", command=lambda:
    plot(_start_time.get(), _end_time.get(), 2))
_switch_button_freq1.grid(row=0, column=1, sticky="W E")
_switch_button_freq2 = ttk.Button(
    _switch_frame, text="Freq 2", command=lambda:
    plot(_start_time.get(), _end_time.get(), 3))
_switch_button_freq2.grid(row=1, column=1, sticky="W E")
_switch_button_switch = ttk.Button(
    _switch_frame, text="Switch", command=lambda:
    plot(_start_time.get(), _end_time.get(), 4))
_switch_button_switch.grid(row=2, column=1, sticky="W E")

_plot_frame = ttk.LabelFrame(
    _mainframe, text="Plot", padding="5 1 0 5")
_plot_frame.grid(row=2, column=0, sticky=("E", "W"), columnspan=2)

_status_frame = ttk.Frame(
    _root, relief='sunken', padding='2 2 2 2')
_status_frame.grid(row=1, column=0, sticky=("E", "W", "S"))
_status_msg = StringVar()
_status_msg.set('Enter an audio file to analyze')
_status = ttk.Label(
    _status_frame, textvariable=_status_msg, anchor=W)
_status.grid(row=0, column=0, sticky=(E, W))

_root.mainloop()