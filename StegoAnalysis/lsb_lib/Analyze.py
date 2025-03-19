from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import os

def analyze(original_image, modified_image):
    BS = 100    # Block size
    img1 = Image.open(original_image)
    img2 = Image.open(modified_image)
    (width1, height1) = img1.size
    (width2, height2) = img2.size
    print(f"[+] Image size {original_image}: {width1}x{height1} pixels.")
    print(f"[+] Image size {modified_image}: {width2}x{height2} pixels.")
    conv1 = img1.convert("RGBA")
    conv2 = img2.convert("RGBA")

    # Trích xuất LSB từ mỗi pixel
    vr1 = []    # Red LSBs
    vg1 = []    # Green LSBs
    vb1= []    # Blue LSBs
    for h in range(height1):
        for w in range(width1):
            (r, g, b, a) = conv1.getpixel((w, h))
            vr1.append(r & 1)
            vg1.append(g & 1)
            vb1.append(b & 1)  # Updated extraction for Blue LSBs
    
    vr2 = []    # Red LSBs
    vg2 = []    # Green LSBs
    vb2 = []    # Blue LSBs
    for h in range(height2):
        for w in range(width2):
            (r, g, b, a) = conv2.getpixel((w, h))
            vr2.append(r & 1)
            vg2.append(g & 1)
            vb2.append(b & 1)

    # Trung bình mỗi giá trị LSB cho mỗi khối BS
    avgR1 = []
    avgG1 = []
    avgB1 = []
    for i in range(0, len(vr1), BS):
        avgR1.append(np.mean(vr1[i:i + BS]))
        avgG1.append(np.mean(vg1[i:i + BS]))
        avgB1.append(np.mean(vb1[i:i + BS]))
    
    avgR2 = []
    avgG2 = []
    avgB2 = []
    for i in range(0, len(vr2), BS):
        avgR2.append(np.mean(vr2[i:i + BS]))
        avgG2.append(np.mean(vg2[i:i + BS]))
        avgB2.append(np.mean(vb2[i:i + BS]))

    # Trung bình mỗi giá trị LSB cho mỗi khối BS để vẽ biểu đồ plot
    numBlocks1 = len(avgR1)
    numBlocks2 = len(avgR2)
    blocks1 = [i for i in range(0, numBlocks1)]
    blocks2 = [i for i in range(0, numBlocks2)]

    plt.subplot(2, 1, 1)
    plt.title('Original Image')
    plt.axis([0, max(len(avgR1), len(avgG1), len(avgB1)), 0, 1])  # Fixed the missing closing parenthesis and corrected 'len(av)' to 'len(avgB1)'
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')
    # plt.plot(blocks1, avgR1, 'r.')  # Uncommented to plot Red LSBs
    # plt.plot(blocks1, avgG1, 'g')    # Uncommented to plot Green LSBs
    plt.plot(blocks1, avgB1, 'bo')  # Uncommented to plot Blue LSBs
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    plt.title('Modified Image')
    plt.axis([0, len(avgB2), 0, 1])  # Fixed the missing closing parenthesis and corrected 'len(av)' to 'len(avgB2)'
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')
    plt.tight_layout()
    # plt.plot(blocks2, avgR2, 'r.')  # Uncommented to plot Red LSBs
    # plt.plot(blocks2, avgG2, 'g')    # Uncommented to plot Green LSBs
    plt.plot(blocks2, avgB2, 'bo')   # Uncommented to plot Blue LSBs
    plt.show()
    plot_path = os.path.join('LSB_Analysis', 'LSB_Analysis.png')
    os.makedirs('LSB_Analysis', exist_ok=True)
    # plt.savefig(plot_path)
    print(f"[+] Biểu đồ được lưu tại: {plot_path}")
    return plot_path

analyze('./img/Gau_KMA.jpg', './img/Gau_KMA_encoded.png')