from tkinter import *
from tkinter import ttk
import tkinter.font
import tkinter.messagebox as msgbox
from xmlFunc import *
from openapi_http import *
import urllib
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO
from EmailSendFunc import *
from DateCheckModule import DateCheck
import telepot
from datetime import datetime

temp = None

YMD = datetime.today().strftime("%Y%m%d")
DAYOFWEEK = datetime.today().weekday()


class MovieApp:
    def __init__(self):
        window = Tk()
        window.title("MovieApp")
        window.geometry("1400x750")
        myFont = tkinter.font.Font(window, family='맑은 고딕', size=14)

        # 텔레그램 봇
        self.bot = telepot.Bot("1135581434:AAH6GHgLSZM5_SSgGl3jXltDyF9wTa2nXDg")

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
        self.rankingPosterImage = []
        self.rankingPosterImageForEmail = []
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
        self.sendEmail_BoxOffice = Button(self.rankingPage, text='Email', command=self.CreateEmailWindow_BoxOffice)
        self.posterButton = []
        for i in range(3):
            self.posterButton.append(Button(self.rankingPage, compound='top', width=210, height=350,
                                            command=lambda idx=i: self.ShowMovieInfo(idx)))
        self.nextPage = Button(self.rankingPage, text='▶', command=self.ShowNextPage)
        self.prevPage = Button(self.rankingPage, text='◀', command=self.ShowPrevPage)
        self.rankingPage.place(x=0, y=100)

        # 배우/감독 검색 페이지
        self.searchPage = Frame(window, width=900, height=650, bg='white')
        self.searchElementComboBox = ttk.Combobox(self.searchPage, width=10)
        self.searchElementComboBox['value'] = ['영화', '배우', '감독']
        self.searchElementComboBox.current(0)
        self.selectedElement = None
        self.searchElementComboBox.place(x=0, y=0)
        self.nameEntry = Entry(self.searchPage, width=55, relief='solid', bd=2)
        self.nameEntry.insert(END, "영화제목/배우/감독의 이름 입력")
        self.nameEntry.place(x=100, y=0)
        self.nameSearchButton = Button(self.searchPage, text='검색', width=5, command=self.NameSearch)
        self.nameSearchButton.place(x=500, y=0)
        self.actorAndDirectorListbox = Listbox(self.searchPage, width=50, height=35, relief='solid', bd=5)
        self.nameSearchResultList = []
        self.filmoListbox = Listbox(self.searchPage, width=50, height=35, relief='solid', bd=5)
        self.filmoList = []
        self.selectedName = None
        self.moviePoster = None
        self.moviePosterForEmail = None
        self.viewFilmoButton = Button(self.searchPage, text='조회', width=5, command=self.ViewFilmo)
        self.viewDetailInfoButton = Button(self.searchPage, text='세부 정보', command=self.ShowDetailInfo)
        self.sendEmail_MovieInfo = Button(self.searchPage, text='Email', command=self.CreateEmailWindow_MovieInfo)
        self.movieListbox = Listbox(self.searchPage, width=100, height=35, relief='solid', bd=5)
        self.movieList = []
        self.searchPage.place(x=0, y=100)

        # 영화관 검색 페이지
        self.theaterPage = Frame(window, width=900, height=650, bg='white')
        self.theaterComboBox = ttk.Combobox(self.theaterPage, width=10)
        self.theaterComboBox['value'] = ['시/군']
        self.searchValue = None
        self.MapView = None
        self.mapImageForEmail = None
        self.theaterComboBox.current(0)
        self.theaterComboBox.place(x=0, y=0)
        self.theaterEntry = Entry(self.theaterPage, width=70, relief='solid', bd=2)
        self.theaterEntry.insert(END, "시/군 입력(경기도에 위치한 시/군만 검색 가능합니다.)")
        self.theaterEntry.place(x=100, y=0)
        self.theaterSearchButton = Button(self.theaterPage, text='검색', width=5, command=self.TheaterSearch)
        self.theaterSearchButton.place(x=610, y=0)
        self.viewMapsButton = Button(self.theaterPage, text='지도 보기', command=self.viewMap)
        self.theaterListbox = Listbox(self.theaterPage, width=100, height=35, relief='solid', bd=5)
        self.theaterList = []
        self.theaterPage.place(x=0, y=100)

        # 처음 시작시 랭킹 페이지가 나오도록 설정함
        self.rankingPage.tkraise()

        self.bot.message_loop(self.CheckMsg)

        window.mainloop()

    def CheckMsg(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            print("텍스트만 입력하세요.")
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('일간') and len(args) > 1:
            if not DateCheck(args[1]):
                self.bot.sendMessage(chat_id, "유효한 날짜를 입력해주세요.\nex)2020년 1월 1일 -> 20200101")
                return
            msg = self.GetDailyRanking(args[1])
            self.bot.sendMessage(chat_id, msg)
        elif text.startswith('주간') and len(args) > 1:
            if not DateCheck(args[1]):
                self.bot.sendMessage(chat_id, "유효한 날짜를 입력해주세요.\nex)2020년 1월 1일 -> 20200101")
            msg = self.GetDailyRanking(args[1])
            self.bot.sendMessage(chat_id, msg)
        elif text.startswith('정보') and len(args) > 1:
            msg = GetDetailInfo(args[1])
            self.bot.sendMessage(chat_id, msg)
        else:
            self.bot.sendMessage(chat_id,
                            '알 수 없는 명령어입니다.\n일간 YYYYMMDD, 주간 YYYYMMDD, 정보 [영화코드] 명령어 중 하나를 입력해주세요\n영화코드는 일간/주간을 검색하면 알 수 있습니다.')

    def GetDailyRanking(self, date):
        tree = DailyRanking(date)
        items = tree.iter('dailyBoxOffice')
        msg = ''
        for item in items:
            name = item.find('movieNm').text
            ranking = item.find('rank').text
            movieCd = item.find('movieCd').text
            msg += ranking + '. ' + name + ' [영화코드: ' + movieCd + ']\n'
        msg += '해당 영화코드를 사용해 해당 영화의 상세정보를 조회할 수 있습니다.'
        return msg

    def GetWeeklyRanking(self, date):
        tree = DailyRanking(date)
        items = tree.iter('weeklyBoxOffice')
        msg = ''
        for item in items:
            name = item.find('movieNm').text
            ranking = item.find('rank').text
            movieCd = item.find('movieCd').text
            msg += ranking + '. ' + name + ' [영화코드: ' + movieCd + ']\n'
        msg += '해당 영화코드를 사용해 해당 영화의 상세정보를 조회할 수 있습니다.'
        return msg

    def GetDetailInfo(self, code):
        return GetDetailInfo(code)

    def RankingRaise(self):
        self.rankingPage.tkraise()
        self.canvas.delete('all')
        self.infoText.delete(1.0, END)
        self.sendEmail_BoxOffice.place_forget()
        self.sendEmail_MovieInfo.place_forget()

    def SearchRaise(self):
        self.searchPage.tkraise()
        self.canvas.delete('all')
        self.infoText.delete(1.0, END)
        self.sendEmail_BoxOffice.place_forget()
        self.sendEmail_MovieInfo.place_forget()

    def TheaterRaise(self):
        self.theaterPage.tkraise()
        self.canvas.delete('all')
        self.infoText.delete(1.0, END)
        self.sendEmail_BoxOffice.place_forget()
        self.sendEmail_MovieInfo.place_forget()

    def RankingSearch(self):
        s = self.periodComboBox.get()
        self.canvas.delete('all')
        self.infoText.delete(1.0, END)
        self.sendEmail_BoxOffice.place_forget()
        self.rankingPosterImage.clear()
        self.detailInfo.clear()
        self.rankingPosterImageForEmail.clear()
        self.pageNum = 0
        date = self.periodEntry.get()
        date_i = int(date)
        YMD_i = int(YMD)
        if s == '일간':
            if date == YMD:
                msgbox.showerror("유효하지 않은 날짜입니다.", "당일 박스오피스 순위는 조회할 수 없습니다.")
                return
            elif YMD_i < date_i:
                msgbox.showerror("유효하지 않은 날짜입니다.", "미래의 박스오피스 순위는 알 수 없습니다.")
                return
            elif not DateCheck(date):
                msgbox.showerror("유효하지 않은 날짜입니다.", "유요한 날짜를 입력해주세요\nex)2020년 1월 1일 -> 20200101")
                return
            tree = DailyRanking(self.periodEntry.get())
            items = tree.iter('dailyBoxOffice')
        else:
            if YMD_i + (6-DAYOFWEEK) < date_i:
                msgbox.showerror("유효하지 않은 날짜입니다.", "미래의 박스오피스 순위는 알 수 없습니다.")
                return
            elif YMD_i - DAYOFWEEK <= date_i <= YMD_i + (6 - DAYOFWEEK):
                msgbox.showerror("유효하지 않은 날짜입니다.", "금주 박스오피스 순위는 조회할 수 없습니다.")
                return
            elif not DateCheck(date):
                msgbox.showerror("유효하지 않은 날짜입니다.", "유요한 날짜를 입력해주세요\nex)2020년 1월 1일 -> 20200101")
                return
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
            url = GetPosterURL_openDt(name, openDt)

            if url != 'NoImage':
                with urllib.request.urlopen(url) as u:
                    data = u.read()
                self.rankingPosterImageForEmail.append(data)
                im = Image.open(BytesIO(data))
                self.rankingPosterImage.append((name, ImageTk.PhotoImage(im)))
            else:
                with open('Images/NoImage.gif', 'rb') as img:
                    self.rankingPosterImageForEmail.append(img.read())
                self.rankingPosterImage.append((name, PhotoImage(file='Images/NoImage.png')))

        for i in range(3):
            self.posterButton[i].configure(text=self.rankingPosterImage[i][0], image=self.rankingPosterImage[i][1])
            self.posterButton[i].place(x=80 + (250 * i), y=150)

        self.nextPage.place(x=850, y=320)
        self.prevPage.place(x=20, y=320)
        self.nextPage['state'] = 'active'
        self.prevPage['state'] = 'disable'

    def NameSearch(self):
        if self.selectedElement == '영화':
            self.movieListbox.place_forget()
            self.viewDetailInfoButton.place_forget()
        elif self.selectedElement == '감독' or self.selectedElement == '배우':
            self.filmoListbox.place_forget()
            self.viewDetailInfoButton.place_forget()
        self.canvas.delete('all')
        self.infoText.delete(1.0, END)
        self.sendEmail_MovieInfo.place_forget()

        self.selectedElement = self.searchElementComboBox.get()
        if self.selectedElement == '영화':
            movieNm = self.nameEntry.get()
            self.movieList = GetMovies(movieNm)
            self.movieListbox.delete(0, END)
            for movie in self.movieList:
                self.movieListbox.insert(END, movie[0])
            self.movieListbox.place(x=20, y=50)
            self.viewDetailInfoButton.place(x=820, y=320)

        elif self.selectedElement == '배우':
            name = self.nameEntry.get()
            self.nameSearchResultList = GetActor(name)
            self.actorAndDirectorListbox.delete(0, END)
            for people in self.nameSearchResultList:
                self.actorAndDirectorListbox.insert(END, people[0])
            self.actorAndDirectorListbox.place(x=20, y=50)
            self.viewFilmoButton.place(x=390, y=320)

        else:
            name = self.nameEntry.get()
            self.selectedName = name
            self.nameSearchResultList = GetDirector(name)
            self.actorAndDirectorListbox.delete(0, END)
            for people in self.nameSearchResultList:
                self.actorAndDirectorListbox.insert(END, people[0])
            self.actorAndDirectorListbox.place(x=20, y=50)
            self.viewFilmoButton.place(x=390, y=320)

    def ShowNextPage(self):
        self.pageNum += 1
        self.prevPage['state'] = 'active'
        if self.pageNum == 3:
            self.nextPage['state'] = 'disable'
            self.posterButton[0].configure(text=self.rankingPosterImage[9][0],
                                           image=self.rankingPosterImage[9][1])
            self.posterButton[1].place_forget()
            self.posterButton[2].place_forget()
        else:
            for i in range(3):
                self.posterButton[i].configure(text=self.rankingPosterImage[i + (3 * self.pageNum)][0],
                                               image=self.rankingPosterImage[i + (3 * self.pageNum)][1])

    def ShowPrevPage(self):
        if self.pageNum == 3:
            self.posterButton[1].place(x=330, y=150)
            self.posterButton[2].place(x=580, y=150)
        self.pageNum -= 1
        self.nextPage['state'] = 'active'
        for i in range(3):
            self.posterButton[i].configure(text=self.rankingPosterImage[i + (3 * self.pageNum)][0],
                                           image=self.rankingPosterImage[i + (3 * self.pageNum)][1])
        if self.pageNum == 0:
            self.prevPage['state'] = 'disable'

    def ShowMovieInfo(self, idx):
        self.canvas.delete('all')
        self.canvas.create_image(250, 150, image=self.rankingPosterImage[idx + (3 * self.pageNum)][1])
        self.infoText.delete(1.0, END)
        self.infoText.insert(END, self.detailInfo[idx + (3 * self.pageNum)])
        self.imageIndex = idx + (3 * self.pageNum)
        self.sendEmail_BoxOffice.place(x=550, y=0)

    def ViewFilmo(self):
        code = self.nameSearchResultList[self.actorAndDirectorListbox.curselection()[0]][1]
        self.selectedName = self.nameSearchResultList[self.actorAndDirectorListbox.curselection()[0]][0]
        self.filmoList = GetFilmo(code, self.selectedElement)
        self.filmoListbox.delete(0, END)
        for filmo in self.filmoList:
            self.filmoListbox.insert(END, filmo[0])
        self.filmoListbox.place(x=450, y=50)
        self.viewDetailInfoButton.place(x=820, y=320)

    def ShowDetailInfo(self):
        if self.selectedElement == '배우':
            title = self.filmoList[self.filmoListbox.curselection()[0]][0]
            code = self.filmoList[self.filmoListbox.curselection()[0]][1]
            url = GetPosterURL_actor(title, self.selectedName)
            if url != 'NoImage':
                with urllib.request.urlopen(url) as u:
                    data = u.read()
                self.moviePosterForEmail = data
                im = Image.open(BytesIO(data))
                self.moviePoster = ImageTk.PhotoImage(im)
                self.canvas.delete('all')
                self.canvas.create_image(250, 150, image=self.moviePoster)
            else:
                with open('Images/NoImage.gif', 'rb') as img:
                    self.moviePosterForEmail = img.read()
                self.moviePoster = PhotoImage(file='Images/NoImage.png')
                self.canvas.delete('all')
                self.canvas.create_image(250, 150, image=self.moviePoster)
            DetailInfo = GetDetailInfo(code)
            self.infoText.delete(1.0, END)
            self.infoText.insert(END, DetailInfo)

        elif self.selectedElement == '감독':
            title = self.filmoList[self.filmoListbox.curselection()[0]][0]
            code = self.filmoList[self.filmoListbox.curselection()[0]][1]
            url = GetPosterURL_director(title, self.selectedName)
            if url != 'NoImage':
                with urllib.request.urlopen(url) as u:
                    data = u.read()
                self.moviePosterForEmail = data
                im = Image.open(BytesIO(data))
                self.moviePoster = ImageTk.PhotoImage(im)
                self.canvas.delete('all')
                self.canvas.create_image(250, 150, image=self.moviePoster)
            else:
                with open('Images/NoImage.gif', 'rb') as img:
                    self.moviePosterForEmail = img.read()
                self.moviePoster = PhotoImage(file='Images/NoImage.png')
                self.canvas.delete('all')
                self.canvas.create_image(250, 150, image=self.moviePoster)
            DetailInfo = GetDetailInfo(code)
            self.infoText.delete(1.0, END)
            self.infoText.insert(END, DetailInfo)

        else:
            title = self.movieList[self.movieListbox.curselection()[0]][0]
            code = self.movieList[self.movieListbox.curselection()[0]][1]
            openDt = self.movieList[self.movieListbox.curselection()[0]][2]
            url = GetPosterURL_openDt(title, openDt)
            if url != 'NoImage':
                with urllib.request.urlopen(url) as u:
                    data = u.read()
                self.moviePosterForEmail = data
                im = Image.open(BytesIO(data))
                self.moviePoster = ImageTk.PhotoImage(im)
                self.canvas.delete('all')
                self.canvas.create_image(250, 150, image=self.moviePoster)
            else:
                with open('Images/NoImage.gif', 'rb') as img:
                    self.moviePosterForEmail = img.read()
                self.moviePoster = PhotoImage(file='Images/NoImage.png')
                self.canvas.delete('all')
                self.canvas.create_image(250, 150, image=self.moviePoster)
            DetailInfo = GetDetailInfo(code)
            self.infoText.delete(1.0, END)
            self.infoText.insert(END, DetailInfo)
        self.sendEmail_MovieInfo.place(x=550, y=0)

    def CreateEmailWindow_BoxOffice(self):
        global temp
        temp = Tk()
        temp.title("Email")
        temp.geometry('240x50')
        e = Entry(temp, width=25)
        e.insert(END, "받는 사람의 메일 주소")
        e.grid(row=0, column=0)
        b = Button(temp, text='보내기', command=self.SendEmail_BoxOffice)
        b.grid(row=1, column=1)

    def CreateEmailWindow_MovieInfo(self):
        global temp
        temp = Tk()
        temp.title("Email")
        temp.geometry('240x50')
        e = Entry(temp, width=25)
        e.insert(END, "받는 사람의 메일 주소")
        e.grid(row=0, column=0)
        b = Button(temp, text='보내기', command=self.SendEmail_MovieInfo)
        b.grid(row=1, column=1)

    def CreateEmailWindow_Map(self):
        global temp
        temp = Tk()
        temp.title("Email")
        temp.geometry('240x50')
        e = Entry(temp, width=25)
        e.insert(END, "받는 사람의 메일 주소")
        e.grid(row=0, column=0)
        b = Button(temp, text='보내기', command=self.SendEmail_MovieInfo)
        b.grid(row=1, column=1)

    def SendEmail_MovieInfo(self):
        global temp
        image = self.moviePosterForEmail
        text = self.infoText.get(1.0, END)
        SendMail(image, text, 'MovieApp에서 보낸 영화 상세 정보입니다.')
        msgbox.showinfo("Email send complete", "메일을 성공적으로 전송했습니다.")
        temp.destroy()

    def SendEmail_BoxOffice(self):
        global temp
        image = self.rankingPosterImageForEmail[self.imageIndex]
        text = self.infoText.get(1.0, END)
        SendMail(image, text, 'MovieApp에서 보낸 박스오피스 정보입니다.')
        msgbox.showinfo("Email send complete", "메일을 성공적으로 전송했습니다.")
        temp.destroy()

    def TheaterSearch(self):
        if self.searchValue == '시/군':
            self.theaterListbox.place_forget()
            self.viewMapsButton.place_forget()
        self.canvas.delete('all')
        self.infoText.delete(1.0, END)  # 초기화

        self.searchValue = self.theaterComboBox.get()

        if self.searchValue == '시/군':
            location = self.theaterEntry.get()
            self.theaterList = GetLocation(location)
            self.theaterListbox.delete(0, END)
            for theater in self.theaterList:
                self.theaterListbox.insert(END, theater[0])
            self.theaterListbox.place(x=20, y=50)
            self.viewMapsButton.place(x=820, y=320)

    def viewMap(self):
        x = self.theaterList[self.theaterListbox.curselection()[0]][1]
        y = self.theaterList[self.theaterListbox.curselection()[0]][2]
        urlData = GetMap(x, y)
        im = Image.open(BytesIO(urlData))
        self.MapView = ImageTk.PhotoImage(im)
        self.canvas.delete('all')
        self.canvas.create_image(250, 150, image=self.MapView)
        Local = '주소 : ' + self.theaterList[self.theaterListbox.curselection()[0]][4]  # 도로명 주소
        self.infoText.delete(1.0, END)
        self.infoText.insert(END, Local)


MovieApp()
