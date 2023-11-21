# Virtual_Mouse_Project-Network-Plus

## Project Name  
Virtual Input Interface Using Webcam (Network Plus)  

## Project Overview  
### [Overview]  
"Convenient computer interaction without traditional keyboard and mouse."

● Traditional "keyboard and mouse" are effective and widely used computer input devices. However, some users may be limited in using these input devices due to physical constraints, convenience issues, or spatial constraints.   
● Our team has developed an innovative solution called "Motion Capture-based Hand-Tracking Mouse," allowing users to manipulate the computer using only a webcam without the need for traditional keyboard and mouse.   
● This program detects and interprets the user's hand gestures, enabling mouse pointer movement, clicking, scrolling, dragging, and other functions on the computer screen.  
● By providing this capability, the program offers a more convenient way to operate the computer for users with physical constraints or in special environments.  

### [Development Objectives]
● Providing Non-Contact Interface :    
To enable users to intuitively manipulate the computer screen without the need for traditional keyboards and mice. By detecting hand movements and replacing cursor and keyboard inputs, it significantly enhances user convenience.    
● Accurate Hand Gesture Recognition :    
Accurately recognizing hand shapes to interpret various movements and reflect them in screen operations. This maximizes the utility of the program by precisely conveying the user's desired actions, enhancing the overall user experience.    
● Real-Time Responsiveness :    
Detecting changes in hand shapes in real-time and promptly responding to screen manipulations. Offering smooth movements without buffering to improve user efficiency in their tasks.
● Diverse Application Areas :    
Suitable for use as an assistive device for individuals with disabilities. It can also serve as an innovative interface in presentation tools, media editing, games, and other applications.    

### [Key Design Points]  

● Utilization of motion capture technology    
 Capture and analyze users' hand movements in real-time using a webcam, interpreting various gestures and actions for computer control.  
● Accurate tracking algorithm   
 Employ a highly accurate model through precise model training to smoothly and accurately control the mouse pointer's movement by recognizing hand movements.  
● Simple user interface   
 Design an intuitive and easy-to-use interface to allow any user to easily access and utilize the program.  

### [Expected Effects]  

● Overcoming physical constraints    
 Provide a better computer usage environment for those who find it challenging to use physical keyboards and mice, expanding the scope of digital activities.  
● Creative utilization   
 Enable new interaction designs based on user hand movements, encouraging creative and interesting ways of using computers.  
● Improved work productivity   
 Enhance work productivity in environments such as industrial settings, where users can manipulate computers without direct physical contact.  
● Enhanced security    
 Strengthen privacy management as computer usage is possible in shared environments without personal input devices.  

## [Technologies Used]  

● Development tools : PyCharm, Visual Studio Code, Qt Designer  
● Programming language : Python 3.7.9  
● Frameworks and technology stack : TensorFlow, Keras, PyQt5  
● Python libraries : OpenCV 4.5.1.48, Mediapipe 0.8.7  
● Modules and libraries : socket, threading, math, numpy, time, psutil, autopy, pyautogui, pygetwindow, zlib, base64, shutil, subprocess, enum, struct, etc.  

## [Project development schedule]    
● Development Phase 1 : 2023.6.1 ~ 7.14    
● Development Phase 2 : 2023.7.17 ~ 8.18    

------------------------------------
## 1. 프로젝트명  
WebCam을 이용한 가상 입력 인터페이스 (네트워크 기능 추가)      

## 2. 프로젝트 개요   
### [개요]  
“기존의 키보드와 마우스 없이도 편리하게”  
● 기존의 “키보드와 마우스”는 효과적이고 널리 사용되는 컴퓨터 입력 장치이다. 그러나 일부 사용자들에게는 신체적인 제약이나 편의성, 장소적 문제로 인해 이러한 입력 장치의 사용이 제한될 수 있다.   
● 우리 조에서 개발한 "Motion Capture 기반의 Hand-Tracking Mouse" 프로그램은 사용자가 기존의 키보드와 마우스 없이 웹캠만을 사용해 컴퓨터를 조작할 수 있게 해주는 혁신적인 솔루션이다.  
● 이 프로그램은 사용자의 손동작을 감지하고 해석하여 컴퓨터 화면 위에서 마우스 포인터를 움직이며 클릭 및 스크롤, 드래그 등의 기능을 구현한다.  
● 이러한 장점을 통해 신체적 제약이 있는 사용자나 특수한 환경에서 더 편리하게 컴퓨터를 조작할 수 있는 환경을 제공한다.  

### [개 발 목 표]
● 비접촉 인터페이스 제공 :
사용자가 기존의 키보드와 마우스 없이도 컴퓨터 화면을 손 모양을 통해 직관적으로 조작할 수 있도록 한다. 손의 동작을 감지하여 커서 및 키보드 입력을 대체하므로 사용자의 편의성을 크게 향상 시킨다.    
● 정확한 손 모양 인식 :     
손 모양을 정확하게 인식하여 다양한 동작을 해석하고 화면 조작에 반영한다. 이를 통해 사용자가 원하는 동작을 정확하게 전달하여 프로그램의 유용성을 최대한 높이며, 사용자 경험을 향상 시킨다.    
● 실시간 반응성 :     
실시간으로 손 모양의 변화를 감지하고 화면 조작에 즉각적으로 반응한다. 버퍼링 없는 자연스러운 움직임을 제공하여 사용자의 작업 효율을 향상 시킨다.    
● 다양한 응용 분야 :     
장애인 보조 장치로도 사용 가능하며 프레젠테이션 도구, 미디어 편집, 게임 등에서 혁신적인 인터페이스로 활용될 수 있다.    

### [설계의 주안점]  
● 모션 캡처 기술 활용   
 웹캠을 사용해 사용자의 손동작을 실시간으로 캡처하고 분석, 이를 통해 다양한 제스처와 동작을 해석하여 컴퓨터 조작에 반영한다.  
● 정확한 트래킹 알고리즘    
 손의 움직임을 정확하게 인식하기 위해 정확도 높은 모델학습을 통해 마우스 포인터의 움직임을 부드럽고 정확하게 제어한다.   
● 간편한 사용 인터페이스    
 직관적이고 쉬운 사용 인터페이스를 디자인하여 어떠한 사용자라도 프로그램을 쉽게 접근하고 활용할 수 있도록 한다.  

### [기대 효과]  
● 신체적 제약극복   
 물리적인 키보드와 마우스 사용이 어려운 사람들에게 더 나은 컴퓨터 사용 환경을 제공하여 디지털 활동의 범위를 확장한다.  
● 창의적 활용   
 사용자의 손동작을 활용한 새로운 Interaction Design을 가능하게 하여 창의적이고 흥미로운 컴퓨터 활용 방식을 유도한다.  
● 작업 생산성 향상   
 산업 현장 등 사용자가 직접적인 접촉 없이도 컴퓨터를 조작할 수 있기에 작업 생산성을 높일 수 있다.   
● 보안 강화   
 공용 장소와 같은 환경에서 개인용 입력 장치 없이도 컴퓨터 사용이 가능하므로 개인 정보 보호 관리가 강화된다.  

### [사용 기술]  
● 개발 도구 : PyCharm, Visual Studio Code, Qt Designer  
● 사용 언어 : Python 3.7.9   
● 프레임워크 및 기술 스택 : TensorFlow, Keras, PyQt5  
● Python 라이브러리 : OpenCV 4.5.1.48, Mediapipe 0.8.7   
● 모듈 및 라이브러리 : socket, threading, math, numpy, time, psutil, autopy, pyautogui, pygetwindow, zlib, base64, shutil, subprocess, enum, struct 등  

### [프로젝트 개발 일정]
● 개발 1단계 : 2023.6.1 ~ 7.14   
● 개발 2단계 : 2023.7.17 ~ 8.18   
