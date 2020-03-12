
# coding: utf-8

# Load packages

# In[1]:


#load necessary packages
import os
from PIL import Image
import numpy as np
import shutil


# In[2]:


#Directory containing images before grouping into sub folders
#input_dir = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET/"

#directories = os.listdir(input_dir)
#Now remove the file extensions
#i = 0

#for thisItem in directories:
#     directories[i] = os.path.splitext(thisItem)[0]
#     i=i+1

#print out filenames without extension
#print(directories)


# In[3]:


import pandas as pd
file_list = pd.read_csv('/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET_CLASSES', header = None)

print(file_list)


# In[4]:


#print out the filename list that belong to group 0
file_list_group0 = file_list.loc[file_list[1] == 0, 0]
print(file_list_group0)


# In[5]:


#print out the filename list that belong to group 1,2,3
file_list_group1 = file_list.loc[file_list[1] == 1, 0]
file_list_group2 = file_list.loc[file_list[1] == 2, 0]
file_list_group3 = file_list.loc[file_list[1] == 3, 0]

print(file_list_group1)


# In[6]:


#print(file_list_group3)

#example why need to add . to every item in the list
#s = 'IMG_6537_sppx12.png'
#print(s.startswith('IMG_6537_sppx1'))
#print(s.startswith('IMG_6537_sppx1.'))
file_list_group0_d = [item + "." for item in file_list_group0]
file_list_group1_d = [item + "." for item in file_list_group1]
file_list_group2_d = [item + "." for item in file_list_group2]
file_list_group3_d = [item + "." for item in file_list_group3]
print(file_list_group3_d)


# In[7]:


#grouping and check if matching
source = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET"
dest_g0 = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET_grouped/g0"
dest_g1 = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET_grouped/g1"
dest_g2 = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET_grouped/g2"
dest_g3 = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET_grouped/g3"

directories = os.listdir(source)
for f in directories:
    if (f.startswith(tuple(file_list_group0_d))):
        shutil.copy2(os.path.join(source,f), dest_g0)
    elif (f.startswith(tuple(file_list_group1_d))):
        shutil.copy2(os.path.join(source,f), dest_g1)
    elif (f.startswith(tuple(file_list_group2_d))):
        shutil.copy2(os.path.join(source,f), dest_g2)
    elif (f.startswith(tuple(file_list_group3_d))):
        shutil.copy2(os.path.join(source,f), dest_g3)


# In[8]:


#Directory containing images you wish to convert
input_dir = "/media/qiwei/165A4AA95A4A8609/Python_playground/smart_bandage/ULCER_SET_grouped"

directories = os.listdir(input_dir)
print(directories)


# In[11]:


index = 0
index2 = 0

for folder in directories:
	#Ignoring .DS_Store dir
	if folder == '.DS_Store':
		pass

	else:
		print("The currently using folder is: ", folder)

		folder2 = os.listdir(input_dir + '/' + folder)
		index += 1

		for image in folder2:
			if image == ".DS_Store":
				pass

			else:
				index2 += 1

				im = Image.open(input_dir+"/"+folder+"/"+image) #Opening image
				resized_im = im.resize((70,70), resample = Image.NEAREST ) # resized image of size 70x70, because origin images were just missing 1 or 2 pixels on edge using nearset neighbor method                
				im = (np.array(resized_im)) #Converting to numpy array


				try:
					r = im[:,:,0] #Slicing to get R data
					g = im[:,:,1] #Slicing to get G data
					b = im[:,:,2] #Slicing to get B data

					if index2 != 1:
						new_array = np.array([[r] + [g] + [b]], np.uint8) #Creating array with shape (3, 70, 70)
						out = np.append(out, new_array, 0) #Adding new image to array shape of (x, 3, 70, 70) where x is image number

					elif index2 == 1:
						out = np.array([[r] + [g] + [b]], np.uint8) #Creating array with shape (3, 70, 70)

					if index == 1 and index2 == 1:
						index_array = np.array([[index]])

					else:
						new_index_array = np.array([[index]], np.int8)
						index_array = np.append(index_array, new_index_array, 0)

				except Exception as e:
					print(e)
					print("Removing image" + image)
					#os.remove(input_dir+"/"+folder+"/"+image)

print("Number of folders/classes: ", index)


# In[12]:


#saving the train image arrays and labels
np.save('features_train.npy', out) #Saving train image arrays
np.save('labels_train.npy', index_array) #Saving train labels

