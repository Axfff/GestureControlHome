import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import queue
import TCP
import threading
from playsound import playsound


def copyQueue(sequence):
    copy = queue.Queue()
    for _ in range(sequence.qsize()):
        v = sequence.get()
        copy.put(v)
        sequence.put(v)
    return copy


def printQueue(sequence):
    check = copyQueue(sequence)
    for i in range(check.qsize()):
        print(check.get(), end=' < ')
    print()


cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

max_hands_sequence_length = 300
hands_sequence = queue.Queue(maxsize=max_hands_sequence_length)
max_state_sequence_length = 100
state_sequence = queue.Queue(maxsize=max_hands_sequence_length)

commands = {0: '', 1: '', 2: 'hanging_light_toggle', 4: 'lamp_toggle', 5: 'tap'}
accumulateOperate = [2, 4]

predicted_command = 0
while True:
    succeed, frame = cap.read()
    hands, img = detector.findHands(frame)

    if hands_sequence.qsize() == max_hands_sequence_length:
        hands_sequence.get()
    hands_sequence.put(hands)
    # print(hands_sequence.qsize())

    if state_sequence.qsize() == max_state_sequence_length:
        state_sequence.get()
    # print(state_sequence.qsize())

    # printQueue(state_sequence)

    if hands:
        fingerUpState = detector.fingersUp(hands[0])
        # print(fingerUpState)

        if fingerUpState == [1, 1, 1, 1, 1]:
            # print(detector.findDistance(hands[0]['lmList'][0], hands[0]['lmList'][5])[0],
            #       detector.findDistance(hands[0]['lmList'][4], hands[0]['lmList'][8])[0])
            if 0.9 * detector.findDistance(hands[0]['lmList'][0], hands[0]['lmList'][5])[0] < \
                    detector.findDistance(hands[0]['lmList'][4], hands[0]['lmList'][8])[0] and \
                    2 * detector.findDistance(hands[0]['lmList'][13], hands[0]['lmList'][17])[0] < \
                    detector.findDistance(hands[0]['lmList'][16], hands[0]['lmList'][20])[0] and \
                    2 * detector.findDistance(hands[0]['lmList'][9], hands[0]['lmList'][10])[0] < \
                    detector.findDistance(hands[0]['lmList'][9], hands[0]['lmList'][12])[0] and \
                    2 * detector.findDistance(hands[0]['lmList'][17], hands[0]['lmList'][18])[0] < \
                    detector.findDistance(hands[0]['lmList'][17], hands[0]['lmList'][20])[0]:
                state_sequence.put({'type': 2})
            else:
                state_sequence.put({'type': 0})
        # elif fingerUpState == [0, 1, 1, 1, 1]:
        #     state_sequence.put(2)

        elif fingerUpState == [0, 1, 1, 1, 0]:
            if 1.8 * detector.findDistance(hands[0]['lmList'][5], hands[0]['lmList'][9])[0] < \
                    detector.findDistance(hands[0]['lmList'][8], hands[0]['lmList'][12])[0]:
                state_sequence.put({'type': 4})
            else:
                state_sequence.put({'type': 0})

        elif fingerUpState == [0, 1, 1, 0, 0]:
            distance, pos = detector.findDistance(hands[0]['lmList'][8], hands[0]['lmList'][12])
            pos = pos[4:]
            if distance < \
                    detector.findDistance(hands[0]['lmList'][5], hands[0]['lmList'][9])[0]:
                print('clicking', distance, pos)
                state_sequence.put({'type': 5, 'pos': pos})
            else:
                state_sequence.put({'type': 0})
        else:
            state_sequence.put({'type': 0})

    else:
        state_sequence.put({'type': 0})

    check = copyQueue(state_sequence)
    faultTolerance = 3
    correct_count = 0
    determination_count = 20
    for i in range(check.qsize() - 1):
        value = check.get()['type']

        if value == predicted_command['type'] and value in accumulateOperate:
            faultTolerance = 3
            correct_count += 1

            if correct_count == determination_count:
                threading.Thread(target=lambda: TCP.sendData(commands[predicted_command['type']])).start()
                state_sequence = queue.Queue(maxsize=max_state_sequence_length)
                threading.Thread(target=lambda: playsound(r'sounds\activate.wav')).start()

        else:
            faultTolerance -= 1

            if faultTolerance <= 0:
                correct_count = 0

    predicted_command = check.get()
    print(predicted_command)

    # Visualization
    if predicted_command['type'] in [2, 4]:
        axes = int(detector.findDistance(hands[0]['lmList'][9], hands[0]['lmList'][12])[0])
        cv.ellipse(frame, hands[0]['lmList'][9], (axes, axes), 0, -90,
                   -90 - int(360 * correct_count / determination_count), (20, 250, 20),
                   int(axes / 7))  # detector.findDistance(hands[0]['lmList'][9], hands[0]['lmList'][12])
        cv.putText(frame, commands[predicted_command['type']], hands[0]['lmList'][9], cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255))
        # print(predicted_command, int(360 * correct_count / determination_count))
    elif predicted_command['type'] in [5]:
        check = copyQueue(state_sequence)
        checkLength = 10
        for i in range(check.qsize()-checkLength):
            check.get()
        for i in range(check.qsize()):
            value = check.get()
            if value['type'] == predicted_command['type']:
                cv.ellipse(frame, value['pos'], (4, 4), 0, 0, 360, (255, 0, 255), 7)

    cv.imshow('cam', frame)  # cv.flip(frame, 1)

    cv.waitKey(10)
