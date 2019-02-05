# tact-di
Automatic Creation of Tactile Diagrams
1. Clone the repo to your preferred location.

2. Make sure you have a working installation of Python 2.7. If not you can install Python from the following link: https://www.python.org/download/releases/2.7.2/

3. Once the python is installed, install Anaconda Distribution from the following link for Python 2.7: https://www.anaconda.com/download/

4. Once the Python and Anaconda is installed, install the following Python packages into your Python environment using their respective commands:
```
  conda install -c anaconda numpy
  conda install -c anaconda scikit-image
  conda install -c conda-forge opencv
  conda install -c conda-forge/label/broken opencv
  conda install -c prkrekel numpy-stl
  conda install -c anaconda python-utils
  conda install -c auto fileutils
  conda install -c travis filepath
  conda install -c anaconda flask
```
If any package is missing in this installation which is required in the project, you can install it manually.

5. Now move inside the project folder and run the following command: python app.py

Now the project will be running on localhost port 5000. Browse to http://127.0.0.1:5000/ and enjoy!

**Note: The code has been tested for Windows Platform.**
