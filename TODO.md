# TODO.md
This document lists items that must be done. This is targeted towards developers. If you do not plan to work on this project, you are not required to read this document.

## Next Actions
This section lists required actions that will help move this project forward.
- [ ] `data_processing.ipynb`: move 2/3 of files to `training` and 1/3 of files to `test`
    - Files must be separated because each file represents one student
    - Files in `training` will be used on model. Files in `test` are used to test the model.
- [ ] Create test for students to cheat on
    - Some example tests include:
        - [Systems of equations with elimination challenge](https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:systems-of-equations/x2f8bb11595b61c86:solving-systems-elimination/e/systems_of_equations_with_elimination)
- [ ] Implement various different model types and compare performance between all of them. Head to [this website](https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html) for more information.
    - [x] Logistic Regresssion
    - [x] Random Forest
    - [ ] Decision Trees
    - [ ] K Nearest Neighbors
    - [ ] K Means Clustering
    - [ ] Support Vector Machines
    - [ ] OPTIONAL: Deep Learning (requires much more effort but can be more accurate than other models)
- [ ] Figure out how to implement curvature formula correctly
    - Currently, curvature is calculated between two points. This may result in incorrect answers as curvature cannot be derived from one straight line.
    - Note, calculating curvature may not work for multiple straight lines. Therefore, it may make sense **not** to implement curvature. However, 
- [ ] Get mouse logging data in all other core subjects (history, English, math, and science)
    - Personally, I recommend to start with math. This is because math requires students to work using pen and paper, and not on the computer.



### Completed Next Actions
Place completed actions here.


## Optional Actions
This section lists possible actions that could be completed in the future. You are not required to complete these.
- [ ] Display logo for mouse logger (see `Images` folder)
    - Currently, it is a Photoshop file. To edit this file, use Photoshop, GIMP, or https://www.photopea.com/.
- [ ] Turn `data_processing.ipynb` into a class
- [ ] Test how performance differs with different screen resolutions
    - [ ] Make program that can scale different screen resolutions such that they are the same size

### Completed Optional Actions
