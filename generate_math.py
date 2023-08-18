import os

import numpy as np
import operator
import cv2
import json
import random

mode1 = np.random.randint(1, 3)

number = 100

annotates = []
questions_lis =[
    'What is the result of the formula in the picture?',
    "What outcome does the formula in the illustration yield?",
    "Can you tell me the output of the equation provided in this image?",
    "What does the formula in the graphic result in?",
    "What's the end product of the equation depicted in the picture?",
    "What's the computation from the formula showcased in this image?",
    "What conclusion can we draw from the formula illustrated in the picture?",
    "Can you show me the answer derived from the formula in this photo?",
    "What value does the formula in this diagram produce?",
    "Do you know the solution to the equation presented in the snapshot?",
    "What final answer will we get from this formula shown in the image?"
]

while number:
    # 二元运算
    # if mode1 == 1:
    abc = [np.random.randint(1, 20), np.random.randint(1, 20)]
    mat = [operator.add, operator.sub, operator.mul, operator.truediv]
    str_mat = ["+", "-", "x", "/"]
    mat_index = [np.random.randint(0, 4)]
    
    answer = mat[mat_index[0]](abc[0], abc[1])
    
    if np.rint(answer) == answer and answer <= 100 and answer >= -100:
        number -= 1
        print("{},   {}".format(number, int(answer)))
    
    # image
    scale1 = 1.5 * np.random.random() + 0.5
    scale2 = 1.5 * np.random.random() + 0.5
    # img = np.zeros((int(224 * scale1), int(224 * scale2)), np.uint8)
    img = np.zeros((224, 224), np.uint8)
    img[:,:] = 255
    # import pdb; pdb.set_trace()
    cv2.imwrite("/data/lessIsMore/generate_data/math/data/image/{}.jpg".format(100-number), img)
    bk_img = cv2.imread("/data/lessIsMore/generate_data/math/data/image/{}.jpg".format(100-number))
    cv2.putText(bk_img, "{}{}{}=".format(str(abc[0]), str_mat[mat_index[0]], str(abc[1])), (65,112), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    cv2.imwrite("/data/lessIsMore/generate_data/math/data/image/{}.jpg".format(100-number), bk_img)
    annotates.append({
        'id' : 100-number,
        'image': "{}.jpg".format(100-number),
        'conversations': [
            {'from':'human','value':random.choice(questions_lis)+'\n<image>'},
            {'from':'gpt','value':str(answer)}
        ]
    })

number = 100
while number:
    # 三元运算
    # if mode1 == 2:
    abc = [np.random.randint(1, 20), np.random.randint(1, 20), np.random.randint(1, 20)]
    mat = [operator.add, operator.sub, operator.mul, operator.truediv]
    mat_index = [np.random.randint(0, 4), np.random.randint(0, 4)]
    # mat_index_1 = [np.random.randint(0, 4), np.random.randint(0, 4)]
    
    answer = mat[mat_index[1]](mat[mat_index[0]](abc[0], abc[1]), abc[2])
    
    if np.rint(answer) == answer and answer <= 100 and answer >= -100:
        number -= 1
        print("{},   {}".format(number, int(answer)))
    
    # image
    scale1 = 1.5 * np.random.random() + 0.5
    scale2 = 1.5 * np.random.random() + 0.5
    img = np.zeros((224, 224), np.uint8)
    img[:,:] = 255
    # import pdb; pdb.set_trace()
    cv2.imwrite("/data/lessIsMore/generate_data/math/data/image/{}.jpg".format(200-number), img)
    bk_img = cv2.imread("/data/lessIsMore/generate_data/math/data/image/{}.jpg".format(200-number))
    cv2.putText(bk_img, "{}{}{}{}{}=".format(str(abc[0]), str_mat[mat_index[0]], str(abc[1]), str_mat[mat_index[1]], str(abc[2])), (20,112), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    cv2.imwrite("/data/lessIsMore/generate_data/math/data/image/{}.jpg".format(200-number), bk_img)

    annotates.append({
        'id' : 100-number,
        'image': "{}.jpg".format(100-number),
        # 'question' : random.choice(questions_lis)+'\n<image>',
        # 'answer' : str(answer)
        'conversations': [
            {'from':'human','value':random.choice(questions_lis)+'\n<image>'},
            {'from':'gpt','value':str(answer)}
        ]
    })

print(annotates[0])
with open('/data/lessIsMore/generate_data/math/annotate.json','w') as f:
    f.write(json.dumps(annotates,ensure_ascii=False))
