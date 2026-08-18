import cv2
import pyzbar

from utils.validators import Validators


def read_qrcode():
    cam = cv2.VideoCapture(0)

    try:
        while True:
            result, frame = cam.read()

            if not result:
                break

            qrcode = pyzbar.decode(frame)

            for qr in qrcode:
                url = qr.data.decode('utf-8')
                access_key = url.split('p=')[-1].split('|')[0]

                if Validators.validate_access_key(access_key):
                    return url

                print(f'QR Code inválido: {url}')
                return False

            cv2.imshow('Leitor de QRCode', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        return False

    finally:
        cam.release()
        cv2.destroyAllWindows()