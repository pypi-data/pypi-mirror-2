""" Test database backends """

import os,sys, pdb
from numpy.testing import TestCase, assert_array_equal, assert_equal
from pymc.examples import DisasterModel
from pymc import MCMC
import pymc, pymc.database

import numpy as np
import nose
import warnings
warnings.simplefilter('ignore', UserWarning)

# TestCase = object

testdir = 'testresults'
try:
    os.mkdir(testdir)
except:
    pass

class test_backend_attribution(TestCase):
    def test_raise(self):
        self.assertRaises(AttributeError, MCMC, DisasterModel, 'heysugar')
    def test_import(self):
        self.assertRaises(ImportError, MCMC, DisasterModel, '__test_import__')


class TestBase(TestCase):
    """Test features that should be common to all databases."""
    @classmethod
    def setUpClass(self):
        self.S = pymc.MCMC(DisasterModel, db='base')

    def test_init(self):
        assert hasattr(self.S.db, '__Trace__')
        assert hasattr(self.S.db, '__name__')

    @classmethod
    def tearDownClass(self):
        try:
            self.S.db.close()
        except:
            pass

    def NDstoch(self):
        nd = pymc.Normal('nd', value=np.ones((2,2,))*.5, mu=np.ones((2,2)), tau=1)
        return nd

class TestRam(TestBase):
    name = 'ram'
    @classmethod
    def setUpClass(self):
        self.S = pymc.MCMC(DisasterModel, db='ram')
        self.S.use_step_method(pymc.Metropolis, self.S.e, tally=True)

    def test_simple_sample(self):

        self.S.sample(50,25,5)

        assert_array_equal(self.S.trace('e')[:].shape, (5,))
        assert_array_equal(self.S.trace('e', chain=0)[:].shape, (5,))
        assert_array_equal(self.S.trace('e', chain=None)[:].shape, (5,))

        assert_equal(self.S.trace('e').length(), 5)
        assert_equal(self.S.trace('e').length(chain=0), 5)
        assert_equal(self.S.trace('e').length(chain=None), 5)

        self.S.sample(10,0,1)

        assert_array_equal(self.S.trace('e')[:].shape, (10,))
        assert_array_equal(self.S.trace('e', chain=1)[:].shape, (10,))
        assert_array_equal(self.S.trace('e', chain=None)[:].shape, (15,))

        assert_equal(self.S.trace('e').length(), 10)
        assert_equal(self.S.trace('e').length(chain=1), 10)
        assert_equal(self.S.trace('e').length(chain=None), 15)

        assert_equal(self.S.trace('e')[:].__class__,  np.ndarray)

        # Test __getitem__
        assert_equal(self.S.trace('e').gettrace(slicing=slice(1,2)), self.S.e.trace[1])

        # Test __getslice__
        assert_array_equal(self.S.trace('e').gettrace(thin=2), self.S.e.trace[::2])

        # Test Sampler trace method
        assert_array_equal(self.S.trace('e')[:].shape, (10,))
        assert_array_equal(self.S.trace('e', chain=0)[:].shape, (5,))
        assert_array_equal(self.S.trace('e', chain=1)[:].shape, (10,))
        assert_array_equal(self.S.trace('e', chain=1)[::2].shape, (5,))
        assert_array_equal(self.S.trace('e', chain=1)[1::].shape, (9,))
        assert_array_equal(self.S.trace('e', chain=1)[0],  self.S.trace('e', chain=1)[:][0])
        assert_array_equal(self.S.trace('e', chain=None)[:].shape, (15,))

        # Test internal state
        t1 = self.S.trace('e', 0)
        t2 = self.S.trace('e', 1)
        assert_equal(t1._chain, 0)


        # Test remember
        s1 = np.shape(self.S.e.value)
        self.S.remember(0,0)
        s2 = np.shape(self.S.e.value)
        assert_equal(s1, s2)


        self.S.db.close()

class TestPickle(TestRam):
    name = 'pickle'
    @classmethod
    def setUpClass(self):
        self.S = pymc.MCMC(DisasterModel,
                           db='pickle',
                           dbname=os.path.join(testdir, 'Disaster.pickle'),
                           dbmode='w')
        self.S.use_step_method(pymc.Metropolis, self.S.e, tally=True)

    def load(self):
        return pymc.database.pickle.load(os.path.join(testdir, 'Disaster.pickle'))

    def test_xload(self):
        db = self.load()
        assert_array_equal(db.trace('e', chain=0)[:].shape, (5,))
        assert_array_equal(db.trace('e', chain=1)[:].shape, (10,))
        assert_array_equal(db.trace('e', chain=-1)[:].shape, (10,))
        assert_array_equal(db.trace('e', chain=None)[:].shape, (15,))
        db.close()

    def test_yconnect_and_sample(self):
        db = self.load()
        S = pymc.MCMC(DisasterModel, db=db)
        S.use_step_method(pymc.Metropolis, S.e, tally=True)
        S.sample(5)
        assert_array_equal(db.trace('e', chain=-1)[:].shape, (5,))
        assert_array_equal(db.trace('e', chain=None)[:].shape, (20,))
        db.close()

    def test_yrestore_state(self):
        db = self.load()
        S = pymc.MCMC(DisasterModel, db=db)
        S.sample(10)
        sm = S.step_methods.pop()
        assert_equal(sm.accepted+sm.rejected, 75)

    def test_nd(self):
        M = MCMC([self.NDstoch()], db=self.name, dbname=os.path.join(testdir, 'ND.'+self.name), dbmode='w')
        M.sample(10)
        a = M.trace('nd')[:]
        assert_equal(a.shape, (10,2,2))
        db = getattr(pymc.database, self.name).load(os.path.join(testdir, 'ND.'+self.name))
        assert_equal(db.trace('nd')[:], a)

class TestTxt(TestPickle):
    name = 'txt'
    @classmethod
    def setUpClass(self):

        self.S = pymc.MCMC(DisasterModel,
                           db='txt',
                           dbname=os.path.join(testdir, 'Disaster.txt'),
                           dbmode='w')

    def load(self):
        return pymc.database.txt.load(os.path.join(testdir, 'Disaster.txt'))


class TestSqlite(TestPickle):
    name = 'sqlite'
    @classmethod
    def setUpClass(self):
        if 'sqlite' not in dir(pymc.database):
            raise nose.SkipTest
        if os.path.exists('Disaster.sqlite'):
           os.remove('Disaster.sqlite')
        self.S = pymc.MCMC(DisasterModel,
                           db='sqlite',
                           dbname=os.path.join(testdir, 'Disaster.sqlite'),
                           dbmode='w')

    def load(self):
        return pymc.database.sqlite.load(os.path.join(testdir, 'Disaster.sqlite'))

    def test_yrestore_state(self):
        raise nose.SkipTest, "Not implemented."
"""
    TODO Create more reliable MySQL backend test
"""
# class TestMySQL(TestPickle):
#     @classmethod
#     def setUpClass(self):
#         if 'mysql' not in dir(pymc.database):
#             raise nose.SkipTest
#         self.S = pymc.MCMC(DisasterModel,
#                            db='mysql',
#                            dbname='pymc_test',
#                            dbuser='pymc',
#                            dbpass='bayesian',
#                            dbhost='www.freesql.org',
#                            dbmode='w')
#
#     def load(self):
#         return pymc.database.mysql.load(dbname='pymc_test',
#                                         dbuser='pymc',
#                                         dbpass='bayesian',
#                                         dbhost='www.freesql.org')
#
#     def test_yrestore_state(self):
#         raise nose.SkipTest, "Not implemented."



class TestHDF5(TestPickle):
    name = 'hdf5'
    @classmethod
    def setUpClass(self):
        if 'hdf5' not in dir(pymc.database):
            raise nose.SkipTest
        self.S = pymc.MCMC(DisasterModel,
                           db='hdf5',
                           dbname=os.path.join(testdir, 'Disaster.hdf5'),
                           dbmode='w')
        self.S.use_step_method(pymc.Metropolis, self.S.e, tally=True)

    def load(self):
        return pymc.database.hdf5.load(os.path.join(testdir, 'Disaster.hdf5'))

    def test_xdata_attributes(self):
        db = self.load()
        assert_array_equal(db.D, DisasterModel.disasters_array)
        db.close()
        del db

    def test_xattribute_assignement(self):
        arr = np.array([[1,2],[3,4]])
        db = self.load()
        db.add_attr('some_list', [1,2,3])
        db.add_attr('some_dict', {'a':5})
        db.add_attr('some_array', arr, array=True)
        assert_array_equal(db.some_list, [1,2,3])
        assert_equal(db.some_dict['a'], 5)
        assert_array_equal(db.some_array.read(), arr)
        db.close()
        del db

        db = self.load()
        assert_array_equal(db.some_list, [1,2,3])
        assert_equal(db.some_dict['a'], 5)
        assert_array_equal(db.some_array, arr)
        db.close()
        del db

    def test_xhdf5_col(self):
        import tables
        db = self.load()
        col = db.e.hdf5_col()
        assert col.__class__ == tables.table.Column
        assert_equal(len(col), len(db.e()))
        db.close()
        del db

    def test_zcompression(self):
        db = pymc.database.hdf5.Database(dbname=os.path.join(testdir, 'DisasterModelCompressed.hdf5'),
                                         dbmode='w',
                                         dbcomplevel=5)
        S = MCMC(DisasterModel, db=db)
        S.sample(45,10,1)
        assert_array_equal(S.trace('e')[:].shape, (35,))
        S.db.close()
        db.close()
        del S



class testHDF5Objects(TestCase):
    @classmethod
    def setUpClass(self):
        if 'hdf5' not in dir(pymc.database):
            raise nose.SkipTest
        import objectmodel
        self.S = pymc.MCMC(objectmodel,
                           db='hdf5',
                           dbname=os.path.join(testdir, 'Objects.hdf5'),
                           dbmode='w')

    def load(self):
        return pymc.database.hdf5.load(os.path.join(testdir, 'Objects.hdf5'))

    def test_simple_sample(self):
        self.S.sample(50, 25, 5)

        assert_array_equal(self.S.trace('B')[:].shape, (5,))
        assert_array_equal(self.S.trace('K')[:].shape, (5,))
        assert_array_equal(self.S.trace('K', chain=0)[:].shape, (5,))
        assert_array_equal(self.S.trace('K', chain=None)[:].shape, (5,))

        assert_equal(self.S.trace('K').length(), 5)
        assert_equal(self.S.trace('K').length(chain=0), 5)
        assert_equal(self.S.trace('K').length(chain=None), 5)


        self.S.sample(10)

        assert_array_equal(self.S.trace('K')[:].shape, (10,))
        assert_array_equal(self.S.trace('K', chain=1)[:].shape, (10,))
        assert_array_equal(self.S.trace('K', chain=None)[:].shape, (15,))

        assert_equal(self.S.trace('K').length(), 10)
        assert_equal(self.S.trace('K').length(chain=1), 10)
        assert_equal(self.S.trace('K').length(chain=None), 15)

        self.S.db.close()

    def test_xload(self):
        db = self.load()
        assert_array_equal(db.B().shape, (10,))
        assert_array_equal(db.K().shape, (10,))
        assert_array_equal(db.K(chain=0).shape, (5,))
        assert_array_equal(db.K(chain=None).shape, (15,))
        db.close()

    def test_yconnect_and_sample(self):
        db = self.load()
        import objectmodel
        S = pymc.MCMC(objectmodel, db=db)
        S.sample(5)
        assert_array_equal(db.K(chain=0).shape, (5,))
        assert_array_equal(db.K(chain=1).shape, (10,))
        assert_array_equal(db.K(chain=2).shape, (5,))
        assert_array_equal(db.K(chain=-1).shape, (5,))
        assert_array_equal(db.K(chain=None).shape, (20,))
        db.close()



def test_identical_object_names():
    A = pymc.Uniform('a', 0, 10)
    B = pymc.Uniform('a', 0, 10)
    try:
        M = MCMC([A,B])
    except ValueError:
        pass


def test_regression_155():
    """thin > iter"""
    M = MCMC(DisasterModel, db='ram')
    M.sample(10,0,100)


def test_interactive():
    if 'sqlite' not in dir(pymc.database):
        raise nose.SkipTest
    M=MCMC(DisasterModel,db='sqlite',
           dbname=os.path.join(testdir, 'interactiveDisaster.sqlite'),
           dbmode='w')
    M.isample(10, out=open('testresults/interactivesqlite.log', 'w'))

# def test_getitem():
#    class tmp(database.base.Database):
#        def gettrace(self, burn=0, thin=1, chain=-1, slicing=None):
#            return


if __name__ == '__main__':
    
    warnings.simplefilter('ignore', DeprecationWarning)
    C =nose.config.Config(verbosity=3)
    nose.runmodule(config=C)
    try:
        S.db.close()
    except:
        pass
