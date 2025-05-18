import os

def extract_images_from_bin(bin_file_path, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(bin_file_path, 'rb') as f:
        data = f.read()

    # Define image signatures (magic numbers)
    signatures = {
        b'\xff\xd8\xff': 'jpg',  # JPEG
        b'\x89PNG\r\n\x1a\n': 'png'  # PNG
    }

    index = 0
    position = 0
    data_length = len(data)

    while position < data_length:
        found = False

        # Look for image signature
        for sig, ext in signatures.items():
            sig_index = data.find(sig, position)

            if sig_index != -1:
                found = True
                end_index = None

                if ext == 'jpg':
                    # Look for JPEG end marker
                    end_marker = b'\xff\xd9'
                    end_index = data.find(end_marker, sig_index)
                    if end_index != -1:
                        end_index += len(end_marker)
                elif ext == 'png':
                    # Look for PNG end marker
                    end_marker = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
                    end_index = data.find(end_marker, sig_index)
                    if end_index != -1:
                        end_index += len(end_marker)

                if end_index:
                    image_data = data[sig_index:end_index]
                    image_path = os.path.join(output_dir, f'image_{index:04d}.{ext}')

                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_data)

                    print(f'[+] Extracted {image_path}')
                    index += 1
                    position = end_index
                else:
                    position = sig_index + len(sig)
                break

        if not found:
            break

    print(f'\n[✓] Extraction completed. Total images: {index}')


if __name__ == "__main__":
    bin_file = 'images_dump.bin'  # Replace with your .bin file path
    output_folder = 'extracted_images'
    extract_images_from_bin(bin_file, output_folder)
