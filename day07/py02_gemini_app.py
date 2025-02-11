# py02_gemini_app.py
# tkinter를 클래스화
from tkinter import *
from tkinter.messagebox import * 
from tkinter.scrolledtext import * 
from tkinter.font import *
import google.generativeai as genai

genai.configure(api_key='AIzaSyDd0Faaw5EU-kqVE9x8koMimr4DgEk5n70')
model = genai.GenerativeModel('gemini-1.5-flash')

class window(Tk):
    def __init__(self):
        super().__init__()  # 부모객체도 같이 초기화
        self.title('제미나이 챗봇 v2.0')
        self.geometry('730x450')
        self.iconbitmap('./image/bot.ico')
        # 클래스 작업할 때는 self...유심히 볼 것
        self.protocol('WM_DELETE_WINDOW', self.onClosing)

        self.initWindow() # 윈도우 화면 초기화 멤버함수(메서드)

    def initWindow(self):
        # Font init
        self.myFont = Font(family='NanumGothic', size=10)
        self.boldFont= Font(family='NanumGothic', size=10, weight=BOLD, slant=ITALIC)
        
        # InputFrame init(UI 화면 구성)
        self.inputFrame = Frame(self, width=730, height=30, bg='pink')
        self.inputFrame.pack(side=BOTTOM, fill=BOTH)
        
        # textMessage Init(inputFrame에 들어갈 Entry 구성)
        self.textMessage = Text(self.inputFrame, width=75, height=1, wrap=WORD, font=self.myFont)
        self.textMessage.bind('<Key>', self.keypress) # 입력창에서 엔터를 치면 keypress 이벤트처리함수
        self.textMessage.pack(side=LEFT, padx=15)

        # buttonsSend init(inputFrame에 들어갈 Button 구성)
        self.buttonSend = Button(self.inputFrame, text='전송', bg='green', fg='white', 
                                 font=self.myFont, 
                                 command=self.responseMessage)
        self.buttonSend.pack(side=RIGHT, padx=20, pady=5)

        # textResult init
        self.textResult = ScrolledText(self, wrap=WORD, bg='gray', fg='white', font=self.myFont) #bg='black'
        self.textResult.pack(fill=BOTH, expand=True)

        self.textResult.tag_configure('user', font=self.boldFont, foreground='yellow')
        self.textResult.tag_configure('ai', font=self.boldFont, foreground='limegreen')   #89F336
        self.textResult.tag_configure('error', font=self.boldFont, foreground='red')  

        self.textMessage.focus_set()

    def keypress(self, event):
            if event.char == '\r':
                self.responseMessage()

    def responseMessage(self):  # 내용 수정
        # showinfo('동작', 
                #  f'이제 API를 호출하면 됩니다!\n{self.textMessage.get("1.0", END)}')
        inputText = self.textMessage.get('1.0', END).replace('\n','').strip()
        print(inputText)
        self.textMessage.delete('1.0', END)

        if inputText:
            try:
                self.textResult.insert(END, '유저: ', BOLD)
                self.textResult.insert(END, f'{inputText}\n\n', 'user')

                ai_response = model.generate_content(inputText)
                response = ai_response.text

                self.textResult.insert(END, '챗봇: ', 'bold')
                self.textResult.insert(END, f'{response}\n\n', 'ai')
            
            except Exception as e:
                self.textResult.insert(END, f'Error: {str(e)}\n\n', 'error')
            finally:
                self.textResult.see(END)    
    
    def onClosing(self):
        if askyesno('종료확인', '종료하시겠습니까?'):
            self.destroy()  # 완전 종료
        
if __name__=='__main__':
    print('Tkinter 클래스 시작!')
    app = window()  #Tkinter 클래스 객체 생성
    app.mainloop()