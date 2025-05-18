import cv2
import os

def images_to_video(image_folder, output_video_path, fps=25):
    images = sorted([img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg"))])
    
    if not images:
        print("No images found in the specified folder.")
        return

    # Read the first image to get the dimensions
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the video codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use 'XVID' or 'avc1'
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    print(f'[✓] Video successfully created at: {output_video_path}')


if __name__ == "__main__":
    image_folder = 'extracted_images'  # Folder containing your images
    output_video = 'output_video.mp4'  # Output video file name
    fps = 25  # Frames per second, adjust as needed

    images_to_video(image_folder, output_video, fps)
