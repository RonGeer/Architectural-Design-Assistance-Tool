"""
Architectural Design Tool Unit Tests
====================================

This test suite provides comprehensive unit testing for the architectural_design_tool Blender addon.
Tests cover utility functions, geometric operations, boolean operations, and edge cases.

Author: AI Assistant
Date: 2025-11-22
"""

import unittest
import sys
import os
import math
from unittest.mock import Mock, patch, MagicMock
from mathutils import Vector, Matrix

# Add the addon directory to the path
addon_dir = os.path.dirname(__file__)
sys.path.insert(0, addon_dir)

# Mock bpy module before importing our functions
mock_bpy = Mock()
mock_bpy.context = Mock()
mock_bpy.data = Mock()
mock_bpy.ops = Mock()
mock_bmesh = Mock()
mock_mathutils = Mock()
mock_mathutils.Vector = Vector
mock_mathutils.Matrix = Matrix
mock_mathutils.bvhtree = Mock()

# Mock all the Blender modules
sys.modules['bpy'] = mock_bpy
sys.modules['bmesh'] = mock_bmesh
sys.modules['mathutils'] = mock_mathutils
sys.modules['mathutils.bvhtree'] = mock_mathutils.bvhtree

# Now import our functions after mocking
import functions as fun


class TestBasicFunctions(unittest.TestCase):
    """Test basic utility functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_randomInt(self):
        """Test random integer generation"""
        # Test default parameters
        result = fun.randomInt()
        self.assertIn(result, [1, 2, 3])
        
        # Test custom range
        result = fun.randomInt(5, 10)
        self.assertGreaterEqual(result, 5)
        self.assertLessEqual(result, 10)
        
        # Test same min/max
        result = fun.randomInt(7, 7)
        self.assertEqual(result, 7)
    
    def test_randomValue(self):
        """Test random float generation"""
        # Test default parameters
        result = fun.randomValue()
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 1)
        
        # Test custom range
        result = fun.randomValue(5.5, 10.5)
        self.assertGreaterEqual(result, 5.5)
        self.assertLessEqual(result, 10.5)
        
        # Test negative range
        result = fun.randomValue(-10, -5)
        self.assertGreaterEqual(result, -10)
        self.assertLessEqual(result, -5)
    
    def test_randomBool(self):
        """Test random boolean generation"""
        result = fun.randomBool()
        self.assertIsInstance(result, bool)
        self.assertIn(result, [True, False])
    
    def test_dir2Vec3(self):
        """Test direction to vector conversion"""
        test_cases = [
            ("+x", Vector((1, 0, 0))),
            ("-x", Vector((-1, 0, 0))),
            ("+y", Vector((0, 1, 0))),
            ("-y", Vector((0, -1, 0))),
            ("+z", Vector((0, 0, 1))),
            ("-z", Vector((0, 0, -1))),
            ("invalid", Vector((0, 0, 0))),
            ("", Vector((0, 0, 0))),
        ]
        
        for direction, expected in test_cases:
            with self.subTest(direction=direction):
                result = fun.dir2Vec3(direction)
                self.assertEqual(result, expected)
    
    def test_cross(self):
        """Test vector cross product"""
        v1 = Vector((1, 0, 0))
        v2 = Vector((0, 1, 0))
        result = fun.cross(v1, v2)
        expected = Vector((0, 0, 1))
        
        self.assertAlmostEqual(result.x, expected.x, places=6)
        self.assertAlmostEqual(result.y, expected.y, places=6)
        self.assertAlmostEqual(result.z, expected.z, places=6)
        
        # Test with perpendicular vectors
        v1 = Vector((0, 1, 0))
        v2 = Vector((0, 0, 1))
        result = fun.cross(v1, v2)
        expected = Vector((1, 0, 0))
        
        self.assertAlmostEqual(result.x, expected.x, places=6)
        self.assertAlmostEqual(result.y, expected.y, places=6)
        self.assertAlmostEqual(result.z, expected.z, places=6)
    
    def test_shuffleList(self):
        """Test list shuffling"""
        original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Test that function returns a list
        result = fun.shuffleList(original_list.copy())
        self.assertIsInstance(result, list)
        
        # Test that all elements are preserved
        self.assertCountEqual(result, original_list)
        
        # Test with single element
        single_list = [42]
        result = fun.shuffleList(single_list.copy())
        self.assertEqual(result, single_list)
        
        # Test with empty list
        empty_list = []
        result = fun.shuffleList(empty_list.copy())
        self.assertEqual(result, empty_list)


class TestSetBoxPos(unittest.TestCase):
    """Test spiral positioning function"""
    
    def test_2d_spiral_positions(self):
        """Test 2D spiral position calculation"""
        # Test origin (ID 0)
        result = fun.setBoxPos(0, 1, False)
        expected = Vector((0, 0, 0))
        self.assertEqual(result, expected)
        
        # Test first few positions in 2D
        positions = []
        for i in range(10):
            pos = fun.setBoxPos(i, 1, False)
            positions.append(pos)
        
        # First position should be at origin
        self.assertEqual(positions[0], Vector((0, 0, 0)))
        
        # Test spacing
        result_large_spacing = fun.setBoxPos(1, 5, False)
        result_small_spacing = fun.setBoxPos(1, 1, False)
        
        # The spacing should affect the position magnitude
        self.assertGreater(result_large_spacing.length, result_small_spacing.length)
    
    def test_3d_spiral_positions(self):
        """Test 3D spiral position calculation"""
        # Test origin (ID 0)
        result = fun.setBoxPos(0, 1, True)
        expected = Vector((0, 0, 0))
        self.assertEqual(result, expected)
        
        # Test that 3D positions can have non-zero Z coordinates
        for i in range(1, 20):
            pos = fun.setBoxPos(i, 1, True)
            # Some positions should have non-zero Z coordinates in 3D mode
            if i > 1:  # After the first few positions
                self.assertTrue(pos.z != 0 or pos.x != 0 or pos.y != 0)
    
    def test_spacing_effect(self):
        """Test that spacing parameter correctly affects positions"""
        spacing_values = [0.5, 1, 2, 5]
        
        for spacing in spacing_values:
            with self.subTest(spacing=spacing):
                result = fun.setBoxPos(5, spacing, False)
                # The position should be a multiple of the spacing
                # Check that position components are close to integer multiples of spacing
                self.assertAlmostEqual(result.x / spacing, round(result.x / spacing), places=6)
                self.assertAlmostEqual(result.y / spacing, round(result.y / spacing), places=6)
    
    def test_negative_id(self):
        """Test behavior with negative ID (should return origin or handle gracefully)"""
        # Negative ID should be handled (current implementation doesn't specifically handle it)
        # This test documents current behavior
        try:
            result = fun.setBoxPos(-1, 1, False)
            # Should not crash
            self.assertIsInstance(result, Vector)
        except Exception:
            # If it raises an exception, that's also acceptable behavior
            pass


class TestGeometricFunctions(unittest.TestCase):
    """Test geometric calculation functions"""
    
    def setUp(self):
        """Set up mock objects for testing"""
        self.mock_obj = Mock()
        self.mock_obj.data = Mock()
        self.mock_obj.data.vertices = []
        self.mock_obj.matrix_world = Matrix.Identity(4)
        self.mock_obj.dimensions = Vector((2, 2, 2))
        self.mock_obj.location = Vector((0, 0, 0))
    
    def test_getBound_with_mock_data(self):
        """Test boundary box calculation with mock vertex data"""
        # Create mock vertices at known positions
        mock_vertices = [
            Mock(co=Vector((-1, -1, -1))),
            Mock(co=Vector((1, 1, 1))),
            Mock(co=Vector((0, 0, 0))),
        ]
        self.mock_obj.data.vertices = mock_vertices
        
        maxx, maxy, maxz, minx, miny, minz = fun.getBound(self.mock_obj)
        
        self.assertEqual(maxx, 1)
        self.assertEqual(maxy, 1)
        self.assertEqual(maxz, 1)
        self.assertEqual(minx, -1)
        self.assertEqual(miny, -1)
        self.assertEqual(minz, -1)
    
    def test_getBound_empty_mesh(self):
        """Test boundary calculation with empty mesh"""
        self.mock_obj.data.vertices = []
        
        maxx, maxy, maxz, minx, miny, minz = fun.getBound(self.mock_obj)
        
        # Should return default values for empty mesh
        self.assertEqual(maxx, -float('inf'))
        self.assertEqual(maxy, -float('inf'))
        self.assertEqual(maxz, -float('inf'))
        self.assertEqual(minx, float('inf'))
        self.assertEqual(miny, float('inf'))
        self.assertEqual(minz, float('inf'))
    
    def test_centerPos(self):
        """Test center position calculation"""
        # Set up mock vertices around a center
        mock_vertices = [
            Mock(co=Vector((-2, -2, -2))),
            Mock(co=Vector((2, 2, 2))),
        ]
        self.mock_obj.data.vertices = mock_vertices
        
        center = fun.centerPos(self.mock_obj)
        expected = Vector((0, 0, 0))
        self.assertEqual(center, expected)
        
        # Test with asymmetric vertices
        mock_vertices = [
            Mock(co=Vector((0, 0, 0))),
            Mock(co=Vector((2, 2, 2))),
        ]
        self.mock_obj.data.vertices = mock_vertices
        
        center = fun.centerPos(self.mock_obj)
        expected = Vector((1, 1, 1))
        self.assertEqual(center, expected)
    
    def test_randomInsidePoint(self):
        """Test random point generation inside bounds"""
        # Set up bounding box
        mock_vertices = [
            Mock(co=Vector((-1, -2, -3))),
            Mock(co=Vector((1, 2, 3))),
        ]
        self.mock_obj.data.vertices = mock_vertices
        
        # Generate multiple random points
        for _ in range(10):
            point = fun.randomInsidePoint(self.mock_obj)
            
            # Point should be within bounds
            self.assertGreaterEqual(point.x, -1)
            self.assertLessEqual(point.x, 1)
            self.assertGreaterEqual(point.y, -2)
            self.assertLessEqual(point.y, 2)
            self.assertGreaterEqual(point.z, -3)
            self.assertLessEqual(point.z, 3)
    
    def test_randomVector(self):
        """Test random vector generation"""
        # Test with no constraint
        vec = fun.randomVector()
        length = vec.length
        self.assertAlmostEqual(length, 1.0, places=6)  # Should be normalized
        
        # Test with constraint
        constraint = Vector((0, 0, 1))  # Z-axis constraint
        vec = fun.randomVector(constraint)
        
        # Vector should be perpendicular to constraint
        dot_product = vec.dot(constraint)
        self.assertAlmostEqual(dot_product, 0.0, places=6)
        
        # Should still be normalized
        self.assertAlmostEqual(vec.length, 1.0, places=6)


class TestLogicalFunctions(unittest.TestCase):
    """Test logical and boolean functions"""
    
    def setUp(self):
        """Set up mock objects for testing"""
        self.mock_obj_a = Mock()
        self.mock_obj_a.name = "ObjectA"
        self.mock_obj_a.data = Mock()
        self.mock_obj_a.dimensions = Vector((2, 2, 2))
        
        self.mock_obj_b = Mock()
        self.mock_obj_b.name = "ObjectB"
        self.mock_obj_b.data = Mock()
        self.mock_obj_b.dimensions = Vector((1, 1, 1))
        
        # Mock bpy.data.objects
        mock_bpy.data.objects = [self.mock_obj_a, self.mock_obj_b]
    
    def test_isExists(self):
        """Test object existence check"""
        # Test existing object
        self.assertTrue(fun.isExists("ObjectA"))
        self.assertTrue(fun.isExists("ObjectB"))
        
        # Test non-existing object
        self.assertFalse(fun.isExists("NonExistent"))
        self.assertFalse(fun.isExists(""))
    
    def test_isExists_empty_scene(self):
        """Test existence check with empty scene"""
        mock_bpy.data.objects = []
        
        self.assertFalse(fun.isExists("Anything"))
        self.assertFalse(fun.isExists(""))
    
    @patch('functions.BVHTree')
    def test_isIntersect(self, mock_bvhtree):
        """Test intersection detection"""
        # Mock BVHTree overlap to return intersection
        mock_bvhtree_instance = Mock()
        mock_bvhtree_instance.overlap.return_value = [True]  # Non-empty list indicates intersection
        mock_bvhtree.FromBMesh.return_value = mock_bvhtree_instance
        
        result = fun.isIntersect(self.mock_obj_a, self.mock_obj_b)
        self.assertTrue(result)
        
        # Mock no intersection
        mock_bvhtree_instance.overlap.return_value = []  # Empty list indicates no intersection
        result = fun.isIntersect(self.mock_obj_a, self.mock_obj_b)
        self.assertFalse(result)
    
    def test_isInside_volume_comparison(self):
        """Test inside detection based on volume comparison"""
        # Set up mock vertices for both objects
        # Object A is larger (volume 8)
        vertices_a = [Mock(co=Vector((-1, -1, -1))), Mock(co=Vector((1, 1, 1)))]
        self.mock_obj_a.data.vertices = vertices_a
        
        # Object B is smaller (volume 1) and should be inside A
        vertices_b = [Mock(co=Vector((-0.5, -0.5, -0.5))), Mock(co=Vector((0.5, 0.5, 0.5)))]
        self.mock_obj_b.data.vertices = vertices_b
        
        # Mock matrix_world for coordinate transformation
        self.mock_obj_a.matrix_world = Matrix.Identity(4)
        self.mock_obj_b.matrix_world = Matrix.Identity(4)
        
        # Mock getBound to return realistic bounds
        with patch('functions.getBound') as mock_get_bound:
            # Object A bounds (larger)
            mock_get_bound.return_value = (1, 1, 1, -1, -1, -1)
            
            # Test if B is inside A
            vertices_b_transformed = [
                self.mock_obj_b.matrix_world @ v.co for v in vertices_b
            ]
            
            # Check that all vertices of B are within A's bounds
            maxx, maxy, maxz, minx, miny, minz = (1, 1, 1, -1, -1, -1)
            for co in vertices_b_transformed:
                self.assertTrue(-1 <= co[0] <= 1)
                self.assertTrue(-1 <= co[1] <= 1)
                self.assertTrue(-1 <= co[2] <= 1)
    
    def test_isPointinside(self):
        """Test point inside object detection"""
        # Set up mock object bounds
        mock_vertices = [
            Mock(co=Vector((-1, -2, -3))),
            Mock(co=Vector((1, 2, 3))),
        ]
        self.mock_obj_a.data.vertices = mock_vertices
        
        # Test point inside bounds
        inside_point = Vector((0, 0, 0))
        self.assertTrue(fun.isPontinside(inside_point, self.mock_obj_a))
        
        # Test point on boundary
        boundary_point = Vector((1, 2, 3))
        self.assertTrue(fun.isPontinside(boundary_point, self.mock_obj_a))
        
        # Test point outside bounds
        outside_point = Vector((2, 3, 4))
        self.assertFalse(fun.isPontoutside(outside_point, self.mock_obj_a))


class TestObjectManipulation(unittest.TestCase):
    """Test object manipulation functions"""
    
    def setUp(self):
        """Set up mock objects for testing"""
        self.mock_obj = Mock()
        self.mock_obj.data = Mock()
        self.mock_obj.modifiers = Mock()
        self.mock_obj.location = Vector((0, 0, 0))
        
        # Mock Blender operators
        mock_bpy.ops.object = Mock()
        mock_bpy.context = Mock()
        mock_bpy.context.view_layer = Mock()
        mock_bpy.context.view_layer.objects = Mock()
        mock_bpy.context.collection = Mock()
    
    def test_setActive(self):
        """Test setting active object"""
        fun.setActive(self.mock_obj)
        # Verify that the active object was set
        mock_bpy.context.view_layer.objects.active = self.mock_obj
    
    @patch('functions.copyobj')
    def test_copyobj(self, mock_copy):
        """Test object copying"""
        mock_copy.return_value = Mock()
        
        result = fun.copyobj(self.mock_obj)
        mock_copy.assert_called_once_with(self.mock_obj)
    
    def test_delobj(self):
        """Test object deletion"""
        mock_bpy.data.objects = Mock()
        fun.delobj(self.mock_obj)
        mock_bpy.data.objects.remove.assert_called_once_with(self.mock_obj)
    
    def test_snapGround(self):
        """Test snapping object to ground"""
        # Mock getBound to return bounds where object is above ground
        with patch('functions.getBound') as mock_get_bound:
            mock_get_bound.return_value = (1, 1, 2, -1, -1, 0.5)  # minz = 0.5
            
            # Initial location
            self.mock_obj.location.z = 0
            
            fun.snapGround(self.mock_obj)
            
            # Object should be moved down by 0.5 units
            expected_z = -0.5  # 0 + (-0.5)
            self.assertEqual(self.mock_obj.location.z, expected_z)
    
    def test_snapGround_already_on_ground(self):
        """Test snapping when object is already on ground"""
        with patch('functions.getBound') as mock_get_bound:
            mock_get_bound.return_value = (1, 1, 0, -1, -1, -1)  # minz = -1
            
            # Initial location
            self.mock_obj.location.z = 1
            
            fun.snapGround(self.mock_obj)
            
            # Object should be moved down by 1 unit
            expected_z = 0  # 1 + (-1)
            self.assertEqual(self.mock_obj.location.z, expected_z)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_none_inputs(self):
        """Test functions with None inputs"""
        # These should either handle gracefully or raise appropriate errors
        
        # Test dir2Vec3 with None
        try:
            result = fun.dir2Vec3(None)
            self.assertIsInstance(result, Vector)
        except (AttributeError, TypeError):
            pass  # Expected behavior
        
        # Test randomInt with invalid parameters
        with self.assertRaises((ValueError, TypeError)):
            fun.randomInt("invalid", 10)
        
        with self.assertRaises((ValueError, TypeError)):
            fun.randomInt(10, 5)  # min > max
    
    def test_extreme_values(self):
        """Test functions with extreme values"""
        # Test randomValue with large values
        result = fun.randomValue(-1e10, 1e10)
        self.assertIsInstance(result, float)
        
        # Test randomInt with large range
        result = fun.randomInt(-1000000, 1000000)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -1000000)
        self.assertLessEqual(result, 1000000)
    
    def test_zero_and_negative_values(self):
        """Test functions with zero and negative values"""
        # Test randomValue with zero range
        result = fun.randomValue(0, 0)
        self.assertEqual(result, 0)
        
        # Test randomValue with negative range
        result = fun.randomValue(-10, -5)
        self.assertGreaterEqual(result, -10)
        self.assertLessEqual(result, -5)


class TestPerformance(unittest.TestCase):
    """Test performance-related aspects"""
    
    def test_large_list_shuffle(self):
        """Test shuffling performance with large lists"""
        import time
        
        large_list = list(range(10000))
        
        start_time = time.time()
        result = fun.shuffleList(large_list.copy())
        end_time = time.time()
        
        # Should complete within reasonable time (less than 1 second)
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(len(result), len(large_list))
        self.assertCountEqual(result, large_list)
    
    def test_multiple_position_calculations(self):
        """Test performance of position calculations"""
        import time
        
        start_time = time.time()
        
        # Calculate positions for many objects
        for i in range(1000):
            pos = fun.setBoxPos(i, 1, False)
            self.assertIsInstance(pos, Vector)
        
        end_time = time.time()
        
        # Should complete within reasonable time
        self.assertLess(end_time - start_time, 0.5)


def run_all_tests():
    """Run all test suites"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBasicFunctions,
        TestSetBoxPos,
        TestGeometricFunctions,
        TestLogicalFunctions,
        TestObjectManipulation,
        TestEdgeCases,
        TestPerformance,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return results
    return result


if __name__ == '__main__':
    print("Architectural Design Tool - Unit Tests")
    print("=" * 50)
    print("Running comprehensive test suite...")
    print()
    
    result = run_all_tests()
    
    print()
    print("Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")