import cv2
import numpy as np

scale = 0.4
cam = cv2.VideoCapture('Video.mp4')
left_top = (0, 0)
left_bottom = (0, 0)
right_top = (0, 0)
right_bottom = (0, 0)

while True:
    ret, frame = cam.read()

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dim = (width, height)

    frame = cv2.resize(frame, dim)
    frame_2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not ret:
        break

    frame_3 = np.zeros(shape=frame_2.shape, dtype=np.int32)

    upper_right = (int(width * 0.55), int(height*0.75))
    upper_left = (int(width * 0.5), int(height*0.75))
    lower_left = (0, height)
    lower_right = (width, height)

    trapezoid_bounds = np.array([upper_right, upper_left, lower_left, lower_right], dtype=np.int32)
    frame_3 = np.uint8(cv2.fillConvexPoly(frame_3, trapezoid_bounds, 255))

    frame_2 = frame_2 * frame_3

    trapezoid_bounds = np.float32(trapezoid_bounds)

    magic_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, np.array([(width, 0), (0, 0), (0, height), (width, height)], dtype=np.float32))

    frame_4 = cv2.warpPerspective(frame_2, magic_matrix, (width, height))

    frame_5 = cv2.blur(frame_4, ksize=(3, 3))

    sobel_vertical = np.float32([[-1, -2, -1],[0,0,0],[1,2,1]])
    sobel_horizontal = np.transpose(sobel_vertical)

    frame_5 = np.float32(frame_5)

    vertical_frame_6 = cv2.filter2D(frame_5, -1, sobel_vertical)
    horizontal_frame_6 = cv2.filter2D(frame_5, -1, sobel_horizontal)

    frame_7 = np.sqrt(vertical_frame_6 ** 2 + horizontal_frame_6 ** 2)

    frame_8 = cv2.convertScaleAbs(frame_7)

    _, frame_9 = cv2.threshold(frame_8, 127, 255, cv2.THRESH_BINARY)

    frame_10 = frame_9.copy()
    frame_10[0:height, 0:int(width * 0.05)] = 0
    frame_10[0:height, int(width * 0.95):width] = 0

    left_half = frame_10[0:height, 0:width//2]
    right_half = frame_10[0:height, width//2:width]

    left_points = np.argwhere(left_half > 1)
    left_xs = [t[1] for t in left_points]
    left_ys = [t[0] for t in left_points]

    right_points = np.argwhere(right_half > 1)
    right_xs = [(t[1] + width//2) for t in right_points]
    right_ys = [t[0] for t in right_points]

    left_line = np.polynomial.polynomial.polyfit(left_xs, left_ys, deg = 1)
    right_line = np.polynomial.polynomial.polyfit(right_xs, right_ys, deg = 1)

    left_top_y = 0
    left_top_x = int(-left_line[0] / left_line[1])
    left_bottom_y = height
    left_bottom_x = int((left_bottom_y - left_line[0]) / left_line[1])

    right_top_y = 0
    right_top_x = int(-right_line[0] / right_line[1])
    right_bottom_y = height
    right_bottom_x = int((right_bottom_y - right_line[0]) / right_line[1])


    if abs(left_bottom_x) <= (10**8):
        left_bottom = (left_bottom_x, left_bottom_y)
    else:
        left_bottom = (left_bottom[0], left_bottom_y)

    if abs(left_top_x) <= (10**8):
        left_top = (left_top_x, left_top_y)
    else:
        left_top = (left_top[0], left_top_y)

    if abs(right_bottom_x) <= (10**8):
        right_bottom = (right_bottom_x, right_bottom_y)
    else:
        right_bottom = (right_bottom[0], right_bottom_y)

    if abs(right_top_x) <= (10**8):
        right_top = (right_top_x, right_top_y)
    else:
        right_top = (right_top[0], right_top_y)


    cv2.line(frame_10, left_top, left_bottom, (100, 0, 0), 5)
    cv2.line(frame_10, right_top, right_bottom, (200, 0, 0), 5)
    cv2.line(frame_10, (width//2, 0), (width//2, height), (255, 0, 0), 1)

    left_frame_11 = np.zeros(frame.shape, dtype=np.uint8)
    cv2.line(left_frame_11, left_top, left_bottom, (255, 0, 0), 5)

    magic_matrix = cv2.getPerspectiveTransform(np.array([(width, 0), (0, 0), (0, height), (width, height)], dtype=np.float32), trapezoid_bounds)

    left_frame = cv2.warpPerspective(left_frame_11, magic_matrix, (width, height))
    left_points = np.argwhere(left_frame > 1)

    right_frame_11 = np.zeros(frame.shape, dtype=np.uint8)
    cv2.line(right_frame_11, right_top, right_bottom, (255, 0, 0), 5)

    magic_matrix = cv2.getPerspectiveTransform(np.array([(width, 0), (0, 0), (0, height), (width, height)], dtype=np.float32), trapezoid_bounds)


    right_frame = cv2.warpPerspective(right_frame_11, magic_matrix, (width, height))
    right_points = np.argwhere(right_frame > 1)

    final_frame = frame.copy()

    for p in left_points:
        final_frame[p[0], p[1]] = [50, 50, 250]

    for p in right_points:
        final_frame[p[0], p[1]] = [50, 250, 50]

    cv2.imshow('Frame3', frame_3)
    cv2.imshow('Frame4', frame_4 * 255)
    cv2.imshow('Frame8', frame_8)
    cv2.imshow('Frame9', frame_9)
    cv2.imshow('Frame10', frame_10)
    cv2.imshow('Final', final_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
