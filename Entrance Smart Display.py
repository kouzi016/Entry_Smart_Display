import tkinter as tk
import tkinter.messagebox  as tmsg
from tkinter import *
import requests
import json
import datetime as dt
import pytz 
import time
from tkinter import ttk
import os

#データ辞書
l={"北海道":"016000","青森県":"020000","岩手県":"030000","宮城県":"040000","秋田県":"050000","山形県":"060000","福島県":"070000","茨城県":"080000","栃木県":"090000","群馬県":"100000","埼玉県":110000,"千葉県":120000,"東京都":130000,"神奈川県":140000,"山梨県":190000,"長野県":200000,"岐阜県":210000,"静岡県":220000,"愛知県":230000,"三重県":240000,"新潟県":150000,"富山県":160000,"石川県":170000,"福井県":180000,"滋賀県":250000,"京都府":260000,"大阪府":270000,"兵庫県":280000,"奈良県":290000,"和歌山県":300000,"鳥取県":310000,"島根県":320000,"岡山県":330000,"広島県":"340000","山口県":350000,"徳島県":360000,"香川県":37000,"愛媛県":380000,"高知県":390000,"福岡県":400000,"佐賀県":410000,"長崎県":420000,"熊本県":430000,"大分県":440000,"宮崎県":450000,"鹿児島県":460100,"沖縄県":471000}
day_list=["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]

#実行フォルダのパス取得
path=__file__
path_len=len(path)
number=(path_len)-25
img_path=path[:number]

#時間と日付のための準備
now = dt.datetime.now(pytz.timezone('Asia/Tokyo'))
now_time=dt.datetime.now(pytz.timezone('Asia/Tokyo')).time()
date = dt.datetime.now(pytz.timezone('Asia/Tokyo'))
today = now.strftime('%m月%d日')
hour=date.hour 
minute = date.minute
second=date.second
day=now.weekday()

#初期値
icon ="preparing.png"
code=130000
place="東京都"


def time_string():
    return time.strftime('%H:%M:%S')

def update():
    global id
    clock.configure(text=time_string())
    id = clock.after(1000, update)

def w_update():
    global image
    global image2
    global canvas
    global jma_weather
    global file
    global canvas2
    place=entry_place.get()
    jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
    jma_json = requests.get(jma_url).json()
    jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    weather.configure(text=f"{place}の天気：{jma_weather}")
    canvas.delete()
    select_icon(jma_weather)
    file=f"{img_path}\{icon}"
    canvas = tk.Canvas(root,width=300,height=300,bg="white")
    canvas.place(relx=0.36,rely=0.5)
    image = tk.PhotoImage(file=file,master=canvas)
    canvas.create_image(150,150,image=image)
    if "雨" in jma_weather or "雪" in jma_weather:
        umbrella="umbrella.png"
        file_umbrella=f"{img_path}\{umbrella}"
        canvas2.delete()
        canvas2 = tk.Canvas(root,width=300,height=300,bg="white")
        canvas2.place(relx=0.65,rely=0.5)
        image2 = tk.PhotoImage(file=file_umbrella,master=canvas2)
        canvas2.create_image(150,150,image=image2)
    else:
        canvas2.delete()
        canvas2=tk.Canvas(root,width=300,height=300,bg="white")
        canvas2.place(relx=0.65,rely=0.5)

        
def ButtonClick():
    global code
    global place
    if "県" in place or "府" in place or "東京都" in place or "北海道"in place:
        place=entry_place.get()
        code=l[f"{place}"]
        tmsg.showinfo("Entrance Smart Display",f"場所は{place}に設定されました。")

        w_update()
        
    else:
        tmsg.showwarning("Entrance Smart Display","正式名称で入力してください")

def select_icon(name_weather):
    global icon
    if "晴れ" in name_weather and "くもり" in name_weather and "雨" not in name_weather and "雪" not in name_weather:
        icon="cloud and sun.png"
    elif "くもり" in name_weather and "雨" in name_weather and "晴れ" not in name_weather and "雪" not in name_weather:
         icon="cloud and rain.png"
    elif "晴れ" in name_weather and "くもり" not in name_weather and "雨" not in name_weather and "雪" not in name_weather:
        icon="sunny.png"
    elif "くもり" in name_weather and "晴れ" not in name_weather and "雨" not in name_weather and "雪" not in name_weather:
        icon="cloud.png"
    elif "雨" in name_weather and "くもり" not in name_weather and "晴れ" not in name_weather and "雪" not in name_weather:
        icon="rain.png"
    elif "雪" in name_weather:
        icon="snow.png"
        

root = tk.Tk()
root.title("Entrance Smart Display")
root.geometry("1100x800")
root["bg"] = "white"
root.resizable(0,0)

style = ttk.Style()
style.configure('TLabel', background='white', foreground='black')

day_disp=ttk.Label(root,text=f"{today}   {day_list[day]}",font=("Yu Gothic UI",40,"bold"),background="white")
day_disp.place(relx=0.05,rely=0.05)

clock = ttk.Label(root, text=time_string(), font=('Yu Gothic UI', 160),background="white")
clock.place(relx=0.05,rely=0.15)


if hour >= 0 and hour < 12:
  label3=tk.Label(root,text="おはようございます\n気をつけていってらっしゃいませ",font=("Yu Gothic UI",25,"bold"),bg="white")
elif hour >=12 and hour <18:
  label3=tk.Label(root,text="こんにちは",font=("Yu Gothic UI",25,"bold"),bg="white")
else:
  label3=tk.Label(root,text="こんばんは\nおかえりなさい",font=("Yu Gothic UI",25,"bold"),bg="white")

label3.place(relx=0.08,rely=0.55)
jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
jma_json = requests.get(jma_url).json()
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]

canvas2 = tk.Canvas(root,width=300,height=300,bg="white")
canvas2.place(relx=0.65,rely=0.5)
        
select_icon(jma_weather)

file=f"{img_path}\{icon}"
canvas = tk.Canvas(root,width=300,height=300,bg="white")
canvas.place(relx=0.36,rely=0.5)
image = tk.PhotoImage(file=file,master=canvas)
canvas.create_image(150,150,image=image)

please_entry=ttk.Label(root,text="場所の設定",font=("Yu Gothic UI",15),background="white")
please_entry.place(relx=0.05,rely=0.8)

entry_place=ttk.Entry(root,width=20)
entry_place.place(relx=0.05,rely=0.85)

choose_place=ttk.Button(root,text="設定",command=ButtonClick)
choose_place.place(relx=0.18,rely=0.847)

place="東京都"

weather=tk.Message(root,text=f"東京都の天気：{jma_weather}",font=("Yu Gothic UI",20,"bold"),background="white",width=1000)
weather.place(relx=0.05,rely=0.9)

UpdateButton=ttk.Button(root,text="更新",command=w_update)
UpdateButton.place(relx=0.26,rely=0.847)



clock.after(1000, update)
root.mainloop()
