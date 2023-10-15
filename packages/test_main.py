
from image_utils import *
from IQ_generator import * 
import sys


if __name__ == "__main__":
    q = Question(500,500)
    ques_type = random.choice(["1","2","3"])
    ques_type = "4"
    if ques_type  == "1" :
        q.generate_random_lines()
    elif ques_type == "2" :
        q.generate_random_hexa()
    elif ques_type == "3" :
        q.generate_random_boxes()
    elif ques_type == "4" :
        q.generate_random_disks()
