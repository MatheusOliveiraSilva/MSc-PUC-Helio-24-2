def detect_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    # Detectar gestos com base na posição relativa (ajustado para espelhamento)
    if thumb_tip.x > index_tip.x:  # Mão movendo para a direita
        return "NEXT_SLIDE"
    elif thumb_tip.x < index_tip.x:  # Mão movendo para a esquerda
        return "PREV_SLIDE"
    else:
        return None
