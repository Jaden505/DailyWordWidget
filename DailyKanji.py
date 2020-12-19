import tkinter as tk
import re
# import urllib
# from bs4 import BeautifulSoup as bs4
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def get():
    driver = webdriver.PhantomJS()

    delay = 10

    driver.get('https://www.transparent.com/word-of-the-day/today/japanese.html')
    data_url = driver.find_element_by_id('js_wotd_frame').get_attribute('src')
    driver.get(data_url)

    elements = ['js-wotd-wordsound-plus', 'js-wotd-word-transliterated', 'js-wotd-translation']
    string = ''

    for elem in elements:
        try:
            elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                (By.CLASS_NAME, elem)))
            string = f'{string} {elem.text}'
        except TimeoutException:
            print("Loading took too much time!")

    driver.close()

    print(string)

    return string

class TransparentWin(tk.Tk):
    """ Transparent Tkinter Window Class. """

    def __init__(self, word):
        tk.Tk.__init__(self)
        self.Drag = Drag(self)

        self.focus_force()
        self.overrideredirect(True)
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparent", True)

        self.wm_geometry('+' + str(40) + '+' + str(430))

        label = tk.Label(text=(word), font='Forte 80', fg='white')
        label.config(bg='systemTransparent')
        label.master.wm_attributes("-alpha", 0.8)

        label.pack()

        self.Frame = tk.Frame(self)
        self.Frame.bind('<Button-3>', self.exit)
        self.Frame.configure(width=150, height=100)

    def exit(self, event):
        self.destroy()

    def position(self):
        _filter = re.compile(r"(\d+)?x?(\d+)?([+-])(\d+)([+-])(\d+)")
        pos = self.winfo_geometry()
        filtered = _filter.search(pos)
        self.X = int(filtered.group(4))
        self.Y = int(filtered.group(6))

        return self.X, self.Y


class Drag:
    def __init__(self, par, dissable=None, releasecmd=None):
        self.Par        = par
        self.Dissable   = dissable
        self.ReleaseCMD = releasecmd

        self.Par.bind('<Button-1>', self.relative_position)
        self.Par.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position(self, event):
        cx, cy = self.Par.winfo_pointerxy()
        x, y = self.Par.position()
        self.OriX = x
        self.OriY = y
        self.RelX = cx - x
        self.RelY = cy - y
        self.Par.bind('<Motion>', self.drag_wid)

    def drag_wid(self, event):
        cx, cy = self.Par.winfo_pointerxy()
        d = self.Dissable

        if d == 'x':
            x = self.OriX
            y = cy - self.RelY
        elif d == 'y':
            x = cx - self.RelX
            y = self.OriY
        else:
            x = cx - self.RelX
            y = cy - self.RelY

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        self.Par.wm_geometry('+' + str(x) + '+' + str(y))

    def drag_unbind(self, event):
        self.Par.unbind('<Motion>')
        if self.ReleaseCMD != None:
            self.ReleaseCMD()

    def dissable(self):
        self.Par.unbind('<Button-1>')
        self.Par.unbind('<ButtonRelease-1>')
        self.Par.unbind('<Motion>')


def __run__():
    TransparentWin(get()).mainloop()


if __name__ == '__main__':
    __run__()