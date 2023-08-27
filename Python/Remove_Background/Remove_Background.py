import cv2
import numpy as np

def remove_background(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Create a mask with the same size as the image, initialized as background (0)
    mask = np.zeros(image.shape[:2], np.uint8)

    # Define the rectangular bounding box around the foreground
    rect = (1, 1, image.shape[1] - 1, image.shape[0] - 1)

    # Initialize the background and foreground models for the GrabCut algorithm
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Apply the GrabCut algorithm to extract the foreground
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Create a mask where all likely foreground and definite foreground pixels are set to 1
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Apply the mask to the original image to get the foreground without the background
    foreground = image * mask2[:, :, np.newaxis]

    # Save the result
    cv2.imwrite(output_path, foreground)

if __name__ == "__main__":
    input_image_path = "/Users/vanderslof/Documents/Python/Projects/Remove_Background/IMG_0325.jpg"
    output_image_path = "/Users/vanderslof/Documents/Python/Projects/Remove_Background/IMG_0325.png"

    remove_background(input_image_path, output_image_path)
