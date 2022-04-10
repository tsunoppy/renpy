# renpy
- Reinforced concrete capacity package
- Genrate MN-diagram for reinforced concrete columns

## 1. MnGen.py

| class | Description        |
|:------|--------------------|
| MnGen | Mn Curve Generator |

| method      | Description                                                |
|:------------|------------------------------------------------------------|
| __init__    | initialize of variable                                     |
| read_cntl   | read CNTL table in excel data & make variable              |
| read_column | read COLUMN table in excel data & make variable            |
| solve       | solve mn capacity, save result data using column module    |
| solve_deep  | make mn capacity for the deep learning, and make datasets  |
| make_report | under develop                                              |
| read_calc   | read CALC table, generate mn curve figure, make pdf report |

### __init__(input_path)

| variable | Description                         |
|:---------|-------------------------------------|
| inp_path | path to the input data (Excel data) |
| home_dir | directly to the inp_path            |

### read_cntl()

| variable     | Description                              |
|:-------------|------------------------------------------|
| out_path     | output data path                         |
| view_path    | directly path to the inp_path            |
| report_path  | directly path to the pdf output file     |
| report_title | title in output report                   |
|:-------------|------------------------------------------|
| ndiv         | incremental of the neutral axis          |
| mdmax        | maximum bending moment in mn curve graph |
| ndmin        | minimum axial force in mn curve graph    |
| ndmax        | maximum axial force in mn curve graph    |

### read_column()

| varibale      | Description                   |
|:--------------|-------------------------------|
| st            | story                         |
| symb          | column symbol                 |
| fc            | compressive concrete strength |
| fy            | steel bar strength            |
| b             | column width                  |
| d             | column depth                  |
| dia           | bar diameter                  |
| nx,ny,dtx,dty | see input data specification  |
| name          | story column symbol           |

### solve()

| varibale | Description                       |
|:---------|-----------------------------------|
| obj      | column object using column module |

### use example

``` python
input_path = "./test/data.xlsx"
obj = MnGen(input_path) # make object
obj.read_cntl()         # read cntl table data
obj.read_column()       # read column table data
obj.solve()             # solve and save mn curve data
obj.read_calc()         # read calc table data & make pdf data
## or
# obj.solve_deep()      # solve and save datasets for the DL
```

## 1. How to use

``` python
>import column
```
| class  | Description                        |
|:-------|------------------------------------|
| Cap    | Calculation of the column capacity |
| Aft_mn | plot mn-curve graph                |
| Report | Making pdf report                  |


## 1-1. column.Cap()

``` python
>obj = column.Cap(fc,fy,b,dd,nx,ny,dtx,dty,dia)
```

| Parameters | Description                                   | unit  |       |
|:-----------|-----------------------------------------------|-------|-------|
| fc         | compressive concrete strength                 | N/mm2 | float |
| fy         | yield steel bar strength                      | N/mm2 | float |
| b          | width of the column                           | mm    | float |
| dd         | depth of the column                           | mm    | float |
| nx,ny      | number of steel bar                           | Nos   | int   |
| dtx,dty    | position of the steel bar from column surface | mm    | float |

### 1-1-1. column.Cap().mn_result_xlsx()

``` python
>obj.mn_result_xlsx(div,path,sheet_name)
```
| Parameters | Description                  | unit |
|:-----------|------------------------------|------|
| div        | num. of calculation mn data  | int  |
| path       | path to the output xlsx data | str  |
| sheet_name | column name                  | str  |



## Attribute

## Input data

### CNTL
### COLUMN
| item | unit | remark        | example |
|:-----|------|---------------|---------|
| st   | -    | story.        | 1       |
| sym  | -    | column symbol | c1      |
|      |      |               |         |

### CALC

# beam.py
# panel.py
# aij.py
