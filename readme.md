# Crack Detection

## Algorithm

1. **Apply Median Filter**
The street surface is NOT flat and a lot of sand or dust is on the the street.
Median filter is really good for reduce pepper-and-salt noise which can be apply to this problem.

2. **Convert to Binary Image**
Apply Adaptive Thresholding built-in method in OpenCV for different thresholds in different regions of the image to get a better transformation
The threshold value is Gaussian weighted sum of the (11, 11) region.

3. **Grouping Adjacent White Pixels**
Extract the white pixels from the image and store the them into the list of corresponding xy position.
Apply DBSCAN to grouping adjacent pixel into different cluster.

4. **Remove Minnor Groups**
There are a lot of small groups containing few pixels which we could consider as noise.
One of the provious way to remove them is to eleminate the cluster that has a number of pixels less than the average.
By observation, the threshold should work if it is 6 times the average value.

5. **Connecting group to form a crack**
I am working on it and have some ideas: Base on the group that have a shape like a line, I could find the direction and connect the groups on that direction and fill the gap between them to illustract a crack.

## Discussion

At this time, all the parameters for the methods like median filter, binary transform is a fixed number.
It is not good to use the global variable for parameter because each image has its own context, some of the street are rough, while the others might more flat.
Thus, the algorithm should understand the context of the image to set a good param for the methods.

I have try to transform the problem in to a segmentation problem.
Instead of finding a crack, I try to recognize the regions divided by the crack.
With a thick crack, this method work quite good.
However, for the skinny one, it cannot segment at all.
In addition, if the crack do not form a closed border, the result might get wrong.

## Experiment

- Language: Python 2.7
- Library: OpenCV 3.2.0, scikit-learn 0.20.4
- Coding File: `crack_detection.py`
- Output Directory: `/output_edges`