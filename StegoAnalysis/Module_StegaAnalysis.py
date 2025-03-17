import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image

def compare_images(image1_path, image2_path, conversion_mode, output_dir='Image_Output'):
    
    def convert_to_delta(image):
    # Chuyển ảnh sang chế độ delta
    # Đầu vào: ảnh (grayscale hoặc color)
        if len(image.shape) == 2:
            # Grayscale image
            delta_h = np.zeros_like(image)
            delta_v = np.zeros_like(image)
            
            delta_h[:, :-1] = np.abs(image[:, 1:] - image[:, :-1])
            delta_v[:-1, :] = np.abs(image[1:, :] - image[:-1, :])
        else:
            # Color image
            delta_h = np.zeros_like(image)
            delta_v = np.zeros_like(image)
            
            delta_h[:, :-1, :] = np.abs(image[:, 1:, :] - image[:, :-1, :])
            delta_v[:-1, :, :] = np.abs(image[1:, :, :] - image[:-1, :, :])
        
        delta = (delta_h + delta_v) // 2 # Gộp 2 ma trận delta_h và delta_v lại
        return delta
    
    def convert_to_rgb(image):
        if len(image.shape) == 2:  # Grayscale image
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 3:  # Already BGR (OpenCV standard)
            return image
        elif image.shape[2] == 4:  # BGRA
            return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        else:
            raise ValueError("[!] Lỗi chuyển đổi ảnh sang RGB")
    
    def calculate_similarity(img1, img2):
        if img1.shape != img2.shape:
            raise ValueError("[!] Ảnh phải có cùng kích thước")
        
        # Tính toán Mean Squared Error (MSE) giữa 2 ảnh
        mse = np.mean((img1.astype("float") - img2.astype("float")) ** 2)
        
        # Chuyển MSE thành tỉ lệ tương đồng (0% - 100%)
        if mse == 0:
            return 100.0
        max_mse = 255.0 ** 2
        similarity = 100.0 * (1.0 - (mse / max_mse))
        
        return max(0.0, min(100.0, similarity))
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Read images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    
    if image1 is None or image2 is None:
        raise ValueError(f"[!] Không thể so sánh 2 ảnh: {image1_path}, {image2_path}")
    
    # Chuyển đổi ảnh sang chế độ delta hoặc RGB
    if conversion_mode.lower() == 'delta':
        converted1 = convert_to_delta(image1)
        converted2 = convert_to_delta(image2)
    elif conversion_mode.lower() == 'rgb':
        converted1 = convert_to_rgb(image1)
        converted2 = convert_to_rgb(image2)
    else:
        raise ValueError("[!] Lỗi chế độ chuyển đổi. Sử dụng 'rgb' hoặc 'delta'")
    
    h1, w1 = converted1.shape[:2]
    h2, w2 = converted2.shape[:2]
    
    if h1 != h2 or w1 != w2:
        # Thay đổi kích thước ảnh để so sánh
        converted2 = cv2.resize(converted2, (w1, h1))
    
    # Lưu ảnh đã chuyển đổi
    base1 = os.path.basename(image1_path)
    base2 = os.path.basename(image2_path)
    
    converted_path_1 = os.path.join(output_dir, f"{conversion_mode}_{base1}")
    cv2.imwrite(converted_path_1, converted1)
    
    converted_path_2 = os.path.join(output_dir, f"{conversion_mode}_{base2}")
    cv2.imwrite(converted_path_2, converted2)
    
    # Tính toán độ tương đồng
    match_percentage = calculate_similarity(converted1, converted2)
    
    return match_percentage

def analyse(original_image, modified_image):
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
            vb1.append(b & 1)  # Add extraction for Blue LSBs
    
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
    plt.axis([0, max(len(avgR1), len(avgG1)), 0, 1])
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')
    plt.plot(blocks1, avgR1, 'r.')  # Uncommented to plot Red LSBs
    plt.plot(blocks1, avgG1, 'g')    # Uncommented to plot Green LSBs
    plt.plot(blocks1, avgB1, 'bo')  # Uncommented to plot Blue LSBs
    
    plt.subplot(2, 1, 2)
    plt.title('Modified Image')
    plt.axis([0, max(len(avgR2), len(avgG2)), 0, 1])
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')
    plt.plot(blocks2, avgR2, 'r.')  # Uncommented to plot Red LSBs
    plt.plot(blocks2, avgG2, 'g')    # Uncommented to plot Green LSBs
    plt.plot(blocks2, avgB2, 'bo')   # Uncommented to plot Blue LSBs
    
    # Save the plot
    plot_path = os.path.join('LSB_Analysis', 'LSB_Analysis.png')
    os.makedirs('LSB_Analysis', exist_ok=True)
    plt.savefig(plot_path)
    print(f"[+] Biểu đồ được lưu tại: {plot_path}")
    return plot_path, plt.show()
