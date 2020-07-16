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




