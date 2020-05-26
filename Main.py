from tkinter import *
from tkinter import ttk
from xmlFunc import *


class MovieApp:
    def __init__(self):
        window = Tk()
        window.title("MovieApp")
        window.geometry("800x600")

        # 각 버튼에 표시될 이미지를 로드
        self.rankingImg = PhotoImage(file='Button_Image/ranking.png')
        self.searchImg = PhotoImage(file='Button_Image/search.png')
        self.theaterImg = PhotoImage(file='Button_Image/theater.png')

        # 랭킹/검색/영화관 검색 프레임 변경을 위한 버튼들
        self.rankingButton = Button(window, relief='groove', image=self.rankingImg, command=self.RankingRaise)
        self.rankingButton.place(x=0, y=0)
        self.searchButton = Button(window, relief='groove', image=self.searchImg, command=self.SearchRaise)
        self.searchButton.place(x=55, y=0)
        self.theaterButton = Button(window, relief='groove', image=self.theaterImg, command=self.TheaterRaise)
        self.theaterButton.place(x=110, y=0)

        # 박스오피스 랭킹 페이지
        self.rankingPage = Frame(window, width=550, height=400, bg='white')
        self.periodComboBox = ttk.Combobox(self.rankingPage, width=10)
        self.periodComboBox['value'] = ['일간', '주간']
        self.periodComboBox.current(0)
        self.periodComboBox.place(x=0, y=0)
        self.periodEntry = Entry(self.rankingPage, width=55, relief='solid', bd=2)
        self.periodEntry.insert(END, "YYYYMMDD ex)2020.01.01 → 20200101")
        self.periodEntry.place(x=100, y=0)
        self.rankingSearchButton = Button(self.rankingPage, text='검색', width=5, command=self.RankingSearch)
        self.rankingSearchButton.place(x=500, y=0)
        self.rankingPage.place(x=0, y=100)

        # 배우/감독 검색 페이지
        self.searchPage = Frame(window, width=550, height=400, bg='white')
        self.searchElementComboBox = ttk.Combobox(self.searchPage, width=10)
        self.searchElementComboBox['value'] = ['배우', '감독']
        self.searchElementComboBox.current(0)
        self.searchElementComboBox.place(x=0, y=0)
        self.nameEntry = Entry(self.searchPage, width=55, relief='solid', bd=2)
        self.nameEntry.insert(END, "배우/감독의 이름 입력")
        self.nameEntry.place(x=100, y=0)
        self.nameSearchButton = Button(self.searchPage, text='검색', width=5)
        self.nameSearchButton.place(x=500, y=0)
        self.searchPage.place(x=0, y=100)

        # 영화관 검색 페이지
        self.theaterPage = Frame(window, width=550, height=400, bg='white')
        self.theaterPage.place(x=0, y=100)

        # 처음 시작시 랭킹 페이지가 나오도록 설정함
        self.rankingPage.tkraise()

        window.mainloop()

    def RankingRaise(self):
        self.rankingPage.tkraise()

    def SearchRaise(self):
        self.searchPage.tkraise()

    def TheaterRaise(self):
        self.theaterPage.tkraise()

    def RankingSearch(self):
        s = self.periodComboBox.get()

        if s == '일간':
            DailyRanking(self.periodEntry.get())
        elif s == '주간':
            WeaklyRanking(self.periodEntry.get())

MovieApp()
