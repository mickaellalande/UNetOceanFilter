import os
import psutil


def check_memory():
    print('Memory usage: ' + str(psutil.virtual_memory().percent) + '%')
    

def check_path(path):
    # check path and create it if it doesn't exist
    temp_path = ''
    for sub_path in path.split('/'):
        temp_path += sub_path+'/'
        if not os.path.isdir(temp_path):
            os.mkdir(temp_path)
            
               
def get_zone(name):
    if name != 'global':
        # South Atlantic
        if name == 'zone1': 
            x0 = 1020; y0 = 300; 
        
        # Around Japan (include lands)
        elif name == 'zone2': 
            x0 = 180; y0 = 540;

        # Antarctic Circumpolar Current
        elif name == 'zone3': 
            x0 = 500; y0 = 130;
        
        # South Australia
        elif name == 'zone4': 
            x0 = 150; y0 = 160;
        
        # Pacific Equator
        elif name == 'zone5': 
            x0 = 440; y0 = 440;
        
        # North Atlantic
        elif name == 'zone6': 
            x0 = 900; y0 = 550;

        box_size = 160
        (x_min, x_max) = (x0, x0+box_size); (y_min, y_max) = (y0, y0+box_size);
    
    # This global size is for having multiples that can be divided many times for testing different machine learning architectures without any problem during the max_pooling/upsampling operations
    else:
        x_min=0; x_max=1440; y_min=15; y_max=992+15;
         
    return x_min, x_max, y_min, y_max
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
