import tarfile
import paddle
import numpy as np
import tvm
import cv2
from tvm import relay
from convert_image import resize_norm_img

model = paddle.jit.load("./build/ocr_en/inference")

img = cv2.imread('imgs_words_en/word_116.png')
img = resize_norm_img(img, [3,32,320])
img_data = img.astype("float32")

# # Add the batch dimension, as we are expecting 4-dimensional input: NCHW.
img_data = np.expand_dims(img_data, axis=0)

print(img_data.shape)
target = "llvm"
shape_dict = {"x": img_data.shape}
mod, params = relay.frontend.from_paddle(model, shape_dict)

with tvm.transform.PassContext(opt_level=3):
    executor = relay.build_module.create_executor(
        "graph", mod, tvm.cpu(0), target, params
    ).evaluate()

dtype = "float32"
tvm_output = executor(tvm.nd.array(img_data.astype(dtype))).numpy()
print(tvm_output.shape)


d = "#0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~!\"#$%&'()*+,-./  "
pred_flat = tvm_output.reshape([-1])
last_index = 0
score = 0
count = 0
for i in range(80):
    argmax_idx = 0
    max_value = 0.0
    for j in range(97):
        if pred_flat[i*97 + j] > max_value:
            max_value = pred_flat[i*97 + j]
            argmax_idx = j
    if argmax_idx > 0 and (not (i > 0 and argmax_idx == last_index)):
        score += max_value
        count += 1
        print(argmax_idx, max_value,d[argmax_idx])
    last_index = argmax_idx
print(score / count)

print('************************')
for i in range(10):
    print(pred_flat[i])