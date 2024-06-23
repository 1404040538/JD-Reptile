import tkinter.messagebox
from tkinter import *
import 滑块验证码实战 as hk
import 层次分析法 as cly
import 随机森林 as forest

import threading
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidget()

    def createWidget(self):
        Label(root,text='欢迎来到京东商品价格指导系统').place(width=200,height=20,x=150)

        Label(root,text='请输入需要质询的商品名称:').place(width=150,height=20,y=20)

        self.entry01 = Entry(root)
        self.entry01.place(width=150,height=20,x=150,y=20)

        Button(root,text='查询',command=self.consult).place(width=30,height=20,x=310,y=20)
        Button(root,text='结束查询',command=self.end_chrome).place(width=60,height=20,x=310,y=40)
        Button(root,text='退出系统',command=self.master.destroy).place(width=60,height=20,x=310,y=60)


        self.text01 = Text(root,width=100,height=10)
        self.text01.place(x=50,y=100)
        Button(root, text='开始分类数据', command=self.classify).place(width=80, height=20, x=310, y=240)

        Label(root, text='请输入需要预测的商品价格:').place(width=150, height=100, y=300)
        self.entry02 = Entry(root)
        self.entry02.place(width=150, height=20, x=150, y=340)

        Label(root, text='请输入需要预测的商品名字:').place(width=150, height=100, y=370)
        self.entry03 = Entry(root)
        self.entry03.place(width=150, height=20, x=150, y=410)

        Button(root, text='开始预测', command=self.forest_start).place(width=60, height=20, x=300, y=410)
    def consult(self):
        good_name = self.entry01.get()
        t = threading.Thread(target=self.startup, args=(good_name,))
        t.start()

    def startup(self, good_name):
            try:
                message = hk.startup(good_name)
                for i in message:
                    self.text01.insert(END,str(i)+'\n')
                tkinter.messagebox.showinfo("Message", "运行结束，请查看数据文件")
                hk.end()
            except EXCEPTION as e:
                print(e)
    def forest_start(self):
        try:
            pre_pr = self.entry02.get()
            pre_name = self.entry03.get()
            t2 = threading.Thread(target=self.back_forest, args=(pre_pr, pre_name))
            t2.start()
        except EXCEPTION as e:
            print(f"出现错误：{e}")

    def back_forest(self,pre_pr,pre_name):
        message2 = forest.run(pre_pr,pre_name)
        print("运行成功")
        self.text01.insert(END,"预计评论数量为"+str(message2[0])+'\n')

    def classify(self):
        try:
            message1,goods_list = cly.run()
            print("分类成功")
            for i in message1:
                self.text01.insert(END,str(i)+'\n')
            print("得分前十的商品为："+'\n')
            for ii in goods_list:
                self.text01.insert(END,f"商品名：{ii[1]},售价：{ii[2]},评论数量：{ii[3]}，得分：{ii[0]}\n")
        except:
            print("运行出现错误")


    def end_chrome(self):
        hk.end()


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x500")
    root.title('京东商品价格指导')
    app = Application(master=root)
    root.mainloop()