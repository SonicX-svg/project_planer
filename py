from tkinter import *
import geocoder
from tkcalendar import Calendar
from tkinter import Label, Tk
from PIL import Image, ImageTk
import requests


root = Tk()
root.title('Hellper_2.0')
root['bg'] = '#fafafa'
icon = PhotoImage(file="aaa.png")
root.iconphoto(True, icon)
root.wm_attributes('-alpha', 0.7)
root.geometry('980x520')

#canvas = Canvas(root, height=500, width=520)
#canvas.pack()


frame = Frame(root, bg='white', width=200, height=200)
#frame.configure(width=520, height=500)
frame.pack(fill = BOTH, expand = True, side=RIGHT)
frame1 = Frame(root, bg='blue', width=200, height=200)
#frame.configure(width=520, height=500)
frame1.pack(fill = BOTH, expand = True, side=RIGHT)

#Для погоды по геолокации
image = Image.open("/home/sonikx/projject/picture.png")
resized_image = image.resize((28, 28))
photo = ImageTk.PhotoImage(resized_image)

#фрейм с погодой    
frame2 = Frame(frame, bg='white', width=100, height=100)
frame2.pack(side='top', fill = X)


def func():                         # Определяет геолокацию и погоду
     BASE_URL = "https://api.open-meteo.com/v1/forecast"
     g = geocoder.ip('me')
     city = g.latlng
# Параметры запроса для Краснодара
     params = {
     "latitude": city[0],       # широта Краснодара
     "longitude": city[1],      # долгота Краснодара
     "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum", # минимальная и максимальная температура, сумма осадков
     "timezone": "Europe/Moscow" } # временная зона для Краснодара 
     response = requests.get(BASE_URL, params=params)
     data = response.json()
     user_name['text'] =  str(g.city) + ' : '+str(data['daily']['temperature_2m_max'][1])
     
#кнопка с фото
#title = Label(frame2, bg='white')
btn = Button(frame2, text='Создать задачу', bg='white', image=photo, command=func)
btn.configure(width=28, height=28)
btn.pack(side=LEFT)
#title.pack(side='left')

user_name = Label(frame2, text='wheather', font=25, bg='white')
user_name.pack(side=LEFT)

btn.invoke() #кнопка погоды нажатие
print('cick') 


import datetime
dt_now = str(datetime.datetime.now()).split()[0].split('-')
print()
print(int(dt_now[1]))
tkc = Calendar(frame,selectmode = "day",year=int(dt_now[0]),month=int(dt_now[1]),date=int(dt_now[2]))
#tkc.configure(width=50, height=50)
#tkc.geometry("50x5 0")  
tkc.pack(fill='both', expand=True)

#Работа с календарем
def updateLabel(event):
    labelblue.config(text="Selected Date: " + tkc.get_date(), font=40)
    for i in frame3.winfo_children():
        i.destroy()
    for i in range(1, len(dict_[tkc.get_date()])):
         current_task = dict_[tkc.get_date()][i]
         #current_task[-1].pack(fil=X, font=40)
         print(current_task[1])
         current_task[-1] = Checkbutton(frame3, text = current_task[0], font=35,bg='white',  
                      variable = current_task[1], 
                      onvalue = 1, 
                      offvalue = 0, highlightthickness=0,bd=0
                      )
         current_task[-1].pack(anchor='nw', padx=7)

frame4 = Frame(frame1, bg='white')
frame4.pack(side='top',fill = X)

dict_ = {}
def func1():
    stroka = labelblue.cget("text").split()[-1]
    dict_[stroka] = dict_.get(stroka, []) + [stroka[-1]]
    
    def fetch():
        dict_[stroka] = dict_.get(stroka, []) + [ent.get()]
        print(dict_)
        print('Ввод = "%s"' % ent.get()) # извлечь строку
        ent.delete(0, END)
        
    def close():
        for i in range(1,len(dict_[stroka])):
            a = 'Checkbutton' + str(i) + stroka
            locals()[a] = IntVar() # в a переменая кнопки 
            #print(a)
            button = 'button' + str(i)
            locals()[button] = IntVar() # в a переменая кнопки 
            button = Checkbutton(frame3, text = dict_[stroka][i], font=35,bg='white',  
                      variable = a, 
                      onvalue = 1, 
                      offvalue = 0, highlightthickness=0,bd=0
                      )
            button.pack(anchor='nw', padx=7)              
            dict_[stroka][i] = [dict_[stroka][i], a, button]   
            print(dict_)
            newWindow.destroy()
            #Checkbutton1 = IntVar()   ###!!!! строка как переменая https://www.geeksforgeeks.org/python-tkinter-checkbutton-widget/
        
    newWindow = Toplevel(root)
    newWindow.title("Add your task")
    newWindow.geometry("300x70")
    ent = Entry(newWindow)
    ent.insert(0, 'Ввод текста')        
    ent.pack(side=TOP, fill=X)
    ent.focus()                          # передать фокус в поле ввода
    ent.bind('<Return>', (lambda event: fetch()))   
    Button(newWindow, text='OK', command=fetch).pack(side=BOTTOM)
    newWindow.protocol("WM_DELETE_WINDOW", close)                        #close window trigger
    
btn1 = Button(frame4, text='ADD', bg='white', command=func1)
#btn1.configure(width=10, height=10)
btn1.pack(side=LEFT)


labelblue = Label(frame4, text="Selected Date: ", font=40, bg='white')
labelblue.pack(side=LEFT)    

tkc.bind('<<CalendarSelected>>', updateLabel) #нажатие на дату


frame3 = Frame(frame1, bg='white')
frame3.pack(fill = BOTH, expand = True)




#proba
#frame2 = Frame(frame1, bg='yellow', width=100, height=100)

#frame2.pack(side='top', fill = X)



root.mainloop()
