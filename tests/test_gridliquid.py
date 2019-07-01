from unittest import TestCase
from phi.flow import *


class TestGridLiquid(TestCase):
    def test_direct_liquid(self):
        liquid = GridLiquid(Domain([16, 16]))
        assert liquid.default_physics() == GRIDLIQUID
        liquid2 = GRIDLIQUID.step(liquid)
        assert(liquid2.age == 1.0)
        assert(liquid.age == 0.0)
        assert(liquid2.trajectorykey == liquid.trajectorykey)

    def test_gridliquid(self):
        world = World()
        world.batch_size = 2
        liquid = world.GridLiquid(Domain([16, 16]))
        inflow = world.Inflow(Sphere((8, 8), radius=4))
        world.step()
        world.step(liquid)
        self.assertAlmostEqual(world.state.age, 2.0)
        self.assertAlmostEqual(liquid.age, 2.0)
        self.assertAlmostEqual(inflow.age, 1.0)
        self.assertEqual(liquid._batch_size, 2)

    def test_gridliquid_initializers(self):
        def typetest(liquid):
            self.assertIsInstance(liquid, GridLiquid)
            self.assertIsInstance(liquid.velocity, StaggeredGrid)
            np.testing.assert_equal(liquid.density.shape, [1,4,4,1])
            np.testing.assert_equal(liquid.velocity.shape, [1,5,5,2])
        typetest(GridLiquid(Domain([4, 4]), density=0.0, velocity=0.0))
        typetest(GridLiquid(Domain([4, 4]), density=1.0, velocity=1.0))
        typetest(GridLiquid(Domain([4, 4]), density=zeros, velocity=zeros))
        typetest(GridLiquid(Domain([4, 4]), density=randn(), velocity=randn()))
        typetest(GridLiquid(Domain([4, 4]), density=np.zeros([1, 4, 4, 1]), velocity=StaggeredGrid(np.zeros([1, 5, 5, 2]))))
        typetest(GridLiquid(Domain([4, 4]), density=np.zeros([1, 4, 4, 1]), velocity=np.zeros([1, 5, 5, 2])))
        typetest(GridLiquid(Domain([4, 4])))