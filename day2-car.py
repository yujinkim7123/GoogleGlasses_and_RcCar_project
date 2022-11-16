# SSAFY8 embedded proj.
# day 2. RC Vehicle

'''
- 주어진 킷트를 조립하여 rc-car를 제작한다.
- Raspberry pi 4 model B 를 컨트롤러로 사용하여 ssh로 연결된 호스트컴퓨터(pc)에서 콘솔에 명령어를 입력함으로써 차량을 제어할 수 있다.
- 구현해야할 기본 명령은 '앞으로/ 뒤로/ 정지/ 빠르게/ 느리게/ 오른쪽/ 왼쪽/ 중앙' 이다.
- wifi통해 네트워크 연결되도록 한다.
'''

# 모듈 로드
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

# 모터 초기설정
mh = Raspi_MotorHAT(addr = 0x6f)
motor = mh.getMotor(2) # M2단자에 모터연결
speed = 125 # 모터 속도 0~255
motor.setSpeed(speed)

# 서보 초기설정
servo = mh._pwm
servo.setPWMFreq(50)

servoCH = 0 # 서보 연결된 핀
SERVO_PULSE_MAX = 400   # 서보 작동 범위
SERVO_PULSE_MIN = 200

# 앞으로
def go():
    motor.run(Raspi_MotorHAT.FORWARD)

# 뒤로
def back():
    motor.run(Raspi_MotorHAT.BACKWARD)

# 모터 정지
def stop():
    motor.run(Raspi_MotorHAT.RELEASE)

# 빠르게
def speed_up():
    global speed
    speed = 255 if speed >= 235 else speed + 20 # 최대 255, 20단위로 증가
    motor.setSpeed(speed)

# 느리게
def speed_down():
    global speed
    speed = 0 if speed <= 20 else speed - 20 # 최하 0
    motor.setSpeed(speed)

# 각도만큼 핸들 틀기
def steer(angle = 0):   
    if angle <= -60:
        angle = -60
    if angle >= 60:
        angle = 60
    pulse_time = SERVO_PULSE_MIN + (SERVO_PULSE_MAX - SERVO_PULSE_MIN) // 180 * (angle + 90) # angle = -90˚~ +90˚ 사이의 값. 비례해서 pulse_time이 정해짐

    servo.setPWM(servoCH, 0, pulse_time)

# 우회전
def steer_right():
    steer(30)

# 좌회전
def steer_left():
    steer(-30)

# 핸들 중앙
def steer_center():
    steer(0)

def main():
    command = ['go', 'back', 'stop', 'fast', 'slow', 'right', 'left', 'center']
    func = [go, back, stop, speed_up, speed_down, steer_right, steer_left, steer_center]

    try:
        while True:
            word = input("명령['go', 'back', 'stop', 'fast', 'slow', 'right', 'left', 'center'] : ")
            if word in command:
                func[command.index(word)]() # word에 해당하는 index의 func 실행

    except KeyboardInterrupt:
        print('\n사용자의 요청으로 종료합니다...')
    except:
        print('\n확인되지 않은 오류입니다...')
    finally:
        motor.run(Raspi_MotorHAT.RELEASE)
    
if __name__ == '__main__':
    main()
