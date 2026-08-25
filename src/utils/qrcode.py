import cv2
import pyzbar

from utils.validators import Validators


class QRCode:
    def read_qrcode(self):
        camera = cv2.VideoCapture(0)

        try:
            while True:
                result, frame = camera.read()

                if not result:
                    break

                qrcode = pyzbar.decode(frame)

                for qr in qrcode:
                    url = qr.data.decode('utf-8')
                    access_key = QRCode._extract_access_key()

                    if Validators.validate_access_key(access_key):
                        return url

                    print(f'QR Code inválido: {url}')
                    return False

                cv2.imshow('Leitor de QRCode', frame)

                
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            return False

        finally:
            QRCode._close_camera()


    @staticmethod
    def _extract_access_key(value):
        return value.split('p=')[-1].split('|')[0]

    @staticmethod
    def _close_camera(camera):
        camera.release()
        cv2.destroyAllWindows()

