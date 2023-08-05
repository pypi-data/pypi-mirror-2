'''
TODO:

* Coordinates and conversions
* Sampling and resampling
* Loaders for CIPIC, MIT-KEMAR databases
* Calculated HRTFs with reflections and varying distance

ROMAIN'S NOTES:

HRTF module
===========
It would be good to have a set of functions to load and analyse HRTF data.
A good way to do that would be to have HRTFSet class, which would contain and manage
a complete set of HRTFs (class HRTF).

HRTF
----
This is basically two arrays with some general information (sampling frequency).
* Binaural information: phase, ITD and ILD with several methods (frequency-dependent)
** hrtf.ITD(freq1,freq2,method="MaxICC")
** hrtf.phase(freq) or hrtf.phase() # all frequencies
* Fourier domain / time domain conversion
* hrtf.left, hrtf.right (the two impulse responses, as Sound objects)

The HRTF class could derive from a stereo Sound class.

HRTFSet
-------
* Loading
* Coordinate conversion
* hrtf[azimuth,elevation] returns the HRTF for the given direction
* Slices: hrtf[a1:a2,e1:e2]
* Maybe interpolation (I would say: interpolate in the Fourier domain, then convert to time domain)
* Artificial HRTFs (sphere etc?)
* Simultaneous calculations (all directions): ITD, etc
'''

# TODO: add some docstrings!

from brian import *
from brian.hears.filtering import *
from brian.hears.sounds import *
from scipy.signal import lfilter
from scipy.io import loadmat # NOTE: this requires scipy 0.7+
from glob import glob
from copy import copy
from scipy.io.wavfile import *
import os

__all__ = [
    # Base classes
    'HRTF', 'HRTFSet', 'HRTFDatabase',
    # Coordinate systems
    'CartesianCoordinates', 'SphericalCoordinates', 'AzimElev', 'AzimElevDegrees', 'AzimElevDistDegrees',
    # IRCAM LISTEN database
    'IRCAM_HRTFSet', 'IRCAM_LISTEN',
    'GerbilHRTFSet', 'GerbilDatabase',
    'InRoomHRTFSet', 'InRoomDatabase',
    # GUINEA_PIG database
    'GuineaPigHRTFSet', 'GuineaPigDatabase',
    # BRIAN KATZ database
    'KatzHRTFSet', 'KatzDatabase'
    ]


class HRTF(object):
    '''
    HRTF class
    
    Has attributes:
    
    ``left``, ``right``
        The two HRTFs (``Sound`` objects)
    ``samplerate``
        The sample rate of the HRTFs.
    '''
    def __init__(self, hrir_l, hrir_r):
        self.samplerate = hrir_l.rate
        self.left = hrir_l
        self.right = hrir_r

    def apply(self, sound):
        # TODO: check samplerates match
        sound_l = Sound(lfilter(self.left, 1, sound), rate=self.samplerate)
        sound_r = Sound(lfilter(self.right, 1, sound), rate=self.samplerate)
        return (sound_l, sound_r)


class HRTFSet(object):
    '''
    Base class for a collection of HRTFs for one individual
    
    Should have attributes:
    
    ``name``
        A unique string identifying this individual.
    ``data``
        An array of shape (2, num_indices, num_samples) where data[0,:,:] is
        the left ear and data[1,:,:] is the right ear, num_indices is the number
        of HRTFs for each ear, and num_samples is the length of the HRTF.
    ``samplerate``
        The sample rate for the HRTFs (should have units of Hz).
    ``coordinates``
        The record array of length num_indices of coordinates.
    
    Derived classes should override the ``load(...)`` method which should create
    the attributes above. The ``load`` method should have the following optional
    keywords:
    
    ``samplerate``
        The intended samplerate (resampling will be used if it is wrong). If
        left unset, the natural samplerate of the data set will be used.        
    ``coordsys``
        The intended coordinate system (conversion will be performed if it is
        different).
    
    Automatically generates the attributes:
    
    ``hrtf``
        A list of ``HRTF`` objects for each index.
    ``num_indices``
        The number of HRTF locations.
    ``num_samples``
        The sample length of each HRTF.
    
    Has methods:
    
    ``subset(cond)``
        Generates the subset of the set of HRTFs whose coordinates satisfy
        the condition cond. cond should be a function whose argument names are
        names of the parameters of the coordinate system, e.g. for AzimElev you
        might do cond=lambda azim:azim<pi/2.
    '''
    def __init__(self, *args, **kwds):
        self.load(*args, **kwds)
        self.prepare()

    def load(self, *args, **kwds):
        raise NotImplementedError

    def prepare(self):
        L, R = self.data
        self.hrtf = []
        for i in xrange(self.num_indices):
            l = Sound(self.data[0, i, :], rate=self.samplerate)
            r = Sound(self.data[1, i, :], rate=self.samplerate)
            self.hrtf.append(HRTF(l, r))

    def subset(self, cond):

        ns = dict((name, self.coordinates[name]) for name in cond.func_code.co_varnames)

        try:
            I = cond(**ns)
        except:
            I = False
        if type(I) == type(True): # vector-based calculation doesn't work
            n = len(ns[cond.func_code.co_varnames[0]])
            I = array([cond(**dict((name, ns[name][j]) for name in cond.func_code.co_varnames)) for j in range(n)])
            I = I.nonzero()[0]

        hrtf = [self.hrtf[i] for i in I]
        coords = self.coordinates[I]
        data = self.data[:, I, :]
        obj = copy(self)
        obj.hrtf = hrtf
        obj.coordinates = coords
        obj.data = data
        return obj
    @property
    def num_indices(self):
        return self.data.shape[1]
    @property
    def num_samples(self):
        return self.data.shape[2]


class HRTFDatabase(object):
    '''
    Base class for databases of HRTFs
    
    Should have an attribute 'subjects' giving a list of available subjects,
    and a method ``load_subject(subject)`` which returns an ``HRTFSet`` for that
    subject.
    
    The initialiser should take (optional) keywords:
    
    ``samplerate``
        The intended samplerate (resampling will be used if it is wrong). If
        left unset, the natural samplerate of the data set will be used.
    ``coordsys``
        The intended coordinate system (conversion will be performed if it is
        different).
    
    Should have a method:
    
    ``subject_name(subject)``
        Which returns a unique string id for the database and subject within
        the database.
    '''
    def __init__(self, samplerate=None, coordsys=None):
        raise NotImplementedError

    def load_subject(self, subject):
        raise NotImplementedError

############# COORDINATE SYSTEMS ###############################################

class Coordinates(ndarray):
    names = None

    def convert_to(self, target):
        raise NotImplementedError
    @staticmethod
    def convert_from(source):
        raise NotImplementedError
    @property
    def system(self):
        return self.__class__
    @classmethod
    def make(cls, shape): #initialize a ndarray
        x = cls(shape=shape, dtype=cls.construct_dtype())
        return x
    @classmethod
    def construct_dtype(cls):
        return [(name, float) for name in cls.names]


class CartesianCoordinates(Coordinates):
    names = ('x', 'y', 'z')

    def convert_to(self, target):
        if target is self.system:
            return self
        else:
            return target.convert_from(self)


class SphericalCoordinates(Coordinates):
    names = ('r', 'theta', 'phi')


class AzimElev(Coordinates):
    names = ('azim', 'elev')

    def convert_to(self, target):
        out = target.make(self.shape)
        if target is self.system:
            return self
        elif target is CartesianCoordinates:
            # Individual looking along x axis, ears at +- 1 on y axis, z vertical
            out['x'] = sin(self['azim']) * cos(self['elev'])
            out['y'] = cos(self['azim']) * cos(self['elev'])
            out['z'] = sin(self['elev'])
            return out
        elif target is AzimElevDegrees:
            azim = self['azim'] * 180 / pi
            azim[azim < 0] += 360
            out['azim'] = azim
            out['elev'] = self['elev'] * 180 / pi
            return out
        else:
            # Try to convert by going via Cartesian coordinates
            inter = self.convert_to(CartesianCoordinates)
            return target.convert_from(inter)
    @staticmethod
    def convert_from(source):
        if isinstance(source, AzimElev):
            return source
        elif isinstance(source, CartesianCoordinates):
            out = AzimElev.make(source.shape)
            x, y, z = source['x'], source['y'], source['z']
            r = sqrt(x ** 2 + y ** 2 + z ** 2)
            x /= r
            y /= r
            z /= r
            elev = arcsin(z / r)
            azim = arctan2(x, y)
            out['azim'] = azim
            out['elev'] = elev
            return out


class AzimElevDegrees(Coordinates):
    names = ('azim', 'elev')

    def convert_to(self, target):
        if target is self.system:
            return self
        elif target is AzimElev:
            out = target.make(self.shape)
            out['azim'] = self['azim'] * pi / 180
            out['elev'] = self['elev'] * pi / 180
            return out
        else:
            inter = self.convert_to(AzimElev)
            return inter.convert_to(target)
    @staticmethod
    def convert_from(source):
        if isinstance(source, AzimElevDegrees):
            return source
        elif isinstance(source, CartesianCoordinates):
            inter = AzimElev.convert_from(source)
            return inter.convert_to(AzimElevDegrees)


class AzimElevDistDegrees(Coordinates):
    names = ('azim', 'elev', 'dist')

    def convert_to(self, target):
        if target is self.system:
            return self
        elif target is CartesianCoordinates:
            out = target.make(self.shape)
            # Individual looking along x axis, ears at +- 1 on y axis, z vertical
            out['x'] = self['dist'] * sin(self['azim'] * pi / 180) * cos(self['elev'] * pi / 180)
            out['y'] = self['dist'] * cos(self['azim'] * pi / 180) * cos(self['elev'] * pi / 180)
            out['z'] = self['dist'] * sin(self['elev'] * pi / 180)
            return out
        elif target is AzimElev:
            out = target.make(self.shape)
            out['azim'] = self['azim'] * pi / 180
            out['elev'] = self['elev'] * pi / 180
            return out
        else:
            # Try to convert by going via Cartesian coordinates
            inter = self.convert_to(CartesianCoordinates)
            return target.convert_from(inter)
    @staticmethod
    def convert_from(source):
        if isinstance(source, AzimElevDegrees):
            return source
        elif isinstance(source, CartesianCoordinates):
            inter = AzimElev.convert_from(source)
            return inter.convert_to(AzimElevDegrees)

############# IRCAM HRTF DATABASE ##############################################

class IRCAM_HRTFSet(HRTFSet):
    def load(self, filename, samplerate=None, coordsys=None, name=None):
        # TODO: check samplerate
        if name is None:
            _, name = os.path.split(filename)
        self.name = name
        m = loadmat(filename, struct_as_record=True)
        if 'l_hrir_S' in m.keys(): # RAW DATA
            affix = '_hrir_S'
        else:                      # COMPENSATED DATA
            affix = '_eq_hrir_S'
        l, r = m['l' + affix], m['r' + affix]
        self.azim = l['azim_v'][0][0][:, 0]
        self.elev = l['elev_v'][0][0][:, 0]
        l = l['content_m'][0][0]
        r = r['content_m'][0][0]
        coords = AzimElevDegrees.make(len(self.azim))
        coords['azim'] = self.azim
        coords['elev'] = self.elev
        if coordsys is not None:
            self.coordinates = coords.convert_to(coordsys)
        else:
            self.coordinates = coords
        # self.data has shape (num_ears=2, num_indices, hrir_length)
        self.data = vstack((reshape(l, (1,) + l.shape), reshape(r, (1,) + r.shape)))
        self.samplerate = 44.1 * kHz


class IRCAM_LISTEN(HRTFDatabase):
    def __init__(self, basedir, compensated=False, samplerate=None):
        self.basedir = basedir
        self.compensated = compensated
        names = glob(os.path.join(basedir, 'IRC_*'))
        splitnames = [os.path.split(name) for name in names]

        self.subjects = [int(name[4:]) for base, name in splitnames]
        self.samplerate = samplerate

    def subject_name(self, subject):
        return 'IRCAM_' + str(subject)

    def load_subject(self, subject):
        subject = str(subject)
        fname = os.path.join(self.basedir, 'IRC_' + subject)
        if self.compensated:
            fname = os.path.join(fname, 'COMPENSATED/MAT/HRIR/IRC_' + subject + '_C_HRIR.mat')
        else:
            fname = os.path.join(fname, 'RAW/MAT/HRIR/IRC_' + subject + '_R_HRIR.mat')
        return IRCAM_HRTFSet(fname, samplerate=self.samplerate, name=self.subject_name(subject))

def remove_nan_zero(x, axis=1):
    '''
    Removes all (rows/columns/etc.) which are all zero or have NaNs in them
    '''
    keep_index = []
    x = x.swapaxes(0, axis)
    for i in range(x.shape[0]):
        y = x[i, ...]
        if (abs(y) < 1e-50).all() or isnan(y).any():
            keep_index.append(False)
        else:
            keep_index.append(True)
    keep_index = array(keep_index, dtype=bool)
    x = x[keep_index, ...]
    x = x.swapaxes(0, axis)
    return x

### room database from  Barbara Shinn-Cunningham:
class InRoomHRTFSet(HRTFSet):
    def load(self, filename, samplerate=None, coordsys=None, name=None):
        # TODO: check samplerate
        if name is None:
            _, name = os.path.split(filename)
        self.name = name
        m = loadmat(filename, struct_as_record=True)
        affix = 'fimp_'
        l, r = m[affix + 'l'], m[affix + 'r']
        # Added by Dan - remove recordings with NaNs or all 0s
        # The reason being, that some of the recordings failed and were replaced
        # with (I think) NaNs (but the readme says zeros, so I put both conditions
        # here).
        l = remove_nan_zero(l, axis=1)
        r = remove_nan_zero(r, axis=1)
        # Question from Dan - is this OK to take the mean of several recordings?
        l = mean(l, axis=1)
        r = mean(r, axis=1)
        l = reshape(l, (-1, 21)).T
        r = reshape(r, (-1, 21)).T

        print l.shape, r.shape

        self.azim = tile(linspace(0, 90, 7), 3) #tile because 3x7 -> 1:7|1:7|1:7    
        self.elev = zeros((21))
        self.dist = repeat(array([0.15, 0.40, 1]), 7) #repeat because with reshape 3x7
        coords = AzimElevDistDegrees.make(len(self.azim))
        coords['azim'] = self.azim
        coords['elev'] = self.elev
        coords['dist'] = self.dist

        if coordsys is not None:
            self.coordinates = coords.convert_to(coordsys)
        else:
            self.coordinates = coords
        # self.data has shape (num_ears=2, num_indices, hrir_length)
        self.data = vstack((reshape(l, (1,) + l.shape), reshape(r, (1,) + r.shape)))

        # Added by Dan - normalise to +/- 1
        self.data /= amax(abs(self.data))

        print self.data.shape
        #self.data = vstack((reshape(l, (1,)+l.shape), reshape(r, (1,)+r.shape)))
        self.samplerate = 44.1 * kHz

# TODO: change the name (LISTEN is the name of the IRCAM project)
class InRoomDatabase(HRTFDatabase):
    def __init__(self, basedir, samplerate=None):
        self.basedir = basedir
        names = glob(os.path.join(basedir, '*Rev*'))
        splitnames = [os.path.split(name) for name in names]
        self.subjects = [name.rstrip('Rev.mat') for base, name in splitnames]
        self.samplerate = samplerate

    def subject_name(self, subject):
        return str(subject) + 'Rev'

    def load_subject(self, subject):
        subject = str(subject)
        if subject == 'all':
            subjects = ('back', 'center', 'corner', 'ear') # we don't use anech
            hrtfsets = [self.load_subject(s) for s in subjects]
            hrtfset = hrtfsets[0]
            hrtfset.name = 'all'
            hrtfsets = hrtfsets[1:]
            c = hrtfset.coordinates
            for h in hrtfsets:
                hrtfset.data = hstack((hrtfset.data, h.data))
                c = hstack((c, h.coordinates))
            co = AzimElevDistDegrees.make(hrtfset.num_indices)
            for i, n in enumerate(co.names):
                co[n] = c[n]
            hrtfset.coordinates = co
            hrtfset.prepare()
            return hrtfset
        else:
            fname = os.path.join(self.basedir, subject + 'Rev')
            return InRoomHRTFSet(fname, samplerate=self.samplerate, name=self.subject_name(subject))

############# GERBIL HRTF DATABASE ##############################################
class GerbilHRTFSet(HRTFSet):
    def load(self, filename, samplerate=None, coordsys=None, name=None):
        # TODO: check samplerate
        if name is None:
            _, name = os.path.split(filename)
        self.name = name
        #load coordinates and data by reading the content of filename 
        names = glob(os.path.join(filename, 'IMPL*'))
        splitnames = [os.path.split(name) for name in names]
        self.azim = zeros(len(names) / 2 - 1, uint16)
        self.elev = zeros(len(names) / 2 - 1, int16)
        counter = 0
        for az in arange(-180, 180, 10):
            for el in arange(-40, 100, 10):
                filepath = os.path.join(filename, 'IMPL' + `az` + 'AZ' + `el` + 'EL')
                if os.path.exists(filepath + '_L.txt'):
                    self.azim[counter], self.elev[counter] = mod(az, 360), el
                    #read the hrtf
                    hrtf_left = loadtxt(filepath + '_L.txt')
                    hrtf_right = loadtxt(filepath + '_R.txt')
                    if counter == 0:
                        #initialize the hrtf database
                        # self.data has shape (num_ears=2, num_indices, hrir_length)
                        self.data = zeros((2, len(names) / 2 - 1, len(hrtf_left)))
                    self.data[:, counter, ] = vstack((hrtf_left, hrtf_right))
                    counter += 1

        coords = AzimElevDegrees.make(len(self.azim))
        coords['azim'] = self.azim
        coords['elev'] = self.elev
        if coordsys is not None:
            self.coordinates = coords.convert_to(coordsys)
        else:
            self.coordinates = coords

        self.samplerate = 97.65625 * kHz


class GerbilDatabase(HRTFDatabase):
    def __init__(self, basedir, samplerate=None):
        self.basedir = basedir
        names = glob(os.path.join(basedir, 'No*'))
        splitnames = [os.path.split(name) for name in names]

        self.subjects = [int(name[2:]) for base, name in splitnames]
        self.samplerate = samplerate

    def subject_name(self, subject):
        return 'GERBIL_' + str(subject)

    def load_subject(self, subject):
        subject = str(subject)
        fname = os.path.join(self.basedir, 'No' + subject)
        #fname = os.path.join(fname, 'IMPL')
        return GerbilHRTFSet(fname, samplerate=self.samplerate, name=self.subject_name(subject))

############# GUINEA_PIG HRTF DATABASE ##############################################
class GuineaPigHRTFSet(HRTFSet):
    def load(self, filename, samplerate=None, coordsys=None, name=None):
        # TODO: check samplerate
        if name is None:
            _, name = os.path.split(filename)
        self.name = name
        #load coordinates and data by reading the content of filename 
        names = glob(os.path.join(filename, 'gphrir*'))
        splitnames = [os.path.split(name) for name in names]
        self.azim = zeros(len(names), uint16)
        self.elev = zeros(len(names), int16)

        for j in range(len(names)):
            temp_name = splitnames[j][1].split('_')
            self.azim[j] = uint16(mod(int(temp_name[1]), 360))
            self.elev[j] = int16(int(temp_name[2][:-4]))#remove the .wav
            #read the hrtf
            temp_wav = read(names[j])
            hrtf_left = temp_wav[1][:, 0]
            hrtf_right = temp_wav[1][:, 1]
            if j == 0:
                #initialize the hrtf database
                # self.data has shape (num_ears=2, num_indices, hrir_length)
                self.data = zeros((2, len(names), len(hrtf_left)))
                self.samplerate = temp_wav[0] * Hz
            self.data[:, j, ] = vstack((hrtf_left, hrtf_right))


        coords = AzimElevDegrees.make(len(self.azim))
        coords['azim'] = self.azim
        coords['elev'] = self.elev
        if coordsys is not None:
            self.coordinates = coords.convert_to(coordsys)
        else:
            self.coordinates = coords


class GuineaPigDatabase(HRTFDatabase):
    def __init__(self, basedir, samplerate=None):
        self.basedir = basedir
        names = ''#glob(os.path.join(basedir, 'No*'))
        #splitnames = [os.path.split(name) for name in names]

        self.subjects = 0#[int(name[2:]) for base, name in splitnames]
        self.samplerate = samplerate

    def subject_name(self, subject):
        return 'GUINEA_PIG' + str(subject)

    def load_subject(self, subject):
        subject = str(subject)
        fname = self.basedir#os.path.join(self.basedir, 'No'+subject)
        #fname = os.path.join(fname, 'IMPL')
        return GuineaPigHRTFSet(fname, samplerate=self.samplerate, name=self.subject_name(subject))

### Mannequin database from Brian Katz:
class KatzHRTFSet(HRTFSet):
    def load(self, filename, samplerate=None, coordsys=None, name=None):
        # TODO: check samplerate
        if name is None:
            _, name = os.path.split(filename)
        self.name = name
        m = loadmat(filename, struct_as_record=True)
        if 'l_hrir_S' in m.keys():
            affix = '_hrir_S'
        else:
            affix = '_hrir_sim_S'
        l, r = m['l' + affix], m['r' + affix]
        self.azim = l['azim_v'][0][0][:, 0]
        self.elev = l['elev_v'][0][0][:, 0]
        l = l['content_m'][0][0]
        r = r['content_m'][0][0]
        coords = AzimElevDegrees.make(len(self.azim))
        coords['azim'] = self.azim
        coords['elev'] = self.elev
        if coordsys is not None:
            self.coordinates = coords.convert_to(coordsys)
        else:
            self.coordinates = coords
        # self.data has shape (num_ears=2, num_indices, hrir_length)
        self.data = vstack((reshape(l, (1,) + l.shape), reshape(r, (1,) + r.shape)))
        self.samplerate = 44.1 * kHz


class KatzDatabase(HRTFDatabase):
    def __init__(self, basedir, samplerate=None):
        self.basedir = basedir + '\\Measured mannequin\\'
        names = glob(os.path.join(self.basedir, '*IRC*'))
        splitnames = [os.path.split(name) for name in names]
        self.subjects = [name.replace('.mat', '').strip('IRC_1518') for base, name in splitnames]
        self.samplerate = 44.1 * kHz

    def subject_name(self, subject):
        return str(subject)

    def load_subject(self, subject):
        subject = str(subject)
        fname = os.path.join(self.basedir, 'IRC_1518_' + subject + '.mat')
        return KatzHRTFSet(fname, samplerate=self.samplerate, name=self.subject_name(subject))

### EXAMPLES
if __name__ == '__main__':

    choice = 'Guinea Pig'#IRCAM,Gerbil, Guinea Pig, In Room, Brian Katz
    hrtf_locations = [
            r'D:\HRTF\\' + choice,
            r'/home/bertrand/Data/Measurements/HRTF/' + choice,
            r'C:\Documents and Settings\dan\My Documents\Programming\\' + choice
            ]
    found = 0
    for path in hrtf_locations:
        if os.path.exists(path):
            found = 1
            break
    if found == 0:
        raise IOError('Cannot find IRCAM HRTF location, add to ircam_locations')
    else:
        if choice == 'IRCAM':

            ircam = IRCAM_LISTEN(path)
            h = ircam.load_subject(1002)
            #h = h.subset(lambda azim,elev:azim==90 and elev==90)
            h = h.subset(lambda azim, elev:(azim, elev) in ((90, 60), (60, 30)))
            subplot(211)
            plot(h.hrtf[0].left)
            plot(h.hrtf[0].right)
            title(choice + " Coordinates : " + `h.coordinates[0]`)
            subplot(212)
        ##    c = h.coordinates.convert_to(AzimElev)
        ##    plot(h.coordinates['azim'], h.coordinates['elev'], 'o')
        ##    from enthought.mayavi import mlab
        ##    c = h.coordinates.convert_to(CartesianCoordinates)
        ##    mlab.points3d(c['x'], c['y'], c['z'])
        ##    mlab.show()
            c = h.coordinates
        #    c2 = AzimElevDegrees.convert_from(c.convert_to(CartesianCoordinates))
        #    print amax(c['elev']-c2['elev'])
            plot(c['azim'], c['elev'], 'o')
            show()
        elif choice == 'Gerbil':

            gerbil = GerbilDatabase(path)
            h = gerbil.load_subject(521)
            #h = h.subset(lambda azim,elev:azim==90 and elev==90)
            #h = h.subset(lambda azim,elev:(azim in array([60,90])) & (elev in array([40,50])) )
            h2 = h.subset(lambda azim, elev:([azim, elev] in [[80, 60], [90, 30]]))
            subplot(211)
            plot(h.hrtf[400].left)
            plot(h.hrtf[400].right)
            title(choice + " Coordinates : " + `h.coordinates[400]`)
            subplot(212)
            c = h.coordinates
            c2 = AzimElevDegrees.convert_from(c.convert_to(CartesianCoordinates))
            print amax(c['elev'] - c2['elev'])
            plot(c['azim'], c['elev'], 'o')
            show()
        elif choice == 'In Room':
            in_room = InRoomDatabase(path)
            h = in_room.load_subject('anech')
            #h = h.subset(lambda azim,elev:azim==90 and elev==90)
            #h = h.subset(lambda azim,elev:(azim==90) & (elev==40) )
            subplot(211)
            plot(h.hrtf[0].left)
            plot(h.hrtf[0].right)
            title(choice + " Coordinates : " + `h.coordinates[0]`)
            subplot(212)
            c = h.coordinates
        #        c2 = AzimElevDegrees.convert_from(c.convert_to(CartesianCoordinates))
        #        print amax(c['elev']-c2['elev'])
            plot(c['azim'], c['elev'], 'o')
            show()
        elif choice == 'Guinea Pig':

            guinea_pig = GuineaPigDatabase(path)
            h = guinea_pig.load_subject(0)
            #h = h.subset(lambda azim,elev:azim==90 and elev==90)
            #h = h.subset(lambda azim,elev:(azim in array([60,90])) & (elev in array([40,50])) )
            h = h.subset(lambda azim, elev:([azim, elev] in [[40, 10], [90, 30]]))
            subplot(211)
            plot(h.hrtf[0].left)
            plot(h.hrtf[0].right)
            title(choice + " Coordinates : " + `h.coordinates[0]`)
            subplot(212)
            c = h.coordinates
            c2 = AzimElevDegrees.convert_from(c.convert_to(CartesianCoordinates))
            print amax(c['elev'] - c2['elev'])
            plot(c['azim'], c['elev'], 'o')
            show()
        elif choice == 'Brian Katz':

            katz = KatzDatabase(path)
            h = katz.load_subject('sim')
            #h = h.subset(lambda azim,elev:azim==90 and elev==90)
            h = h.subset(lambda azim, elev:[azim, elev] in [[20, 20]])
            subplot(211)
            plot(h.hrtf[0].left)
            plot(h.hrtf[0].right)
            title(choice + " Coordinates : " + `h.coordinates[0]`)
            subplot(212)
        ##    c = h.coordinates.convert_to(AzimElev)
        ##    plot(h.coordinates['azim'], h.coordinates['elev'], 'o')
        ##    from enthought.mayavi import mlab
        ##    c = h.coordinates.convert_to(CartesianCoordinates)
        ##    mlab.points3d(c['x'], c['y'], c['z'])
        ##    mlab.show()
            c = h.coordinates
        #    c2 = AzimElevDegrees.convert_from(c.convert_to(CartesianCoordinates))
        #    print amax(c['elev']-c2['elev'])
            plot(c['azim'], c['elev'], 'o')
            show()
