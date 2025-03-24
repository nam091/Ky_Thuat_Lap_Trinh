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
            delta_h = np.zeros_like(image) # Khởi tạo ma trận rỗng với kích thước ảnh gốc
            delta_v = np.zeros_like(image) # Có thể gọi là làm phẳng ảnh
            
            delta_h[:, :-1] = np.abs(image[:, 1:] - image[:, :-1]) # Tính toán độ chênh lệch giữa các pixel bên trái và bên phải
            delta_v[:-1, :] = np.abs(image[1:, :] - image[:-1, :])
        else:
            # Color image
            delta_h = np.zeros_like(image)
            delta_v = np.zeros_like(image)
            
            delta_h[:, :-1, :] = np.abs(image[:, 1:, :] - image[:, :-1, :]) # Tính toán độ chênh lệch giữa các pixel bên trái, phải và giữ nguyên kênh màu alpha
            delta_v[:-1, :, :] = np.abs(image[1:, :, :] - image[:-1, :, :])
        
        delta = (delta_h + delta_v) // 2 # Gộp 2 ma trận delta_h và delta_v lại
        return delta
    
    
    def convert_to_rgb(image):
        if len(image.shape) == 2:  # Chuyển đổi ảnh grayscale sang RGB
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 3:  # Ảnh đã có 3 kênh màu (BGR)
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
        return mse
        # Chuyển MSE thành tỉ lệ tương đồng (0% - 100%)
        # if mse == 0:
        #     return 100.0
        # max_mse = 255.0 ** 2
        # similarity = 100.0 * (1.0 - (mse / max_mse))
        # return similarity



    
    os.makedirs(output_dir, exist_ok=True)
    
    # Read images
    image1 = cv2.imread(image1_path) # Đọc ảnh gốc
    image2 = cv2.imread(image2_path) # Đọc ảnh đã chỉnh sửa
    
    # temp_2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('Image_Output/image1.png', temp_2)
    
    if image1 is None or image2 is None:
        raise ValueError(f"[!] Không thể so sánh 2 ảnh: {image1_path}, {image2_path}")
    
    # Chuyển đổi ảnh sang chế độ delta hoặc RGB
    if conversion_mode.lower() == 'delta': ## Chuyển đổi ảnh sang không gian màu delta
        converted1 = convert_to_delta(image1)
        converted2 = convert_to_delta(image2)
    elif conversion_mode.lower() == 'rgb': # Chuyển đổi ảnh sang không gian màu RGB
        converted1 = convert_to_rgb(image1)
        converted2 = convert_to_rgb(image2)
    elif conversion_mode.lower() == 'gray': # Chuyển đổi ảnh sang không gian màu xám
        converted1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        converted2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    elif conversion_mode.lower() == 'hsv': # Chuyển đổi ảnh sang không gian màu HSV
        converted1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
        converted2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    elif conversion_mode.lower() == 'lab': # Chuyển đổi ảnh sang không gian màu LAB
        converted1 = cv2.cvtColor(image1, cv2.COLOR_BGR2Lab)
        converted2 = cv2.cvtColor(image2, cv2.COLOR_BGR2Lab)
    else:
        raise ValueError("[!] Lỗi chế độ chuyển đổi. Sử dụng 'rgb', 'delta', 'gray', 'hsv' hoặc 'lab'")
    
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

def show_pixel_examples(image, num_samples=5):
    """
    Shows some pixel examples before and after delta conversion
    
    Args:
        image: The input image
        num_samples: Number of pixel examples to show
    """
    # Create a copy to avoid modifying original
    img_copy = cv2.imread(image)
    if img_copy is None:
        raise ValueError(f"[!] Không thể đọc ảnh: {image}")
    
    # Get image dimensions
    h, w = img_copy.shape[:2]
    
    # Choose random pixel positions
    np.random.seed(42)  # For reproducibility
    sample_positions = []
    for _ in range(num_samples):
        y = np.random.randint(1, h-1)
        x = np.random.randint(1, w-1)
        sample_positions.append((y, x))
    
    print("\n=== Pixel Delta Conversion Examples ===")
    for i, (y, x) in enumerate(sample_positions):
        if len(img_copy.shape) == 2:  # Grayscale
            original = img_copy[y, x]
            right = img_copy[y, x+1]
            down = img_copy[y+1, x]
            delta_h = abs(original - right)
            delta_v = abs(original - down)
            delta = (delta_h + delta_v) // 2
            # Visualize the pixels for better understanding
            pixel_visual = f"""
            Original: {original}
            Right →: {right} (Δh: {delta_h})
            Down ↓: {down} (Δv: {delta_v})
            Final delta: {delta}
            """
            print(f"Example {i+1} at position ({y},{x}):")
            print(pixel_visual)
        else:  # Color image
            original = img_copy[y, x]
            right = img_copy[y, x+1]
            down = img_copy[y+1, x]
            delta_h = np.abs(original - right)
            delta_v = np.abs(original - down)
            delta = (delta_h + delta_v) // 2
            
            # Create pixel_visual for color images too
            pixel_visual = f"""
            Original (BGR): {original}
            Right → (BGR): {right} (Δh: {delta_h})
            Down ↓ (BGR): {down} (Δv: {delta_v})
            Final delta: {delta}
            """
            print(f"Example {i+1} at position ({y},{x}):")
            print(pixel_visual)
        print()
    
    return delta

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
            vr1.append(r & 1) # Ghi bit cuối cùng của kênh màu đỏ vào mảng
            vg1.append(g & 1) # Ghi bit cuối cùng của kênh màu xanh lá vào mảng
            vb1.append(b & 1) # Ghi bit cuối cùng của kênh màu xanh dương vào mảng
    
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
    avgR1 = [] # Red LSBs
    avgG1 = [] # Green LSBs
    avgB1 = [] # Blue LSBs
    for i in range(0, max(len(vr1), len(vg1), len(vb1)), BS): # Tính trung bình mỗi giá trị LSB cho mỗi khối BS
        avgR1.append(np.mean(vr1[i:i + BS])) # Tính trung bình mỗi giá trị LSB kênh màu đỏ cho mỗi khối BS
        avgG1.append(np.mean(vg1[i:i + BS])) # Tính trung bình mỗi giá trị LSB kênh màu xanh lá cho mỗi khối BS
        avgB1.append(np.mean(vb1[i:i + BS])) # Tính trung bình mỗi giá trị LSB kênh màu xanh dương cho mỗi khối BS
    
    avgR2 = []
    avgG2 = []
    avgB2 = []
    for i in range(0, max(len(vr2), len(vg2), len(vb2)), BS):
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
    plt.axis([0, len(avgB2), 0, 1])  # Tùy chỉnh trục x và y cho biểu đồ theo kích thước của avgB2
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')
    plt.tight_layout()
    # plt.plot(blocks2, avgR2, 'r.')  # Uncommented to plot Red LSBs
    # plt.plot(blocks2, avgG2, 'g')    # Uncommented to plot Green LSBs
    plt.plot(blocks2, avgB2, 'bo') # Biểu diễn LSB với kênh màu xanh dương
    plt.show()
    plot_path = os.path.join('LSB_Analysis', 'LSB_Analysis.png')
    os.makedirs('LSB_Analysis', exist_ok=True)
    # plt.savefig(plot_path)
    print(f"[+] Biểu đồ được lưu tại: {plot_path}")
    return plot_path
