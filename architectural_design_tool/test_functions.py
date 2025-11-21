"""
Unit tests for architectural_design_tool addon
Tests for functions.py module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the addon path to sys.path for imports
addon_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, addon_path)

# Import the modules to test
import functions as fun


class TestBasicFunctions(unittest.TestCase):
    """Test basic utility functions"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock bpy and other Blender modules
        self.bpy_mock = Mock()
        self.vector_mock = Mock()
        self.matrix_mock = Mock()
        
        # Patch Blender modules
        self.patchers = [
            patch('functions.bpy', self.bpy_mock),
            patch('functions.Vector', self.vector_mock),
            patch('functions.Matrix', self.matrix_mock),
        ]
        
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        """Clean up after each test method."""
        for patcher in self.patchers:
            patcher.stop()

    def test_cross(self):
        """Test cross product function"""
        v1 = (1, 2, 3)
        v2 = (4, 5, 6)
        
        # Expected cross product: (2*6-3*5, 3*4-1*6, 1*5-2*4) = (-3, 6, -3)
        expected = (-3, 6, -3)
        result = fun.cross(v1, v2)
        
        self.assertEqual(result, expected)

    def test_dir2Vec3(self):
        """Test direction to vector conversion"""
        # Mock Vector constructor
        mock_vector = Mock()
        self.vector_mock.side_effect = lambda x: mock_vector
        
        # Test all valid directions
        directions = ["+x", "+y", "+z", "-x", "-y", "-z"]
        expected_vectors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), 
                           (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
        
        for direction, expected in zip(directions, expected_vectors):
            result = fun.dir2Vec3(direction)
            self.vector_mock.assert_called_with(expected)
            self.assertEqual(result, mock_vector)
        
        # Test invalid direction
        result = fun.dir2Vec3("invalid")
        self.vector_mock.assert_called_with((0, 0, 0))

    @patch('functions.random.uniform')
    def test_randomValue(self, mock_uniform):
        """Test random value generation"""
        mock_uniform.return_value = 3.14
        result = fun.randomValue(1.0, 5.0)
        mock_uniform.assert_called_once_with(1.0, 5.0)
        self.assertEqual(result, 3.14)

    @patch('functions.random.choice')
    def test_randomBool(self, mock_choice):
        """Test random boolean generation"""
        mock_choice.return_value = True
        result = fun.randomBool()
        mock_choice.assert_called_once_with([True, False])
        self.assertTrue(result)

    def test_setActive(self):
        """Test setting active object"""
        mock_obj = Mock()
        fun.setActive(mock_obj)
        self.bpy_mock.context.view_layer.objects.active = mock_obj

    @patch('functions.bpy')
    def test_copyobj(self, mock_bpy):
        """Test object copying"""
        mock_obj = Mock()
        mock_new_obj = Mock()
        
        # Configure mocks
        mock_obj.copy.return_value = mock_new_obj
        mock_obj.data.copy.return_value = Mock()
        
        result = fun.copyobj(mock_obj)
        
        # Verify method calls
        mock_obj.copy.assert_called_once()
        mock_obj.data.copy.assert_called_once()
        mock_bpy.context.collection.objects.link.assert_called_once_with(mock_new_obj)
        self.assertEqual(result, mock_new_obj)

    @patch('functions.bpy')
    def test_delobj(self, mock_bpy):
        """Test object deletion"""
        mock_obj = Mock()
        fun.delobj(mock_obj)
        mock_bpy.data.objects.remove.assert_called_once_with(mock_obj)


class TestGenerationFunctions(unittest.TestCase):
    """Test object generation functions"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.bpy_mock = Mock()
        self.patchers = [patch('functions.bpy', self.bpy_mock)]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        """Clean up after each test method."""
        for patcher in self.patchers:
            patcher.stop()

    @patch('functions.getBound')
    @patch('functions.randomValue')
    def test_randomInsidePoint(self, mock_random_value, mock_get_bound):
        """Test random point generation inside object bounds"""
        # Mock bounds
        mock_get_bound.return_value = (2, 2, 2, 0, 0, 0)
        
        # Mock random values
        mock_random_value.side_effect = [1, 1, 1]
        
        mock_obj = Mock()
        result = fun.randomInsidePoint(mock_obj)
        
        mock_get_bound.assert_called_once_with(mock_obj)
        self.assertEqual(mock_random_value.call_count, 3)
        
        # Verify the result is a Vector (mocked)
        self.assertIsNotNone(result)

    @patch('functions.random.choice')
    def test_randomDir(self, mock_choice):
        """Test random direction selection"""
        directions = ["+x", "+y", "+z", "-x", "-y", "-z"]
        mock_choice.return_value = "+y"
        
        result = fun.randomDir()
        mock_choice.assert_called_once_with(directions)
        self.assertEqual(result, "+y")

    @patch('functions.randomValue')
    @patch('functions.Vector')
    def test_randomVector_no_constraint(self, mock_vector, mock_random_value):
        """Test random vector generation without direction constraint"""
        # Mock random values
        mock_random_value.side_effect = [1, 1, 1]
        
        # Mock vector creation
        mock_rand_vec = Mock()
        mock_rand_vec.normalized.return_value = Mock()
        mock_vector.return_value = mock_rand_vec
        
        # Test with zero vector constraint
        constraint = (0, 0, 0)
        result = fun.randomVector(constraint)
        
        mock_vector.assert_called_once_with((1, 1, 1))
        mock_rand_vec.normalized.assert_called_once()

    @patch('functions.bpy')
    @patch('functions.randomValue')
    def test_randomCube(self, mock_random_value, mock_bpy):
        """Test random cube generation"""
        # Mock random values for dimensions and position
        mock_random_value.side_effect = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        
        # Mock cube creation
        mock_cube = Mock()
        mock_bpy.context.active_object = mock_cube
        
        result = fun.randomCube(1.0, 5.0, 10.0)
        
        # Verify bpy.ops.mesh.primitive_cube_add was called
        mock_bpy.ops.mesh.primitive_cube_add.assert_called_once_with(
            size=1,
            enter_editmode=False,
            align="WORLD",
            location=(5.0, 6.0, 7.0),
            scale=(2.0, 3.0, 4.0),
        )
        
        self.assertEqual(result, mock_cube)

    @patch('functions.applyMod')
    @patch('functions.delobj')
    @patch('functions.setActive')
    def test_calBool(self, mock_set_active, mock_delobj, mock_apply_mod):
        """Test boolean operations"""
        mock_base_obj = Mock()
        mock_bool_obj = Mock()
        mock_modifier = Mock()
        
        # Mock the modifier creation
        self.bpy_mock.context.active_object = mock_base_obj
        mock_base_obj.modifiers.new.return_value = mock_modifier
        
        # Test different boolean types
        test_cases = [
            ("add", "UNION"),
            ("sub", "DIFFERENCE"),
            ("mul", "INTERSECT"),
        ]
        
        for bool_type, expected_operation in test_cases:
            with self.subTest(bool_type=bool_type):
                result = fun.calBool(mock_base_obj, mock_bool_obj, bool_type)
                
                mock_base_obj.modifiers.new.assert_called_with(name="Boolean", type="BOOLEAN")
                self.assertEqual(mock_modifier.operation, expected_operation)
                self.assertEqual(mock_modifier.object, mock_bool_obj)
                mock_apply_mod.assert_called_with(mock_base_obj, "Boolean")
                mock_delobj.assert_called_with(mock_bool_obj)
                self.assertEqual(result, mock_base_obj)


class TestOptimizationFunctions(unittest.TestCase):
    """Test mesh optimization functions"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.bpy_mock = Mock()
        self.bmesh_mock = Mock()
        self.patchers = [
            patch('functions.bpy', self.bpy_mock),
            patch('functions.bmesh', self.bmesh_mock),
        ]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        """Clean up after each test method."""
        for patcher in self.patchers:
            patcher.stop()

    @patch('functions.setActive')
    def test_optimizeMesh(self, mock_set_active):
        """Test mesh optimization"""
        mock_obj = Mock()
        mock_bm = Mock()
        mock_bmesh_ops = Mock()
        
        # Mock bmesh operations
        self.bmesh_mock.from_edit_mesh.return_value = mock_bm
        self.bmesh_mock.ops = mock_bmesh_ops
        
        result = fun.optimizeMesh(mock_obj, merge_threshold=0.001)
        
        # Verify function calls
        mock_set_active.assert_called_once_with(mock_obj)
        self.bpy_mock.ops.object.mode_set.assert_any_call(mode='EDIT')
        self.bmesh_mock.from_edit_mesh.assert_called_once_with(mock_obj.data)
        mock_bmesh_ops.remove_doubles.assert_called_once_with(
            mock_bm, verts=mock_bm.verts, dist=0.001
        )
        self.bmesh_mock.update_edit_mesh.assert_called_once_with(mock_obj.data)
        self.bpy_mock.ops.object.mode_set.assert_any_call(mode='OBJECT')
        
        self.assertEqual(result, mock_obj)


class TestLogicalFunctions(unittest.TestCase):
    """Test logical functions for object relationships"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.bpy_mock = Mock()
        self.patchers = [
            patch('functions.bpy', self.bpy_mock),
        ]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        """Clean up after each test method."""
        for patcher in self.patchers:
            patcher.stop()

    def test_isExists_found(self):
        """Test object existence check - object found"""
        mock_obj1 = Mock()
        mock_obj1.name = "TestObject"
        mock_obj2 = Mock()
        mock_obj2.name = "OtherObject"
        
        self.bpy_mock.data.objects = [mock_obj1, mock_obj2]
        
        result = fun.isExists("TestObject")
        self.assertTrue(result)

    def test_isExists_not_found(self):
        """Test object existence check - object not found"""
        mock_obj1 = Mock()
        mock_obj1.name = "OtherObject"
        
        self.bpy_mock.data.objects = [mock_obj1]
        
        result = fun.isExists("TestObject")
        self.assertFalse(result)

    @patch('functions.getBound')
    @patch('functions.randomValue')
    def test_randomInsidePoint(self, mock_random_value, mock_get_bound):
        """Test random point generation inside object"""
        # Mock bounds
        mock_get_bound.return_value = (10, 20, 30, 0, 10, 20)
        
        # Mock random values
        mock_random_value.side_effect = [5, 15, 25]
        
        mock_obj = Mock()
        
        with patch('functions.Vector') as mock_vector:
            result = fun.randomInsidePoint(mock_obj)
            
            mock_get_bound.assert_called_once_with(mock_obj)
            self.assertEqual(mock_random_value.call_count, 3)
            
            # Check if Vector was called with the random values
            mock_vector.assert_called_once_with((5, 15, 25))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.bpy_mock = Mock()
        self.patchers = [patch('functions.bpy', self.bpy_mock)]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        """Clean up after each test method."""
        for patcher in self.patchers:
            patcher.stop()

    @patch('functions.setActive')
    @patch('functions.bmesh')
    def test_optimizeMesh_with_zero_threshold(self, mock_bmesh, mock_set_active):
        """Test mesh optimization with zero threshold"""
        mock_obj = Mock()
        mock_bm = Mock()
        mock_bmesh_ops = Mock()
        
        mock_bmesh.from_edit_mesh.return_value = mock_bm
        mock_bmesh.ops = mock_bmesh_ops
        
        fun.optimizeMesh(mock_obj, merge_threshold=0.0)
        
        mock_bmesh_ops.remove_doubles.assert_called_once_with(
            mock_bm, verts=mock_bm.verts, dist=0.0
        )

    def test_randomVector_with_zero_constraint_vector(self):
        """Test random vector with zero constraint vector"""
        with patch('functions.Vector') as mock_vector, \
             patch('functions.randomValue') as mock_random:
            
            mock_rand_vec = Mock()
            mock_rand_vec.normalized.return_value = "normalized_vector"
            mock_vector.return_value = mock_rand_vec
            
            constraint = (0, 0, 0)
            result = fun.randomVector(constraint)
            
            self.assertEqual(result, "normalized_vector")


if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [TestBasicFunctions, TestGenerationFunctions, 
                   TestOptimizationFunctions, TestLogicalFunctions, TestEdgeCases]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")