from PIL import Image

def change_text_color(image_path, output_path, old_color, new_color):
    # Open the image
    image = Image.open(image_path).convert("RGBA")

    # Load the image data
    data = image.getdata()

    # Create a list to hold the new data
    new_data = []
    
    # Replace the text color
    for item in data:
        # If the pixel matches the old color (ignoring alpha), replace it
        if item[:3] == old_color:
            new_data.append((*new_color, item[3]))  # Keep the original alpha
        else:
            new_data.append(item)  # Otherwise, keep the original pixel

    # Update the image data
    image.putdata(new_data)

    # Save the new image
    image.save(output_path)

# Define the old text color (e.g., black text)
old_text_color = (0, 0, 0)  # Black

# Define the new text color (e.g., red text)
new_text_color = (218, 218, 218)

# Change the text color in the image
change_text_color("static/img/pbj-logo.png", "static/img/pbj-logo-light.png", old_text_color, new_text_color)