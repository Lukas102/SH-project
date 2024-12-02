"""
Extracting bio-film area coverage from wide-field agar images
"""
# %%
#to stop plot inlining in shell used
%matplotlib qt
#imports
import numpy as np
import skimage as ski
import os 
from skimage import io, color
import matplotlib.pyplot as plt
import skimage.filters as skfilt
from matplotlib.path import Path
from matplotlib.patches import Polygon
from skimage import morphology
from skimage import filters
from skimage import measure
from skimage.segmentation import chan_vese
# %%
#reading in unaltered image
im1 = io.imread("B1-1.tif", plugin="tifffile")

#Showing image
plt.axis('off')
plt.imshow(im1)
plt.show()


#%%
#manual thresholding cell in case thresholding algoritms fail

#finding image intensity
print(f"Image shape: {im1.shape}, dtype: {im1.dtype}")
print(f"Intensity range: {im1.min()} to {im1.max()}")

# Visualizing  the original image
plt.figure(figsize=(6, 6))
plt.imshow(im1, cmap='gray')
plt.title("Original Image")
plt.axis('off')
plt.show()

# Defining manual threshold range for pixel brightness
lower_bound = 65
upper_bound = 260

#manual thresholding
binary = np.zeros_like(im1)
binary[(im1 >= lower_bound) & (im1 <= upper_bound)] = 1

# Visualizing the thresholded image
plt.figure(figsize=(6, 6))
plt.imshow(binary, cmap='gray')
plt.title(f"Thresholded Image ({lower_bound}-{upper_bound})")
plt.axis('off')
plt.show()
#%%


#applying otsu thresh to image
#skip cell if manual thresholding already done
thresh = skfilt.threshold_otsu(im1)
binary = im1 > thresh
plt.imshow(binary, cmap = 'gray')
plt.show()

#intial count after first thresholding
count1 = np.sum(binary)
print(count1)

# %%
#removing outer area's not of intrest
center_x, center_y = binary.shape[1] // 2, binary.shape[0] // 2  # Center of the circle
radius = min(binary.shape[0], binary.shape[1]) // 5  # Define radius

# Create a circular mask
Y, X = np.ogrid[:binary.shape[0], :binary.shape[1]]
dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
mask = dist_from_center <= radius

# Applying a mask to keep only the circular region
binary_2 = np.zeros_like(binary)  # Create a blank image
binary_2[mask] = binary[mask]     # Copy only the region inside the circle

# Plot the result
plt.imshow(binary_2, cmap='gray')
plt.axis("off")

# Drawing the circular ROI 
circle = plt.Circle((center_x, center_y), radius, color='yellow', fill=False, linewidth=2)
plt.gca().add_patch(circle)
plt.show()

#intial count
count_i = np.sum(binary_2)
print("the intial count is " +str(count_i))

#%%
#showing latest threshold to remove more areas manually
print(np.sum(binary_2))
plt.imshow(binary_2)
plt.show()


# %%
#polygon patch to remove any desired area
polygon_vertices = np.array([[1036,832], [1099,755],[1309,762],[1306,1083],[1099,1099],[1020,995]])
#additional polygans that can be removed simulatneously
#polygon_vertices = np.array([[1460,916], [1456,963],[1495,943]])
#polygon_vertices3 = np.array([[697,815], [769,779],[818,797],[732,736]])

plt.imshow(binary_2, cmap='gray')
plt.axis("off")

# Overlaying the polygon on the image for visualization
polygon_patch = Polygon(polygon_vertices, closed=True, edgecolor='red', fill=False, linewidth=2)
#polygon_patch2 = Polygon(polygon_vertices2, closed=True, edgecolor='red', fill=False, linewidth=2)
#polygon_patch3 = Polygon(polygon_vertices3, closed=True, edgecolor='red', fill=False, linewidth=2)
plt.gca().add_patch(polygon_patch)
#plt.gca().add_patch(polygon_patch2)
#plt.gca().add_patch(polygon_patch3)

plt.show()


# %%
#removing the polygon specified area from the image

# Create a mask using the polygon vertices
X, Y = np.meshgrid(np.arange(binary_2.shape[1]), np.arange(binary_2.shape[0]))  # Coordinate grid
points = np.vstack((X.ravel(), Y.ravel())).T                              # All (x, y) points in the image

# Define the polygon path and check which points are inside it
polygon_path = Path(polygon_vertices)
mask = polygon_path.contains_points(points).reshape(binary_2.shape)          # Reshape mask to the image dimensions

# Apply the mask to remove the polygonal area (set to 0)
binary3 = np.copy(binary_2)       # Make a copy of the original image
# everything within mask set to 0
binary3[mask] = 0
print(np.sum(mask))
print(np.sum(binary3))

#everthing outside of mask set to 0
#binaryi[~mask] = 0     


#print(np.sum(binary3))
#print("Original non-zero pixel count:", original_pixel_count)
#print("Non-zero pixel count after operation:", after_pixel_count)
# Plot the result
plt.imshow(binary3, cmap='gray')
plt.axis("off")

# %%
#extra threshold step to force morpholgy step to work
#this is needed if manual thresholding is applied 
#might be able to fix by removing dimensions ??
thresh = skfilt.threshold_otsu(binary3)
binary_add = binary3 > thresh
after_pixel_count = np.count_nonzero(binary_add)
print("Non-zero pixel count after operation:", after_pixel_count)
plt.imshow(binary_add, cmap='gray')
plt.axis("off")

#%%

# using a small pixel area remover to remove any other minor clusters

min_size = 85000  # Minimum size of objects to keep
binary4 = morphology.remove_small_objects(binary_add, min_size=min_size, connectivity= 2)

# Plot the original and the processed image with small objects removed
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# Plot original binary image
ax[0].imshow(binary_add, cmap='gray')
ax[0].set_title("Original Image")
ax[0].axis("off")

# Plot image after small objects are removed
ax[1].imshow(binary4, cmap='gray')
ax[1].set_title(f"Large Objects (min_size={min_size})")
ax[1].axis("off")

plt.show()

# %%
#final pixel count after removing small pixel clusters
#cmap set tp gray to avoid matplotlib auto colour scaling
plt.imshow(binary4, cmap='gray')
plt.axis("off")
plt.show()
count = np.count_nonzero(binary4)
#Finding final count to save 
print("the final pixel count is " + str(count))
# %%


