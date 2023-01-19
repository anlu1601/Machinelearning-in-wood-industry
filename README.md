# Machinelearning-in-wood-industry
This is a final project for Master degree in computer science. It investigates four different methods in machine learning to find which fits the problem best. The problem being identifying faults with wooden planks on a processing line.

The four methods used are ZFNet, DenseNet, Convolutional Auto-encoder with SVM, and Yolo.
ZFNet is concluded to be the best method for this problem and a inference script is added for that method.


## Inference usage

To use the inference script this is the command. To avoid warnings tensorflow needs to be version 2.8.3.

```
python3 inferenceZF.py [-s] filename.mp4
```

This initializes the model that resides in ./my_model and then binary search is performed on the frames in the mp4 file.
The -s flag is to run the model from start to find the first frame of error where it stops. This takes longer but might be more reliable.
