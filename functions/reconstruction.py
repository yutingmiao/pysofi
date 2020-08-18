import numpy as np
import tifffile as tiff
import scipy.special

def average_image(filepath, filename):
    '''
    Get the average image for a video file (tiff stack).
    '''
    imstack = tiff.TiffFile(filepath + '/' + filename)
    xdim, ydim = np.shape(imstack.pages[0])
    mvlength = len(imstack.pages)
    mean_im = np.zeros((xdim, ydim))
    
    for frame_num in range(mvlength):
        im = tiff.imread(filepath + '/' + filename, key=frame_num)
        mean_im = mean_im + im

    mean_im = mean_im / mvlength
    
    return mean_im

def calc_moments(filepath, filename, highest_order, m_set={}, mean_im=None):
    '''
    Get all moment-reconstructed images to the user-defined highest order for
    a video file(tiff stack).

    Parameters
    ----------
    filepath: str
        Path to the tiff file.
    Filename: str
        Name of the tiff file.
    highest_order: int
        The highest order number of moment-reconstructed images.
    m_set: dict 
        order number (int) -> image (ndarray)
        A dictionary of previously calcualted moment-reconstructed images.
    mean_im: ndarray
        Average image of the tiff stack.

    Returns
    -------
    m_set: dict
        order number (int) -> image (ndarray)
        A dictionary of calcualted moment-reconstructed images.

    Examples
    --------
    TODO: Please refer to the demo Jupyter Notebook ''.
    '''
    if m_set:
        current_order = max(m_set.keys())
    else:
        current_order = 0
            
    if mean_im is None:
        mean_im = average_image(filepath, filename)

    imstack = tiff.TiffFile(filepath + '/' + filename)
    xdim, ydim = np.shape(imstack.pages[0])
    mvlength = len(imstack.pages)
                
    if highest_order > current_order:
        for order in range(current_order, highest_order):
            m_set[order+1] = np.zeros((xdim, ydim))
            for frame_num in range(mvlength):
                im = tiff.imread(filepath + '/' + filename, key=frame_num)
                m_set[order+1] = m_set[order+1] + \
                                 np.power(im - mean_im, order+1)
        
            m_set[order+1] = np.int64(m_set[order+1] / mvlength)
    return m_set


def calc_cumulants_from_moments(moment_set):
    '''
    Calculate cumulant-reconstructed images from moment-reconstructed images.

    Parameters
    ----------
    moment_set: dict
        order number (int) -> image (ndarray)
        A dictionary of calcualted moment-reconstructed images.

    Returns
    -------
    k_set: dict
        order number (int) -> image (ndarray)
        A dictionary of calcualted cumulant-reconstructed images.

    Examples
    --------
    TODO: Please refer to the demo Jupyter Notebook ''.
    '''
    if moment_set == {}:
        raise Exception("'moment_set' is empty.")
        
    k_set = {}
    highest_order = max(moment_set.keys())
    for order in range(1, highest_order + 1):
        k_set[order] = np.int64(moment_set[order] - \
            np.sum(np.array(
                [scipy.special.comb(order-1,i)*k_set[order-i]*moment_set[i]
                for i in range(1,order)]),axis=0))
    
    return k_set


