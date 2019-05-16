import wx
from threading import Thread
from moxa_main import *


class MyFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.SetSize((500, 450))
        self.SetMaxSize((500, 450))
        self.SetMinSize((500, 450))
        self.SetTitle("MOXA刷机程序")

        # 初始化变量
        self.file = ""
        self.ip = "http://192.168.127.253"

        # 面板设计
        self._init_frame()

        # 事件绑定
        self._func_event()

        self.Center()
        self.Show()

    def _init_frame(self):
        # 设置画板
        pnl = wx.Panel(self)
        vb = wx.BoxSizer(wx.VERTICAL)
        hb1 = wx.BoxSizer(wx.HORIZONTAL)
        hb2 = wx.BoxSizer(wx.VERTICAL)
        hb3 = wx.BoxSizer(wx.VERTICAL)

        ######################################
        # 第一层 配置文件
        ######################################
        text1 = wx.StaticText(pnl, wx.ID_ANY, u"配置文件")
        self.hb1_tc2 = wx.TextCtrl(pnl)
        self.hb1_button1 = wx.Button(pnl, label=u"打开")
        self.hb1_button2 = wx.Button(pnl, label=u"网络检测")
        hb1.AddMany([(text1, 0, wx.ALIGN_CENTER | wx.ALL, 5),
                     (self.hb1_tc2, 1, wx.EXPAND | wx.ALL, 5),
                     (self.hb1_button1, 0, wx.EXPAND | wx.ALL, 5),
                     (self.hb1_button2, 0, wx.EXPAND | wx.ALL, 5),])

        ######################################
        # 第二层 测试区域
        ######################################
        box3 = wx.StaticBoxSizer(wx.StaticBox(pnl, 0, label="测试区域"))
        text4 = wx.StaticText(box3.GetStaticBox(), wx.ID_ANY, u"交换机IP:")
        self.hb2_tc5 = wx.TextCtrl(box3.GetStaticBox())
        self.hb2_tc5.AppendText(self.ip)  # 写入初始化IP地址
        self.hb2_button2 = wx.Button(box3.GetStaticBox(), wx.ID_ANY, u"刷机",
                                    wx.DefaultPosition, wx.Size(80, 30), 0)
        self.hb2_button2.Disable()
        self.hb2_button3 = wx.Button(box3.GetStaticBox(), wx.ID_ANY, u"检查",
                                    wx.DefaultPosition, wx.Size(80, 30), 0)
        box3.AddMany([(text4, 0, wx.ALIGN_CENTER | wx.ALL, 5),
                      (self.hb2_tc5, 1, wx.EXPAND | wx.ALL, 5),
                      (self.hb2_button2, 0, wx.EXPAND | wx.ALL, 5),
                      (self.hb2_button3, 0, wx.EXPAND | wx.ALL, 5),
                      ])
        hb2.AddMany([(box3, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5),
                     ])

        ######################################
        # 第三层 打印区域
        ######################################
        self.pt_text = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)

        vb.AddMany([(hb1, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5),
                    (hb2, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5),
                    (self.pt_text, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5)])
        pnl.SetSizer(vb)
        self.CreateStatusBar()

    def _func_event(self):
        # 对事件绑定
        self.hb1_button1.Bind(wx.EVT_BUTTON, self._open_file)
        self.hb1_button2.Bind(wx.EVT_BUTTON, self._ping_event)
        self.hb2_button2.Bind(wx.EVT_BUTTON, self._start_event)
        self.hb2_button3.Bind(wx.EVT_BUTTON, self._check_event)

    def _open_file(self, e):
        """
        选择固件升级的文件的事件
        :param e:
        :return:
        """
        wildcard = "*.*"
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(),
                            "", wildcard, wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetFilename()
            file_path = dlg.GetDirectory()
            self.hb1_tc2.AppendText(file_name)
            self.file = os.path.join(file_path, file_name)
        dlg.Destroy()

    def _ping_event(self, e):
        # 网络检测的事件，并打开刷机的按键
        ip = self.hb2_tc5.GetValue()
        ip = ip.split("//")[1]
        var = 1
        self.hb2_button2.Enable()
        ping_thread = Thread(target=self._check_ping, args=(ip, var))
        ping_thread.start()

    def _start_event(self, e):
        # 刷机的事件，并关闭刷机按键
        ip = self.hb2_tc5.GetValue()
        self.hb2_button2.Disable()
        start_thread = Thread(target=self._start_moxa, args=(ip, self.file))
        start_thread.start()

    def _check_event(self, e):
        # 检查的事件
        ip = self.hb2_tc5.GetValue()
        check_thread = Thread(target=self._check_moxa, args=(ip,))
        check_thread.start()

    def _start_moxa(self, ip, file):
        """
        刷机的函数体，先对文件传递进来的文件进行判断，而后调用函数进行刷机，
        对交换机持续进行ping，网络通后，打印结束，退出
        :param ip:
        :param file:
        :return:
        """
        if not file:
            self.pt_text.AppendText(u"%s文件不存在或为空，请重新选择\n" % time_now())
            return
        else:
            self.pt_text.Clear()
            web = moxa_info(self.ip)  # 登陆
            self.pt_text.AppendText(u"%s刷机开始\n"%time_now())
            moxa_up(web, file)  # 升级
            ping_ip = ip.split("//")[1]
            for i in range(65):
                time.sleep(1)
                res = check_ip_ping(ping_ip)
                self.pt_text.AppendText("%d,"%i)
                if not res:
                    self.pt_text.AppendText("\n交换机正在启动.......\n")
                    break
            self._check_ping(ping_ip)
            self.pt_text.AppendText(u"%s刷机已经成功，请点击检查\n" % time_now())

    def _check_moxa(self, ip):
        """
        检查的函数体，调用函数进行检查，并返回检查结果
        :param ip:
        :return:
        """
        web = moxa_info(ip)  # 登陆
        res = moxa_check(web)  # 检查
        if isinstance(res,int):
            text = "检查完毕，对应模块数量为%d\n"%res
            self.pt_text.AppendText(text)
        else:
            self.pt_text.AppendText("%s%s"%(time_now(),res))

    def _check_ping(self, ip, var=0):
        """
        网络检查函数体，并返回结果
        :param ip:
        :param var:
        :return:
        """
        while True:
            time.sleep(1)
            res = check_ip_ping(ip)
            if res:
                self.pt_text.AppendText(u"%s网络重连成功\n" % time_now())
                if var:
                    wx.MessageBox(u"交换机重启成功，点击“刷机”",
                                  u"成功", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox(u"交换机重启成功，点击“检查”",
                                  u"成功", wx.OK | wx.ICON_INFORMATION)
                return
            else:
                self.pt_text.AppendText(u"%s网络重连中...\n" % time_now())


if __name__ == '__main__':
    app = wx.App()
    win = MyFrame(None)
    app.MainLoop()