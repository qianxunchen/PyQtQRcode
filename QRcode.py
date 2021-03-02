import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QPushButton, QMessageBox, QLabel,QComboBox,QRadioButton, QFileDialog, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
import qrcode
from PIL import Image
import time

class Start(QtWidgets.QWidget):
    def __init__(self):
        super(Start, self).__init__()
        # 创建窗口
        self.window = QWidget()
        self.window.resize(540, 410)
        self.window.setWindowTitle("二维码生成器")
        #图标
        self.window.setWindowIcon(QIcon("./Tools/icon.png"))
        # 创建输入窗口
        self.text_tips = QLabel(self.window)
        self.text_tips.setText("请在下面输入需要生成二维码的信息：")
        self.text_tips.move(30, 20)
        self.textBox = QPlainTextEdit(self.window)
        self.textBox.resize(320, 350)
        self.textBox.move(30, 40)
        # 是否使用中心图像
        self.btn1 = QRadioButton(self.window)
        self.btn1.setText("使用中心图像")
        self.btn1.move(355, 40)
        # 默认不选
        self.btn1.setChecked(False)
        #选择图片路径
        self.btn = QPushButton(self.window)
        self.btn.setText("浏览")
        self.btn.move(469, 65)
        self.btn.resize(40, 26)
        self.btn.clicked.connect(self.msg)
        #路径显示
        self.photopath = QLineEdit(self.window)
        self.photopath.move(355, 65)
        self.photopath.resize(112, 25)



        # 二维码颜色下拉框
        self.fill_tips = QLabel(self.window)
        self.fill_tips.move(355, 145)
        self.fill_tips.setText("前景色: ")
        self.fill_color = QComboBox(self.window)
        self.fill_color.move(430, 140)
        self.fill_color.resize(80, 25)
        self.fill_color.addItems(['黑色', '绿色', '橙色', '蓝色'])
        # 背景色下拉框
        self.back_tips = QLabel(self.window)
        self.back_tips.move(355, 115)
        self.back_tips.setText("背景色: ")
        self.back_color = QComboBox(self.window)
        self.back_color.move(430, 110)
        self.back_color.resize(80, 25)
        self.back_color.addItems(['白色', '粉色', '橙黄色', '浅蓝色'])


        #二维码展示
        self.QR_tips = QLabel(self.window)
        self.QR_tips.move(355, 168)
        self.QR_tips.setText("二维码:")
        self.show_QR = QLabel(self.window)
        self.show_QR.move(355, 190)
        self.show_QR.resize(170, 170)
        self.show_QR.setScaledContents(True)#图片大小自适应
        self.show_QR.setPixmap(QPixmap(""))
        # 创建按钮
        self.button = QPushButton("生成", self.window)
        self.button.move(370, 365)
        self.button.resize(56, 25)
        # 监控是否点击按钮
        self.button.clicked.connect(self.make_QRcode)
        # 保存二维码
        self.down_QR = QPushButton("保存", self.window)
        self.down_QR.move(450, 365)
        self.down_QR.resize(56, 25)
        # 监控是否点击按钮
        self.down_QR.clicked.connect(self.down_QRcode)




    def msg(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,"选取文件","./","All Files (*);;Image Files (*.jpg;*.png)")#设置文件扩展名过滤,注意用双分号间隔
        #将读取到的路径显示到文本框中
        self.photopath.setText(fileName1)



    def make_QRcode(self):
        # 获取当前内容
        colors = {
                    '黑色': '#000000',
                    '白色': '#FFFFFF',
                    '粉色': '#FF99FF',
                    '绿色': '#009933',
                    '浅蓝色': '#00CCFF',
                    '蓝色': '#0066FF',
                    '橙色': '#FF9933',
                    '橙黄色': '#FFCC99',
        }
        fill_color = self.fill_color.currentText()
        back_color = self.back_color.currentText()
        back_color = colors.get(back_color)
        fill_color = colors.get(fill_color)
        photo_path = self.photopath.text()
        photo_yes_or_no = self.btn1.isChecked()
        data = self.textBox.toPlainText()

        qr = qrcode.QRCode(
            version=2,#二维码大小
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=4,
        )

        # 添加数据
        qr.add_data(data)
        # 填充数据
        qr.make(fit=True)
        # 生成图片
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        if photo_yes_or_no:
            if len(photo_path) > 0:
                # 添加logo，打开logo照片
                icon = Image.open(photo_path)
                # 获取图片的宽高
                img_w, img_h = img.size
                # 参数设置logo的大小
                factor = 6
                size_w = int(img_w / factor)
                size_h = int(img_h / factor)
                icon_w, icon_h = icon.size
                if icon_w > size_w:
                    icon_w = size_w
                if icon_h > size_h:
                    icon_h = size_h
                # 重新设置logo的尺寸
                icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
                # 得到画图的x，y坐标，居中显示
                w = int((img_w - icon_w) / 2)
                h = int((img_h - icon_h) / 2)
                # 黏贴logo照
                img.paste(icon, (w, h), mask=None)
            else:
                error = QMessageBox()
                error.setWindowTitle(u'错误')
                error.setText("请选择图片!")
                error.setWindowIcon(QIcon("./Tools/icon.png"))
                # 隐藏ok按钮
                # error.addButton(QMessageBox.Ok)
                # error.button(QMessageBox.Ok).hide()
                # 定时关闭提示框
                error.setStandardButtons(QMessageBox.Ok)
                error.button(QMessageBox.Ok).animateClick(2000)
                # 模态对话框
                error.exec_()
                return
        fill_temp = "./Tools/temp"
        img.save(fill_temp)
        # 弹窗
        ok = QMessageBox()
        ok.setWindowTitle(u'提示')
        ok.setText("二维码已生成!")
        ok.setWindowIcon(QIcon("./Tools/icon.png"))
        # 隐藏ok按钮
        # ok.addButton(QMessageBox.Ok)
        # ok.button(QMessageBox.Ok).hide()
        # 定时关闭提示框
        ok.setStandardButtons(QMessageBox.Ok)
        ok.button(QMessageBox.Ok).animateClick(2000)
        # 模态对话框
        ok.exec_()
        fill_name = fill_temp
        self.show_QR.setPixmap(QPixmap(fill_name))

    def down_QRcode(self):
        Time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        name = Time + ".jpg"
        photo = self.show_QR.pixmap().toImage()
        photo.save("./QRcode/%s" % name)
        # 保存成功弹窗
        msgBox = QMessageBox()
        msgBox.setWindowTitle(u'提示')
        msgBox.setText("二维码保存成功!")
        msgBox.setWindowIcon(QIcon("./Tools/icon.png"))
        # 隐藏ok按钮
        # msgBox.addButton(QMessageBox.Ok)
        # msgBox.button(QMessageBox.Ok).hide()
        # 定时关闭提示框
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.button(QMessageBox.Ok).animateClick(2000)
        # 模态对话框
        msgBox.exec_()





if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    start = Start()
    start.window.show()
    # 进入主循环保证界面不关闭
    sys.exit(app.exec_())


