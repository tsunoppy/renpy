#! /Users/tsuno/.pyenv/shims/python3
# -*- coding:utf-8 -*-
import os, sys
#import Image
#import urllib2
#from cStringIO import StringIO


#zipアーカイブからファイルを読み込むため。通常は必要ないはず。
#sys.path.insert(0, 'reportlab.zip')

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

########################################################################
import pandas as pd
import sqlite3

#
import linecache
#

class Report():

    ########################################################################
    # init data
    def __init__(self,cntlfile,draw_path,coldata,st):

        self.cntlFile = cntlfile
        self.pathname = os.path.dirname(self.cntlFile)
        #self.FONT_NAME = "Helvetica"
        self.FONT_NAME = "GenShinGothic"
        GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"
        # フォント登録
        pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))

        self.draw_path = draw_path
        self.coldata = coldata
        self.st = st
        #font_size = 20
        #c.setFont('GenShinGothic', font_size)

    ########################################################################
    # 文字と画像を配置
    def create_row(self,c, index, df, df2, index2):
        #y_shift = -240 * index
        #y_shift = -360 * index
        y_shift = -180 * index # divided by 4
        c.setFont(self.FONT_NAME, 9)


        xlist = [65, (40+560)/3]
        offset = 0.25
        ylist = [self.ypos(0+offset,y_shift),\
                 self.ypos(8+offset,y_shift),\
                 self.ypos(9+offset,y_shift),\
                 self.ypos(10+offset,y_shift),\
                 self.ypos(11+offset,y_shift)]
        c.grid(xlist, ylist )

        #title = "C1"
        #size = "1200x1000"
        #comment = "30-D41"
        #material = "Fc60, SD490"

        b  = "{:.0f}".format(self.coldata[index+index2][0])
        d  = "{:.0f}".format(self.coldata[index+index2][1])
        fc = "{:.0f}".format(self.coldata[index+index2][2])
        fy = "{:.0f}".format(self.coldata[index+index2][3])
        dia= "{:.0f}".format(self.coldata[index+index2][4])
        total = "{:.0f}".format(self.coldata[index+index2][5])

        title = str(self.draw_path[index+index2])
        size = str(b) + "x" + str(d)
        comment = str(total) + "-D" + str(dia)
        material = "Fc" + str(fc) + ", fy=" + str(fy)


        # Model
        c.setFont(self.FONT_NAME, 12)
        c.drawCentredString(53, self.ypos(5,y_shift),
                     str(self.st[index+index2])\
                     )
        c.drawCentredString(130, self.ypos(0,y_shift),
                     title\
                     )
        c.setFont(self.FONT_NAME, 10)

        #
        c.drawString(70, self.ypos(9,y_shift),
                     "BxD:"\
                     )
        c.drawString(70, self.ypos(10,y_shift),
                     "Bar:"\
                     )
        c.drawString(70, self.ypos(11,y_shift),
                     "Fc,fy:"\
                     )
        #
        c.drawCentredString(150, self.ypos(9,y_shift),
                     size\
                     )
        c.drawCentredString(150, self.ypos(10,y_shift),
                     comment\
                     )
        c.drawCentredString(150, self.ypos(11,y_shift),
                     material\
                     )
        """
        mc_x = "{:10.0f}".format(df.iloc[0,1])

        """

        # png
        #imagefile="./db/"+str(index2+index)+"mp.png"
        #imagefile=self.pathname + "/" + df2.iloc[13].replace(' ','') + "mp.png"
        imagefile = "./db/" + self.draw_path[index2+index] + "_mn.png"

        #print("Index=",index2+index)
        #c.drawImage(imagefile, 250,  y_shift + 470, width=5*cm , preserveAspectRatio=True)
        #c.drawImage(imagefile, 300,  y_shift + 280, width=9*cm , preserveAspectRatio=True)
        c.drawImage(imagefile,\
                    210,  y_shift + 310, width=12*cm, preserveAspectRatio=True, mask='auto')

        imagefile = "./db/" + self.draw_path[index2+index] + "_model.png"
        c.drawImage(imagefile,\
                    87,  y_shift + 450, width=3*cm, preserveAspectRatio=True, mask='auto')

    ########################################################################

    # 空の行を作成
    def create_row_brank(self,c, index, df, df2, index2):
        #y_shift = -240 * index
        #y_shift = -360 * index
        y_shift = -180 * index # divided by 4
        c.setFont(self.FONT_NAME, 9)

        xlist = [65, (40+560)/3]
        offset = 0.25
        ylist = [self.ypos(0+offset,y_shift),\
                 self.ypos(8+offset,y_shift),\
                 self.ypos(9+offset,y_shift),\
                 self.ypos(10+offset,y_shift),\
                 self.ypos(11+offset,y_shift)]
        c.grid(xlist, ylist )

    ########################################################################
    def ypos(self,ipos,y_shift):
        #return 730-(ipos-1)*10 + y_shift
        return 730-(ipos-1)*14 + y_shift

    ########################################################################
    # pdfの作成
    def print_page(self, c, index, nCase, title):


        #タイトル描画
        c.setFont(self.FONT_NAME, 20)
        #c.drawString(50, 795, u"Design of the twoway slab")
        #c.drawString(50, 795, u"Fiber Analysis")
        #c.drawString(50, 795, u"MN-Diagram")
        c.drawString(50, 795, title)

        #グリッドヘッダー設定
        #xlist = [40, 380, 560]
        #xlist = [40, (40+560)/2, 560]
        #xlist = [40, (40+560)/3, 560]
        xlist = [40, 65, (40+560)/3, 560]
        #xlist = [40, 65, 560]
        ylist = [760, 780]
        c.grid(xlist, ylist)

        #sub title
        c.setFont(self.FONT_NAME, 12)
        c.drawString(45, 765, u"St.")
        c.drawCentredString(130, 765, u"Section" )
        c.drawCentredString((200+560)/2, 765, u"M-N Diagram")
        #c.drawCentredString(300, 765, u"X-Dir." )
        #c.drawCentredString(480, 765, u"Y-Dir." )

        for i in range(0,nCase):

            """
            df2 = pd.read_csv(self.cntlFile)
            df2 = df2.iloc[i+index,:]
            table = self.pathname + "/" + df2.iloc[13].replace(' ','') + "cap"
            df  = pd.read_csv(table)
            data = df
            """
            data = "."
            df2 = "."

            print("insert row to pdf report, row:", i+index )
            if self.draw_path[i+index] != "*":
                #print(self.draw_path[i+index])
                #print(self.coldata[i+index][0])
                self.create_row( c, i, data, df2, index )
            else:
                #print(self.draw_path[i+index],"^b^")
                #print(self.coldata[i+index][0])
                self.create_row_brank( c, i, data, df2, index )

        #最後にグリッドを更新
        #ylist = [40,  280,  520,  760]
        #ylist = [40,  400,  760]
        #ylist = [40,  160, 280, 400, 520, 640, 760]
        ylist = [40,  220,  400, 580, 760]
        c.grid(xlist, ylist[4 - nCase:] )
        #ページを確定
        c.showPage()

    ########################################################################
    # pdfの作成
    def print_head(self, c , title):

        #title = 'Sample Project'

        #タイトル描画
        c.setFont(self.FONT_NAME, 20)
        c.drawString(50, 795, title)

        #sub title
        c.setFont(self.FONT_NAME, 12)

        #データを描画
        ########################################################################
        inputf = './db/input.txt'
        f = open(inputf,'r', encoding='utf-8')
        tmpData = []
        while True:
            line = f.readline()
            if line:
                if line != '\n':
                    tmpData.append(line.replace('\n',''))
                else:
                    tmpData.append('')
            else:
                break
        f.close()
        data = tmpData
        #c.setFont(self.FONT_NAME, 9)
        for i in range(0,len(data)):
            # txt
            c.drawString(55, 720-(i-1)*14, data[i])
        """
        # Model Diagram
        imagefile = './db/model.png'
        c.drawImage(imagefile, 60,  -300, width=18*cm , preserveAspectRatio=True)
        """
        #ページを確定
        c.showPage()
    ########################################################################
    # whole control
    def create_pdf(self, dataNum, pdfFile, title):

        # Parameter -------
        # inputf   : path to text file
        # imagefile: path to png file
        # pdfFile  : name of making pdf file

        #フォントファイルを指定して、フォントを登録
        #folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
        #pdfmetrics.registerFont(TTFont(FONT_NAME, os.path.join(folder, 'ipag.ttf')))
        #出力するPDFファイル
        c = canvas.Canvas(pdfFile)

        # ページ数
        ########################################################################
        #dataNum = len(inputf)
        numPage = dataNum // 4
        numMod = dataNum % 4
        #print(numPage,numMod)
        if numMod >= 1:
            numPage = numPage + 1

        # pdfの作成
        ########################################################################
        #self.print_head( c , title)

        for i in range(0,numPage):
            index = 4*i # index: 参照データのインデックス
            if numPage == 1:
                self.print_page( c, index, dataNum, title)
            elif i != numPage-1 and numPage != 1:
                self.print_page( c, index, 4, title)
            else:
                if numMod != 0:
                    self.print_page( c, index, numMod, title)
                else:
                    self.print_page( c, index, 4, title)

        #pdfファイル生成
        ########################################################################
        c.save()
        print ("repot.py is Okay!!.")

########################################################################
# END CLASS


"""
########################################################################
# test script

pathname = "./test.pdf"
obj = Report()
# テキストの読み込み
########################################################################
inputf = []
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")

title = "sample"

obj.create_pdf(3,pathname,title)
"""

#title = 'sample'
#pathname = "./test.pdf"
#Report().create_pdf(15,pathname,title)
