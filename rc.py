#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-
# convet vba(coded in 2014) to python script
# 21.12.22 by tsunoppy
########################################################################
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# sympy
import sympy as sym
sym.init_printing()

class rfc:

    def __init__(self):
        self.se = 2.05 * 10**5 # young modulus for steel bar
        self.eps = 10**(-8) # judge deviation

    def rA(self,x): #'鉄筋の断面積
        rA = "未登録"
        if x == 6: rA = 31.7
        if x == 10: rA = 71.3
        if x == 13: rA = 126.7
        if x == 16: rA = 198.6
        if x == 19: rA = 286.5
        if x == 22: rA = 387.1
        if x == 25: rA = 506.7
        if x == 29: rA = 642.4
        if x == 32: rA = 794.2
        if x == 35: rA = 956.6
        if x == 38: rA = 1140.1
        if x == 41: rA = 1339.6
        if x == 51: rA = 2026.8
        #
        if x == 1013: rA = 99.0
        if x == 1310: rA = 99.0
        if x == 1316: rA = 163.0
        if x == 1016: rA = 134.95

        return rA

    def rD(self,x): # 鉄筋の外径
        rD = "未登録"
        if x == 10: rD = 11
        if x == 13: rD = 14
        if x == 16: rD = 18
        if x == 19: rD = 21
        if x == 22: rD = 25
        if x == 25: rD = 28
        if x == 29: rD = 33
        if x == 32: rD = 36
        if x == 35: rD = 40
        if x == 38: rD = 43
        if x == 41: rD = 46

        return rD

    def rdd(self,x): # 鉄筋の公称直径
        rdd = "未登録"

        if x == 10: rdd = 9.53
        if x == 13: rdd = 12.7
        if x == 16: rdd = 15.9
        if x == 19: rdd = 19.1
        if x == 22: rdd = 22.2
        if x == 25: rdd = 25.4
        if x == 29: rdd = 28.6
        if x == 32: rdd = 31.8
        if x == 35: rdd = 34.9
        if x == 38: rdd = 38.1
        if x == 41: rdd = 42.0 # 未確認

        return rdd

    def rphx(self,x): # 鉄筋の周長mm:
        rph = "未登録"
        if x == 10: rph = 30.0
        if x == 13: rph = 40.0
        if x == 16: rph = 50.0
        if x == 19: rph = 60.0
        if x == 22: rph = 70.0
        if x == 25: rph = 80.0
        if x == 29: rph = 90.0
        if x == 32: rph = 100.0
        if x == 35: rph = 110.0
        if x == 38: rph = 120.0
        if x == 41: rph = 130.0
        if x == 51: rph = 160.1

        return rph

    ########################################################################
    #'柱梁接合部の幅の算定
    def bj(self,rbb, lbb, bc, code):

        if code == "+":
            bj = ((rbb + lbb) / 2.0 + bc) / 2.0
        else:
            bj = (rbb + lbb + bc) / 2.0

        if bj > bc :
            bj = bc

        return bj

    ########################################################################
    #'引張重臣距離
    # '46.
    def dtu(self,code):

        if code == 16: dtu = 60 + 0.5 * 46.0
        if code == 17: dtu = 60 + 1.5 * 46.0
        if code == 18: dtu = 60 + 0.5 * 46.0
        if code == 19: dtu = 60 + 1.5 * 46.0
        return dtu

    ########################################################################
    #'引張重臣距離
    def dtb(self,code):
        if code == 16 : dtb = 60.0 + 0.5 * 46.0
        if code == 17 : dtb = 60.0 + 1.5 * 46.0
        if code == 18 : dtb = 60.0 + 1.5 * 46.0
        if code == 19 : dtb = 60.0 + 0.5 * 46.0
        return dtb


    ########################################################################
    #'引張重臣距離
    #'x:鉄筋呼径
    def dtu2(self,code, x):
        if code == 16: dtu2 = 60.0 + 0.5 * self.rD(x)
        if code == 17: dtu2 = 60.0 + 1.5 * self.rD(x)
        if code == 18: dtu2 = 60.0 + 0.5 * self.rD(x)
        if code == 19: dtu2 = 60.0 + 1.5 * self.rD(x)
        return dtu2

    ########################################################################
    #'引張重臣距離
    #'x:鉄筋呼径
    def dtb2(self,code, x):
        if code == 16: dtb2 = 60.0 + 0.5 * self.rD(x)
        if code == 17: dtb2 = 60.0 + 1.5 * self.rD(x)
        if code == 18: dtb2 = 60.0 + 1.5 * self.rD(x)
        if code == 19: dtb2 = 60.0 + 0.5 * self.rD(x)
        return dtb2

    ########################################################################
    #'se 鉄筋の応力度N/mm2
    #'sigy 降伏応力度
    def sig(self,se, eu, xn, dt, sigy):
        sig = se * eu * (xn - dt) / xn
        if abs(sig) > sigy :
            if sig < 0  : sig = -sigy
            if sig >= 0 : sig = sigy
        return sig

    ########################################################################
    #'ACI 梁耐力の算定(下端引張り）
    #'x        鉄筋径mm
    #'fc       設計基準強度N/mm2
    #'b        梁幅mm
    #'dd       梁せいmm
    #'bb       有効幅mm
    #'rat1, rat2, rac1, rac2  主筋断面積mm2
    #'srat     スラブ鉄筋
    #'sr       スラブ筋の鉄筋重臣距離
    #'st       スラブ厚mm
    #'sigy1    主筋の降伏応力度N/mm2
    #'sigy2    スラブ筋の降伏応力度N/mm2
    #'code     鉄筋の並び
    #'
    #'se 鉄筋のヤング係数N/mm2
    #'eu コンクリートの圧縮ひずみ0.003
    #'xn 中立軸mm
    #'sep 鉄筋の許容ひずみ
    def mbuu(self,x, fc, b, dd, bb, rat1, rat2, rac1, rac2, srat,\
             sr, st, sigy1, sigy2, code):

        #'パラメータセット

        if fc <= 28.0 : k1 = 0.85
        elif 28 < fc and fc < 56 :  k1 = 0.85 - 0.05 * (fc - 28.0) / 7.0
        else: k1 = 0.65

        k3 = 0.85
        se = 2.05 * 10 ** 5
        eu = 0.003
        sep = 0.01

        dc1 = self.dtu2(code, x)
        dc2 = dc1 + 2.7 * self.rdd(x)
        dt1 = dd - self.dtb2(code, x)
        dt2 = dt1 - 2.7 * self.rdd(x)

        # initial '初期条件
        xn = dd / 4.0 + 50.0
        k2 = 0.5 * st / xn + 0.5 * k1 * b * (k1 * xn - st) / (b * (k1 * xn - st) + bb * st)
        if k1 * xn < st :
            k2 = 0.5 * k1

        rsc1 = self.sig(se, eu, xn, dc1, sigy1)
        rsc2 = self.sig(se, eu, xn, dc2, sigy1)
        rst1 = self.sig(se, eu, xn, dt1, sigy1)
        rst2 = self.sig(se, eu, xn, dt2, sigy1)
        srs  = self.sig(se, eu, xn, sr, sigy2)

        cc = k3 * fc * (b * (k1 * xn - st) + bb * st)
        if k1 * xn < st :
            cc = k1 * k3 * fc * bb * xn

        f = cc + rac1 * rsc1 + rac2 * rsc2 + rat1 * rst1 + rat2 * rst2 + srat * srs

        #
        xnnxt = 1.0

        #'歪1.0%の時のcodeデータ
        kk = 1

        #'収斂計算
        ###
        for i in range(1 ,10000):

            if kk == 2 : eu = -sep * xnnxt / (xnnxt - dt1)
            k2 = 0.5 * st / xnnxt + 0.5 * k1 * b * (k1 * xnnxt - st) / (b * (k1 * xnnxt - st) + bb * st)
            if k1 * xnnxt < st:
                k2 = 0.5 * k1

            rsc1nxt = self.sig(se, eu, xnnxt, dc1, sigy1)
            rsc2nxt = self.sig(se, eu, xnnxt, dc2, sigy1)
            rst1nxt = self.sig(se, eu, xnnxt, dt1, sigy1)
            rst2nxt = self.sig(se, eu, xnnxt, dt2, sigy1)
            srsnxt = self.sig(se, eu, xnnxt, sr, sigy2)
            ccnxt = k3 * fc * (b * (k1 * xnnxt - st) + bb * st)
            if k1 * xnnxt < st :
                ccnxt = k1 * k3 * fc * bb * xnnxt

            #'    if ccnxt < 0 Then ccnxt = 0#

            fnxt = ccnxt + rac1 * rsc1nxt + rac2 * rsc2nxt + rat1 * rst1nxt + rat2 * rst2nxt + srat * srsnxt

            xn2 = xnnxt
            xnnxt = (fnxt * xn - f * xnnxt) / (fnxt - f)
            #'if xnnxt < 0# Then xnnxt = xn + 1#
            f = fnxt
            xn = xn2

            if abs(fnxt) < self.eps :
                ssepu = -eu * (xn - dt1) / xn

                #print(ssepu,sep,xn,dt1,eu)

                if ssepu < sep + self.eps : break;
                kk = 2
                #'再初期設定
                xn = dd / 4.0 + 50.0
                k2 = 0.5 * st / xn + 0.5 * k1 * b * (k1 * xn - st) / (b * (k1 * xn - st) + bb * st)
                if k1 * xn < st :k2 = 0.5 * k1
                eu = -sep * xn / (xn - dt1)
                #print(eu)

                rsc1 = self.sig(se, eu, xn, dc1, sigy1)
                rsc2 = self.sig(se, eu, xn, dc2, sigy1)
                rst1 = self.sig(se, eu, xn, dt1, sigy1)
                rst2 = self.sig(se, eu, xn, dt2, sigy1)
                srs = self.sig(se, eu, xn, sr, sigy2)
                cc = k3 * fc * (b * (k1 * xn - st) + bb * st)
                if k1 * xn < st :
                    cc = k1 * k3 * fc * bb * xn
                f = cc + rac1 * rsc1 + rac2 * rsc2 + rat1 * rst1 + rat2 * rst2 + srat * srs

                xnnxt = 1.0
                #break;
                #'        Exit For
                #Next i

        rsc1 = rsc1nxt
        rsc2 = rsc2nxt
        rst1 = rst1nxt
        rst2 = rst2nxt
        srs = srsnxt
        cc = ccnxt

        #'曲げモーメントの算定
        mb1 = cc * (dd / 2.0 - k2 * xn)
        mb1 = mb1 + rst1 * rat1 * (dd / 2.0 - dt1)
        mb1 = mb1 + rst2 * rat2 * (dd / 2.0 - dt2)
        mb1 = mb1 + rsc1 * rac1 * (dd / 2.0 - dc1)
        mb1 = mb1 + rsc2 * rac2 * (dd / 2.0 - dc2)
        mb1 = mb1 + srs * srat * (dd / 2.0 - sr)
        mb1 = mb1 / 10 ** 6

        mb2 = xn
        mb3 = -eu * (xn - dt1) / xn * 100
        mb4 = eu * 100

        if -eu * (xn - dt1) / xn > sep + self.eps * 2 :
            mb1 = "Error"

        #print("Cal i",i,"return",mb1,mb2,mb3,mb4)
        return mb1,mb2,mb3,mb4

    ########################################################################
    #'ACI 梁耐力の算定(上端引張り）
    #'fc       設計基準強度N/mm2
    #'b        梁幅mm
    #'dd       梁せいmm
    #'bb       有効幅mm
    #'rat1, rat2, rac1, rac2  主筋断面積mm2
    #'srat     スラブ鉄筋
    #'sr       スラブ筋の鉄筋重臣距離
    #'st       スラブ厚mm
    #'sigy1    主筋の降伏応力度N/mm2
    #'sigy2    スラブ筋の降伏応力度N/mm2
    #'code     鉄筋の並び
    #'
    #'se 鉄筋のヤング係数N/mm2
    #'eu コンクリートの圧縮ひずみ0.003
    #'xn 中立軸mm
    #'sep 鉄筋の許容ひずみ
    def mbut(self,x, fc, b, dd, bb, rat1, rat2, rac1, rac2, srat,\
             sr, st, sigy1, sigy2, code):

        #'パラメータセット
        if fc <= 28.0 : k1 = 0.85
        elif 28 < fc and fc < 56 :  k1 = 0.85 - 0.05 * (fc - 28.0) / 7.0
        else: k1 = 0.65

        k3 = 0.85
        se = 2.05 * 10 ** 5
        eu = 0.003
        sep = 0.01

        dc1 = self.dtu2(code, x)
        dc2 = dc1 + 2.7 * self.rdd(x)
        dt1 = dd - self.dtb2(code, x)
        dt2 = dt1 - 2.7 * self.rdd(x)

        # initial '初期条件
        xn = dd / 4.0 + 50.0
        k2 = 0.5 * k1
        rsc1 = self.sig(se, eu, xn, dc1, sigy1)
        rsc2 = self.sig(se, eu, xn, dc2, sigy1)
        rst1 = self.sig(se, eu, xn, dt1, sigy1)
        rst2 = self.sig(se, eu, xn, dt2, sigy1)
        srs = self.sig(se, eu, xn, dd - sr, sigy2)
        cc = k1 * k3 * fc * b * xn
        f = cc + rac1 * rsc1 + rac2 * rsc2 + rat1 * rst1 + rat2 * rst2 + srat * srs

        xnnxt = 1.0

        #'歪1.0%の時のcodeデータ
        kk = 1

        #'収斂計算
        for i in range(1,10000):

            if kk == 2 : eu = -sep * xnnxt / (xnnxt - dt1)

            rsc1nxt = self.sig(se, eu, xnnxt, dc1, sigy1)
            rsc2nxt = self.sig(se, eu, xnnxt, dc2, sigy1)
            rst1nxt = self.sig(se, eu, xnnxt, dt1, sigy1)
            rst2nxt = self.sig(se, eu, xnnxt, dt2, sigy1)
            srsnxt = self.sig(se, eu, xnnxt, dd - sr, sigy2)
            ccnxt = k1 * k3 * fc * b * xnnxt
            #'    if ccnxt < 0 Then ccnxt = 0#

            fnxt = ccnxt + rac1 * rsc1nxt + rac2 * rsc2nxt \
                + rat1 * rst1nxt + rat2 * rst2nxt + srat * srsnxt

            xn2 = xnnxt
            xnnxt = (fnxt * xn - f * xnnxt) / (fnxt - f)
            if xnnxt < 0.0: xnnxt = xn + 1.0
            f = fnxt
            xn = xn2

            if abs(fnxt) < self.eps :
                ssepu = -eu * (xn - dt1) / xn
                if ssepu < sep + self.eps: break;
                kk = 2
                #'再初期設定
                xn = dd / 4.0 + 50.0
                eu = -sep * xn / (xn - dt1)
                k2 = 0.5 * k1
                rsc1 = self.sig(se, eu, xn, dc1, sigy1)
                rsc2 = self.sig(se, eu, xn, dc2, sigy1)
                rst1 = self.sig(se, eu, xn, dt1, sigy1)
                rst2 = self.sig(se, eu, xn, dt2, sigy1)
                srs = self.sig(se, eu, xn, dd - sr, sigy2)
                cc = k1 * k3 * fc * b * xn
                f = cc + rac1 * rsc1 + rac2 * rsc2 + rat1 * rst1 + rat2 * rst2 + srat * srs

                xnnxt = 1.0

        rsc1 = rsc1nxt
        rsc2 = rsc2nxt
        rst1 = rst1nxt
        rst2 = rst2nxt
        srs = srsnxt
        cc = ccnxt

        #'曲げモーメントの算定
        mb1 = cc * (dd / 2.0 - k2 * xn)
        mb1 = mb1 + rst1 * rat1 * (dd / 2.0 - dt1)
        mb1 = mb1 + rst2 * rat2 * (dd / 2.0 - dt2)
        mb1 = mb1 + rsc1 * rac1 * (dd / 2.0 - dc1)
        mb1 = mb1 + rsc2 * rac2 * (dd / 2.0 - dc2)
        mb1 = mb1 - srs * srat * (dd / 2.0 - sr)
        mb1 = mb1 / 10 ** 6

        mb2 = xn
        mb3 = -eu * (xn - dt1) / xn * 100
        mb4 = eu * 100
        if -eu * (xn - dt1) / xn > sep + self.eps * 2 :
            mb1 = "Error"

        #print("Cal i",i,"return",mb1,mb2,mb3,mb4)
        return mb1,mb2,mb3,mb4

    ########################################################################
    # allowable bending moment strength (kN.m)
    #'fc 許容圧縮応力度（N/mm2)
    #'ft 許容引張応力度 (N/mm2)
    #'dc1 圧縮鉄筋の位置dc/d
    #'γ   腹筋比
    #'pt  引っ張り鉄筋比at/b/d
    #'b   梁幅
    #'d   有効せい
    def gma(self, fc, ft, n, dc1, gamma, pt, b, d):

        xn1 = (n * (1.0 + gamma) - gamma) ** 2 + 2.0 / pt \
            * (n * (1.0 + gamma * dc1) - gamma * dc1)
        xn1 = pt * (xn1 ** (0.5) - (n * (1.0 + gamma) - gamma))
        c1 = n * (1.0 - xn1) * (3.0 - xn1)\
            - gamma * (n - 1) * (xn1 - dc1) * (3.0 * dc1 - xn1)
        c1 = c1 * pt * fc / (3.0 * xn1)

        c2 = n * (1.0 - xn1) * (3.0 - xn1)\
            - gamma * (n - 1) * (xn1 - dc1) * (3.0 * dc1 - xn1)
        c2 = c2 * pt * ft / (3.0 * n * (1.0 - xn1))

        if c1 < c2 :
            gma = c1 * b * d ** 2 / 10 ** 6
            judge = "C"
        if c2 <= c1 :
            gma = c2 * b * d ** 2 / 10 ** 6
            judge = "S"

        return gma,judge,xn1*d

########################################################################
# 柱、MN計算
class Panel:

    def __init__(self,\
                 fc,nw1,nw2,dia_w,fwy,p_type,\
                 bc,dc,nx,ny,dtx,dty,dia_c,fyc,hh,\
                 bg,dg,ntop,nbot,g_type,dia_gtop,dia_gbot,fyb,ll\
                 ):

        #
        self.ees = 2.05 * 10**5

        # set parameter
        # for panel
        self.fc     = fc
        self.nw1    = nw1
        self.nw2    = nw2
        self.dia_w  = dia_w
        self.fwy    = fwy
        self.p_type = p_type

        # for column
        self.bc    = bc
        self.dc    = dc
        self.nx    = nx
        self.ny    = ny
        self.dtx   = dtx
        self.dty   = dty
        self.dia_c = dia_c
        self.fyc   = fyc
        self.hh    = hh

        # for beam
        self.bg     = bg
        self.dg     = dg
        self.ntop   = np.array(ntop)
        self.nbot   = np.array(nbot)
        self.g_type = g_type
        self.dia_gtop  = dia_gtop
        self.dia_gbot  = dia_gbot
        self.fyb    = fyb
        self.ll     = ll

        # print out
        print("# make panel obj")

        # area of each bars
        prop = rfc()
        self.asw = prop.rA(self.dia_w)
        self.asc = prop.rA(self.dia_c)
        print("asw",self.asw,"asc",self.asc)

        self.thy = nw1 * nw2 * self.asw * self.fwy

        print("thy",self.thy)

        self.set_para()
        self.set_column()
        self.set_beam()

    ########################################################################
    # init parameter calc.
    def set_para(self):

        # aci parameter
        self.eu = 0.003
        if fc > 28.0:
            self.k1 = 0.85 - 0.05 * (fc * 10 - 280) / 70
            if self.k1 < 0.65: self.k1 = 0.65
        else:
            self.k1 = 0.85
        self.k2 = self.k1 / 2.0
        self.k3 = 0.85

        # yield strain
        self.ey_b = self.fyb / self.ees
        self.ey_c = self.fyc / self.ees

        #
        print("ACI Prameter")
        print("k1",self.k1,"k2",self.k2,"k3",self.k3)
        print("yield prameter")
        print("beam,ey",self.ey_b,"column,ey",self.ey_c)

    ########################################################################
    # init column.
    def set_column(self):

        # make bar postion
        self.xs = []
        for i in range(0,len(nx)):
            self.bar_pos(nx[i],ny[i],dtx[i],dty[i])


        dcmin = dc/4.0
        print(len(self.xs),self.xs)

        nt = 0
        g  = 0
        for i in range(0,len(self.xs)):
            if self.xs[i] < dcmin:
                nt = nt + 1
                g  = g + self.xs[i]
        g = g / float(nt)

        self.gc = self.dc - 2.0 * g
        # 引張鉄筋の降伏強度
        self.tcy = float(nt) * self.asc * self.fyc
        # 中段鉄筋の降伏強度
        self.tmy = float(len(self.xs)-2.0*nt) * self.asc * self.fyc

        print("gc=",self.gc,"tcy",self.tcy,"tmy",self.tmy)
        self.gc = self.gc / self.dc

    ########################################################################
    # for set_column
    def bar_pos(self,nx,ny,dtx,dty):

        delx = ( self.dc - 2.0 * dtx ) / (nx-1.0)

        for i in range(0,nx):
            self.xs.append( dtx + i * delx )
            self.xs.append( dtx + i * delx )

        for i in range(0,ny-2):
            self.xs.append( dtx )
            self.xs.append( self.dc - dtx )

    ########################################################################
    # for set_column
    def set_beam(self):

        prop = rfc()

        dc = []
        dt = []

        dc.append( prop.dtu2(self.g_type, self.dia_gbot[0]) )

        for i in range(1,len(nbot)):
            dc.append( dc[0] + 2.7 * float(i) * prop.rdd(self.dia_gbot[i]) )

        dt.append( self.dg - prop.dtb2(self.g_type, self.dia_gtop[0]) )

        for i in range(1,len(ntop)):
            dt.append( dt[0] - 2.7 * float(i) * prop.rdd(self.dia_gtop[i]) )

        dc = np.array(dc)
        dt = np.array(dt)

        gb = np.dot(dt,self.ntop)/np.sum(ntop) - np.dot(dc,self.nbot)/np.sum(nbot)

        prop = rfc()
        ab = 0.0
        for i in range(0,len(ntop)):
            ab = ab + ntop[i] * prop.rA(self.dia_gtop[i])

        self.tgy = ab * self.fyb
        print("Tgy",self.tgy)

        self.gb = gb/self.dg


        print("gb",gb,"bar position",dc,dt)

    ########################################################################
    def limit_area(self,nc):
        # nc: axial force [N]

        print("------------------------------")
        print("start, limit area")
        print("------------------------------")
        # aspect ratio
        rr = self.dg/ self.dc

        tb2 = 0.5 * ( 1.0 - self.gb ) * self.bg * self.dg * self.k3 * self.fc
        tc2 = 0.5 * ( 1.0 - self.gc ) * self.bg * self.dc * self.k3 * self.fc - 0.5 * nc

        xi2x = 0.5 / self.k1 * ( 1.0 - self.gb )
        xi2y = 0.5 / self.k1 * ( 1.0 - self.gc )

        print( "gb,gc",self.gb,self.gc)
        print('Tb2',tb2,'Tc2',tc2)
        print('ξ2x',xi2x,'ξ2y',xi2y)

        aa = 1.0 + rr**2
        bb = 1.0 + 1.0/rr**2

        sym.var('x', real = True)

        tb1 = 1.0/ aa * x \
            * self.bc * self.dg * self.k1 * self.k3 * self.fc

        tc1 = 1.0/ bb * x \
            * self.bc * self.dc * self.k1 * self.k3 * self.fc - 0.5 * nc


        prop = rfc()
        ab = 0.0
        for i in range(0,len(ntop)):
            ab = ab + ntop[i] * prop.rA(self.dia_gtop[i])

        ac = self.tcy / self.fyc
        print("ab",ab,"ac",ac)


        f = 1.0 / ( 1.0 + rr**2 ) * self.gb * ( tb1 +tb2 )/2.0 / self.ees / ab \
            + 1.0 / ( 1.0 + 1.0/rr**2 ) * self.gc * ( tc1 + tc2 ) /2.0 / self.ees/ac \

        f = f * x \
            -( 1.0 - x - ( xi2x + xi2y ) ) * self.eu

        xi1 = max(sym.solve(f,x))

        #print(tb1,tc1)
        #print(f)
        print("solve, ξ1",xi1)

        mjh = 1.0/ aa * ( self.gb - 1.0/aa * self.k1 * xi1 )\
            * self.k1 * xi1 * self.bc * self.dg**2 * self.k3 * self.fc\
            + 0.25 * ( 1.0 - self.gb )**2 * self.bg * self.dg**2 * self.k3 * self.fc

        gamma_h = 2.0 * self.gb

        mjv = 1.0/ bb * ( self.gc - 1.0/bb * self.k1 * xi1)\
            * self.k1 * xi1 * self.bc * self.dc**2 * self.k3 * self.fc\
            + 0.25 * ( 1.0 - self.gc )**2 * self.bg * self.dc**2 * self.k3 * self.fc

        gamma_v = 2.0 * self.gc

        mjb = 0.5 * ( mjh + mjv ) / \
            ( 1.0 - 0.5*( gamma_h* self.dg/self.hh + gamma_v * self.dc/self.ll ) )


        tbb = 1.0/aa * xi1 * self.bc * self.dg * self.k1 * self.k3 * self.fc\
            - 0.5 * self.thy + mjb/self.hh

        tcb = 1.0/bb * xi1 * self.bc * self.dc * self.k1 * self.k3 * self.fc\
            - 0.5 * ( nc + self.tmy ) + mjb/self.ll

        """
        print(bb,xi1,self.bc,self.dc,self.k1,self.k3,self.fc)
        print("tcb,Check")
        print( 1.0/bb * xi1 * self.bc * self.dc * self.k1 * self.k3 * self.fc)
        print( - 0.5 * ( nc + self.tmy ) )
        print( mjb/self.ll )
        """

        mjh = mjh/10**6
        mjv = mjv/10**6
        mjb = mjb/10**6

        print("mjh",mjh,"mjv",mjv,"mjb",mjb)
        print("tbb",tbb,"tcb",tcb)

        # difine
        self.tbb = tbb
        self.tcb = tcb


    ########################################################################
    # ultimate panel moment
    def center(self,nc):
        self.limit_area(nc)

        print("------------------------------")
        print("start, center")
        print("------------------------------")

        # tension bar
        #tb1 = min ( self.tgy, self.tbb )
        #tc1 = min ( self.tcy, self.tcb )
        tb1 = self.tgy
        tc1 = self.tcy

        # panel moment

        mjh = ( self.gb - (tb1 + 0.5 * self.thy)/(self.bc*self.dg*self.k3*self.fc) )\
            * ( self.tgy + 0.5 * self.thy ) * self.dg\
            + 0.25*(1.0-self.gb)**2 * self.bg * self.dg**2 * self.k3 * self.fc

        gamma_h = self.gb + 2.0 * ( tb1 + 0.5*self.thy )/( self.bc * self.dg * self.k3 * self.fc )

        mjv = ( self.gc - ( tc1 + 0.5 * ( nc + self.tmy ) )/(self.bc*self.dc*self.k3*self.fc) )\
            *( tc1 + 0.5 * ( nc + self.tmy ) ) * self.dc\
            + 0.25 * ( 1.0 - self.gc )**2 * self.bg * self.dc**2 * self.k3 * self.fc

        gamma_v = self.gc + 2.0* ( tc1 + 0.5*(nc+self.tmy) )\
            / ( self.bc * self.dc * self.k3 * self.fc )

        mju = 0.5 * ( mjh + mjv ) / \
            ( 1.0 - 0.5*( gamma_h* self.dg/self.hh + gamma_v * self.dc/self.ll ) )


        # compression bar at beam
        tb2 = 0.5 * ( 1.0 - self.gb ) * self.bg * self.dg * self.k3 * self.fc\
            - 0.5 * self.thy - mju/self.hh

        tb2_tmp = tb2
        if tb2 > self.tgy: tb2_tmp = self.tgy
        if tb2 <= -self.tgy: tb2_tmp = -self.tgy
        if tb2 <= -self.eu/self.ey_b * self.tgy:
            tb2_tmp = -self.eu/self.ey_b * self.tgy
        if tb2_tmp <= -self.eu/self.ey_b * self.tgy:
            tb2_tmp = -self.eu/self.ey_b * self.tgy

        print("tb2",tb2,"tb2/limit",tb2_tmp)

        if tb2 != tb2_tmp:
            print("modified")

            alpha_b = tb2_tmp/tb1

            mjh = 1.0 - (1.0+self.bc/self.bg)*(tb1+0.5*self.thy)\
                /(self.bc*self.dg*self.k3*self.fc)
            mjh = mjh * (tb1 + 0.5*self.thy) * self.dg
            mjh2 = (1.0-alpha_b)
            mjh2 = mjh2*( (1.0-self.gb) - self.bc/self.bg\
                          * ( (1.0+alpha_b) * tb1 + self.thy )\
                          / ( self.bc*self.dg*self.k3*self.fc ) )
            mjh = mjh-mjh2* tb1 * self.dg

            gamma_h = (1.0-self.bc/self.bg)*(tb1+0.5*self.thy)\
                /(self.bc*self.dg*self.k3*self.fc)\
                +(1.0-alpha_b)*self.bc/self.bg*tb1/(self.bc*self.dg*self.k3*self.fc)
            gamma_h = 1.0 + 2.0 * gamma_h

        # compression bar in column
        tc2 = 0.5 * ( 1.0-self.gc) * self.bg * self.dg * self.k3 * self.fc\
            - 0.5*(nc+self.tmy) + mju/self.ll

        print("tc2=")
        print(0.5 * ( 1.0-self.gc) * self.bg * self.dg * self.k3 * self.fc)
        print(- 0.5*(nc+self.tmy) )
        print( mju/self.ll )

        print("mjh",mjh/10**6,"mjv",mjv/10**6,"mju",mju/10**6)


        tc2_tmp = tc2
        if tc2 > self.tcy: tc2_tmp = self.tcy
        if tc2 <= -self.tcy: tc2_tmp = -self.tcy
        if tc2 <= -self.eu/self.ey_c * self.tcy:
            tc2_tmp = -self.eu/self.ey_c * self.tcy
        if tc2_tmp <= -self.eu/self.ey_c * self.tcy:
            tc2_tmp = -self.eu/self.ey_c * self.tcy

        print("tc2",tc2,"tc2_tmp",tc2_tmp)

        if tc2 != tc2_tmp:
            print("modified tc2")

            alpha_c = tc2_tmp/tc1

            mjv = 1.0 - (1.0+self.bc/self.bg)*(tc1+0.5*(nc+self.tmy))\
                /(self.bc*self.dc*self.k3*self.fc)
            mjv = mjv * (tc1 + 0.5*(nc+self.tmy)) * self.dc
            mjv2 = (1.0-alpha_c)
            mjv2 = mjv2*( (1.0-self.gc) - self.bc/self.bg\
                          * ( (1.0+alpha_c) * tc1 + (nc+self.tmy) )\
                          / ( self.bc*self.dc*self.k3*self.fc ) )
            mjv = mjv-mjv2* tc1 * self.dc

            gamma_v = (1.0-self.bc/self.bg)*(tc1+0.5*(nc+self.tmy))\
                /(self.bc*self.dc*self.k3*self.fc)\
                +(1.0-alpha_c)*self.bc/self.bg*tc1/(self.bc*self.dc*self.k3*self.fc)
            gamma_v = 1.0 + 2.0 * gamma_v

            print(alpha_c,mjv,gamma_v)

        if tc2 != tc2_tmp or tb2 != tb2_tmp:
            mju = 0.5 * ( mjh + mjv ) / \
                ( 1.0 - 0.5*( gamma_h* self.dg/self.hh + gamma_v * self.dc/self.ll ) )

        mjh = mjh/10**6
        mjv = mjv/10**6
        mju = mju/10**6

        print("mjh",mjh,"mjv",mjv,"mju",mju)


########################################################################
# End of Class

if __name__ == '__main__':
    # for panel
    fc     = 60
    nw1    = 6
    nw2    = 4
    dia_w  = 13
    fwy    = 295.0
    p_type = "center"
    # for column
    bc    = 950.0
    dc    = 950.0
    nx    = [5]
    ny    = [7]
    dtx   = [100.0]
    dty   = [100.0]
    dia_c = 41
    fyc   = 490.0
    hh    = 3500.0/2.0
    # for beam
    bg     = 650.0
    dg     = 850.0
    ntop   = [4,4]
    nbot   = [4,2]
    g_type = 19
    dia_gtop  = [41,38]
    dia_gbot  = [41,38]
    fyb    = 490.0
    ll     = 6400.0/2.0


"""
obj = Panel(\
            fc,nw1,nw2,dia_w,fwy,p_type,\
            bc,dc,nx,ny,dtx,dty,dia_c,fyc,hh,\
            bg,dg,ntop,nbot,g_type,dia_gtop,dia_gbot,fyb,ll\
            )

#obj.limit_area(bc*dc*48*0.3)
obj.center(bc*dc*48*0.3)
#obj.center(bc*dc*48*0.4)
#obj.center(-2000.0)
"""


########################################################################
# end of class
"""
test = rfc()

x = 41.0
fc = 36.0
b = 600.0
bb = 950.0
dd = 900.0
rat1 = 4.0*1340.0
rat2 = 4.0*1340.0
rac1 = 4.0*1340.0
rac2 = 4.0*1340.0
srat = 0.0
sr = 40.0
st = 150.0
sigy1 = 490.0
sigy2 = 295.0
code = 17

print(test.mbuu(x, fc, b, dd, bb, rat1, rat2, rac1, rac2, srat, sr, st, sigy1, sigy2, code))
print(test.mbut(x, fc, b, dd, bb, rat1, rat2, rac1, rac2, srat, sr, st, sigy1, sigy2, code))

fc = 2./3.*fc
ft = 490.0
n = 10.0
dc1 = 0.1
gamma = 1.0
pt = (rat1+rat2)/(dd-100)/b
d = dd -100.0
print(test.gma(fc, ft, n, dc1, gamma, pt, b, d))
"""
