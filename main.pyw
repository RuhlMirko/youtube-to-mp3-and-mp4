from pytube import YouTube
import ttkbootstrap as tb
import re
import math

window = tb.Window(themename="darkly", title='Converter')
window.iconbitmap('./converter-logo.ico')

# ---------------------------- CONSTANTS ------------------------------- #
PRIMARY_COLOR = '#f43542'
SECONDARY_COLOR = '#ebb'
SECONDARY_BTN = '#eeb2ba'
TERTIARY_COLOR = '#868c8d'
PRIMARY_FONT = 'Segoe UI'
SECONDARY_FONT = 'Courier New'


# ---------------------------- FUNCTIONS  ---------------------------- #
def getLinkInfo():
    if link_entry.get() == '':
        print('null value')
    else:
        link = link_entry.get()
        checkLink = re.match("^https://www.youtube.com/.*", link)
        if checkLink:
            try:
                yt = YouTube(link)
                status_label.configure(text=f'Title: {yt.title}'
                                            f'\nUploader: {yt.author}'
                                            f'\nLength: {math.floor(yt.length / 60)}:{yt.length % 60} minutes'
                                       )
                status_label.configure()

                video = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                audio = yt.streams.filter(type='audio')
                print(audio)

                quality = []
                for video in video:
                    quality.append(video.resolution)
                resolution_btn.configure(state='enabled', values=quality)
                download_btn.configure(state='enabled')

                audios = []
                for audio in audio:
                    audios.append(audio.mime_type.removeprefix("audio/").upper())
                audio_mp3.configure(state='enabled', values=audios)
                download_audio_btn.configure(state='enabled')

            except Exception as e:
                status_label.configure(text=f"Error, try another link.\n{e}")
                print(e)




def download():
    yt = YouTube(link_entry.get())
    ys = yt.streams.filter(file_extension='mp4').filter(resolution=resolution_btn.get()).first()
    status_label.configure(text='Download started')
    ys.download('./videos')
    status_label.configure(text='Download complete')


def download_audio():
    yt = YouTube(link_entry.get())
    ys = yt.streams.filter(mime_type=f"audio/{audio_mp3.get()}".lower()).first()
    status_label.configure(text='Download started')
    ys.download('./audios')
    status_label.configure(text='Download complete')


# ---------------------------- UI SETUP ------------------------------- #
# --------Style Setup------- #
my_style = tb.Style()
my_style.configure('danger.TButton', font=(PRIMARY_FONT, 15), background=PRIMARY_COLOR, relief='flat')
my_style.configure('danger.TLabel', font=(PRIMARY_FONT, 18), foreground=SECONDARY_COLOR)
my_style.configure('primary.TLabel', foreground=PRIMARY_COLOR)

# --------Title------- #
label = tb.Label(text="Youtube to MP4 and MP3", font=(SECONDARY_FONT, 35, "italic"), bootstyle="primary")
label.grid(column=0, row=0, pady=20, columnspan=2, padx=20)

###---- First row ----###
first_row_label = tb.Label(text="Youtube link: ", font=(SECONDARY_FONT, 15, "bold"), bootstyle="danger")
first_row_label.grid(column=0, row=1, pady=5)

# - Convert Button -#
button_convert = tb.Button(text="Get video info", style="danger", width=20, command=getLinkInfo)
button_convert.grid(column=1, row=1, padx=20)
# - Entry Widget -#
link_entry = tb.Entry(font=(PRIMARY_FONT, 10), width=80, foreground=PRIMARY_COLOR)
link_entry.grid(column=0, row=2, pady=10, columnspan=2)

# -- Tertiary labels --#
# - Video label -#
video_label = tb.Label(text="Video", foreground=TERTIARY_COLOR)
video_label.grid(column=0, row=3)
# - Audio Label -#
audio_label = tb.Label(text="Audio", foreground=TERTIARY_COLOR)
audio_label.grid(column=1, row=3)
# - Separator -#
separator = tb.Separator(window)
separator.grid(column=0, row=4, padx=20, pady=5, sticky='we', columnspan=2)

# - Resolution_btn -#
resolution_btn = tb.Combobox(window, style='danger', state='disabled', width=27)
resolution_btn.grid(column=0, row=5)
# - MP3 btn
audio_mp3 = tb.Combobox(window, style='danger', state='disabled', width=27)
audio_mp3.grid(column=1, row=5)
# - OGG btn -#
##------ WIP ------#
# - Download -#
download_btn = tb.Button(text='Download', width=15, style='danger', state='disabled', command=download)
download_btn.grid(column=0, row=6, ipady=5, pady=2)

download_audio_btn = tb.Button(text='Download', width=15, style='danger', state='disabled', command=download_audio)
download_audio_btn.grid(column=1, row=6, ipady=5, pady=2)
# - Status Label -#
status_label = tb.Label(text='', style='success')
status_label.grid(column=0, row=7, pady=40, columnspan=2)

window.mainloop()
