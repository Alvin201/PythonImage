import cv2
import numpy as np
import easygui

class Percent(float):
    def __str__(self):
        return '{:.2%}'.format(self)

original = cv2.imread("images/Untitled.jpg")
image_to_compare = cv2.imread("images/Untitled1.jpg")

#invert image
original = cv2.bitwise_not(original)
image_to_compare = cv2.bitwise_not(image_to_compare)


# original = cv2.imread("images/tanda-tangan-ansori.jpg",0)
# image_to_compare = cv2.imread("images/tanda-tangan-fake1.jpg",0)


# for Handwriting
# original = 255-original # invert image
# image_to_compare = 255-image_to_compare # invert image
# #n_black = cv2.countNonZero(original)
#
# number_of_white_pix_1 = np.sum(original == 255)
# number_of_white_pix_2 = np.sum(image_to_compare == 255)
# print('Number of white pixels:', number_of_white_pix_1)
# print('Number of white pixels:', number_of_white_pix_2)

# image_to_compare = 255-image_to_compare # invert image
# f_black = cv2.countNonZero(image_to_compare)
#
# height, width = original.shape
# n_total = height * width
#
# print(n_black)
# print(f_black)

# 1) Check if 2 images are equals
if original.shape == image_to_compare.shape:
    print("The images have same size and channels")
    difference = cv2.subtract(original, image_to_compare)
    b, g, r = cv2.split(difference)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("The images are completely Equal")
    else:
        print("The images are NOT equal")

# 2) Check for similarities between the 2 images
sift = cv2.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(original, None)
kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

#print(desc_1)

index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(desc_1, desc_2, k=2)
#print(matches)

good_points = []

for m, n in matches:
    a = 0.7 * n.distance #79.9316
                         #m.distance 113
    if m.distance < a:
        good_points.append(m)
        #print(good_points.append(m))

# Define how similar they are
number_keypoints = 0
if len(kp_1) <= len(kp_2):
    number_keypoints = len(kp_1)
else:
    number_keypoints = len(kp_2)

#goodmatch/keypoint
res = len(good_points) / number_keypoints * 1
#res = number_keypoints / len(good_points) * 1

msg_res = Percent(res)
result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)

# print(len(good_points))
# print(number_keypoints)

cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
cv2.imwrite("feature_matching.jpg", result)

if (res >= 0.08):
    easygui.msgbox("Keypoints original Image: " + str(len(kp_1)) +'\n'+
                   "Keypoints compare Image: " + str(len(kp_2)) + '\n' +
                   "Matches Point:" + str(len(good_points)) + '\n\n' +
                   "Match Indication: " + "Match" + '\n' +
                   "Accurate similarity: " + str(msg_res),
                   title="Complete")
else:
    easygui.msgbox("Keypoints original Image: " + str(len(kp_1)) + '\n' +
                   "Keypoints compare Image: " + str(len(kp_2)) + '\n' +
                   "Matches Point:" + str(len(good_points)) + '\n\n' +
                   "Match Indication: " + "Unmatch" + '\n' +
                   "Accurate similarity: " + str(msg_res),
                   title="Complete")

#cv2.imshow("Original", cv2.resize(original, None, fx=0.4, fy=0.4))
#cv2.imshow("Duplicate", cv2.resize(image_to_compare, None, fx=0.4, fy=0.4))
cv2.waitKey(0)
cv2.destroyAllWindows()