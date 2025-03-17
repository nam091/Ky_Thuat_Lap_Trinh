from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import time
from skimage.util import view_as_windows

def improved_entropy(signal):
    """Faster entropy calculation using numpy's bincount"""
    # Convert to integers if not already
    if signal.dtype.kind == 'f':
        signal = signal.astype(np.int32)
        
    # Get counts using bincount (much faster than iterating)
    counts = np.bincount(signal)
    
    # Filter out zeros
    counts = counts[counts > 0]
    
    # Calculate probabilities and entropy directly
    probs = counts / signal.size
    ent = -np.sum(probs * np.log2(probs))
    return ent

def calculate_entropy_faster(image):
    """Optimized entropy calculation function using vectorization"""
    print("Running optimized entropy calculation...")
    
    # Use the improved entropy function
    # Create a windowed view of the image for faster processing
    
    # Optional: Reduce image size for testing
    # greyIm_small = greyIm[::2, ::2]  # Take every other pixel
    
    # Create a faster version using sliding windows if available
    N = 5  # Window size
    greyIm = np.array(Image.open(image).convert('L'))
    S = greyIm.shape
    E = np.zeros(S, dtype=float)
    
    try:
        # For newer numpy versions
        window_size = 2*N + 1
        # Create padded image
        padded = np.pad(greyIm, N, mode='reflect')
        # Create sliding windows
        windows = view_as_windows(padded, (window_size, window_size))
        
        # Calculate entropy for each window
        E_fast = np.zeros(S, dtype=float)
        
        # Process in batches for better performance
        batch_size = 100
        for i in range(0, S[0], batch_size):
            end_i = min(i + batch_size, S[0])
            for j in range(0, S[1], batch_size):
                end_j = min(j + batch_size, S[1])
                
                # Process a batch of windows
                batch_windows = windows[i:end_i, j:end_j]
                for ri in range(end_i - i):
                    for ci in range(end_j - j):
                        E_fast[i+ri, j+ci] = improved_entropy(batch_windows[ri, ci].flatten())
            
            if i % 100 == 0:
                print(f"Fast processing: {i}/{S[0]} rows")
                
        return E_fast
    
    except (AttributeError, ImportError):
        # Fallback for older numpy versions
        print("Using fallback method - consider upgrading numpy for better performance")
        return E

# Compare performance

original_image = './img/org1.jpg'
modified_image = './img/half_image.png'
start_time = time.time()
E_Original = calculate_entropy_faster(original_image)
E_optimized = calculate_entropy_faster(modified_image)
end_time = time.time()
print(f"Optimized calculation took {end_time - start_time:.2f} seconds")

# Optionally display and save the optimized result
plt.figure(figsize=(10, 5))
plt.subplot(1,2,1)
plt.imshow(E_Original, cmap=plt.cm.jet)
plt.title('Original Image')

plt.subplot(1,2,2)
plt.imshow(E_optimized, cmap=plt.cm.jet)
plt.title('Optimized Entropy')
np.save('./Image_Output/optimized_entropy.npy', E_optimized)

plt.savefig('./Image_Output/entropy_comparison.png')
plt.show()