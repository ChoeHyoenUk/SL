from xml.etree import ElementTree
from tkinter import *
from tkinter import ttk
import tkinter.font
from xmlFunc import *
import urllib
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO


class MovieApp:
    def __init__(self):
        window = Tk()
        window.title("MovieApp")
        window.geometry("1400x750")
        myFont = tkinter.font.Font(window, family='맑은 고딕', size=14)

        # 각 버튼에 표시될 이미지를 로드
        self.rankingImg = PhotoImage(file='Images/ranking.png')
        self.searchImg = PhotoImage(file='Images/search.png')
        self.theaterImg = PhotoImage(file='Images/theater.png')

        # 랭킹/검색/영화관 검색 프레임 변경을 위한 버튼들
        self.rankingButton = Button(window, relief='groove', image=self.rankingImg, command=self.RankingRaise)
        self.rankingButton.place(x=0, y=0)
        self.searchButton = Button(window, relief='groove', image=self.searchImg, command=self.SearchRaise)
        self.searchButton.place(x=55, y=0)
        self.theaterButton = Button(window, relief='groove', image=self.theaterImg, command=self.TheaterRaise)
        self.theaterButton.place(x=110, y=0)

        # 세부 정보가 출력될 위젯들
        self.canvas = Canvas(window, relief='solid', width=500, height=300)
        self.canvas.place(x=900, y=100)
        self.infoText = Text(window, relief='solid', width=50, height=13, font=myFont)
        self.infoText.place(x=900, y=410)

        # 박스오피스 랭킹 페이지
        self.rankingPage = Frame(window, width=900, height=650, bg='white')
        self.detailInfo = []
        self.posterImage = []
        self.pageNum = 0
        self.periodComboBox = ttk.Combobox(self.rankingPage, width=10)
        self.periodComboBox['value'] = ['일간', '주간']
        self.periodComboBox.current(0)
        self.periodComboBox.place(x=0, y=0)
        self.periodEntry = Entry(self.rankingPage, width=55, relief='solid', bd=2)
        self.periodEntry.insert(END, "YYYYMMDD ex)2020.01.01 → 20200101")
        self.periodEntry.place(x=100, y=0)
        self.rankingSearchButton = Button(self.rankingPage, text='검색', width=5, command=self.RankingSearch)
        self.rankingSearchButton.place(x=500, y=0)
        self.posterButton = []
        for i in range(3):
            self.posterButton.append(Button(self.rankingPage, compound='top', width=210, height=330,
                                            command=lambda idx=i: self.ShowMovieInfo(idx)))
        self.nextPage = Button(self.rankingPage, text='▶', command=self.ShowNextPage)
        self.prevPage = Button(self.rankingPage, text='◀', command=self.ShowPrevPage)
        self.rankingPage.place(x=0, y=100)

        # 배우/감독 검색 페이지
        self.searchPage = Frame(window, width=900, height=650, bg='white')
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
        self.theaterPage = Frame(window, width=900, height=650, bg='white')
        self.nameEntry = Entry(self.theaterPage, width=55, relief='solid', bd=2)
        self.nameEntry.insert(END, "시/군 입력(경기도에 위치한 시/군만 검색 가능합니다.)")
        self.nameEntry.place(x=0, y=0)
        self.nameSearchButton = Button(self.theaterPage, text='검색', width=5)
        self.nameSearchButton.place(x=500, y=0)
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
        self.posterImage.clear()
        self.detailInfo.clear()
        self.pageNum = 0

        if s == '일간':
            tree = DailyRanking(self.periodEntry.get())
            items = tree.iter('dailyBoxOffice')
        elif s == '주간':
            tree = WeaklyRanking(self.periodEntry.get())
            items = tree.iter('weeklyBoxOffice')

        for item in items:
            name = item.find('movieNm').text
            ranking = item.find('rank').text
            oldAndNew = item.find('rankOldAndNew').text
            openDt = item.find('openDt').text.replace('-', '')
            sales = item.find('salesAcc').text
            audi = item.find('audiAcc').text
            detail = '제목: ' + name + '\n' + \
                     '순위: ' + ranking + '(' + oldAndNew + ')' + '\n' + \
                     '개봉일: ' + openDt + '\n' + \
                     '누적 매출: ' + sales + '\n' + \
                     '누적 관객: ' + audi
            self.detailInfo.append(detail)
            url = GetPosterURL(name, openDt)

            if url != 'NoImage':
                with urllib.request.urlopen(url) as u:
                    data = u.read()
                im = Image.open(BytesIO(data))
                self.posterImage.append((name, ImageTk.PhotoImage(im)))
            else:
                self.posterImage.append((name, PhotoImage(file='Images/NoImage.png')))

        for i in range(3):
            self.posterButton[i].configure(text=self.posterImage[i][0], image=self.posterImage[i][1])
            self.posterButton[i].place(x=80 + (250 * i), y=150)

        self.nextPage.place(x=850, y=320)
        self.prevPage.place(x=20, y=320)
        self.nextPage['state'] = 'active'
        self.prevPage['state'] = 'disable'

    def ShowNextPage(self):
        self.pageNum += 1
        self.prevPage['state'] = 'active'
        if self.pageNum == 3:
            self.nextPage['state'] = 'disable'
            self.posterButton[0].configure(text=self.posterImage[9][0],
                                           image=self.posterImage[9][1])
            self.posterButton[1].configure(text='BLANK',
                                           image=PhotoImage(file='Images/NoImage.png'))
            self.posterButton[2].configure(text='BLANK',
                                           image=PhotoImage(file='Images/NoImage.png'))
        else:
            for i in range(3):
                self.posterButton[i].configure(text=self.posterImage[i + (3 * self.pageNum)][0],
                                               image=self.posterImage[i + (3 * self.pageNum)][1])

    def ShowPrevPage(self):
        self.pageNum -= 1
        self.nextPage['state'] = 'active'
        for i in range(3):
            self.posterButton[i].configure(text=self.posterImage[i + (3 * self.pageNum)][0],
                                           image=self.posterImage[i + (3 * self.pageNum)][1])
        if self.pageNum == 0:
            self.prevPage['state'] = 'disable'

    def ShowMovieInfo(self, idx):
        self.canvas.delete('all')
        self.canvas.create_image(250, 150, image=self.posterImage[idx + (3 * self.pageNum)][1])
        self.infoText.delete(1.0, END)
        self.infoText.insert(END, self.detailInfo[idx+(3*self.pageNum)])


MovieApp()
