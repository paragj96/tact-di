import pip

def install(package):
    pip.main(['install', package])

# Example
if __name__ == '__main__':
    install('collections')
    install('cv2')
    install('matplotlib')
    install('numpy')
    install('skimage')
    install('stl')
    install('Tkinter')
    install('tkFileDialog')