# DEVELOPERS.md
Contains important information that developers should know when working on this program.

`mouse_tracker.py` has only been tested on Python version 3.9. It is likely that the code will work for later releases. However, for earlier releases, stability is unknown (though it should still be able to run).

Before using `machine_learning.ipynb`, please make sure that you have run `data_processing.ipynb` on the data first.

Each test must have different folders. Additionally, models should only be trained on one specific type of test. If the test is different, new models must be trained for that test.

For example, let's say you have the following tests:
- `Chapter 1 Test`
- `Chapter 2 Test`

Make folders for *each* test and store data in the folder that it belongs.

After, run `data_processing.ipynb` in the `Chapter 1 Test` folder and `Chapter 2 Test`folder. Then, run `machine_learning.ipynb` inside both folders.
