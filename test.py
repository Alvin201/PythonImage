from PIL import Image
import imagehash
hash0 = imagehash.average_hash(Image.open('images/Untitled.jpg'))
hash1 = imagehash.average_hash(Image.open('images/Untitled1.jpg'))
cutoff = 5  # maximum bits that could be different between the hashes.

print(hash0)
print(hash1)

if hash0 - hash1 < cutoff:
  print('images are similar')
else:
  print('images are not similar')


