import qrcode

class QRCode:

    def __init__(self, data=None):
        self.data = data
        self.qr, self.img = self.generateQR()

    def generateQR(self):
        qr = qrcode.QRCode(version=None, error_correction=qrcode.ERROR_CORRECT_H)
        qr.add_data(self.data)
        qr.make(fit=True)
        return qr, qr.make_image(back_color=(255, 255, 255), fill_color=(0, 0, 0))

    def setData(self, data):
        self.data = data
        self.qr, self.img = self.generateQR()
