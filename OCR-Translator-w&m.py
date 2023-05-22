#!/usr/bin/sh
#-*-coding:utf-8 -*-


## for windows&mac ##

import os
import platform
import pytesseract  
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
import pyautogui
from datetime import *
from tkinter import *
from tkinter import messagebox
import googletrans  #pip install googletrans==4.0.0-rc1
from PIL import ImageGrab
from functools import partial
if platform.system() == 'Windows':
    import mouse #for windows
elif platform.system() == 'Darwin':
    import macmouse #for mac
else:
    print('unsurrpot os')
import time
from pynput import keyboard
#import clipboard



def on_press(key):
    return key
def on_release(key):
    return key

# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

def introduction():
    introScreen = Toplevel(screen)
    xs, ys = pyautogui.size()
    if (xs < 501) or (ys < 501):
        temp = "500x500+0+0"
    else:
        temp = "500x500+{0}+{1}".format(int((xs/2)-250),int((ys/2)-250))
    introScreen.geometry(temp)
    
    introText = "\n1. 인식하고싶은 언어를 빈칸에 입력해 주세요.\n2. 번역시작 버튼을 누르고 번역 하고 싶은 범위의 왼쪽 위와 오른쪽 아래를 클릭해 주세요.\n3. 바탕화면에 생성된 텍스트 파일을 확인합니다.\n"
    introTextLang = "eng = 영어, deu = 독일어, fra = 프랑스어, rus = 러시아어\nkor = 한국어, jpn = 일본어, chi_sim = 중국어(간체), lat = 라틴어\n"
    
    
    label4 = Label(introScreen, text = introText)
    label4.pack()
    
    label5 = Label(introScreen, text = introTextLang)
    label5.pack()

def translateAllScreen(event):
    print("translateAllScreen started")
    btn1["state"] = DISABLED
    if platform.system() == 'Windows':
        dir = os.path.join(os.path.expanduser('~'),'Desktop')
        print("desktop :", dir)
    elif platform.system() == 'Darwin':
        dir = os.path.join(os.path.expanduser('~')+'/Desktop')
        print("desktop :", dir)
    else:
        print('unsurpport os')
        messagebox.showerror("warning", "Unsurpport os.")
        btn1['state'] = NORMAL
        return
    
    dx,dy=pyautogui.size()
    im = pyautogui.screenshot(region=(0,0,dx,dy))

        
    #language = textBox.get(1.0, 'end-1c')                          #check box 만들면 intvar로 변경
    language = langVar.get()


    if language == "":
        print("lang = x")
        text = pytesseract.image_to_string(im)
    else:
        print("lang = {}".format(language))
        try:
            text = pytesseract.image_to_string(im, lang = language)
        except pytesseract.pytesseract.TesseractError:
            messagebox.showerror("warning", "Failed loading language \'{}\'".format(language))
            btn1['state'] = NORMAL
            return
        
    if text == "\u000c": #U+000c
        messagebox.showerror("warning", "No characters detected\nerror-1")
        btn1['state'] = NORMAL
        return
    
    print("--------text--------\n" + text)
    print("-"*20)
    
    translator = googletrans.Translator()
    try:
        tText = translator.translate(text, dest = 'ko') #mouse sleep == 0.01  ->  error
    except IndexError:
        print("googletranse error1")
        print("\n"*3)
        messagebox.showerror("warning", "No charactrs detected\nerror-2")
        btn1['state'] = NORMAL
        return
    except TypeError:
        print('googletranse error2')
        print("\n"*3)
        messagebox.showerror("warning", "No charactrs detected\nerror-3")
        btn1['state'] = NORMAL
        return
    
    resultText = tText.text
    
    now = datetime.now()
    nowTime = now.strftime("%Y_%m_%d-%H%M%S")
    if platform.system() == 'Windows':
        fileName = dir + "\\" + "translated_text-" + nowTime
    elif platform.system() == 'Darwin':
        fileName = dir + "/translated_text-"+nowTime
    else:
        print("unsupport os")
    
    if saveImage.get() == 1:
        print("save image")

        if platform.system() == 'Windows':
            im.save("{0}\\image-{1}.png".format(dir, nowTime))
        elif platform.system() == 'Darwin':
            im.save('{0}/image-{1}.png'.format(dir, nowTime))
        #im.show()
        else:
            print("unsupport os")
    
    
    memo = open("%s.txt" %fileName, "w", encoding = "utf-8")
    memo.write("%s" %resultText)
    memo.close()
    messagebox.showinfo("complete", "complete")
    btn1['state'] = NORMAL
    print("finish")
    return





def btncmd(event):
    print("btncmd started")
    btn1["state"] = DISABLED
    while 1:
        #btn1['state'] = DISABLED
        time.sleep(0.01)
        
        if platform.system() == 'Windows':
            dir = os.path.join(os.path.expanduser('~'),'Desktop')
            print("desktop :", dir)
        elif platform.system() == 'Darwin':
            dir = os.path.join(os.path.expanduser('~')+'/Desktop')
            print("desktop :", dir)
        else:
            print('unsurpport os')
            messagebox.showerror("warning", "Unsurpport os.")
            btn1['state'] = NORMAL
            break
        
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        
        if platform.system() == 'Windows':
            while True:
                if mouse.is_pressed("left"):
                    x1, y1 = mouse.get_position()
                    print(x1,y1)
                    time.sleep(0.1)
                    
                    while True:
                        if mouse.is_pressed("left"):
                            x2, y2 = mouse.get_position()
                            if x1 == x2:
                                x2 += 1
                            if y1 == y2:
                                y2 += 1
                            print(x2,y2)
                            break
                    break
            
            # if x1 > x2:
            #     x = x2
            #     dx = x1-x2
            # else:
            #     x = x1
            #     dx = x2 - x1
                
            # if y1 > y2:
            #     y = y2
            #     dy = y1 - y2
            # else:
            #     y = y1
            #     dy = y2 - y1

            x = min([x1,x2])
            y = min([y1,y2])
            dx = abs(x1-x2)
            dy = abs(y1-y2)

        elif platform.system() == 'Darwin': #  == mac os
            while True:
                if macmouse.is_pressed("left"):
                    x1, y1 = macmouse.get_position()
                    x1*=2#맥북 마우스 위치 해상도와 실제 표시되는 해상도가 2배 차이남
                    y1*=2
                    print(x1,y1)
                    time.sleep(1)                       ###########################################time.sleep(0.1)
                    
                    while True:
                        if macmouse.is_pressed("left"):
                            x2, y2 = macmouse.get_position()
                            x2*=2#맥북 마우스 위치 해상도와 실제 표시되는 해상도가 2배 차이남
                            y2*=2
                            if x1 == x2:
                                x2 += 1
                            if y1 == y2:
                                y2 += 1
                            print(x2,y2)
                            break
                    break
            x = min([x1,x2])
            y = min([y1,y2])
            dx = abs(x1-x2)
            dy = abs(y1-y2)

        else:
            print('unsurpport os')
            messagebox.showerror("warning", "Unsurpport os.")
            btn1['state'] = NORMAL
            break
        

        im = pyautogui.screenshot(region=(x, y, dx, dy))

        
        #language = textBox.get(1.0, 'end-1c')                          #check box 만들면 intvar로 변경
        language = langVar.get()


        if language == "":
            print("lang = x")
            text = pytesseract.image_to_string(im)
        else:
            print("lang = {}".format(language))
            try:
                text = pytesseract.image_to_string(im, lang = language)
            except pytesseract.pytesseract.TesseractError:
                messagebox.showerror("warning", "Failed loading language \'{}\'".format(language))
                btn1['state'] = NORMAL
                break
                
        
        #clipboard.copy(text) #test
        
        if text == "\u000c": #U+000c
            messagebox.showerror("warning", "No characters detected\nerror-1")
            btn1['state'] = NORMAL
            break
        
        print("--------text--------\n" + text)
        print("-"*20)
        
        translator = googletrans.Translator()
        try:
            tText = translator.translate(text, dest = 'ko') #mouse sleep == 0.01  ->  error
        except IndexError:
            print("googletranse error1")
            print("\n"*3)
            messagebox.showerror("warning", "No charactrs detected\nerror-2")
            btn1['state'] = NORMAL
            break
        except TypeError:
            print('googletranse error2')
            print("\n"*3)
            messagebox.showerror("warning", "No charactrs detected\nerror-3")
            btn1['state'] = NORMAL
            break
        
        resultText = tText.text
        
        now = datetime.now()
        nowTime = now.strftime("%Y_%m_%d-%H%M%S")
        if platform.system() == 'Windows':
            fileName = dir + "\\" + "translated_text-" + nowTime
        elif platform.system() == 'Darwin':
            fileName = dir + "/translated_text-"+nowTime
        else:
            print("unsupport os")
        
        if saveImage.get() == 1:
            print("save image")

            if platform.system() == 'Windows':
                im.save("{0}\\image-{1}.png".format(dir, nowTime))
            elif platform.system() == 'Darwin':
                im.save('{0}/image-{1}.png'.format(dir, nowTime))
            #im.show()
            else:
                print("unsupport os")
        
        
        memo = open("%s.txt" %fileName, "w", encoding = "utf-8")
        memo.write("%s" %resultText)
        memo.close()
        messagebox.showinfo("complete", "complete")
        btn1['state'] = NORMAL
        print("finish")
        break
    
    
def keyread():
    keyScreen = Toplevel(screen)
    keyScreen.resizable(False, False)
    xs, ys = pyautogui.size()
    if (xs < 101) or (ys < 101):
        temp = "100x100+0+0"
    else:
        temp = "100x100+{0}+{1}".format(int((xs/2)-50),int((ys/2)-50))
    keyScreen.geometry(temp)
    
    label3 = Label(keyScreen, text='reading key...')
    label3.pack()
    

def setting():
    settingScreen = Toplevel(screen)
    settingScreen.resizable(False, False)
    xs, ys = pyautogui.size()
    if (xs < 201) or (ys < 201):
        temp = "200x200+0+0"
    else:
        temp = "200x200+{0}+{1}".format(int((xs/2)-100),int((ys/2)-100))
    settingScreen.geometry(temp)
    
    label2 = Label(settingScreen, text = "단축키 설정")
    label2.pack()
    btn3 = Button(settingScreen, text = 'key', command = keyread)
    btn3.pack()


if platform.system() == 'Windows':
    print("os : Windows")
    path = os.path.realpath(__file__)
    print("current file path :", path)
    tesserPath = path[:len(path)-17] + "windows\\Tesseract-OCR\\tesseract"
    print("tesseract file path :", tesserPath)
    pytesseract.pytesseract.tesseract_cmd = r"{}".format(tesserPath)
elif platform.system() == 'Darwin':
    print("os : Darwin")
    path = os.path.realpath(__file__)
    print("current file path :", path)
    tesserPath = path[:len(path)-21] + "mac/tesseract/5.3.1/bin/tesseract"
    print("tesseract file path :", tesserPath)
    pytesseract.pytesseract.tesseract_cmd = r"{}".format(tesserPath)
else:
    print("unsupport os")

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    


screen = Tk()
screen.title("OCR-Translator")
xs, ys = pyautogui.size()
if (xs < 301) or (ys < 351):
    temp = "300x350+0+0"
else:
    temp = "300x350+{0}+{1}".format(int((xs/2)-150),int((ys/2)-175))
    screen.geometry(temp)
#screen.attributes('-alpha', 0)
screen.resizable(False,False)


label1=Label(screen, text='\n원하는 언어를 입력하고\n버튼을 누르고 번역할 범위를\n마우스로 클릭해 주세요.\n')
label1.place(x=80,y=0)

# textBox = Text(screen, height=1)
# textBox.pack()                                                    # 라디오버튼 만들기 #############################################

langVar = StringVar()
radioBtn1 = Radiobutton(screen, text = "영어", variable = langVar, value = 'eng', state='normal')
radioBtn1.place(x=10,y=100-20)
radioBtn2 = Radiobutton(screen, text = '독일어', variable = langVar ,value = 'deu', state='normal')
radioBtn2.place(x=100,y=100-20)
radioBtn3 = Radiobutton(screen, text = '프랑스어', variable = langVar, value = "fra", state='normal')
radioBtn3.place(x=200,y=100-20)
radioBtn4 = Radiobutton(screen, text = '러시아어', variable = langVar, value = 'rus', state='normal')
radioBtn4.place(x=10,y=150-30)
radioBtn5 = Radiobutton(screen, text = '한국어', variable = langVar, value = 'kor', state='normal')
radioBtn5.place(x=100,y=150-30)
radioBtn6 = Radiobutton(screen, text = '일본어', variable = langVar, value = 'jpn', state='normal')
radioBtn6.place(x=200,y=150-30)
radioBtn7 = Radiobutton(screen, text = '중국어(간체)', variable = langVar, value = 'chi_sim', state='normal')
radioBtn7.place(x=10,y=200-40)
radioBtn8 = Radiobutton(screen, text = '라틴어', variable = langVar, value = 'lat', state='normal')
radioBtn8.place(x=100,y=200-40)



saveImage = IntVar()
cBox = Checkbutton(screen, text = "Save image", variable = saveImage)
cBox.place(x=0,y=230-20)
btn1 = Button(screen, text = '번역 시작')#, command = btncmd)
btn1.place(x=0,y=250-20)
btn1.bind("<Button-1>",btncmd)
screen.bind("<Control-Shift-t>",translateAllScreen)
screen.bind("<Control-Shift-T>",translateAllScreen)
btn2 = Button(screen, text = '설정', command = setting)
btn2.place(x=0,y=280-20)
btn3 = Button(screen, text = '사용법 보기', command = introduction)
btn3.place(x=0,y=310-20)
 
screen.mainloop()