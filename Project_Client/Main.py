# main.py : 프로그램 시작점.

import sys
from PyQt5.QtWidgets import QApplication
from App_Init import App_Control


__copyright__ = 'HTML Team (Hand Tracking MotionCapture Lab) 2023 '
__version__ = '2023_08 '
__license__ = 'MIT License'
__developer__ = 'KimDaeYoung42, Woosss99, Su-hwanKim, minseok4266, ELUKA123'
__author_email__ = 'Representative : Hawkthema@gmail.com'
__url__ = 'https://github.com/KimDaeYoung42/Virtual_Mouse_Project'

# Copyright (c) [2023_08] ['KimDaeYoung42, Woosss99, Su-hwanKim, minseok4266, ELUKA123']
#
# 이 소프트웨어는 MIT 라이선스 하에 배포됩니다.
# 자세한 내용은 LICENSE 파일을 참조하십시오.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App_Control()
    window.show()
    sys.exit(app.exec_())


