import pandas as pd
import openpyxl

class bank:
    
    def __init__(self):
        print("초기 설정 완료")
        self.log = ''
        self.data = dict()
        self.bank_data = pd.Series([self.data.keys(),self.data.values()], index = ['name', 'money'])

        try:    
            self.files = openpyxl.load_workbook('data.xlsx')
            self.xlsx = self.files.active
            self.load()

        except FileNotFoundError:
            files = openpyxl.Workbook()
            files.save('data.xlsx')            
            
            self.files = openpyxl.load_workbook('data.xlsx')
            self.xlsx = self.files.active
            
    def add_user(self, user):
        if user in self.data.keys():
            print("이미 존제하는 유저입니다.")
            return 1

        else:
            print(f"{user} 추가 성공")
            self.data[user] = 0
            return 0

    def manage(self, user, money):
        if user in self.data.keys():
            print(f"{user} 한테서 {money} 추가했습니다.")
            self.data[user] += int(money)
            return 0
        
        else:
            print('존제하지 않는 유저입니다.')
            return 1

    def save(self):
        for i in range(len(self.data)): 
            self.xlsx.cell(row=i+2, column=1).value = list(self.data.keys())[i]
            self.xlsx.cell(row=i+2, column=2).value = self.data[list(self.data.keys())[i]]
            
        self.files.save('data.xlsx')

    def load(self):
        num = 1
        while True:
            if self.xlsx.cell(row=num+1, column=1).value != None:
                self.data[self.xlsx.cell(row=num+1, column=1).value] = self.xlsx.cell(row=num+1, column=2).value
                num += 1

            else:
                break
            
        self.bank_data = pd.Series([self.data.keys(),self.data.values()], index = ['name', 'money'])
    
    def cheack(self, user):
        return self.data[user]

    def log_add(self, log_data):
        self.log += log_data + '\n'
    
    def log_save(self):
        with open("log.txt", "r") as f:
            _log = f.read()
            self.log = _log + self.log

        with open("log.txt", "w") as f:
            f.write(self.log)



# bot = bank()
# bot.add_user('야스')
# bot.add_user('잭스')
# print(bot.bank_data)
# bot.manage('이누', 100)
# print(bot.bank_data)
# bot.save()





