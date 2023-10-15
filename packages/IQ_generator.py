##############################################################################
# package description  and copyrights go here
#
#
#
##############################################################################


import cv2 
import numpy as np
from image_utils import *
import json
import random
import math

class Question ():

    def __init__(self, image_height, image_width) :
        """
        Contructor of class image
            @image_height : type int 
                            description lenght of image
            @image_width : type : int
                            description width of image
        """
        self.image = image(image_height, image_width)
        start_x, start_y, box_size = self.calculate_question_box_size(image_height, image_width)
        self.image.init_question(start_x, start_y, box_size,3)
        self.image.draw_question_boxes()

    def calculate_question_box_size(self, height, width):
        """
        Calculate question params 
        @height : type int, lenght of image
        @width : int, width of image
        """
        start_x = int( height/ 5)
        start_y = int(width / 5)
        box_size = (int(height/5), int(width / 5))
        return  start_x,start_y,box_size

    def save_question_explication(self, explication, path):
        """
        Save given explication to a specific path in json format
        @ explication ; dict , question explication
        @ patn : str, location of saving directory
        """
        file_responce = open(path,"w")
        json.dump(explication,file_responce)
        file_responce.close()

    def generate_possible_shifts(self, number_of_positions, distance_of_position):
        """
        Generate possible shifts on a given distance
        @ number_of_positions ; int 
        @ distance_of_position : int
        """
        dec = int(distance_of_position / (1+number_of_positions))
        possible_shifts = [dec + (i*dec) for i in range(number_of_positions)]
        return possible_shifts

    def generate_random_lines(self):
        """
        Generate and draw lines pattern
        """
        possible_horizontal_shifts = self.generate_possible_shifts(3, self.image.box_height)
        possible_vertical_shifts = self.generate_possible_shifts(3, self.image.box_width)
        initial_horizontal_position = random.choice(possible_horizontal_shifts)
        index_intial_h_position = possible_horizontal_shifts.index(initial_horizontal_position)
        next_pos_h = index_intial_h_position
        pos_y_line = self.image.pos_y
        for _ in range(3):
            pos_x_line =  self.image.pos_x
            for _ in range(3):
                self.image.add_h_lines(pos_x_line ,pos_y_line + possible_horizontal_shifts[next_pos_h], self.image.box_height)
                true_dec_h = possible_horizontal_shifts[next_pos_h]
                pos_x_line+= self.image.box_height + 5
            next_pos_h = (next_pos_h + 1) % 3
            pos_y_line += self.image.box_width + 5
        initial_vertical_position = random.choice(possible_vertical_shifts)
        index_intial_v_position = possible_vertical_shifts.index(initial_vertical_position)
        next_pos_v = index_intial_v_position
        pos_x_line = self.image.pos_x
        for _ in range(3):
            pos_y_line =  self.image.pos_y
            for _ in range(3):
                self.image.add_v_lines(pos_x_line + possible_vertical_shifts[next_pos_v] ,pos_y_line , self.image.box_width)
                true_dec_v = possible_vertical_shifts[next_pos_v]
                pos_y_line+= self.image.box_height + 5
            next_pos_v = (next_pos_v + 1) % 3
            pos_x_line += self.image.box_width + 5
        explication = {}
        explication["true_responce"]= {"status" :"correct"}
        explication["true_responce"]["explication"] = """La reponce est correcte les ligne verticale et horizontal sont a la meme position que
les traits verticales et horizontales de chaque image de la meme ligne et colone"""
        used_positions = [(true_dec_v, true_dec_h)] 
        false_reponce_number = 0
        while false_reponce_number < 7:
            image = np.zeros([self.image.box_height,self.image.box_width,3],dtype=np.uint8)
            image[:,:,:] = np.array(self.image._box_color)
            pos_v, pos_h = random.choice(possible_horizontal_shifts), random.choice(possible_vertical_shifts)
            pos = (pos_v, pos_h)
            if pos not in used_positions :
                false_reponce_number+=1
                if pos_v != true_dec_v and pos_h != true_dec_h :
                    false_explication = (
                    "Le trait vertical doit être à la même position que le trait vertical"
                    " de chaque image de la même colonne Le trait horizontal doit être à la même"
                    " position que le trait horizontal de chaque image sur la même ligne")
                elif   pos_h != true_dec_h :
                    false_explication =  (
                    "Le trait horizontal doit être à la même position que le trait"
                    " horizontal de chaque image sur la même ligne")
                elif pos_v != true_dec_v :
                    false_explication =  (
                    "Le trait vertical doit être à la même position que le trait " 
                    "vertical de chaque image de la même colonne")
                explication["false_responce" + str(false_reponce_number)]= {"status" :"incorrect"}
                explication["false_responce" + str(false_reponce_number)]["explication"] = false_explication
                image = cv2.line(image, (0, pos_h), (self.image.box_height, pos_h), self.image._shapes_color, 2)
                image = cv2.line(image, (pos_v, 0), (pos_v, self.image.box_width), self.image._shapes_color, 2)
                used_positions.append(pos)
                cv2.imwrite("../question/false_responce" + str(false_reponce_number)+ '.png', image)
        self.save_question_explication(explication,"../question/question_explication.json")
        self.image.save_question_info("../question/")
        self.image.save_image("../question/question.png")

    def generate_random_boxes(self):
        """
        Generate and draw boxes pattern
        """
        frame_dec = int(self.image.box_height/(18))
        object_size = int(self.image.box_width / 4.5)
        pos_x_line =  self.image.box_height  + frame_dec 
        pos_x_frame = self.image.box_height 
        size = self.image.box_width
        initial_number = random.choice((3,1))
        possible_dec = [frame_dec , int(self.image.box_height/3) + frame_dec , int(self.image.box_height/1.5) +frame_dec]
        initial_box_pos = random.choice(possible_dec)
        index_initial_box_pos = possible_dec.index(initial_box_pos) 
        next_pos_box = index_initial_box_pos
        true_responce_cords = {"number_of_objects" : 0, "position_of_objects" : 0}
        for _ in range(3):
            pos_y_frame = self.image.pos_y
            pos_y_line = self.image.pos_y + int(object_size / 2)
            counter = initial_number
            for _ in range(3):
                dec = frame_dec
                true_responce_cords["number_of_objects"] = counter
                for _ in range(counter):
                    self.image.create_frame((object_size,object_size), pos_x_frame+possible_dec[next_pos_box], pos_y_frame+dec, self.image._shapes_color_2)
                    self.image.create_frame((object_size,object_size), pos_x_frame+possible_dec[next_pos_box], pos_y_frame+dec, self.image._shapes_color, thick=2)
                    self.image.add_h_lines(pos_x_line , pos_y_line + dec , size - 2*frame_dec)
                    dec += int(size/3) 
                    true_responce_cords["position_of_objects"] = possible_dec[next_pos_box]            
                if initial_number == 3 :
                    counter-=1
                else :
                    counter+=1
                pos_y_frame += self.image.box_height + 5
                pos_y_line += size + 5
            next_pos_box = (next_pos_box + 1) % 3
            pos_x_line += size + 5
            pos_x_frame += self.image.box_height + 5
        number_of_false_responce = 0
        explication = {}
        explication["true_responce"]= {"status" :"correct"}
        explication["true_responce"]["explication"] = ('Sur une même ligne, le nombre d’objet est le même dans chaque image'
                            'Sur une même colonne, les objets de chaque image sont à la même position')
        while number_of_false_responce < 7:
            image = np.zeros([self.image.box_height,self.image.box_height,3],dtype=np.uint8)
            image[:,:,:] = np.array(self.image._box_color)
            pos_box= random.choice(possible_dec)
            lines_number = random.choice((1,2,3))
            columns_number = random.choice((1,2,3))
            if pos_box != true_responce_cords["position_of_objects"] or columns_number != true_responce_cords["number_of_objects"] :
                index_initial_box_pos = possible_dec.index(pos_box) 
                pos_y_frame = pos_box
                dec2 = 10 
                pos_y_line = int(self.image.box_height/3) - int(object_size/2)
                pos_x_frame = pos_box
                pos_x_line = int(object_size / 2) + frame_dec 
                for _ in range(columns_number):
                    dec = 0
                    next_pos_box = index_initial_box_pos
                    for _ in range(lines_number):
                        image = self.image.sub_frame(image, (object_size,object_size),
                                        possible_dec[next_pos_box] ,frame_dec + dec2, self.image._shapes_color_2)
                        image = self.image.sub_frame(image, (object_size,object_size),
                                        possible_dec[next_pos_box], frame_dec + dec2, self.image._shapes_color, thick=2)
                        
                        #image = self.image.add_sub_h_lines(image, int(object_size / 2) , dec+ frame_dec, size- 2*frame_dec)       
                        dec += object_size 
                        next_pos_box = (next_pos_box + 1) % 3
                    image = self.image.add_sub_h_lines(image, frame_dec  , pos_y_line , size - 2*frame_dec)
                    pos_y_line += object_size+ frame_dec 
                    dec2 += object_size + frame_dec
                number_of_false_responce+=1
                if pos_box != true_responce_cords["position_of_objects"] and columns_number != true_responce_cords["number_of_objects"] :
                    false_explication = ('Sur une même ligne, le nombre d’objet est le même dans chaque image'
                            'Sur une même colonne, les objets de chaque image sont à la même position')
                elif pos_box != true_responce_cords["position_of_objects"] :
                    false_explication = ('Sur une même colonne, les objets de chaque image sont à la même position')
                elif columns_number != true_responce_cords["number_of_objects"] :
                    false_explication = ('Sur une même ligne, le nombre d’objet est le même dans chaque image')
                explication["false_responce" + str(number_of_false_responce)]= {"status" :"incorrect"}
                explication["false_responce" + str(number_of_false_responce)]["explication"] = false_explication
                cv2.imwrite("../question/false_responce" + str(number_of_false_responce)+ '.png', image)
        self.save_question_explication(explication,"../question/question_explication.json")
        self.image.save_question_info("../question/")
        self.image.save_image("../question/question.png")

    def generate_random_indexs(self):
        """
        Genrate random color on hexagone
        """
        list_shapes= []
        # choose 1 index for first and second column
        for _ in range(2):
            indexs = [i for i in range(6)]
            # initialize the first shape of column 
            shape_one = [0 for _ in range(6)]
            # initialize the second shape of column 
            shape_two = [0 for _ in range(6)]
            # choose a random index to set to 1
            new = random.randint(1, 2)
            for i in range(new):
                index = random.choice(indexs)
                shape_one[index] = 1
                # remove our choice 
                indexs.pop(index)
                index = random.choice(indexs)
                shape_two[index] = 1
            shape_three = [int((i or j)) for i,j in zip(shape_one,shape_two)]
            list_shapes.append((shape_one, shape_two, shape_three))
        # choose 2 index for third column
        shape_one = [0 for _ in range(6)]
        shape_two = [0 for _ in range(6)]
        indexs = [i for i in range(6)]
        for i in range(2) :
            index = random.choice(indexs)
            indexs.remove(index)
            shape_one[i] = 1
        # index = random.choices(indexs) ##Pourquoi ???
        for i in range(2) :
            index = random.choice(indexs)
            indexs.remove(index)
            shape_two[index] = 1
        shape_three = [int((i or j)) for i,j in zip(shape_one,shape_two)]
        list_shapes.append((shape_one, shape_two, shape_three))
        return list_shapes
        
    def generate_random_hexa(self):
        """
        Generate and draw hexagone pattern
        """
        pos_x = self.image.pos_x + int(self.image.box_height / 5)
        pos_y = self.image.pos_y + int(self.image.box_width / 5)
        shapes = self.generate_random_indexs()
        centre = int(self.image.box_height / 3.55)
        size = int(self.image.box_height / 6)
        for i in range(3):
            pos_y = self.image.pos_y + int(self.image.box_width / 5)
            list_shapes = shapes[i]
            for shape in list_shapes:
                self.image.draw_hexagon((pos_x+ centre, pos_y+centre),size,shape)
                pos_y += self.image.box_width+ 5 
                responce_shape = shape
            pos_x+=self.image.box_height + 5 
        explication = {}
        explication["true_responce"]= {"status" :"correct"}
        explication["true_responce"]["explication"] = ("L’image sur la dernière ligne contient l’ensemble des couleurs"
                                        "claires des 2 images contenues dans la même colonne")
        number_of_false_responce = 0
        while number_of_false_responce < 7:
            fake_image = image(self.image.box_height, self.image.box_width)
            fake_image.create_frame((self.image.box_height,self.image.box_width), 0, 0)
            shape = [random.randint(0,1) for _ in range(6)]
            if shape != responce_shape :
                pos_y = int(self.image.box_width / 5)
                pos_x = int(self.image.box_width / 5)
                fake_image.draw_hexagon((pos_x + centre, pos_y+centre),size,shape)
                number_of_false_responce+=1
                explication["false_responce"+ str(number_of_false_responce)]= {"status" :"false"}
                explication["false_responce"+ str(number_of_false_responce)]["explication"] = ("L’image sur la dernière ligne contient l’ensemble des couleurs"
                                        "claires des 2 images contenues dans la même colonne")
                cv2.imwrite("../question/false_responce" + str(number_of_false_responce)+ '.png', fake_image.image)
        self.save_question_explication(explication,"../question/question_explication.json")
        self.image.save_question_info("../question/")
        self.image.save_image("../question/question.png")

    #######################################################################################

    def generate_random_disks(self):
        """
        Generate and draw disks pattern
        """
        pos_x = self.image.pos_x + int(self.image.box_height / 5)
        pos_y = self.image.pos_y + int(self.image.box_width / 5)
        shapes = self.generate_random_indexs()
        centre = int(self.image.box_height / 3.55)
        size = int(self.image.box_height / 6)
        for i in range(3):
            pos_y = self.image.pos_y + int(self.image.box_width / 5)
            list_shapes = shapes[i]
            for shape in list_shapes:
                self.image.draw_disk((pos_x+ centre, pos_y+centre),size,shape)
                pos_y += self.image.box_width+ 5 
                responce_shape = shape
            pos_x+=self.image.box_height + 5 
        explication = {}
        explication["true_responce"]= {"status" :"correct"}
        explication["true_responce"]["explication"] = ("L’image sur la dernière ligne contient l’ensemble des couleurs"
                                        "claires des 2 images contenues dans la même colonne")
        number_of_false_responce = 0
        while number_of_false_responce < 7:
            fake_image = image(self.image.box_height, self.image.box_width)
            fake_image.create_frame((self.image.box_height,self.image.box_width), 0, 0)
            shape = [random.randint(0,1) for _ in range(6)]
            if shape != responce_shape :
                pos_y = int(self.image.box_width / 5)
                pos_x = int(self.image.box_width / 5)
                fake_image.draw_disk((pos_x + centre, pos_y+centre),size,shape)
                number_of_false_responce+=1
                explication["false_responce"+ str(number_of_false_responce)]= {"status" :"false"}
                explication["false_responce"+ str(number_of_false_responce)]["explication"] = ("L’image sur la dernière ligne contient l’ensemble des couleurs"
                                        "claires des 2 images contenues dans la même colonne")
                cv2.imwrite("../question/false_responce" + str(number_of_false_responce)+ '.png', fake_image.image)
        self.save_question_explication(explication,"../question/question_explication.json")
        self.image.save_question_info("../question/")
        self.image.save_image("../question/question.png")

    #######################################################################################


if __name__ == "__main__":
    q = Question(1000,1000)
    q.generate_random_hexa()
    q.image.show("image")
            
