import pytest
from preprocessing.multiscale import Multiscale
import numpy as np
import gdal
import os

@pytest.fixture(params=np.random.randint(100, 2000, 5))
def nx(request):
    return request.param

@pytest.fixture(params=np.random.randint(100, 2000, 5))
def ny(request):
    return request.param

@pytest.fixture(params=np.random.randint(1, 10, 5))
def ml(request):
    return request.param

def create_tif(npx, npy, fn):
    image_size = (npx, npy)
    lat_range = [-90, 90]
    lon_range = [-180, 180]

    x = np.linspace(0, 1, npx)
    y = np.linspace(0, 1, npy)
    x, y = np.meshgrid(x, y)
    vals = np.float32(np.sin((x**2+y**2)*np.pi))

    # create 1-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create(fn, npx, npy, 1, gdal.GDT_Float32)
    dst_ds.GetRasterBand(1).WriteArray(vals)
    dst_ds = None
# end func

def test_multiscale(nx, ny, ml):
    fn = '/tmp/test.%d.%d.tif'%(nx,ny)
    create_tif(nx, ny, fn)

    flist = open('/tmp/flist.txt', 'w+')
    flist.write(fn)
    flist.close()

    print 'Testing Multiscale with nx:%d, ny:%d, max_level:%d'%(nx,ny,ml)
    ms = Multiscale('/tmp/flist.txt', '/tmp', level=ml, file_extension='.tif',
                    mother_wavelet_name='coif6',
                    extension_mode='smooth',
                    extrapolate=True,
                    max_search_dist=5,
                    smoothing_iterations=10)
    ms.process()

    os.system('rm -f %s' % fn)
    os.system('rm -f /tmp/flist.txt')

    # cleanup output files produced
    for l in range(1,ml+1):
        fn = '/tmp/test.%d.%d.level_%03d.tif'%(nx,ny, l)
        os.system('rm -f %s' % fn)