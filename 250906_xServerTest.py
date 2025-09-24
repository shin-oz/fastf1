import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2
img = cv2.imread('test.png')
if img is None:
    print("画像の読み込みに失敗しました。")
else:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.savefig('output.jpg')
    plt.close()
    print("画像がoutput.jpgに保存されました。")