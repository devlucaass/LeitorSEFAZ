import cv2
from pyzbar.pyzbar import decode

from utils.validators import Validators


class QRCode:
    @staticmethod
    def read_qrcode():
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return None, None

        try:
            while True:
                result, frame = camera.read()

                if not result:
                    break

                decoded_qrcodes = decode(frame)

                for qr in decoded_qrcodes:
                    url = qr.data.decode('utf-8')
                    access_key = QRCode._extract_access_key(url)

                    if not access_key:
                        return None, None

                    if Validators.validate_access_key(access_key):
                        return url, access_key

                    return None, None

                cv2.imshow('Leitor de QRCode', frame)

                if QRCode._is_exit_key():
                    break

            return None, None

        finally:
            QRCode._close_camera(camera)


    @staticmethod
    def _extract_access_key(url):
        if "p=" not in url:
            return None

        return url.split('p=')[-1].split('|')[0]

    @staticmethod
    def _close_camera(camera):
        camera.release()
        cv2.destroyAllWindows()

    @staticmethod
    def _is_exit_key():
        return cv2.waitKey(1) & 0xFF == 27

