# import module
from PIL import Image, ImageChops

# assign images
img1 = Image.open("images/tanda-tangan-ansori.jpg")
img2 = Image.open("images/tanda-tangan-fake.jpg")

# finding difference
diff = ImageChops.difference(img1, img2)

# showing the difference
# diff.show()
if diff.getbbox():
    diff.show()