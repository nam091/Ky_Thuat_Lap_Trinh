import numpy as np
import cv2
from PIL import Image
import os

import matplotlib.pyplot as plt

def plot_image_histogram(image_path, output_path=None, bins=256, color=True):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    plt.figure(figsize=(10, 6))
    
    if color:
        # Split the image into its color channels
        colors = ('b', 'g', 'r')
        channel_names = ('Blue', 'Green', 'Red')
        
        for i, color in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [bins], [0, 256])
            plt.plot(hist, color=color, label=channel_names[i])
        
        plt.title('Color Histogram')
        plt.legend()
        
    else:
        # Convert to grayscale if not already
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        hist = cv2.calcHist([gray], [0], None, [bins], [0, 256])
        plt.plot(hist, color='gray')
        plt.title('Grayscale Histogram')
    
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.xlim([0, bins-1])
    # Save if output path is provided
    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        plt.savefig(output_path)
    
    return plt.gcf(), plt.show()

def compare_histograms(original_path, modified_path, output_path, bins=256, color=True):
    # Read the images
    original = cv2.imread(original_path)
    modified = cv2.imread(modified_path)
    
    if original is None or modified is None:
        raise ValueError("Could not read one or both images")
    
    plt.figure(figsize=(12, 8))
    
    if color:
        colors = ('b', 'g', 'r')
        channel_names = ('Blue', 'Green', 'Red')
        
        for i, col in enumerate(colors):
            # Original image histogram
            hist_orig = cv2.calcHist([original], [i], None, [bins], [0, 256])
            hist_orig = hist_orig / hist_orig.sum()  # Normalize for comparison
            
            # Modified image histogram
            hist_mod = cv2.calcHist([modified], [i], None, [bins], [0, 256])
            hist_mod = hist_mod / hist_mod.sum()  # Normalize for comparison
            
            plt.subplot(3, 1, i+1)
            plt.plot(hist_orig, color=col, linestyle='-', label=f'Original {channel_names[i]}')
            plt.plot(hist_mod, color=col, linestyle='--', label=f'Modified {channel_names[i]}')
            plt.title(f'{channel_names[i]} Channel Histogram Comparison')
            plt.legend()
            plt.xlim([0, bins-1])
    
    else:
        # Convert to grayscale
        if len(original.shape) > 2:
            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        else:
            original_gray = original
            
        if len(modified.shape) > 2:
            modified_gray = cv2.cvtColor(modified, cv2.COLOR_BGR2GRAY)
        else:
            modified_gray = modified
        
        # Original image histogram
        hist_orig = cv2.calcHist([original_gray], [0], None, [bins], [0, 256])
        hist_orig = hist_orig / hist_orig.sum()  # Normalize
        
        # Modified image histogram
        hist_mod = cv2.calcHist([modified_gray], [0], None, [bins], [0, 256])
        hist_mod = hist_mod / hist_mod.sum()  # Normalize
        
        plt.plot(hist_orig, color='blue', label='Original')
        plt.plot(hist_mod, color='red', label='Modified')
        plt.title('Grayscale Histogram Comparison')
        plt.legend()
        plt.xlim([0, bins-1])
    
    plt.xlabel('Pixel Value')
    plt.ylabel('Normalized Frequency')
    plt.tight_layout()
    # Save if output path is provided
    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        plt.savefig(output_path)
    
    return plt.gcf(), plt.show()

def analyze_lsb_histogram(image_path, output_path):
    # Read image using PIL
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    
    # Extract LSBs from each channel
    r_lsb = []
    g_lsb = []
    b_lsb = []
    
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            r_lsb.append(r & 1)  # Extract LSB
            g_lsb.append(g & 1)  # Extract LSB
            b_lsb.append(b & 1)  # Extract LSB
    
    plt.figure(figsize=(12, 8))
    
    # Plot LSB distribution for each channel
    plt.subplot(3, 1, 1)
    plt.hist(r_lsb, bins=2, color='r', alpha=0.7)
    plt.title('Red Channel LSB Distribution')
    plt.xticks([0, 1])
    plt.xlim([-0.5, 1.5])
    
    plt.subplot(3, 1, 2)
    plt.hist(g_lsb, bins=2, color='g', alpha=0.7)
    plt.title('Green Channel LSB Distribution')
    plt.xticks([0, 1])
    plt.xlim([-0.5, 1.5])
    
    plt.subplot(3, 1, 3)
    plt.hist(b_lsb, bins=2, color='b', alpha=0.7)
    plt.title('Blue Channel LSB Distribution')
    plt.xticks([0, 1])
    plt.xlim([-0.5, 1.5])
    
    plt.tight_layout()
    # Save if output path is provided
    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        plt.savefig(output_path)
    
    # Calculate statistics
    stats = {
        'red': {'zeros': r_lsb.count(0), 'ones': r_lsb.count(1)},
        'green': {'zeros': g_lsb.count(0), 'ones': g_lsb.count(1)},
        'blue': {'zeros': b_lsb.count(0), 'ones': b_lsb.count(1)}
    }
    
    return plt.gcf(), stats, plt.show()