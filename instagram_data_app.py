import tkinter
import instaloader
from datetime import date
from datetime import timedelta
import os
from difflib import Differ
from tkinter import *
from pathlib import Path


def set_dir(username):

    today = date.today()
    cwd = os.getcwd()
    new_user = f"{cwd}\\{username}"
    user_check = os.path.exists(new_user)
    if not user_check:
        os.mkdir(new_user)
    new_day = f"{cwd}\\{username}\\{today}"
    day_check = os.path.exists(new_day)
    if not day_check:
        os.mkdir(new_day)
    base_date = f"{cwd}\\{username}\\2000-01-01"
    base_date_check = os.path.exists(base_date)
    if not base_date_check:
        os.mkdir(base_date)
    base_text = open(f"{base_date}\\2000-01-01.txt", "w")
    if not base_date_check:
        os.mkdir(base_date)
    return new_user, new_day, base_date, base_text


def get_date(username):

    cwd = os.getcwd()
    new_user = f"{cwd}\\{username}"
    today = date.today()
    x = 1
    nearest_date = today - timedelta(days=x)
    while not Path(f"{new_user}\\{nearest_date}").exists():
        nearest_date = today - timedelta(days=x)
        x = x + 1
    return today, nearest_date


def get_instadata(username, password, today):

    cwd = os.getcwd()
    new_day = f"{cwd}\\{username}\\{today}"
    print("LOADING... PLEASE WAIT...")
    date_list = open(f'{new_day}\\{today}.txt', 'w+')
    date_list1 = open(f'{new_day}\\followee_{today}.txt', 'w+')
    L = instaloader.Instaloader()
    L.login(username, password)
    profile = instaloader.Profile.from_username(L.context, username)
    follow_list = []
    followee_list = []
    count = 0

    for follower in profile.get_followers():
        follow_list.append(follower.username)
        date_list.write(follow_list[count])
        date_list.write("\n")
        count = count + 1

    count = 0

    for followee in profile.get_followees():
        followee_list.append(followee.username)
        date_list1.write(followee_list[count])
        date_list1.write("\n")
        count = count + 1
    date_list.close()
    date_list1.close()


def get_compdata(today, nearest_date, username):

    cwd = os.getcwd()
    new_user = f"{cwd}\\{username}"
    new_day = f"{cwd}\\{username}\\{today}"
    date_list_old = open(f'{new_user}\\{nearest_date}\\{nearest_date}.txt', 'r')
    diff = open(f"{new_day}\\differences_{today}.txt", "w")
    diff1 = open(f"{new_day}\\unfollowee_{today}.txt", "w")
    duplicate_data = []
    duplicate_data_final =[]
    with open(f"{new_day}\\{today}.txt", 'r+') as date_list:
        print(date_list)
        differ = Differ()
        print(date_list_old)
        for line in differ.compare(date_list_old.readlines(), date_list.readlines()):
            diff.write(line)
    diff.close()

    with open(f"{new_day}\\differences_{today}.txt", "r+") as diff:
        d = diff.readlines()
        diff.seek(0)
        for i in d:
            if i[0] == "+":
                diff.write(i)
            if i[0] == "-":
                diff.write(i)
        diff.truncate()

    with open(f"{new_day}\\{today}.txt", 'r+') as date_list, open(f'{new_day}\\followee_{today}.txt',
                                                                  'r+') as date_list1:
        print(date_list)
        differ = Differ()
        print(date_list1)
        for line in differ.compare(date_list1.readlines(), date_list.readlines()):
            diff1.write(line)

    with open(f"{new_day}\\unfollowee_{today}.txt", "r+") as diff1:
        dif = diff1.readlines()
        diff1.seek(0)
        for item in dif:
            if item[0] == "+":
                diff1.write(item)
            if item[0] == "-":
                diff1.write(item)
        diff1.truncate()

    with open(f"{new_day}\\unfollowee_{today}.txt", "r+") as diff1:
        dif1 = diff1.readlines()
        diff1.seek(0)
        for item in dif1:
            xitem = item[1:]
            if xitem not in duplicate_data_final:
                duplicate_data_final.append(xitem)
        diff1.seek(0)
        for item1 in duplicate_data_final:
            diff1.write(item1)
        diff1.truncate()

    with open(f"{new_day}\\unfollowee_{today}.txt", "r+") as diff1, open(f"{new_day}\\{today}.txt", 'r+') as date_list:
        dif11 = diff1.readlines()
        for og_item in date_list:
            xog_item = " "+og_item
            duplicate_data.append(xog_item)
        diff1.seek(0)
        for item111 in dif11:
            if item111 not in duplicate_data:
                item1111 = item111[1:]
                diff1.write(item1111)
        diff1.truncate()
    print("DONE")


def gui():

    def button():

        follower_box.delete(0, END)
        diff_box.delete(0, END)
        error_box.delete(0, END)
        username = user_entry.get()
        password = pass_entry.get()
        try:
            t = set_dir(username)
            a = get_date(username)
            error_box.insert(0, "Loading, please wait...")
            root.update()
            get_instadata(username, password, a[0])
            get_compdata(a[0], a[1], username)
            today = a[0]
            j = open(f'{t[1]}\\{today}.txt', 'r+')
            p = open(f'{t[1]}\\differences_{today}.txt', 'r+')
            r = open(f'{t[1]}\\unfollowee_{today}.txt', 'r+')
            for h in reversed(j.readlines()):
                follower_box.insert(0, h)
            for w in p:
                diff_box.insert(0, w)
            for u in reversed(r.readlines()):
                unfollowee_box.insert(0,u)
            j.close()
            p.close()
            error_box.insert(0, "Process finished without any problems.")
            root.update()
        except FileExistsError:
            error_box.insert(0, "Wrong username and/or password. Please try again.")
        except Exception as e:
            error_box.insert(0, e)

    def save_button():

        username = user_entry.get()
        password = pass_entry.get()
        cwd = os.getcwd()
        new_user = f"{cwd}\\{username}"
        profile_box.insert(0, username)
        user_login_info = open(f"{cwd}\\login_info_{username}.txt", "w")
        user_login_info.write(username + "\n")
        user_login_info.write(password)
        user_login_info.close()

    def import_profile():

        user_entry.delete(0, END)
        pass_entry.delete(0, END)
        try:
            click_response = profile_box.get(profile_box.curselection())
            with open(f"login_info_{click_response}.txt", "r") as login_cred:
                saved_user = login_cred.readline()[:-1]
                saved_pass = login_cred.readline()
                user_entry.insert(0, saved_user)
                pass_entry.insert(0, saved_pass)
                button()
        except FileExistsError:
            error_box.insert(0, "Wrong username and/or password. Please try again.")
        except tkinter.TclError:
            error_box.insert(0, "Please select a profile to import.")
        except Exception as e:
            error_box.insert(0, e)

    cwd = os.getcwd()
    root = Tk(className=" INSTAGRAM DATA ANALYZER")
    root.geometry("800x400")
    root.iconbitmap("icon.ico")
    root.config(bg="#c2e8f5")
    root.resizable(False, False)
    user_label = Label(root, text="Username:", bg='#c2e8f5')
    user_label.place(x=20, y=210)
    pass_label = Label(root, text="Password:", bg="#c2e8f5")
    pass_label.place(x=20, y=270)
    text = StringVar()
    text1 = StringVar()
    user_entry = Entry(root, textvariable=text, bg="#e8f5c2", width=24)
    user_entry.place(x=20, y=230)
    pass_entry = Entry(root, textvariable=text1, show="*", bg="#e8f5c2", width=24)
    pass_entry.place(x=20, y=290)
    follower_box = Listbox(root, height=12, width=24, bg="#e8f5c2")
    follower_box.place(x=220, y=60)
    follower_label = Label(root, text="Current Followers:", bg="#c2e8f5")
    follower_label.place(x=220, y=40)
    diff_box = Listbox(root, height=12, width=24, bg="#e8f5c2")
    diff_box.place(x=420, y=60)
    diff_label = Label(root, text="Differences to Last Time:", bg="#c2e8f5")
    diff_label.place(x=420, y=40)
    unfollowee_box = Listbox(root, height=12, width=24, bg="#e8f5c2")
    unfollowee_box.place(x=620, y=60)
    unfollowee_label = Label(root, text="Users Not Following Back:", bg="#c2e8f5")
    unfollowee_label.place(x=620, y=40)
    profile_box = Listbox(root, height=6, width=24, bg="#e8f5c2")
    profile_box.place(x=20, y=60)
    profile_label = Label(root, text="Saved Profiles:", bg="#c2e8f5")
    profile_label.place(x=20, y=40)
    error_box = Listbox(root, height=3, width=91, bg="#e8f5c2")
    error_box.place(x=220, y=300)
    error_label = Label(root, text="Messages and Warnings:", bg="#c2e8f5")
    error_label.place(x=220, y=280)
    error_box.insert(0,"the next day since there is no prior data to compare.")
    error_box.insert(0,"If this is the first time you are using this app, Differences to Last Time feature will start working")
    sub_but = Button(root, text="Submit", bg="#e8f5c2", command=button)
    sub_but.place(x=20, y=330)
    save_but = Button(root, text="Save Profile", bg="#e8f5c2", command=save_button)
    save_but.place(x=95, y=330)
    im_but = Button(root, text="Import Profile", bg="#e8f5c2", command=import_profile)
    im_but.place(x=20, y=170)
    cwd_list = os.listdir(cwd)
    for log_file in cwd_list:
        if log_file.startswith('login_info'):
            with open(log_file, "r") as saved_login:
                username_ch = saved_login.readline()[:-1]
                profile_box.insert(1, username_ch)
    root.mainloop()


def main():
    gui()


main()
