from tkinter import *
from tkinter import ttk, filedialog


def open_file():
    filename = filedialog.askopenfilename(
        filetypes=(("Wav Files", "*.wav"), ("Mp3 Files", "*.mp3"), ("Aac Files", "*.aac")))
    _file.set(filename)
    _status_msg.set("Loaded file")
    pass


_root = Tk()  # instantiate instance of Tk class
_root.title('SPIDAM')

_root.geometry("800x600")
_root.minsize(800, 600)
_root.maxsize(800, 600)
_root.resizable(False, False)
_root.grid_rowconfigure(0, weight=1)

_mainframe = ttk.Frame(_root, padding='5 5 5 5')
_mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S"))

_file_frame = ttk.LabelFrame(
    _mainframe, text='File', padding="5 1 0 5")
_file_frame.grid(row=0, column=0, sticky=("E", "W"))
_file_frame.columnconfigure(0, weight=1)
_file_frame.rowconfigure(0, weight=1)

_file = StringVar()
_file.set("File Directory")
_file_entry = ttk.Entry(
    _file_frame, width=110, text=_file)
_file_entry.grid(row=0, column=0)

_file_button = ttk.Button(
    _file_frame, text="Open File", command=open_file)
_file_button.grid(row=0, column=1, padx=15, sticky='W E')

_file_button = ttk.Button(
    _file_frame, text="Analyze Audio")
_file_button.grid(row=1, column=1, padx=15, sticky='W E')

_data_frame = ttk.LabelFrame(
    _mainframe, text="Data", padding="5 1 0 5")
_data_frame.grid(row=1, column=0, sticky=("E", "W"))

_data_time_label1 = ttk.Label(
    _data_frame, text="Start Time ")
_data_time_label1.grid(row=0, column=0, sticky=("E", "W"))
_data_time_label2 = ttk.Label(
    _data_frame, text="End Time   ")
_data_time_label2.grid(row=1, column=0, sticky=("E", "W"))

_data_time_entry1 = ttk.Entry(
    _data_frame, width=5)
_data_time_entry1.grid(row=0, column=1, sticky=("E", "W"))
_data_time_entry2 = ttk.Entry(
    _data_frame, width=5)
_data_time_entry2.grid(row=1, column=1, sticky=("E", "W"))

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

_status_frame = ttk.Frame(
    _root, relief='sunken', padding='2 2 2 2')
_status_frame.grid(row=1, column=0, sticky=("E", "W", "S"))
_status_msg = StringVar()
_status_msg.set('Enter an audio file to analyze')
_status = ttk.Label(
    _status_frame, textvariable=_status_msg, anchor=W)
_status.grid(row=0, column=0, sticky=(E, W))

_root.mainloop()