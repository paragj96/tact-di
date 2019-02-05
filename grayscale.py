import numpy as np
from skimage import measure
import cv2
from stl import mesh
from skimage.filters import threshold_otsu

import file_utils
import file_paths as file
import image_properties as prop


def convertGrayScaleToSTL(imageurl):
    image = cv2.imread(imageurl)
    # img = np.array(image, dtype=np.uint8)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform 'closing' morphological operation on the image
    kernel = np.ones((1, 1), np.uint8)
    gray_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    # Figure out the scaling parameter according to original size and then scale
    scale = prop.get_scaling_factor()
    gray_image = cv2.resize(gray_image, (0, 0), fx=scale, fy=scale)

    # Normalize all pixels to assume values from 0 to 1
    gray_image = gray_image / 255.0
    gray_image = np.subtract(1.0, gray_image)

    # Find the threshold to separate foreground from background using OTSU's thresholding method
    threshold = threshold_otsu(gray_image)
    (rows, cols) = gray_image.shape

    '''
    Create a 3D voxel data from the image
    The top-most (#1) and bottom-most (#13) layer will contain all zeros
    The middle 10 layers (#3 to #12) contain the same pixel values as the gray scale image
    There is an additional layer(#2) for the base of the model 
    '''
    layers = 13
    rows += 2
    cols += 2
    voxel = np.zeros((rows, cols, layers))
    voxel[:, :, 1] = np.ones((rows, cols)).astype('float32')

    # making the boundary voxel values to be zero, for the marching cubes algorithm to work correctly
    voxel[0, :, :] = np.zeros((cols, layers)).astype('float32')
    voxel[(rows - 1), :, :] = np.zeros((cols, layers)).astype('float32')

    voxel[:, 0, :] = np.zeros((rows, layers)).astype('float32')
    voxel[:, (cols - 1), :] = np.zeros((rows, layers)).astype('float32')

    '''
    Create the middle 10 layers from the image
    Based on the pixel values the layers are created to assign different heights to different regions in the image
    '''
    for level in range(1, 10):
        level_threshold = level * 0.1
        for j in range(0, rows - 2):
            for k in range(0, cols - 2):
                pixel_value = gray_image[j][k]
                if pixel_value > level_threshold:
                    voxel[j + 1][k + 1][level + 1] = pixel_value

    '''
    Run the marching cubes algorithm to extract surface mesh from 3D volume. Params:
        volume : (M, N, P) array of doubles
            Input data volume to find isosurfaces. Will be cast to `np.float64`.
        level : float
            Contour value to search for isosurfaces in `volume`. If not
            given or None, the average of the min and max of vol is used.
        spacing : length-3 tuple of floats
            Voxel spacing in spatial dimensions corresponding to numpy array
            indexing dimensions (M, N, P) as in `volume`.
        gradient_direction : string
            Controls if the mesh was generated from an isosurface with gradient
            descent toward objects of interest (the default), or the opposite.
            The two options are:
            * descent : Object was greater than exterior
            * ascent : Exterior was greater than object
    '''
    verts, faces, normals, values = measure.marching_cubes_lewiner(volume=voxel, level=threshold,
                                                                   spacing=(1., 1., 1.), gradient_direction='descent')

    # Export the mesh as stl
    mymesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        for j in range(3):
            mymesh.vectors[i][j] = verts[f[j], :]

    file_utils.save_mesh_to_file(imageurl, mymesh)


if __name__ == "__main__":
    convertGrayScaleToSTL(file.get_image_path())


