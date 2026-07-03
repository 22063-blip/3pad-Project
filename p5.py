import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk


# quiz app thing i made
class QuizApp:
    def __init__(self, win):

        self.win = win
        self.win.title("Flow Computing Quiz")
        self.win.geometry("900x800")
        self.win.configure(bg="#d8c8ff")

        # user stuff i guess
        self.user = ""
        self.score = 0
        self.lives = 3
        self.mode = ""

        # banner image for all screens (bit slow to load ngl)
        self.banner_img = Image.open(r"C:\Users\OEM\OneDrive - Lynfield College\Documents\3Pad\Code\math banner.jpg")
        self.banner_img = self.banner_img.resize((320, 130))
        self.banner = ImageTk.PhotoImage(self.banner_img)

        # questions for the quiz, just shoved here
        self.quiz = {
            "easy": [["e1.png", 10], ["e2.png", 13], ["e3.png", 5], ["e4.png", 13], ["e5.png", 5]],
            "medium": [["m1.png", 8], ["m2.png", 20], ["m3.png", 11], ["m4.png", 13], ["m5.png", 5]],
            "hard": [["h1.png", 12], ["h2.png", 24], ["h3.png", 8], ["h4.png", 13], ["h5.png", 5]]
        }

        # screens setup thing
        self.login = LoginScreen(self)
        self.menu = MenuScreen(self)
        self.quiz_screen = QuizScreen(self)

        self.login_page()

    # back to login i think
    def login_page(self):
        self.menu.hide()
        self.quiz_screen.hide()
        self.login.show()

    # menu screen thing
    def menu_page(self):
        self.login.hide()
        self.menu.show()
        self.quiz_screen.hide()

    # start game
    def start(self, mode):

        self.mode = mode
        self.score = 0
        self.lives = 3

        self.login.hide()
        self.menu.hide()

        self.quiz_screen.start(mode)
        self.quiz_screen.show()


# login screen thing
class LoginScreen:
    def __init__(self, app):

        self.app = app
        self.frame = tk.Frame(app.win, bg="#d8c8ff")

        tk.Label(self.frame, image=app.banner, bg="#d8c8ff").pack(pady=10)

        tk.Label(self.frame, text="Flow Computing Quiz",
                 font=("Calisto MT", 28, "bold"),
                 bg="#d8c8ff").pack(pady=20)

        tk.Label(self.frame, text="user", bg="#d8c8ff", font=("Calisto MT", 22)).pack()
        self.user = tk.Entry(self.frame, font=("Calisto MT", 22))
        self.user.pack(pady=8)

        tk.Label(self.frame, text="pass", bg="#d8c8ff", font=("Calisto MT", 22)).pack()
        self.password = tk.Entry(self.frame, font=("Calisto MT", 22), show="*")
        self.password.pack(pady=8)

        tk.Button(self.frame, text="Sign Up",
                  font=("Calisto MT", 16), width=18, height=2,
                  command=self.signup).pack(pady=8)

        tk.Button(self.frame, text="Login",
                  font=("Calisto MT", 16), width=18, height=2,
                  command=self.login).pack(pady=8)

        tk.Button(self.frame, text="Quit",
                  font=("Calisto MT", 16), width=18, height=2,
                  bg="red", fg="white",
                  command=app.win.destroy).pack(pady=10)

        self.status = tk.Label(self.frame, text=" ",
                               bg="#d8c8ff", font=("Calisto MT", 14))
        self.status.pack(pady=10)

    def signup(self):

        u = self.user.get()
        p = self.password.get()

        if u == "" or p == "":
            messagebox.showerror("error", "fill both boxes")
            return

        f = open("usernpass.txt", "a")
        f.write(u + "," + p + "\n")
        f.close()

        messagebox.showinfo("ok", "account made")

    def login(self):

        u = self.user.get()
        p = self.password.get()

        try:
            f = open("usernpass.txt", "r")

            for line in f:
                parts = line.strip().split(",")

                if len(parts) == 2:
                    if parts[0] == u and parts[1] == p:

                        self.app.user = u
                        self.status.config(text="logged in " + u)

                        self.app.menu_page()
                        return

            messagebox.showerror("error", "wrong login")

        except:
            messagebox.showerror("error", "no file")

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


# menu screen thing
class MenuScreen:
    def __init__(self, app):

        self.app = app
        self.frame = tk.Frame(app.win, bg="#d8c8ff")

        tk.Label(self.frame, image=app.banner, bg="#d8c8ff").pack(pady=10)

        tk.Label(self.frame, text="pick difficulty",
                 font=("Calisto MT", 26, "bold"),
                 bg="#d8c8ff").pack(pady=30)

        tk.Button(self.frame, text="Easy",
                  font=("Calisto MT", 18), width=20, height=2,
                  command=lambda: app.start("easy")).pack(pady=8)

        tk.Button(self.frame, text="Medium",
                  font=("Calisto MT", 18), width=20, height=2,
                  command=lambda: app.start("medium")).pack(pady=8)

        tk.Button(self.frame, text="Hard",
                  font=("Calisto MT", 18), width=20, height=2,
                  command=lambda: app.start("hard")).pack(pady=8)

        tk.Button(self.frame, text="Back",
                  font=("Calisto MT", 14),
                  command=app.login_page).pack(pady=15)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


# QUIZ screen
class QuizScreen:
    def __init__(self, app):

        self.app = app
        self.q = 0
        self.questions = []

        self.frame = tk.Frame(app.win, bg="#d8c8ff")

        # banner again same as other pages
        tk.Label(self.frame, image=app.banner, bg="#d8c8ff").pack(pady=10)

        self.title = tk.Label(self.frame, text="Quiz",
                              font=("Calisto MT", 22, "bold"),
                              bg="#d8c8ff")
        self.title.pack(pady=10)

        # just shows score and stuff
        self.info = tk.Label(self.frame, text="", bg="#d8c8ff", font=("Calisto MT", 14))
        self.info.pack(pady=5)

        # question text (not much here yet)
        self.question = tk.Label(self.frame, text="",
                                 font=("Calisto MT", 18),
                                 bg="#d8c8ff")
        self.question.pack(pady=10)

        # image goes here
        self.image = tk.Label(self.frame, bg="#d8c8ff")
        self.image.pack(pady=10)

        # answer box
        self.answer = tk.Entry(self.frame, font=("Calisto MT", 18), width=18)
        self.answer.pack(pady=10)

        # submit button
        tk.Button(self.frame, text="Submit",
                  font=("Calisto MT", 16), width=18, height=2,
                  command=self.check).pack(pady=8)

        # result text under button
        self.result = tk.Label(self.frame, text="", bg="#d8c8ff", font=("Calisto MT", 14))
        self.result.pack(pady=5)

        # back button just in case
        tk.Button(self.frame, text="Back",
                  font=("Calisto MT", 14),
                  command=app.menu_page).pack(pady=10)

    def start(self, mode):

        # load questions from chosen mode
        self.questions = self.app.quiz[mode]
        self.q = 0

        self.load()

    def load(self):

        # stop if no more questions
        if self.q >= len(self.questions):
            self.end()
            return

        img, ans = self.questions[self.q]
        self.ans = ans

        # updating top info bar
        self.info.config(
            text="Q " + str(self.q + 1)
                 + " score " + str(self.app.score)
                 + " lives " + str(self.app.lives)
        )

        self.question.config(text="solve it")

        # load image if it works
        try:
            pic = tk.PhotoImage(file=img)
            self.image.config(image=pic)
            self.image.image = pic
        except:
            self.image.config(text="no image")

        # clear old answer
        self.answer.delete(0, tk.END)

    def check(self):

        # check answer
        try:
            g = float(self.answer.get())
        except:
            messagebox.showerror("error", "numbers only")
            return

        # scoring stuff
        if g == self.ans:
            self.app.score += 1
        else:
            self.app.lives -= 1

        # update display
        self.result.config(
            text="score " + str(self.app.score)
                 + " lives " + str(self.app.lives)
        )

        # game over if no lives
        if self.app.lives <= 0:
            self.end()
            return

        # next question
        self.q += 1
        self.load()

    def end(self):

        # finish screen thing
        messagebox.showinfo("done", "score " + str(self.app.score))

        # save score to file
        f = open("scores.txt", "a")
        f.write(self.app.user + "," + self.app.mode + ","
                + str(self.app.score) + "," + str(datetime.now()) + "\n")
        f.close()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


# run
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
