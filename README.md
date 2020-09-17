# excelMaxRow
Programme for analysing RTQuIC data using python in concert with MS Excel. RT-QuIC is a method for detecting prions that generates numeric data in rows. The data can be exported as excel files


## Installation
This repository only contains source code at the moment. The can be run using IDLE, Spider, Thorny etc 

## Usage
The programme extracts numeric RTQuIC data from an excel file. It can compute a number of values of interest to RT-QuIC users. It can place these computed values conveniently in an excel destination file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please contact me (Alex Peden) 

## License
```
[MIT](https://choosealicense.com/licenses/mit/)
```

## Acknowledgements
Eric Gazoni, Charlie Clark who created with openpyxl library.

## Plotting a single RT-QuIC traces selected from a dataframe
Once a dataframe has been generated from multiple excel files it is possible to use a function called tracePlot to plot a single trace. The trace can be selected by supplying two arguments: the name of the excel file, and the sample label. An example plot is shown below. 

![Single trace](https://github.com/apeden/excelMaxRow/blob/master/sing_trace.png)


## Plotting multiple traces
Using a function called tracePlot you can plot multiple traces:

![Multiple traces](https://github.com/apeden/excelMaxRow/blob/master/mult_trace.png)

In the above example, 9 traces are plotted
- y axis : flourescence values
- x axis : time in hours
* horizontal line
- green: baseline threshold, base + 5 standard deviations
- blue: lag value (three times base, if achieved)
- red: maximum value
* orange line: gradient of log growth phase


# Features
* lag time
* Value at lag time
* Time to maximum value
* Maximum value
* Gradient of growth phase
* Baseline value
* Baseline threshold
* Time to breaching baseline threshold
* Area under the curve

## Plotting two features on a scattergram
Using this programme, it is possible to generate a data frame of features and then select two of these features for plotting a scattergram. The following example shows the area under the curve (AUC) plotted against Time to maximum value. The features have been scaled to between 0 (minimum) and 1 (maximum).

![AUC versus time to max](https://github.com/apeden/excelMaxRow/blob/master/AUC%20vs%20Time%20to%20max.jpeg)
- blue : positive controls
- red: blinded positive controls
- green: negative controls
- cyan: the test samples

Another example, this time of AUC versus lagtime is shown below

![AUC versus time to max](https://github.com/apeden/excelMaxRow/blob/master/AUC%20vs%20Lag%20Time.jpeg)

## Best features for decriminating positive from negatives
An important question is what combination of features best discriminates a positive sample from a negative sample. If we restrict the number of features to 6, their are (6(6-1))/2 = 15 pairwise combinations of features, and (6 x 6 x 6) = 216 triplet-wize combinations of features. Using a sextuplet-wize combination of feat

## Plotting a scatter matrix
It is possible to plot a scatter_matrix of scattergrams using the matplotlip.plotting module this programme. The datapoints in this scattergram are normalised as above. The scatter_matrix provides a convenient way for searching for correlations in the data. 

![Scatter_matrix](https://github.com/apeden/excelMaxRow/blob/master/example_scatter_matrix.png)

## Plotting a correlation heatmap
Using functions within dataframe and matplotlib it is possible to plot a heat map of pair-wise correlations between variable. Green indicates minimal correlation, yellow is  a positive correlation and blue a negative correlation. 

![Scatter_matrix](https://github.com/apeden/excelMaxRow/blob/master/heat_map.png)
