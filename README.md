

# A Machine Learning Technique to Attenuate the Imprint of Chaotic Ocean Variability in Altimetric Observations

Mickaël Lalande, Redouane Lguensat, Sally Close and Thierry Penduff

[IGE - Institut des Géosciences de l'Environnement](http://www.ige-grenoble.fr/)<br/>
<mickael.lalande@univ-grenoble-alpes.fr>


<br/>
This repository aims to make available the code for the submission of the paper "A Machine Learning Technique to Attenuate the Imprint of Chaotic Ocean Variability in Altimetric Observations". An example of use of the U-Net algorithm is presented in the notebook **estimate_forced_component.ipynb**. 


# U-Net architecture 

![](img/unet.png)

(a) Snapshot (January 3, 1979; member 50) of SLA contributions (x and y correspond to model grid indices). The black boxes show the training zones and the green boxes show testing zones (160x160 pixels). (b) The U-Net architecture used in this study: inputs are total SLA 5-daily model fields and outputs their forced counterparts (in zone 1 for this example). Each blue box corresponds to a feature map (volume corresponding to the image size times the number of stacked images). White boxes represent copied feature maps. The arrows denote the different operations.

# Example of result

![](img/pred.png)

Illustration on January 3, 1979 of the performance of the U-Net algorithm trained on zone 1+2+3. Top left: total signal (member 1); top right: true forced signal (ensemble mean); bottom right: predicted forced signal; bottom left: difference between the predicted and true forced signals.
