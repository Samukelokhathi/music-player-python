# pygame is for creating games or multi media
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import time
import tkinter.ttk as ttk
from mutagen.mp3 import MP3 #python module that handle Audio metaData,allows us to scan song and see length

next_time=0

# Grab song length
def play_time():
  global next_time

  global current_song_time # get current song time
  current_song_time = mixer.music.get_pos() / 1000 #to convert milliseconds to seconds
  # print(current_song_time)

    
  global converted_current_time # convert to time format
  converted_current_time = time.strftime('%M:%S', time.gmtime(current_song_time))
  # print(converted_current_time)

  # get current_song -----------------
  current_song = songList.curselection()
  # print(current_song)
  song = songList.get(current_song)
  # print(song)
  song = f'C:/Users/Xolani/Music/{song}'
  # print(song)

  # print(song)
  #-----------------------------------

  # load song  with mutagen
  song_mutagen = MP3(song)
  # print(song_mutagen)

  # get song length
  global song_length
  song_length = song_mutagen.info.length 
  # print(song_length)

  
  converted_song_length = time.strftime('%M:%S', time.gmtime(song_length)) # Convert to time format
  # print(converted_song_length)

  current_song_time += 1
  # print(int(current_song_time))

  if int(my_slider.get()) == int(song_length):

    status_bar.config(text=f'{converted_song_length} - {converted_song_length}  ') # changing text attribute to conveted_current_time_song

  elif not paused:
    pass


  elif int(my_slider.get()) == int(current_song_time):
    # print("slider hasn't moved")
    my_slider.config(to=int(song_length), value=int(current_song_time))


  else:
    # print("slider has moved")
    my_slider.config(to=int(song_length), value=int(my_slider.get()))
    
    converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
    status_bar.config(text=f'{converted_current_time} of {converted_song_length}  ') # changing text attribute to conveted_current_time_song

    # adding one to slider position
    
    next_time = int(my_slider.get()) + 1
    my_slider.config(value=next_time)
    # print(next_time)






  # output time to status bar
  # my_slider.config(value=current_song_time)
  
  # update time
  status_bar.after(1000, play_time) # return milliseconds -------------------





def load_music():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/Xolani/Music', title='Audio', filetypes=(('mp3 Files', '*.mp3'),))

    for song in songs:
        song = song.replace('C:/Users/Xolani/Music/', '') #Removing initial directory

        # append song to songList
        songList.insert(END, song) 
        # print(songList)


def play_music(time=0):


    # Opening the song
    global song
    song = songList.get(ACTIVE) #get the current clicked value on the Listbox
    song = f'C:/Users/Xolani/Music/{song}' #Return initial directory to the song

    mixer.music.load(song) #Check type of file and load for playback e.g Mp3/Video

    if time:
      print(mixer.music.play(start=time))

      # next_time = int(my_slider.get_pos()) 
      # my_slider.config(value=next_time)

    else:
      mixer.music.play()

    play_time()

    # update slider TO position
    # my_slider.config(to=int(song_length), value=0)

   
song_playing = False
paused = False #song is playing


#pause the song if it is Unpaused and unpause the song if it is paused.

paused_time=0

def pause_music():
  global paused, play_btn_img, play_button, pause_btn_img,song_playing,song ,next_time

  print(paused)
  if paused:    #if song is not playing

    play_button.config(image=play_btn_img)
    mixer.music.pause()
    print('not playing')
    paused = False 


  else:
    play_music(next_time + 1)

    play_button.config(image=pause_btn_img)
    print('playing')
    paused = True
    







def next_music():

    global pause_btn_img

    songs = songList.size() 
    next_song = songList.curselection() #Return a position of a selected item as a Tuple.

    next_song = next_song[0]+1 #Adding one to that current tuple index.Following song.
  
    if next_song +1 > songs:
      next_song = 0
    
    song = songList.get(next_song) #getting the active song
    song = f'C:/Users/Xolani/Music/{song}' #Putting back original details of a song as it saved on files.
    # print(song)


    mixer.music.load(song) #Check type of file and load for playback e.g Mp3/Video
    #

    mixer.music.play() #Plays the the loaded type of file.
    play_button.config(image=pause_btn_img)




    songList.selection_clear(0,END) #clear the active bar playlist listbox

    songList.activate(next_song) #Activate bar playlist

    songList.select_set(next_song) #Play all the listed songs
    # print(next_song)



def prev_music():
    songs = songList.size()
    # print(songs)

    prev_song = songList.curselection()
    prev_song = prev_song[0]-1
    print(prev_song)

    if prev_song  < 0:
      prev_song = songs -1

      

    song = songList.get(prev_song)
    song = f'C:/Users/Xolani/Music/{song}'
    # print(song)




    mixer.music.load(song)
    mixer.music.play()


    songList.selection_clear(0, END) #clear the active bar playlist listbox

    songList.activate(prev_song) #Activate bar playlist

    songList.select_set(prev_song) #Play all the listed songs #Tuple index will out of range if we do not include the select_set.

def slider(x):
  mixer.music.play(start=int(my_slider.get())) # get the current position of the song

def volume(x):
  mixer.music.set_volume(float(x)/100)






window = Tk()
window.title('Music player')
window.geometry('500x450') 

mixer.init() #allow us to play Audio

filePathBtn = Button(window, text='choose music',command=load_music)
filePathBtn.pack()

#stores the collection of items.
songList = Listbox(window, bg='black', fg='green',width=100,height=15) #orders the information for readability and easy to be found.
songList.pack(pady=10)

print(songList.size())



next_btn_img = PhotoImage(file='next.png')
prev_btn_img = PhotoImage(file='prev.png')
pause_btn_img = PhotoImage(file='pause.png')
play_btn_img = PhotoImage(file='play.png')

frame = Frame(window)
frame.pack()

next_button = Button(frame, image=next_btn_img, command=next_music)
pre_button = Button(frame, image=prev_btn_img, command=prev_music)
# pause_button = Button(frame, image=pause_btn_img, command=pause_music)
play_button = Button(frame, image=play_btn_img, command=pause_music)

next_button.grid(row=0, column=3, padx=10)
pre_button.grid(row=0, column=0, padx=10)
# pause_button.grid(row=0, column=2, padx=10)
play_button.grid(row=0, column=1, padx=10)

# Status bar provide information about the current state of a window.
# label widget used to display text.

status_bar = Label(window, text='status bar', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


my_slider = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL ,value=0, command=slider, length=360)
my_slider.pack(pady=10)

volume_slider = ttk.Scale(window, from_=100, to=0, orient=VERTICAL ,value=100, length=110, command=volume)
volume_slider.place(x=10, y=290)

# slider label 
# slider_label = Label(window, text='0')
# slider_label.pack(pady=20)






window.mainloop()

















