from utils.video_stream import VideoStream
from gesture_recognition.hand_landmark import HandLandmarkDetector
from slide_control.slide_control import SlideController
import time

import time  # Para controle do tempo

class GestureStateMachine:
    def __init__(self, threshold=0.05, stabilization_time=1.0, cooldown_time=0.5):
        self.state = "NEUTRO"  # Estado inicial
        self.last_command_time = None  # Timestamp do último comando emitido
        self.last_hand_position = None  # Posição inicial da mão no estado NEUTRO
        self.threshold = threshold  # Limiar de movimentação para mudança de estado
        self.stabilization_time = stabilization_time  # Tempo de estabilização
        self.cooldown_time = cooldown_time  # Tempo de espera entre comandos
        self.slide_controller = SlideController()

    def is_neutral(self, hand_landmarks):
        """Verifica se a mão está na posição neutra."""
        index_tip = hand_landmarks[8].x
        middle_tip = hand_landmarks[12].x
        wrist = hand_landmarks[0].x

        # A mão está vertical e alinhada
        return abs(index_tip - middle_tip) < 0.02 and abs(index_tip - wrist) < 0.05

    def is_moving_right(self, hand_landmarks):
        """Verifica se a mão está se movendo para a direita."""
        if self.last_hand_position is None:
            return False  # Sem referência inicial
        current_x = hand_landmarks[8].x  # Posição X do dedo indicador
        return current_x - self.last_hand_position > self.threshold

    def is_moving_left(self, hand_landmarks):
        """Verifica se a mão está se movendo para a esquerda."""
        if self.last_hand_position is None:
            return False  # Sem referência inicial
        current_x = hand_landmarks[8].x  # Posição X do dedo indicador
        return self.last_hand_position - current_x > self.threshold

    def update_state(self, hand_landmarks):
        """Atualiza o estado com base nos landmarks."""
        if self.last_command_time is None:
            self.last_command_time = time.time()  # Inicializa o temporizador de cooldown

        # Verifica se estamos no cooldown
        if time.time() - self.last_command_time < self.cooldown_time:
            return  # Ainda no cooldown, não faz nada

        if self.state == "NEUTRO":
            # Verifica se a mão está neutra
            if self.is_neutral(hand_landmarks):
                self.last_hand_position = hand_landmarks[8].x  # Atualiza a posição neutra
            elif self.is_moving_right(hand_landmarks):
                self.state = "NEXT_SLIDE"
                self.last_command_time = time.time()  # Atualiza o tempo do comando
                self.last_hand_position = hand_landmarks[8].x  # Atualiza a posição inicial
                self.slide_controller.next_slide()
            elif self.is_moving_left(hand_landmarks):
                self.state = "PREV_SLIDE"
                self.last_command_time = time.time()  # Atualiza o tempo do comando
                self.last_hand_position = hand_landmarks[8].x  # Atualiza a posição inicial
                self.slide_controller.prev_slide()
        elif self.state in ["NEXT_SLIDE", "PREV_SLIDE"]:
            # Após um comando, verifica se a mão retornou ao neutro
            if self.is_neutral(hand_landmarks):
                self.state = "NEUTRO"  # Retorna ao estado neutro

    def reset_state(self):
        """Reseta o estado para NEUTRO."""
        self.state = "NEUTRO"
        self.last_hand_position = None
        self.last_detection_time = None


def main():
    video = VideoStream()
    detector = HandLandmarkDetector()
    state_machine = GestureStateMachine(threshold=0.05)  # Define o limiar

    for frame in video.capture_frames():
        landmarks_list = detector.get_hand_landmarks(frame)

        if landmarks_list:  # Se detectarmos landmarks
            hand_landmarks = landmarks_list[0].landmark  # Usar a primeira mão detectada
            state_machine.update_state(hand_landmarks)  # Atualizar máquina de estados
        else:
            state_machine.reset_state()  # Resetar estado se nenhuma mão for detectada

        video.show_frame(frame)


if __name__ == "__main__":
    main()
