## GestureControlHome
A test project finished when I'm in grade 10.

This project uses a Home Assitant server to achieve home control, which is not invoved in the source code. I signed my equipments to a Raspberry Pi 3 running Home Assistant OS, then build a TCP service using Node Red app. This project is actually interacting with the TCP service I build.

It captures live video using a camera using opencv, recognizes hand landmarks using mediapipe, then use some simple rules to judge gesture type by considering the relation of the coordinates in the image.

It provides a visualize window to let the operator know whether the recognition succeed and the process of an operation.

