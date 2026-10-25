
# -*- coding: utf-8 -*-
'''
Interfaz Grafica Realizada Por: Israel Dryer

Adaptado y Modificado En un 90% Por: Cristian M. Veliz C.
Correo Electronico: "cristianvel2015mvc@gmail.com".
Modified: 2021-04-07
Adapted for ttkbootstrap from: https://github.com/israel-dryer/Mini-VLC-Player


"Este Reproductor de Musica y Videos, Reproduce formatos 'MP3, MP4, MKV y AVI', 
Esta Desarrollado en: "Python 3.8.3, pyInstaller 4.5", y enpaquetado con, "Setup Factory 9.5",
Versión del Software: v.20, para Windows "x64".
Fecha de Creación: "01/06/2,021"
Este Software, Esta con un Treeview, para la Info sobre los Tracks Ingresados,\
Teclas de Atajo en el Software: ESC: = Salir (cerrar app), Teclas CTRL+P: = Pause,
CTRL+O: = Buscar Archivos (*.*), Solamente se podra escoger Un Solo Archivo, Sin agregarlo a La Lista de Reproducción,
Solamente Pulsar Play y Listo,\
Ahun esta en Desarrollo.")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 → GitGraper v_1.3· 🔒 Modo Ético-Edition
🎯 → Soft - EN MEGA:
→    https://mega.nz/file/KkEXWSBB#DywciVCNulp7pmQpO0jWnBMRRe8vTXmJD1LQ3k8i95c
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
##===========================================================================================================================
##===========================================================================================================================
import tkinter
from tkinter import ttk, CENTER, TOP, BOTH, BOTTOM, RIDGE, RIGHT, VERTICAL, HORIZONTAL, X, Y, NW, INSIDE, OUTSIDE
from tkinter import Label
from tkinter import Button
from tkinter import messagebox
from tkinter import filedialog
import tkinter.simpledialog as simpledialog
##=========================================
from ttkthemes import ThemedStyle
##=========================================
import os
os.add_dll_directory(os.getcwd())
from os import path
import os, errno, sys, re
##=========================================
import vlc
##=========================================
import time
import datetime
import time
##=========================================
from PIL import Image, ImageTk
from PIL import Image as Ima
##=========================================
import queue
import pathlib
from queue import Queue
from threading import Thread
##=========================================
from pygame import mixer
##=========================================
import webbrowser as wb
##=========================================
import numpy as np
import cv2
import imutils
##===========================================================================================================================
##===========================================================================================================================
stopped = False
current_song=""
track_info=""

paused = 'play'
_stopped  = None
volMuted = False

archivo_abierto = ""
path = ""
title_app = "Media Player. (V.I.P.v20)"

player_1 = ""
innitial_dir = "/gui/desktop"
full = "normal"
current_volume = float(0.5)
mute = False

cuadros_frames_time_0 = 18
cuadros_frames_time_1 = 30
cuadros_frames_time_2 = ""
cuadros_frames_time_3 = ""
cap = None
cap_2 = None
Video_Salida = ""
frame_3 = ""
salida = ""
##===========================================================================================================================
##===========================================================================================================================
class Application(tkinter.Tk):
	def __init__(self):
		super().__init__()

		global title_app
		self.title(title_app)

		self.style = ThemedStyle(self)
		self.style.theme_use('blue')

		self.player=Player(self)

		self.player.pack(fill='both', expand='yes')
		self.style.configure('TButton', font='Helvetica 15')
#==============================================================
#==============================================================
		##Ajustando Geometry de App
		app_width = 1000    ##  1366	366
		app_height = 600	##  768		188

		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()

		x = (screen_width / 2) - (app_width / 2)
		y = (screen_height / 2) - (app_height / 2)

		self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')   ##Forma Modificada
#==============================================================
#==============================================================
		self.bind("<Control-o>", lambda e: Player.Open_songs(self, e))
		self.bind("<Control-p>", lambda e: Player.pause(self, e))
		self.bind("<Escape>", lambda e: Player.OnClose(self, e))
##===========================================================================================================================
##===========================================================================================================================
class Player(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.configure(padding=1)
##===========================================================================================================================
##===========================================================================================================================
		global volVar

		self.CurrentDate = tkinter.StringVar(value="")
		self.CurrentTime = tkinter.StringVar(value="")
		self.Fecha_Hora_Actual = tkinter.StringVar(value="")

		self.rate_mas_1 = tkinter.StringVar(value='1')
		self.rate_menos_1 = tkinter.StringVar(value='1.9')

		self.screen_width_0 = tkinter.IntVar()
		self.screen_height_0 = tkinter.IntVar()

		self.dimensiones_2 = tkinter.IntVar()

		self.file_directori = tkinter.StringVar(value='txt')
		self.search_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()))		
		self.file_Open_Browse = tkinter.StringVar(value='txt')
		self.search_term_var = tkinter.StringVar(value='txt') 
		self.search_type_var = tkinter.StringVar(value='endswidth') 
		self.search_count = 0
		self.volVar = tkinter.IntVar()

		self.timeVar = tkinter.DoubleVar()

		self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', style='success.Horizontal.TProgressbar')
##===================================================================================================================================
##===================================================================================================================================		

		#Player.Dimenciones_Imagen(self)
		self.bind('<Configure>', lambda e: Player.Dimenciones_Imagen(self, e))
		self.data_queue = queue.Queue()

		screen_width = self.winfo_screenwidth() -368				##  app_width = 1000    ##  1366	366
		screen_height = self.winfo_screenheight() -300				##  app_height = 580	##  768		188

		self.screen_width_0.set(screen_width)
		self.screen_height_0.set(screen_height)
#==============================================================
#==============================================================
		im_background = Path.resource_path('assets\\mp_background.png')
		imagen_0=Image.open(im_background)
		imagen_1=imagen_0.resize((self.screen_width_0.get(), self.screen_height_0.get()),Image.Resampling.LANCZOS)
		self.background=ImageTk.PhotoImage(imagen_1)

		self.controls = {						
						'play': 'Play',						
						'skip-next': 'Next'+' +',
						'skip-previous': 'Previous'+' -',
						'pause': 'Pause',
						'stop': 'Stop',
						'open-file': '\U0001f4c2',
						'mute': 'Mute',
						'Full-Video': 'Full Screen'}
#==============================================================
#==============================================================
		global track_info, archivo_abierto, a, b

		archivo_abierto = ""
		a = ""
		b = ""

		# track information header
		self.track_info = tkinter.StringVar(value='')
#==============================================================
#==============================================================
		# right-click menu for treeview
		self.menu = tkinter.Menu(self, tearoff=False, bg='black', fg='white')		
#==============================================================
#==============================================================
		self.menu.add_separator()
		self.menu.add_separator()
#==============================================================
#==============================================================				
		self.Menu_Selectet_Video = tkinter.Menu(self.menu, bg='black', fg='white', tearoff=False)
		self.menu.add_cascade(label='Selección De Video\\Audio:', menu = self.Menu_Selectet_Video)		
		##
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_command(label='Selected Directory MP3?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.on_browse_1(self))
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_command(label='Selected Directory MP4?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.on_browse_2(self))
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_command(label='Selected Directory MKV?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.on_browse_3(self))
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_command(label='Selected Directory AVI?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.on_browse_4(self))
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_command(label='Selected Directory (Vid.*?)', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.on_browse_5(self))
		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()
#==============================================================
#==============================================================				
		self.Menu_Selectet_Prop_Video = tkinter.Menu(self.Menu_Selectet_Video, bg='black', fg='white', tearoff=False)
		self.Menu_Selectet_Video.add_cascade(label='Selección De Fames\\Scale:', menu = self.Menu_Selectet_Prop_Video)		
		##		
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_command(label='Seleccionar Escala Mas?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.Video_Mas(self))
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_command(label='Seleccionar Escala Menos?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.Video_Menos(self))
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_command(label='Seleccionar Frame Mas?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.frame_Mas(self))
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_command(label='Seleccionar Frame Menos?', activebackground='#000080', activeforeground='#37ff37', command = lambda: Player.frame_Menos(self))
		self.Menu_Selectet_Prop_Video.add_separator()
		self.Menu_Selectet_Prop_Video.add_separator()

		self.Menu_Selectet_Video.add_separator()
		self.Menu_Selectet_Video.add_separator()		
#==============================================================
#==============================================================
		self.menu.add_separator()
		self.menu.add_separator()
		self.menu.add_command(label='Crear Captura del Video?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: Player.Cap_Pick(self))
		self.menu.add_separator()
		self.menu.add_separator()
		self.menu.add_command(label='Close Full Screen?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: Player.Sotop_Video_Now_2(self))
		self.menu.add_separator()
		self.menu.add_separator()		
		self.menu.add_command(label='Open File Video\\Audio (*.*)', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: Player.Open_songs(self))
		self.menu.add_separator()
		self.menu.add_separator()
		self.menu.add_command(label='Clean List?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: Player.clean_tree(self))
		self.menu.add_separator()
		self.menu.add_separator()
#==============================================================
#==============================================================				
		self.Menu_tut_vid = tkinter.Menu(self.menu, bg='black', fg='white', tearoff=False)
		self.menu.add_cascade(label='Obciones Vid. Tutorial:', menu = self.Menu_tut_vid)		
		##		
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_command(label='Ver Video Tutorial?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: vid_audio.tuto_vid(self))
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_command(label='Finalizar Video Tutorial?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Vid_Cam_Web_USB.Finalizar_Reproduccion(self))
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_command(label='Incrementar Vol.?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: vid_audio.increase_volume(self))
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_command(label='Decrementar Vol.?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: vid_audio.reduce_volume(self))
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_command(label='Mute Vol.?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: vid_audio.mute_vol(self))
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_command(label='Optener el Codigo Fuente.?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: Open_Cod.Open_Codigo_fuente(self))
		self.Menu_tut_vid.add_separator()
		self.Menu_tut_vid.add_separator()

		self.menu.add_separator()
		self.menu.add_separator()
#==============================================================
#==============================================================	
		self.Menu_Cam_Web_USB = tkinter.Menu(self.menu, bg='black', fg='white', tearoff=False)
		self.menu.add_cascade(label='Menu_Cam_Web_USB:', menu = self.Menu_Cam_Web_USB)		
		##		
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_command(label='Video Vigilancia?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Vid_Cam_Web_USB.En_q_win_1(self))
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_command(label='Grabar Video?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Cap_Vide_Web_USB.En_q_win_2(self))
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_command(label='Finalizar WebCam?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Vid_Cam_Web_USB.Finalizar_Reproduccion(self))
		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_separator()
#==============================================================
#==============================================================	
		self.Fotografia = tkinter.Menu(self.Menu_Cam_Web_USB, bg='black', fg='white', tearoff=False)
		self.Menu_Cam_Web_USB.add_cascade(label='Menu_Fotografia:', menu = self.Fotografia)
		#
		self.Fotografia.add_separator()
		self.Fotografia.add_separator()
		self.Fotografia.add_command(label='Capturar Fotografia?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Capturar_Im_Web_USB.En_q_win_3(self))
		self.Fotografia.add_separator()
		self.Fotografia.add_separator()
		self.Fotografia.add_command(label='Cerrar Capturar Fotografia?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Vid_Cam_Web_USB.Captura_Im_Pick(self))		
		self.Fotografia.add_separator()
		self.Fotografia.add_separator()

		self.Menu_Cam_Web_USB.add_separator()
		self.Menu_Cam_Web_USB.add_separator()
#==============================================================
#==============================================================
		self.menu.add_separator()
		self.menu.add_separator()
		self.menu.add_command(label='Info Sobre La App.?', activebackground='#37ff37', activeforeground='#0000ff', command = lambda: Player.Info_App(self))	
		self.menu.add_separator()
		self.menu.add_separator()
		self.menu.add_command(label='Exit?', activebackground='#37ff37', activeforeground='#0000ff', command= lambda: Application.quit(self))
		self.menu.add_separator()
		self.menu.add_separator()

		self.master.bind("<Button-3>", self.showMenu)
		self.pack()
#==============================================================
#==============================================================
		## CollapsingFrame Principal
		cf = CollapsingFrame(self)
		cf.pack(fill='both')
#==============================================================
#==============================================================
		# option group 1 En CollapsingFrame
		group1 = ttk.Frame(cf, padding=10)
#==============================================================
#==============================================================
		global tree_2
		# search results tree
		self.scroll_y = ttk.Scrollbar(group1,orient=VERTICAL)
		self.scroll_x = ttk.Scrollbar(group1,orient=HORIZONTAL)

		tree_2 = ttk.Treeview(group1, style='info.Treeview', height=10, takefocus=True, yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
		self.scroll_x.pack(side=BOTTOM, fill = X, expand=True)
		self.scroll_y.pack(side=RIGHT, fill = Y, expand=True)

		tree_2.pack(side=TOP, fill=BOTH,  pady=0, expand=True)
		tree_2['columns'] = ('modified', 'type', 'size', 'path')
		tree_2.column('#0', width=600, minwidth=10, anchor=CENTER)
		tree_2.column('modified',  width=200, minwidth=10, anchor=CENTER, stretch=False) 
		tree_2.column('type',  width=50, minwidth=10, anchor=CENTER, stretch=False) 
		tree_2.column('size',  width=100, minwidth=10, anchor=CENTER, stretch=False)
		tree_2.column('path',  width=600, minwidth=10, anchor=CENTER, stretch=False) 
		tree_2.heading('#0', text='Name')
		tree_2.heading('modified',  text='Modified date') 
		tree_2.heading('type',  text='Type') 
		tree_2.heading('size',  text='Size') 
		tree_2.heading('path',  text='Path')

		self.scroll_y.config(command=tree_2.yview)
		self.scroll_x.config(command=tree_2.xview)

		s = ttk.Style()
		s.configure('TScrollbar', background='#9F9E9E')
		s.configure('TScrollbar', background='#9F9E9E')

		tree_2.bind("<ButtonRelease-1>", lambda e: Player.open_file(self, e))
#==============================================================
#==============================================================
		cf.add(group1, title=self.track_info.get(), style='primary.TButton')
#==============================================================
#==============================================================
		# media container
		self.container = Label(self, image=self.background, justify=CENTER, bg='#6d9bcd')
		self.container.pack(fill=BOTH, expand=True, pady=0)
#==============================================================
#==============================================================
#==============================================================
#==============================================================
		## CollapsingFrame Principal
		cf_2 = CollapsingFrame(self)
		cf_2.pack(fill='both')
#==============================================================
#==============================================================
		# option group 1 En CollapsingFrame
		group2 = ttk.Frame(cf_2, padding=5)
#==============================================================
#==============================================================
		# progress bar		
		self.volSlider = tkinter.Scale(group2, variable=self.volVar, command=self.OnVolume,
			from_=0, to=200, orient=tkinter.HORIZONTAL, length=500, showvalue=0, label='Volume')
		self.volVar.set(100)
		self.volSlider.configure(background='#808080', foreground='#80ff00')
		self.volSlider.pack(fill=BOTH, expand=True, padx=0, pady=0)
#==============================================================
#==============================================================
		cf_2.add(group2, title="Botones de Control", style='primary.TButton')
#==============================================================
#==============================================================
		##Label y SCale, Para El Posiciónamiento en el Video
		self.lbl_time = ttk.Label(self, text = "Tiempo De Rep. : 00:00:00")   ##text = "<<Slaid Poss:>>")
		self.lbl_time.place(x=11, y=6, bordermode=INSIDE, anchor=NW)

		# progress bar		
		self.timeSlider = tkinter.Scale(self, variable=self.timeVar, command=self.OnTime,
			from_=0, to=1000, orient=tkinter.HORIZONTAL, length=500, showvalue=0)
		self.timeSliderLast = 0
		self.timeSliderUpdate = time.time()

		##Label y SCale, Para El Posiciónamiento en el Video
		self.lbl_time_2 = ttk.Label(self, text = "Tiempo Transcurrido : 00:00:00")   ##text = "<<Slaid Poss:>>")		
##===========================================================================================================================
##===========================================================================================================================
		# button controls
		control_frame = ttk.Frame(self) 
		control_frame.pack(fill='x',expand='yes')
		self.buttons = {
						'play': ttk.Button(control_frame,  text=self.controls['play'],command=self.play_songs),
						'skip-previous': ttk.Button(control_frame,  text=self.controls['skip-previous'], command=self.Anterior),
						'skip-next': ttk.Button(control_frame,  text=self.controls['skip-next'], command=self.Siguiente),
						'pause': ttk.Button(control_frame,  text=self.controls['pause'],command=self.pause),
						'stop': ttk.Button(control_frame,  text=self.controls['stop'],command=self.stop),
						'open-file': ttk.Button(control_frame,  text=self.controls['open-file'],style='TButton',command=self.on_browse_5),
						'Full-Video': ttk.Button(control_frame,  text=self.controls['Full-Video'], command=self.Stop_Play_Video),						
						'Mute': ttk.Button(control_frame,  text=self.controls['mute'],style='TButton',command=self.OnMute)}

		for button in ['skip-previous', 'play', 'pause', 'stop', 'skip-next', 'open-file', 'Mute', 'Full-Video']:		 

			self.buttons[button].pack(side='left', fill='x', expand='yes', ipadx=5,ipady=5, padx=2, pady=0)
##===========================================================================================================================
##===========================================================================================================================
	def Info_App(self, e = None):
		messagebox.showinfo("INFO", "Este Reproductor de Musica y Videos, Reproduce formatos \'MP3, MP4, MKV y AVI\', Esta Desarrollado en: \"Python 3.8.3, pyInstaller 4.5\", y enpaquetado con, \"Setup Factory 9.5\",\
				\nEsta Desarrollado Por:\n\"Cristian M. Veliz Cano\",\n\nCorreo Electronico:\n\"cristianvel2015mvc@gmail.com\".\
				\nVersión del Software:\nv.20, para Windows \"(\'7sp1\', \'W-8\', \'W-8.1\', y \'W-10 (\'x64bits\'))\".\n\nFecha de Creación:\n\"01/06/2,021\"\
				\n\nEste Software, Esta con un Treeview, para la Info sobre los Tracks Ingresados,\
				\n\nTeclas de Atajo en el Software: \nESC: = Salir (cerrar app),\nTeclas CTRL+P: = Pause,\nCTRL+O: = Buscar Archivos (*.*), \nSolamente se podra escoger Un Solo Archivo,\nSin agregarlo a La Lista de Reproducción,\nSolamente Pulsar Play y Listo,\
				\n\nAhun esta en Desarrollo.")
##===========================================================================================================================
##===========================================================================================================================
	def showMenu(self, e):
		self.menu.post(e.x_root, e.y_root)

	def Dimenciones_Imagen(self, e = None):
		global screen_width_0, screen_height_0, cuadros_frames_time_2, cuadros_frames_time_3

		ico_app = Path.resource_path('Icon\\1.ico')
		self.master.iconbitmap(ico_app)

		print(e.width)
		print(e.height)

		screen_width = e.width
		screen_height = e.height -110

		cuadros_frames_time_2 = screen_width
		cuadros_frames_time_3 = screen_height

		self.screen_width_0.set(screen_width)
		self.screen_height_0.set(screen_height)

		im_background = Path.resource_path('assets\\mp_background.png')
		imagen_0=Image.open(im_background)
		imagen_1=imagen_0.resize((self.screen_width_0.get(), self.screen_height_0.get()),Image.Resampling.LANCZOS)
		self.background=ImageTk.PhotoImage(imagen_1)

		self.container.configure(image=self.background)

		screen_width_poss = e.width -375
		self.timeSlider.place(x=155, y=5, height=20, width=int(screen_width_poss), anchor=NW, bordermode=OUTSIDE)

		##Tiempo Transcurrido
		screen_width_poss_2 = e.width -218
		self.lbl_time_2.place(x=int(screen_width_poss_2), y=6, bordermode=INSIDE, anchor=NW)

	def Open_songs(self, e=None):
		global archivo_abierto, innitial_dir

		archivo_abierto=filedialog.askopenfilename(initialdir = innitial_dir,
		title = "Seleccione Archivo",filetypes = (("Files Video","*.mp4"),("Files Video","*.mkv"),("Files Video","*.avi"),("Files Audio","*.mp3"),
		("All Files","*.*")))

	def play_songs(self, e=None):
		global player, archivo_abierto, container, player_1, full

		print(archivo_abierto)		

		if archivo_abierto == "":
			pass
		else:
			if player_1 == "":
				txt_title1 = archivo_abierto
				txt_title2 = txt_title1.split("\\")
				txt_title3 = txt_title2[-1]				
				self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

				player_1 = "algo"
				print(player_1)
				full = "normal"
				try:
					# Create a basic vlc instance
					instance = vlc.Instance('--verbose 3')
			        # Create an empty vlc media player
					player = instance.media_player_new()
					player.set_mrl(archivo_abierto)

					h = self.container.winfo_id()
					player.set_hwnd(h)
					player.set_xwindow(h)

					Player.OnVolume(self)
					player.toggle_teletext()

					player.play()	  
					time.sleep(5)
					
					player.video_set_mouse_input(True)
					player.video_set_key_input(True)
					self.update()

					self.OnTick()				

				except Exception as e:
					print(e)
				else:
					pass
				finally:
					pass
			else:
				pass

	def Cap_Pick(self):
		global player_1, innitial_dir

		if player_1 == "":
			pass
		else:
			if paused == 'play':
				Player.pause(self)

			dir_salida=filedialog.asksaveasfilename(title="Guardar Como", initialdir = innitial_dir, defaultextension=".png",  
	                filetypes = (("PNG files", "*.png"),("all files", "*.*")))

			num = 0
			psz_filepath = dir_salida
			i_width = int(1920)		## Ancho
			i_height = int(1200)   	## Alto		

			player.video_take_snapshot(num, psz_filepath, i_width, i_height)

			Player.pause(self)

	def Stop_Play_Video(self):
		global player, archivo_abierto, full

		Player.pause(self)
		player.stop()
		print(archivo_abierto)
		txt_title1 = archivo_abierto
		txt_title2 = txt_title1.split("\\")
		txt_title3 = txt_title2[-1]				
		self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")	

		self.timeSlider.set(0)
		player_1 = "algo"
		print(player_1)

		full = "full"

		if archivo_abierto == "":
			pass
		else:
			try:
				# Create a basic vlc instance
				instance = vlc.Instance('--verbose 3')
		        # Create an empty vlc media player
				player = instance.media_player_new()
				player.set_mrl(archivo_abierto)
				player.set_fullscreen(True)				

				Player.OnVolume(self)
				player.toggle_teletext()

				player.play()	  
				time.sleep(5)
				
				player.video_set_mouse_input(True)
				player.video_set_key_input(True)
				self.update()

				self.OnTick()

			except Exception as e:
				print(e)
			else:
				pass
			finally:
				pass
#==============================================================
#==============================================================
	def pause(self, e = None):
		global player, paused, archivo_abierto

		if archivo_abierto == "":
			pass
		else:

			try:
				if paused == 'pause':
					player.set_pause(0)
					paused = 'play'
					print(paused)
					_stopped = False
					mixer.music.unpause()

				else: #paused == 'play':
					player.set_pause(1)
					paused = 'pause'
					print(paused)
					_stopped = False
					mixer.music.pause()

			except Exception as e:
				print(e)
#==============================================================
#==============================================================
	def OnClose(self, e=None):
	    """Closes the window and quit."""
	    print("Salir")
	    self.quit()
#==============================================================
#==============================================================
	def OnMute(self, e=None):
		global volMuted, player, archivo_abierto

		if archivo_abierto == "":
			pass
		else:
			"""Mute/Unmute audio."""
		    # audio un/mute may be unreliable, see vlc.py docs.
			volMuted = m = not volMuted  # player.audio_get_mute()
			player.audio_set_mute(m)
			Player.OnVolume(self)
#==============================================================
#==============================================================
	def stop(self, e=None):
		global player, v_M, archivo_abierto, player_1, mute
		"""Stop the player, resets media."""
		if archivo_abierto == "":
			pass
		else:
			self.master.title(f"Media Player. (V.I.P.v20)")
			player.stop()
			_stopped = True

			self.timeSlider.set(0)

			try:
				mixer.music.stop()
				mute = False
			except Exception as e:
				print(e)
		
		vol = min(self.volVar.get(), 200)
		v_M = "%d%s" % (vol, " (Muted)" if volMuted else '')
		self.track_info.set(value = "Volume " + v_M + "  \\\\  Open  a file to begin playback")
		self.volSlider.config(label=self.track_info.get())
		self.lbl_time_2.config(text="Tiempo Transcurrido : 00:00:00")
		self.lbl_time.config(text="Tiempo De Rep. : 00:00:00")

		archivo_abierto = None
		archivo_abierto = ""
		print(archivo_abierto)

		player_1 = None
		player_1 = ""
		print(player_1)

		Player.Sotop_Video_Now_2(self)
#==============================================================
#==============================================================
	def OnVolume(self, e = None):
		global player, archivo_abierto, v_M, volVar
		"""Volume slider changed, adjust the audio volume."""
		if archivo_abierto == "":
			pass
		else:

			txt_title1 = archivo_abierto
			txt_title2 = txt_title1.split("\\")
			txt_title3 = txt_title2[-1]

			vol = min(self.volVar.get(), 200)
			v_M = "%d%s" % (vol, " (Muted)" if volMuted else '')
			self.volSlider.config(label="Volume " + v_M + "  \\  %s" % (txt_title3))

			if player and not _stopped:
				if player.audio_set_volume(vol):  # and player.get_media():
					showError("Failed to set the volume: %s." % (v_M,))
#==============================================================
#==============================================================
	def frame_Mas(self):
		global a, player, archivo_abierto

		if archivo_abierto == "":
			pass
		else:

			a = float(self.rate_mas_1.get())
			a += 0.5

			print(float(a))
			self.rate_mas_1.set(str(a))

			player.set_rate(float(a))

	def frame_Menos(self):
		global a, player, archivo_abierto

		if archivo_abierto == "":
			pass
		else:

			a = float(self.rate_mas_1.get())
			a -= 0.5
			
			print(float(a))
			self.rate_mas_1.set(str(a))

			player.set_rate(float(a))
#==============================================================
#==============================================================
	def Video_Mas(self):
		global b, player, archivo_abierto

		if archivo_abierto == "":
			pass
		else:

			b = float(self.rate_menos_1.get())
			b += 0.1

			print(float(b))
			self.rate_menos_1.set(str(b))

			player.video_set_scale(float(b))

	def Video_Menos(self):
		global b, player, archivo_abierto

		if archivo_abierto == "":
			pass
		else:

			b = float(self.rate_menos_1.get())
			b -= 0.1
			
			print(float(b))
			self.rate_menos_1.set(str(b))

			player.video_set_scale(float(b))
#==============================================================
#==============================================================
	def Sotop_Video_Now(self):
		global player, v_M, archivo_abierto, volVar, mute

		if archivo_abierto == "":
			pass
		else:
			self.master.title(f"Media Player. (V.I.P.v20)")
			try:
				mixer.music.stop()
				mute = False
			except Exception as e:
				print(e)

			player.stop()

			self.timeSlider.set(0)

			vol = min(self.volVar.get(), 200)
			v_M = "%d%s" % (vol, " (Muted)" if volMuted else '')
			self.track_info.set(value = "Volume " + v_M + "  \\\\  Push Play")
			self.volSlider.config(label=self.track_info.get())

			self.lbl_time_2.config(text="Tiempo Transcurrido : 00:00:00")
			self.lbl_time.config(text="Tiempo De Rep. : 00:00:00")

			archivo_abierto = None
			archivo_abierto = ""
			print(archivo_abierto)

	def Sotop_Video_Now_2(self):
		global player, archivo_abierto, player_1, full, mute 

		if archivo_abierto == "":
			pass
		else:
			self.master.title(f"Media Player. (V.I.P.v20)")
			try:
				mixer.music.stop()
				mute = False
			except Exception as e:
				print(e)

			player.stop()
			player_1 = None
			player_1 = ""
			print(player_1)
			full = "normal"

			self.timeSlider.set(0)
			self.lbl_time_2.config(text="Tiempo Transcurrido : 00:00:00")
			self.lbl_time.config(text="Tiempo De Rep. : 00:00:00")
#==============================================================
#==============================================================	
	def OnTick(self):
		global player, converted_current_time_1, converted_current_time_2
		"""Timer tick, update the time slider to the video time."""
		if archivo_abierto == "":
			pass
		else:
            # since the self.player.get_length may change while
            # playing, re-set the timeSlider to the correct range
			t = player.get_length() * 1e-3 # to seconds
			if t > 0:
				self.timeSlider.config(to=t)				

				converted_current_time_1 = time.strftime('%H:%M:%S', time.gmtime(int(t-1)))	
				#Ouput time to Reproducido
				self.lbl_time.configure(text="Tiempo De Rep. : {}".format(converted_current_time_1))

				converted_current_time_2 = time.strftime('%H:%M:%S', time.gmtime(int(self.timeSlider.get())))	
				#Tiempo De Reproduccion
				self.lbl_time_2.configure(text="Tiempo Transcurrido : {}".format(converted_current_time_2))

				if converted_current_time_2 >= converted_current_time_1:
					##print(f'Tiempo Transcurrido: {converted_current_time_2}  De: {converted_current_time_1}')
					self.lbl_time_2.config(text="Tiempo Transcurrido : "+str(converted_current_time_2))
					self.lbl_time.config(text="Tiempo De Rep. : "+str(converted_current_time_1))
					Player.Verificacion_Full_Normal(self)
					pass
				else:

					t = player.get_time() * 1e-3  # to seconds
	                # don't change slider while user is messing with it
					if t > 0 and time.time() > (self.timeSliderUpdate + 1):
						self.timeSlider.set(t)
						self.timeSliderLast = int(self.timeVar.get())
					
        # start the 1 second timer again
		self.master.after(1000, self.OnTick)

	def OnTime(self, *unused):
		if player:
			t = self.timeVar.get()		
			if self.timeSliderLast != int(t):
                # this is a hack. The timer updates the time slider.
                # This change causes this rtn (the 'slider has changed' rtn)
                # to be invoked.  I can't tell the difference between when
                # the user has manually moved the slider and when the timer
                # changed the slider.  But when the user moves the slider
                # tkinter only notifies this rtn about once per second and
                # when the slider has quit moving.
                # Also, the tkinter notification value has no fractional
                # seconds.  The timer update rtn saves off the last update
                # value (rounded to integer seconds) in timeSliderLast if
                # the notification time (sval) is the same as the last saved
                # time timeSliderLast then we know that this notification is
                # due to the timer changing the slider.  Otherwise the
                # notification is due to the user changing the slider.  If
                # the user is changing the slider then I have the timer
                # routine wait for at least 2 seconds before it starts
                # updating the slider again (so the timer doesn't start
                # fighting with the user).
				player.set_time(int(t * 1e3))  # milliseconds
				self.timeSliderUpdate = time.time()
#==============================================================
#==============================================================
	def clean_tree(self, event=None):
		tree_2.delete(*tree_2.get_children())

	def open_file(self, event=None):
		global path, archivo_abierto, player_1

		if path == "":
			pass
		else:
			archivo_abierto = ""
			
			Player.Sotop_Video_Now(self)

			viewinfo = tree_2.focus()
			viewinfo = tree_2.focus(viewinfo)
			
			try:
				viewinfo = tree_2.focus()
			except Exception as e:			
				print(e)
				messagebox.showerror('Error', 'Error: ' + e)
				return
			else:
				learnerData = tree_2.item(viewinfo)
				row = learnerData['values']
				sb=row
				file_path = sb[3]
				print(file_path)

				archivo_abierto = file_path
				player_1 = ""
				print(player_1)

	def on_browse_1(self):
		global search_path_var, path, innitial_dir
		"""Callback for directory browse""" 
		path = filedialog.askdirectory(title='Directory', initialdir = innitial_dir)

		if path:
			self.search_path_var.set(path)
			self.search_term_var.set('mp3')
			self.search_type_var.set("contains")
			Player.on_search(self)

	def on_browse_2(self):
		global search_path_var, path, innitial_dir
		"""Callback for directory browse""" 
		path = filedialog.askdirectory(title='Directory', initialdir = innitial_dir)

		if path:
			self.search_path_var.set(path)
			self.search_term_var.set('mp4')
			self.search_type_var.set("contains")
			Player.on_search(self)

	def on_browse_3(self):
		global search_path_var, path, innitial_dir
		"""Callback for directory browse""" 
		path = filedialog.askdirectory(title='Directory', initialdir = innitial_dir)

		if path:
			self.search_path_var.set(path)
			self.search_term_var.set('mkv')
			self.search_type_var.set("contains")
			Player.on_search(self)

	def on_browse_4(self):
		global search_path_var, path, innitial_dir
		"""Callback for directory browse""" 
		path = filedialog.askdirectory(title='Directory', initialdir = innitial_dir)

		if path:
			self.search_path_var.set(path)
			self.search_term_var.set('avi')
			self.search_type_var.set("contains")
			Player.on_search(self)

	def on_browse_5(self):
		global search_path_var, path, innitial_dir
		new_name = simpledialog.askstring("Rename", "Enter new name")

		"""Callback for directory browse""" 
		path = filedialog.askdirectory(title='Directory', initialdir = innitial_dir)

		if path:
			self.search_path_var.set(path)
			self.search_term_var.set(str(new_name))
			self.search_type_var.set("contains")
			Player.on_search(self)

	def on_search(self):
		"""Search for a term based on the search type"""   #find_contains

		search_term = self.search_term_var.get() 
		search_path = self.search_path_var.get()
		search_type = self.search_type_var.get()

		print(search_term)
		print(search_path)
		print(search_type)

		if search_term == '':
			return

		Thread(target=Player.file_search, args=(search_term, search_path, search_type), daemon=True).start() 
		self.progressbar.start(10) 
		self.search_count += 1
		id = tree_2.insert('', 'end', self.search_count, text=f'Search {self.search_count}')
		print(id)
		tree_2.item(id, open=True)
		self.check_queue(id)

	def check_queue(self, id):
		"""Check file queue and print results if not empty"""
		if searching and not file_queue.empty():
			filename = file_queue.get()
			self.insert_row(filename,  id) 
			self.update_idletasks()
			self.after(1, lambda: self.check_queue(id))

		elif not searching and not file_queue.empty():
			while not file_queue.empty(): 
				filename = file_queue.get() 
				self.insert_row(filename,  id)

			self.update_idletasks()
			self.progressbar.stop()

		elif searching and file_queue.empty():
			self.after(100, lambda: self.check_queue(id))
		else:
			self.progressbar.stop()

	def insert_row(self, file, id):
		global iid
		"""Insert new row in tree search results"""
		try:
			file_stats = file.stat()
			file_name = file.stem
			file_modified = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%m/%d/%Y %I:%M:%S%p')
			file_type = file.suffix.lower()
			file_size = Player.convert_size(file_stats.st_size)
			file_path = file.absolute()

			iid = tree_2.insert(id, 'end', text=file_name, values=(file_modified,file_type, file_size, file_path))
			tree_2.selection_set(iid)
			tree_2.see(iid)

		except OSError:
			return

	@staticmethod
	def file_search(term, search_path, search_type): 
	##"""Recursively search directory for matching files""" 
		Player.set_searching(1)
		if search_type == 'contains': 
			Player.find_contains(term, search_path)

	@staticmethod
	def find_contains(term, search_path):
		"""Find all files that contain the search term"""
		for path, _, files in pathlib.os.walk(search_path):
			if files:
				for file in files:
					if term in file:
						file_queue.put(pathlib.Path(path) / file) 
		Player.set_searching(False)
		 
	@staticmethod
	def set_searching(state=False): 
		#"""Set searching status""" 
		global searching

		searching = state

	@staticmethod
	def convert_size(size):
		"""Convert bytes to mb or kb depending on scale"""
		kb = size // 1000
		mb = round(kb / 1000, 1)
		if kb > 1000:
			return f'{mb:,.1f} MB'
		else:
			return f'{kb:,d} KB'
#==============================================================
#==============================================================
	def Verificacion_Full_Normal(self):
		global full

		if full == "normal":
			Player.Siguiente(self)
		elif full == "full":
			Player.Siguiente_Full(self)

#Play The Next Song in tehe playlist
	def Siguiente(self):
		global path, archivo_abierto, player_1, player, container

		if path =="":
			pass
		else:
			Player.Sotop_Video_Now(self)

			viewinfo = tree_2.focus()
			iid = tree_2.next(viewinfo)
			tree_2.selection_remove(viewinfo)
			tree_2.selection_add(iid)

			tree_2.set(iid)
			tree_2.selection_set(iid)
			tree_2.focus(iid)

			try:
				viewinfo = tree_2.focus()
			except Exception as e:
				print(e)
				messagebox.showerror('Error', 'Error: ' + e)
				return
			else:

				learnerData = tree_2.item(viewinfo)
				row = learnerData['values']
				sb=row
				if sb == "":
					pass
				else:
					file_path = sb[3]
					print(file_path)
					
					archivo_abierto = file_path					
					txt_title1 = archivo_abierto
					txt_title2 = txt_title1.split("\\")
					txt_title3 = txt_title2[-1]				
					self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

					try:
						# Create a basic vlc instance
						instance = vlc.Instance('--verbose 3')
				        # Create an empty vlc media player
						player = instance.media_player_new()
						player.set_mrl(archivo_abierto)

						h = self.container.winfo_id()
						player.set_hwnd(h)
						player.set_xwindow(h)

						Player.OnVolume(self)
						player.toggle_teletext()

						player.play()	  
						#time.sleep(5)
						
						player.video_set_mouse_input(True)
						player.video_set_key_input(True)
						self.update()

						self.OnTick()				

					except Exception as e:
						print(e)
					else:
						pass
					finally:
						pass

					player_1 = "algo"
					print(player_1)


	#Play The Previus Song in the playlist
	def Anterior(self):
		global path, archivo_abierto, player_1, player, container

		if path == "":
			pass
		else:
			Player.Sotop_Video_Now(self)

			viewinfo = tree_2.focus()
			iid = tree_2.prev(viewinfo)
			tree_2.selection_remove(viewinfo)
			tree_2.selection_add(iid)

			tree_2.set(iid)
			tree_2.selection_set(iid)
			tree_2.focus(iid)

			try:
				viewinfo = tree_2.focus()
			except Exception as e:
				print(e)
				messagebox.showerror('Error', 'Error: ' + e)
				return
			else:
				learnerData = tree_2.item(viewinfo)
				row = learnerData['values']
				sb=row
				file_path = sb[3]
				print(file_path)

				archivo_abierto = file_path				
				txt_title1 = archivo_abierto
				txt_title2 = txt_title1.split("\\")
				txt_title3 = txt_title2[-1]				
				self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

				try:
					# Create a basic vlc instance
					instance = vlc.Instance('--verbose 3')
			        # Create an empty vlc media player
					player = instance.media_player_new()
					player.set_mrl(archivo_abierto)

					h = self.container.winfo_id()
					player.set_hwnd(h)
					player.set_xwindow(h)

					Player.OnVolume(self)
					player.toggle_teletext()

					player.play()	  
					#time.sleep(5)
					
					player.video_set_mouse_input(True)
					player.video_set_key_input(True)
					self.update()

					self.OnTick()				

				except Exception as e:
					print(e)
				else:
					pass
				finally:
					pass

				player_1 = "algo"
				print(player_1)
#==============================================================
#==============================================================
#Play The Next Song in tehe playlist
	def Siguiente_Full(self):
		global path, archivo_abierto, player_1, player, container

		if path =="":
			pass
		else:
			Player.Sotop_Video_Now(self)

			viewinfo = tree_2.focus()
			iid = tree_2.next(viewinfo)
			tree_2.selection_remove(viewinfo)
			tree_2.selection_add(iid)

			tree_2.set(iid)
			tree_2.selection_set(iid)
			tree_2.focus(iid)

			try:
				viewinfo = tree_2.focus()
			except Exception as e:
				print(e)
				messagebox.showerror('Error', 'Error: ' + e)
				return
			else:

				learnerData = tree_2.item(viewinfo)
				row = learnerData['values']
				sb=row
				file_path = sb[3]
				print(file_path)
				
				archivo_abierto = file_path								
				txt_title1 = archivo_abierto
				txt_title2 = txt_title1.split("\\")
				txt_title3 = txt_title2[-1]				
				self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

				try:
					# Create a basic vlc instance
					instance = vlc.Instance('--verbose 3')
			        # Create an empty vlc media player
					player = instance.media_player_new()
					player.set_mrl(archivo_abierto)
					player.set_fullscreen(True)

					Player.OnVolume(self)
					player.toggle_teletext()

					player.play()	  
					#time.sleep(5)
					
					player.video_set_mouse_input(True)
					player.video_set_key_input(True)
					self.update()

					self.OnTick()				

				except Exception as e:
					print(e)
				else:
					pass
				finally:
					pass

				player_1 = "algo"
				print(player_1)
##===========================================================================================================================
##===========================================================================================================================
class Ingresando_Datos_En_Tree():
	
	def in_tree_vidaudio_vidtuto(self):

		vid_open = Path.resource_path('vid_tuto')
		self.search_path_var.set(vid_open)
		self.search_term_var.set('mp4v')
		self.search_type_var.set("contains")
		Player.on_search(self)
##===========================================================================================================================
##===========================================================================================================================
class Path():
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            #PyInstaller Create a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
##===========================================================================================================================
##===========================================================================================================================
class vid_audio():

	def tuto_vid(self, e=None):
		global cap, archivo_abierto, path
		Ingresando_Datos_En_Tree.in_tree_vidaudio_vidtuto(self)

		vid_open = Path.resource_path('vid_tuto\\vid_tuto.mp4')
		archivo_abierto = vid_open
		path = 	vid_open

		tkinter.messagebox.showinfo("Aviso", "Pedes ver el Video Tutorial desde la app,\no desde un Reproductor Exteno?")
		sResprint = tkinter.messagebox.askyesno('Pregunta', 'Desde la App.? \\"SI\\"\no:\nDesde  Repr. Exteno\\"NO\\"')
		if sResprint >0:
		
			txt_title1 = archivo_abierto
			txt_title2 = txt_title1.split("\\")
			txt_title3 = txt_title2[-1]				
			self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

			vid_audio.audio_vid(self)
			vid_audio.mute_vol(self)
			Player.play_songs(self)
		else:
			vid_audio.audio_vid(self)
			vid_audio.mute_vol(self)
			cap = cv2.VideoCapture(archivo_abierto)
			vid_audio.visualizar_rep_unitaria(self)

	def visualizar_rep_unitaria(self, *args, **kwargs):
		global cap, cuadros_frames_time_2, cuadros_frames_time_3
		if cap is not None:
			ret, frame = cap.read()
			
			x = int(cuadros_frames_time_2)
			y = int(cuadros_frames_time_3)

			fra = 30
			if ret == True:
				frame = imutils.resize(frame, width=int(x), height=int(y))
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

				im = Image.fromarray(frame)
				self.img = ImageTk.PhotoImage(image=im)

				self.container.configure(image=self.img)
				self.container.image = self.img
				self.container.after(int(fra), lambda: vid_audio.visualizar_rep_unitaria(self))
			else:
				im_background = Path.resource_path('assets\\mp_background.png')
				imagen_0=Image.open(im_background)
				imagen_1=imagen_0.resize((self.screen_width_0.get(), self.screen_height_0.get()),Image.Resampling.LANCZOS)
				self.background=ImageTk.PhotoImage(imagen_1)

				self.container.configure(image=self.background)

				tkinter.messagebox.showinfo("Aviso","La Reproducción a Finalizado")
				cap.release()
		else:
			pass

	def audio_vid(self):
		try:
			current_song = Path.resource_path('audio_vid\\audio_vid.mp3')
			mixer.init()
			mixer.music.load(current_song)
			mixer.music.play()			

		except Exception as e:
			print(e)

	def reduce_volume(self):
		global current_volume
		print(current_volume)
		try:
			if current_volume <=0:
				return

			current_volume_1 = current_volume - float(0.1)
			current_volume = round(current_volume_1,1)
			mixer.music.set_volume(current_volume)
			print(current_volume)
	        
		except Exception as e:
			print(e)

	def mute_vol(self):
		global mute, current_volume
		if mute == True:
			print('Mute Audio')
			current_volume_1 = float(0.0)
			mixer.music.set_volume(current_volume_1)
			mute = False
			print(mute)
		else:
			print(mute)
			mixer.music.set_volume(current_volume)
			mute = True
			print(mute)	        

	def increase_volume(self):
		global current_volume
		print(current_volume)
		try:
			if current_volume >=1:
				return

			current_volume_1 = current_volume + float(0.1)
			current_volume = round(current_volume_1,1)
			mixer.music.set_volume(current_volume)
			print(current_volume)
	        
		except Exception as e:
			print(e)
##===========================================================================================================================
##===========================================================================================================================
class Open_Cod():

	def Open_Codigo_fuente(self):
		Open_Master_Code = Path.resource_path('code\\1-Reproductor MP4_v20_Portable.exe')
		wb.open_new(Open_Master_Code)
##===========================================================================================================================
##===========================================================================================================================
class Vid_Cam_Web_USB():

	def En_q_win_1(self):
		tkinter.messagebox.showwarning("Aviso", "Esta Opción, No Grabara Ningun Video\nEs Solamente, Para Vigilancia\no como Espejo.")
		sResprint = tkinter.messagebox.askyesno('Pregunta', 'Windows 7 \\"SI\\"\no:\nWindows 10 \\"NO\\"')
		if sResprint >0:
			Vid_Cam_Web_USB.Chec_Cam_P_Video_W7(self)
		else:
			Vid_Cam_Web_USB.Chec_Cam_P_Video_W10(self)

	def Chec_Cam_P_Video_W7(self):
		global cap
        ##Codigo Para Cam en Windows 7
		cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
		Vid_Cam_Web_USB.Chec_Cam_P_Video_Cam(self)

	def Chec_Cam_P_Video_W10(self):
		global cap
        ##Codigo Para Cam en Windows 10
		cap=cv2.VideoCapture(0)
		Vid_Cam_Web_USB.Chec_Cam_P_Video_Cam(self)            

	def Chec_Cam_P_Video_Cam(self):
		global cap, cuadros_frames_time_2, cuadros_frames_time_3

		if cap == None:
			print('Cerro la Cam.')
			pass

		elif cap is not None:
			print(cap)
			resp=cap.isOpened()
			if resp==True:
				
				ret, frame_1 = cap.read()

				x = int(cuadros_frames_time_2)  -100
				y = int(cuadros_frames_time_3)

				fra=10
				if ret == True:
					frame_2 = imutils.resize(frame_1, width=int(x), height=int(y))
					frame_3 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)

					im = Image.fromarray(frame_3)
					self.img = ImageTk.PhotoImage(image=im)

					#lblVideo.configure(image=img)
					self.container.configure(image=self.img)
					self.container.image = self.img
					self.container.after(int(fra), lambda: Vid_Cam_Web_USB.Chec_Cam_P_Video_Cam(self))
				else:					
					pass

			elif resp == None:
				tkinter.messagebox.showinfo("Info","Al parecer No Tienes la Camara Conectada\no no se Encuentra en buen Estado")
			elif resp == "":
				tkinter.messagebox.showinfo("Info","Al parecer No Tienes la Camara Conectada\no no se Encuentra en buen Estado")
			elif resp == False:
				tkinter.messagebox.showinfo("Info","Al parecer No Tienes la Camara Conectada\no no se Encuentra en buen Estado")

	def Finalizar_Reproduccion(self):
		global cap, salida

		if cap is not None:
			video_path = ""				
			cap.release()
			cap = None

			im_background = Path.resource_path('assets\\mp_background.png')
			imagen_0=Image.open(im_background)
			imagen_1=imagen_0.resize((self.screen_width_0.get(), self.screen_height_0.get()),Image.Resampling.LANCZOS)
			self.background=ImageTk.PhotoImage(imagen_1)

			self.container.configure(image=self.background)
			self.master.title(f"Media Player. (V.I.P.v20)")

			try:
				mixer.music.stop()
			except Exception as e:
				print(e)

		if salida == "":
			pass
		else:
			salida.release()

			im_background = Path.resource_path('assets\\mp_background.png')
			imagen_0=Image.open(im_background)
			imagen_1=imagen_0.resize((self.screen_width_0.get(), self.screen_height_0.get()),Image.Resampling.LANCZOS)
			self.background=ImageTk.PhotoImage(imagen_1)

			self.container.configure(image=self.background)
			self.master.title(f"Media Player. (V.I.P.v20)")

	def Captura_Im_Pick(self):
		global cap_2, captura, frame_3
		if cap_2 == "":
			pass
		else:			
			print(captura)
			print(frame_3)
			cv2.imwrite(captura,frame_3)
			cap_2.release()
			tkinter.messagebox.showinfo("Information", "Done")

			im_background = Path.resource_path('assets\\mp_background.png')
			imagen_0=Image.open(im_background)
			imagen_1=imagen_0.resize((self.screen_width_0.get(), self.screen_height_0.get()),Image.Resampling.LANCZOS)
			self.background=ImageTk.PhotoImage(imagen_1)

			self.container.configure(image=self.background)

			View_Recien_Pick.Recien_Pick(self)
			self.master.title(f"Media Player. (V.I.P.v20)")
##===========================================================================================================================
##===========================================================================================================================
class Cap_Vide_Web_USB():

	def En_q_win_2(self):
		global Video_Salida, salida, cuadros_frames_time_1, innitial_dir

		sResprint = tkinter.messagebox.askyesno('Pregunta', 'Windows 7 \\"SI\\"\no:\nWindows 10 \\"NO\\"')
		Video_Salida=filedialog.asksaveasfilename(title="Guardar Como",initialdir = innitial_dir, defaultextension=".mp4v",\
	                filetypes = (("MP4v Files","*.mp4v"),("AVI Files","*.avi")))

		txt_title1 = Video_Salida
		txt_title2 = txt_title1.split("/")
		txt_title3 = txt_title2[-1]				
		self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

		fra_1 = cuadros_frames_time_1
		salida=cv2.VideoWriter(Video_Salida,cv2.VideoWriter_fourcc(*'XVID'),6,(640,480))

		if sResprint >0:
			Cap_Vide_Web_USB.Capture_Cam1_W7(self)
		else:
			Cap_Vide_Web_USB.Capture_Cam1_W10(self)

	def Capture_Cam1_W7(self):
		global cap
		##Codigo Para Cam en Windows 7
		cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
		Cap_Vide_Web_USB.Capture_Cam1(self)

	def Capture_Cam1_W10(self):
		global cap
        ##Codigo Para Cam en Windows 10
		cap=cv2.VideoCapture(0)
		Cap_Vide_Web_USB.Capture_Cam1(self)

	def Capture_Cam1(self):
		global cap, cuadros_frames_time_2, cuadros_frames_time_3, salida

		if cap == None:
			print('Cerro la Cam.')
			pass

		elif cap is not None:
			resp=cap.isOpened()
			if resp==True:								
				ret, frame = cap.read()			
	            
				self.CurrentDate.set(value = time.strftime('%d/%m/%Y'))
				self.CurrentTime.set(value = time.strftime('%H:%M:%S'))
				Fecha_Hora='Fecha: '+self.CurrentDate.get()+' Hora: '+self.CurrentTime.get()
				self.Fecha_Hora_Actual.set(value = Fecha_Hora)
				t=self.Fecha_Hora_Actual.get()

				cv2.putText(frame,t,(340,460),cv2.FONT_HERSHEY_DUPLEX,0.5,(0,255,0),1)
	            
				if ret==True:

					x = int(cuadros_frames_time_2)  -100
					y = int(cuadros_frames_time_3)

					fra_2=10
					frame_2 = imutils.resize(frame, width=int(x), height=int(y))
					frame_3 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)

					im = Image.fromarray(frame_3)
					self.img = ImageTk.PhotoImage(image=im)

					self.container.configure(image=self.img)
					self.container.image = self.img	

					salida.write(frame)			

					self.container.after(int(fra_2), lambda: Cap_Vide_Web_USB.Capture_Cam1(self))

		else:
			tkinter.messagebox.showinfo("Info","Al parecer No Tienes la Camara Conectada\no no se Encuentra en buen Estado")
##===========================================================================================================================
##===========================================================================================================================
class Capturar_Im_Web_USB():

	def En_q_win_3(self):
		global captura, innitial_dir

		sResprint = tkinter.messagebox.askyesno('Pregunta', 'Windows 7 \\"SI\\"\no:\nWindows 10 \\"NO\\"')
		captura = filedialog.asksaveasfilename(title="Guardar Como",initialdir = innitial_dir, defaultextension=".png",\
                        filetypes = (("Png files","*.png"),("Jpg files","*.jpg"),("Jpeg files","*.jpeg"),("all files", "*.*")))

		txt_title1 = captura
		txt_title2 = txt_title1.split("/")
		txt_title3 = txt_title2[-1]				
		self.master.title(f"Media Player. (V.I.P.v20) \\\\ {txt_title3}")

		if sResprint >0:
			Capturar_Im_Web_USB.Tomar_Foto_Cam1_W7(self)
		else:
			Capturar_Im_Web_USB.Tomar_Foto_Cam1_W10(self)

	def Tomar_Foto_Cam1_W7(self):
		global cap_2
        ##Codigo Para Cam en Windows 7
		cap_2=cv2.VideoCapture(0,cv2.CAP_DSHOW)
		Capturar_Im_Web_USB.Tomar_Foto_Cam1(self)

	def Tomar_Foto_Cam1_W10(self):
		global cap_2
        ##Codigo Para Cam en Windows 10
		cap_2=cv2.VideoCapture(0)
		Capturar_Im_Web_USB.Tomar_Foto_Cam1(self)

	def Tomar_Foto_Cam1(self):
		global cap_2, cuadros_frames_time_1, cuadros_frames_time_2, cuadros_frames_time_3, frame_3

		if cap_2 == None:
			print('Cerro la Cam.')
			pass

		elif cap_2 is not None:
			resp=cap_2.isOpened()
			if resp==True:								
				ret, frame = cap_2.read()			
	            
				self.CurrentDate.set(value = time.strftime('%d/%m/%Y'))
				self.CurrentTime.set(value = time.strftime('%H:%M:%S'))
				Fecha_Hora='Fecha: '+self.CurrentDate.get()+' Hora: '+self.CurrentTime.get()
				self.Fecha_Hora_Actual.set(value = Fecha_Hora)
				t=self.Fecha_Hora_Actual.get()

				cv2.putText(frame,t,(340,460),cv2.FONT_HERSHEY_DUPLEX,0.5,(0,255,0),1)
				haarcascade = Path.resource_path('haarcascade\\haarcascade_frontalface_default.xml')
				faceClassif=cv2.CascadeClassifier(haarcascade)
				if ret==True:

					x = int(cuadros_frames_time_2)  -100
					y = int(cuadros_frames_time_3)

					fra_2 = cuadros_frames_time_1
					frame_2 = imutils.resize(frame, width=int(x), height=int(y))
					frame_3 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)
					faces=faceClassif.detectMultiScale(frame_3, 1.3, 5)

					for (x,y,w,h) in faces:
						cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

					im = Image.fromarray(frame_3)
					self.img = ImageTk.PhotoImage(image=im)

					self.container.configure(image=self.img)
					self.container.image = self.img

					self.container.after(int(fra_2), lambda: Capturar_Im_Web_USB.Tomar_Foto_Cam1(self))
		else:
			tkinter.messagebox.showinfo("Info","Al parecer No Tienes la Camara Conectada\no no se Encuentra en buen Estado")
##===========================================================================================================================
##===========================================================================================================================
class View_Recien_Pick():

	def Recien_Pick(self):
		global captura
		wb.open(captura)
##===========================================================================================================================
##===========================================================================================================================
class CollapsingFrame(ttk.Frame):
	"""	A collapsible frame widget that opens and closes with a button click. """

	def __init__(self, *args, **kwargs): 
		super().__init__(*args, **kwargs) 
		self.columnconfigure(0, weight=1) 
		self.cumulative_rows = 0

		im_open = Path.resource_path('assets\\icons8_double_up_24px.png')
		im_closed = Path.resource_path('assets\\icons8_double_right_24px.png')
		self.images = [tkinter.PhotoImage(name='open', file=im_open), tkinter.PhotoImage(name='closed', file=im_closed)]

	def add(self, child, title="", style='primary.TButton',  **kwargs):
		# """Add a child to the collapsible frame
		# :param ttk.Frame child: the child frame to add to the widget
		# :param str title: the title appearing on the collapsible section header
		# :param str style: the ttk style to apply to the collapsible section header
		# """

		if child.winfo_class() != 'TFrame':  # must be a frame
			return

		style_color = style.split('.')[0]
		frm = ttk.Frame(self, style=f'{style_color}.TFrame')
		frm.grid(row=self.cumulative_rows, column=0, sticky='ew')

		# header title
		lbl = ttk.Label(frm, text=title, style=f'{style_color}.Inverse.TLabel')
		if kwargs.get('textvariable'):
			lbl.configure(textvariable=kwargs.get('textvariable'))
		lbl.pack(side='left', fill='both', padx=10)

		# header toggle button
		btn = ttk.Button(frm, image='open', style=style, command=lambda c=child: self._toggle_open_close(child))
		btn.pack(side='right')

		# assign toggle button to child so that it's accesible when toggling (need tochange image)
		child.btn = btn
		child.grid(row=self.cumulative_rows + 1, column=0, sticky='news')

		# increment the row assignment
		self.cumulative_rows += 2
#==============================================================
#==============================================================
	def _toggle_open_close(self,  child):
	# """Open or close the section and change the toggle button image accordingly
	# :param ttk.Frame child: the child element to add or remove from grid manager
	# """
		if child.winfo_viewable(): 
			child.grid_remove() 
			child.btn.configure(image='closed')
		else: 
			child.grid() 
			child.btn.configure(image='open')			
##===========================================================================================================================
##===========================================================================================================================
if __name__ == '__main__':
	file_queue=Queue() 
	Application().mainloop()
##===========================================================================================================================
##===========================================================================================================================