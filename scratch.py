# PROGRAMA QUE RECONOZCA DIGITOS (NUMEROS) A PARTIR DE IMAGENES DE 8 X 8 PIXELES

import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from matplotlib.pyplot import imread
import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Crear interfaz
ventana = Tk()
ventana.title('Reconocimiento de digitos')
ventana.geometry('900x700')

ventana.resizable(width=False, height=False)

fondo = tk.PhotoImage(file='/Users/DavidAlex/Desktop/carbon.png')

fondo1 = tk.Label(ventana, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)

# Agregar elementos a la interfaz
labelSubir = Label(ventana, text='PROGRAMA QUE RECONOZCA DIGITOS (NUMEROS) A PARTIR DE IMAGENES DE 8 X 8 PIXELES',
                   height=3, width=72)
labelSubir.place(x=200, y=50)

etiqueta1 = Label(ventana, text='Usuario: ').place(x=200, y=144)
etiqueta2 = Label(ventana, text='Contraseña:').place(x=185, y=244)


def entrar():
    nombre = usuario.get()
    contraseña = password.get()
    if nombre == 'proyecto' and contraseña == '1234':
        correcto()
    else:
        pass
        incorrecto()

archivo = ""
fig1 = {}
fig2 = {}
def correcto():
    ventana.withdraw()
    window = tk.Toplevel()
    window.geometry('900x700')
    window.title('Bienvenido')
    window.resizable(width=False, height=False)
    fondo = tk.PhotoImage(file='/Users/DavidAlex/Desktop/carbon.png')
    fondo1 = tk.Label(window, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    fondo2 = tk.PhotoImage(file='/Users/DavidAlex/Desktop/carbon.png')
    fondo3 = tk.Label(window, image=fondo2).place(x=710, y=80, width=180, height=300)
    var1 = StringVar()
    mensaje1 = Message(window, textvariable=var1, relief=RAISED, bg='Gray').place(x=710, y=380, width=180, height=150)
    var1.set(
        'Felicidades!!, ganaste un iPhone 12 Pro Max, solo tienes que depositar $1,000.00 a la siguiente cuenta: 4169 1607 0690 9687 y nosotros nos comunicaremos con usted')

    escogerBtn = Button(window, text='Elegir el archivo',
                        fg='Blue', activebackground='black', activeforeground='white',
                        command=lambda: open_file()
                        )
    escogerBtn.place(x=400, y=130)

    calcBtn = Button(window, text='Calcular',
                     fg='Blue', activebackground='black', activeforeground='white',
                     command=lambda: calculate()
                     )
    calcBtn.place(x=420, y=200)

    # Obtener ruta de archivo de la imagen en jpg o jpeg

    def open_file():
        file_path = askopenfilename(filetypes=[('Image Files', "*jpeg *jpg")])
        if file_path is not None:
            global archivo
            archivo = file_path
            pass

    # Fórmula de distancia para algoritmo de K vecinos más cercanos
    def dist(x, y):
        return np.sqrt(np.sum((x - y) ** 2))

    # Cálculo del dígito por ambos algoritmos
    def calculate():
        # Importacion de dígitos de la libreria (base de datos)
        digits = datasets.load_digits()
        # digito subido por medio del explorador de archivos
        digitToTest = imread(archivo)
        # El total de imagenes en la base de datos es de 1797
        Xtrain = digits.data[0:1797]
        Ytrain = digits.target[0:1797]
        # Se entrenará el modelo con todas las imagenes de la base de datos
        # Cambiar imagen subida a escala de grises y conversion de pixeles a una escala de 0 a 16
        R, G, B = digitToTest[:, :, 0], digitToTest[:, :, 1], digitToTest[:, :, 2]
        imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B
        for i, x in enumerate(imgGray):
            for j, a in enumerate(x):
                imgGray[i][j] = abs(round(imgGray[i][j] / 16) - 16)
        imgGray = imgGray.reshape((1, -1))
        ###################################################################
        # ALGORITMO DE K VECINOS MÁS CERCANOS
        X_test = imgGray
        # Normalizacion
        for i in range(len(Xtrain)):
            maximum = np.amax(Xtrain[i])
            Xtrain[i] /= maximum
        maximum = np.amax(X_test)
        X_test /= maximum
        # Obtencion de distancias de cada "punto de prueba" al "punto de entrenamiento"
        l = len(Xtrain)
        distance = np.zeros(l)  # This will store the distance of test from every training value
        for i in range(l):
            distance[i] = dist(Xtrain[i], X_test)
        min_index = np.argmin(distance)
        print("Valor obtenido con algoritmo de k vecinos más cercanos")
        print(Ytrain[min_index])
        output = 'El valor obtenido con el algoritmo de k vecinos más cercanos es de: ' + str(Ytrain[min_index])
        Label(window, text=output, foreground='Green', bg='Black', height=2, width=70).place(x=210, y=250)
        #######IMAGENES
        plt.figure(figsize=(1.65, 1.65))
        dbPlot = plt.matshow(digits.images[min_index], cmap=plt.cm.gray_r, fignum=1, aspect="equal").get_figure()
        plt.title("K vecinos mas proximos - digito de db")
        global fig1,fig2
        if fig1=={}:
            fig1 = FigureCanvasTkAgg(dbPlot, window)
        else:
            fig1.draw()
        fig1.get_tk_widget().place(x=180, y=330)

        plt.figure(figsize=(1.65, 1.65))
        upPlot = plt.matshow(X_test.reshape(8, 8), cmap=plt.cm.gray_r, fignum=2, aspect="equal").get_figure()
        plt.title("K vecinos mas proximos - digito subido")
        if fig2 == {}:
            fig2 = FigureCanvasTkAgg(upPlot, window)
        else:
            fig2.draw()
        fig2.get_tk_widget().place(x=430,y=330)

    def salir():
        window.destroy()

    # boton
    boton2 = tk.Button(window, text='SALIR', command=salir, cursor='hand2', relief='flat', bg='Black', fg='White')
    boton2.pack()

    window.mainloop()


def incorrecto():
    ventana.withdraw()
    window2 = tk.Toplevel()
    window2.geometry('900x700')
    window2.resizable(width=False, height=False)
    fondo = tk.PhotoImage(file='/Users/DavidAlex/Desktop/carbon.png')
    fondo1 = tk.Label(window2, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    etiqueta3 = Label(window2,
                      text='Has ingresado tu usuario y/o contraseña incorrectamente, favor de ingresarlos correctamente',
                      width=100, height=7).place(x=100, y=144)

    def regresar():
        window2.withdraw()
        ventana.deiconify()

    # boton
    boton3 = tk.Button(window2, text='Regresar', command=regresar, cursor='hand2', relief='flat', height=2, bg='Black',
                       fg='White')
    boton3.place(x=400, y=300)

    window2.mainloop()


def salir():
    ventana.destroy()


# Entradas
usuario = tk.StringVar()
password = tk.StringVar()

entrada = tk.Entry(ventana, textvar=usuario, width=22, relief='flat')
entrada.place(x=255, y=144)

entrada2 = tk.Entry(ventana, textvar=password, show='*', width=22, relief='flat')
entrada2.place(x=255, y=244)

# Botones
boton = tk.Button(ventana, text='Entrar', cursor='hand2', command=entrar, width=12, relief='flat')
boton.place(x=110, y=300)

boton1 = tk.Button(ventana, text='Salir', command=salir, cursor='hand2', width=12, relief='flat')
boton1.place(x=370, y=300)

ventana.mainloop()
