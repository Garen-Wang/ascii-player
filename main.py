import time
import os
import cv2
import shutil
import playsound
import threading


size = os.get_terminal_size()
height, width = size.lines, size.columns

candidate_chars = "*^.,:;(!)1@$#"

def generate_frames(filename):
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    if os.path.exists("rframes"):
        shutil.rmtree("rframes")
    if os.path.exists("gframes"):
        shutil.rmtree("gframes")
    os.mkdir("rframes")
    os.mkdir("gframes")

    count = 0
    while success:
        rframe = cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)
        gframe = cv2.cvtColor(rframe, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join("rframes", "frame%d.jpg" % count), rframe)
        cv2.imwrite(os.path.join("gframes", "frame%d.jpg" % count), gframe)
        success, image = vidcap.read()
        # print("Read a new frame: ", count)
        count += 1
    return count


def play():
    t = threading.Thread(target=lambda: playsound.playsound('./神女劈观.m4a', block=False))
    t.start()
    print("\033[?25l", end="")
    n = len(os.listdir("rframes"))
    n = 4800
    for i in range(0, n):
        print("\033[1;1H", end="")
        filename = "frame%d.jpg" % i
        pre_time = time.time()
        rframe = cv2.imread(os.path.join("rframes", filename))
        gframe = cv2.imread(os.path.join("gframes", filename), cv2.IMREAD_GRAYSCALE)
        # cv2.imshow("rframe", rframe)
        # cv2.waitKey(500)
        # cv2.destroyAllWindows()
        # cv2.imshow("gframe", gframe)
        # cv2.waitKey(500)
        # cv2.destroyAllWindows()
        # print(rframe.shape)
        
        buf = ""
        for y in range(height):
            for x in range(width):
                b = int(rframe[y, x, 0])
                g = int(rframe[y, x, 1])
                r = int(rframe[y, x, 2])
                gray = int(gframe[y, x])
                idx = round((gray) / 255 * (len(candidate_chars) - 1))
                ch = candidate_chars[idx]
                # print(r, g, b)
                # print(colored(r, g, b, '1'), end="")

                # print("\033[38;2;{};{};{}m{}\033[38;2;0;0;0m".format(r, g, b, ch), end="")
                temp = "\033[38;2;{};{};{}m{}\033[38;2;0;0;0m".format(r, g, b, ch)
                buf += temp
        print(buf, end="", flush=True)
        used_time = time.time() - pre_time
        if used_time < 0.033:
            time.sleep(0.033 - used_time)
    print("\033[2J")
    print("\033[?25h", end="")
    t.join()

if __name__ == '__main__':
    # generate_frames("神女劈观.mp4")
    play()

