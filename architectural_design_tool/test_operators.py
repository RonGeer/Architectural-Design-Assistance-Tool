"""
Architectural Design Tool - Operator Tests
==========================================

This test suite provides comprehensive unit testing for the Blender operators
in the architectural_design_tool addon.

Author: AI Assistant
Date: 2025-11-22
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock, call
from mathutils import Vector, Matrix

# Add the addon directory to the path
addon_dir = os.path.dirname(__file__)
sys.path.insert(0, addon_dir)

# Mock bpy module before importing
mock_bpy = Mock()
mock_context = Mock()
mock_scene = Mock()
mock_props = Mock()

# Set up comprehensive mock for bpy
mock_bpy.context = mock_context
mock_bpy.context.scene = mock_scene
mock_bpy.context.active_object = Mock()
mock_bpy.context.view_layer = Mock()
mock_bpy.context.collection = Mock()
mock_bpy.context.window_manager = Mock()
mock_bpy.data = Mock()
mock_bpy.ops = Mock()
mock_bpy.utils = Mock()
mock_bpy.types = Mock()

# Set up scene properties
mock_scene.adt_props = mock_props
mock_props.auto_count = 5
mock_props.auto_deformation_count = 1
mock_props.auto_culling_count = 1
mock_props.auto_isorder = True
mock_props.max_attempts = 1000
mock_props.min_size = 0.5
mock_props.max_size = 1.0
mock_props.max_area = 2.0
mock_props.add_box_size = 0.5

# Mock all Blender modules
sys.modules['bpy'] = mock_bpy
sys.modules['bmesh'] = Mock()
sys.modules['mathutils'] = Mock()
sys.modules['mathutils'].Vector = Vector
sys.modules['mathutils'].Matrix = Matrix

# Mock the functions module
mock_functions = Mock()
mock_functions.randomInt.return_value = 1
mock_functions.onePass = Mock()
mock_functions.isExists.return_value = True
mock_functions.randomCube = Mock()
mock_functions.isIntersect.return_value = True
mock_functions.isInside.return_value = (True, "boxA")
mock_functions.calBool = Mock()
mock_functions.setActive = Mock()
mock_functions.getBound.return_value = (1, 1, 1, -1, -1, -1)
mock_functions.applyMod = Mock()
mock_functions.addTwist = Mock()
mock_functions.cutLineWithDir = Mock()
mock_functions.delobj = Mock()
mock_functions.randomValue.return_value = 0.5
mock_functions.randomBool.return_value = True
mock_functions.randomDir.return_value = "+x"
mock_functions.randomVector.return_value = Vector((1, 0, 0))
mock_functions.centerPos.return_value = Vector((0, 0, 0))
mock_functions.snapEdge.return_value = None
mock_functions.offsetShell.return_value = Mock()
mock_functions.crateBoxWithDir.return_value = Mock()
mock_functions.meshTowall.return_value = Mock()
mock_functions.optimizeMesh.return_value = Mock()
mock_functions.copyobj.return_value = Mock()

# Import operators after mocking
try:
    import operators
    from operators import Setbase, Auto, Merge, Branch, Extract, Offset, Shift, Twist, Carve, Frature, Expland
except ImportError as e:
    print(f"Warning: Could not import operators: {e}")
    # Create dummy classes for testing structure
    class Setbase(Mock): pass
    class Auto(Mock): pass
    class Merge(Mock): pass
    class Branch(Mock): pass
    class Extract(Mock): pass
    class Offset(Mock): pass
    class Shift(Mock): pass
    class Twist(Mock): pass
    class Carve(Mock): pass
    class Frature(Mock): pass
    class Expland(Mock): pass


class TestSetbaseOperator(unittest.TestCase):
    """Test the Setbase operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Setbase()
        self.mock_active_object = Mock()
        mock_bpy.context.active_object = self.mock_active_object
    
    def test_execute_sets_name_to_basebox(self):
        """Test that execute method sets object name to BaseBox"""
        context = mock_bpy.context
        
        result = self.operator.execute(context)
        
        self.assertEqual(self.mock_active_object.name, "BaseBox")
        self.assertEqual(result, {"FINISHED"})
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Setbase.bl_idname, "ronge_adt.setbase")
        self.assertEqual(Setbase.bl_label, "SetBase")


class TestAutoOperator(unittest.TestCase):
    """Test the Auto operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Auto()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        self.mock_basebox.name = "BaseBox"
        
        # Mock the scene objects
        mock_bpy.data.objects.__contains__ = Mock(return_value=True)
        mock_bpy.data.objects.__getitem__ = Mock(return_value=self.mock_basebox)
    
    @patch('operators.fun', mock_functions)
    def test_execute_with_default_parameters(self):
        """Test execute method with default parameters"""
        result = self.operator.execute(self.context)
        
        # Should return FINISHED
        self.assertEqual(result, {"FINISHED"})
        
        # Should call fun.randomInt for base shape selection
        self.assertTrue(mock_functions.randomInt.called)
        
        # Should call onePass for each iteration
        expected_calls = mock_props.auto_count
        self.assertEqual(mock_functions.onePass.call_count, expected_calls)
    
    @patch('operators.fun', mock_functions)
    def test_execute_with_merge_operation(self):
        """Test execute when randomInt selects merge (1)"""
        mock_functions.randomInt.return_value = 1
        
        self.operator.execute(self.context)
        
        # Should call merge operator
        mock_bpy.ops.ronge_adt.merge.assert_called()
        
        # Should call onePass with merge addname
        mock_functions.onePass.assert_called()
    
    @patch('operators.fun', mock_functions)
    def test_execute_with_branch_operation(self):
        """Test execute when randomInt selects branch (2)"""
        mock_functions.randomInt.return_value = 2
        
        self.operator.execute(self.context)
        
        # Should call branch operator
        mock_bpy.ops.ronge_adt.branch.assert_called()
    
    @patch('operators.fun', mock_functions)
    def test_execute_with_extract_operation(self):
        """Test execute when randomInt selects extract (3)"""
        mock_functions.randomInt.return_value = 3
        
        self.operator.execute(self.context)
        
        # Should call extract operator
        mock_bpy.ops.ronge_adt.extract.assert_called()
    
    @patch('operators.fun', mock_functions)
    def test_execute_handles_default_fallback(self):
        """Test execute fallback to merge for other randomInt values"""
        mock_functions.randomInt.return_value = 4
        
        self.operator.execute(self.context)
        
        # Should fall back to merge operator
        mock_bpy.ops.ronge_adt.merge.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Auto.bl_idname, "ronge_adt.auto")
        self.assertEqual(Auto.bl_label, "Auto")


class TestMergeOperator(unittest.TestCase):
    """Test the Merge operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Merge()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_with_successful_intersection(self):
        """Test execute when intersection is found"""
        mock_functions.isIntersect.return_value = True
        mock_functions.isInside.return_value = (False, "")
        
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.randomCube.assert_called()
        mock_functions.calBool.assert_called()
    
    @patch('operators.fun', mock_functions)
    def test_execute_handles_max_attempts(self):
        """Test execute when max attempts are reached"""
        mock_functions.isIntersect.return_value = False
        
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"CANCELLED"})
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Merge.bl_idname, "ronge_adt.merge")
        self.assertEqual(Merge.bl_label, "Merge")


class TestBranchOperator(unittest.TestCase):
    """Test the Branch operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Branch()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_creates_branch(self):
        """Test execute method creates branch objects"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.centerPos.assert_called()
        mock_functions.crateBoxWithDir.assert_called()
        mock_functions.calBool.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Branch.bl_idname, "ronge_adt.branch")
        self.assertEqual(Branch.bl_label, "Branch")


class TestExtractOperator(unittest.TestCase):
    """Test the Extract operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Extract()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_creates_extraction(self):
        """Test execute method creates extraction"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.randomInsidePoint.assert_called()
        mock_functions.crateBoxWithDir.assert_called()
        mock_functions.calBool.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Extract.bl_idname, "ronge_adt.extract")
        self.assertEqual(Extract.bl_label, "Extract")


class TestOffsetOperator(unittest.TestCase):
    """Test the Offset operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Offset()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_applies_offset(self):
        """Test execute method applies offset"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.offsetShell.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Offset.bl_idname, "ronge_adt.offset")
        self.assertEqual(Offset.bl_label, "Offset")


class TestShiftOperator(unittest.TestCase):
    """Test the Shift operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Shift()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_performs_shift(self):
        """Test execute method performs shift operation"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.cutLineWithDir.assert_called()
        mock_functions.randomDir.assert_called()
        mock_functions.centerPos.assert_called()
        mock_functions.snapEdge.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Shift.bl_idname, "ronge_adt.shift")
        self.assertEqual(Shift.bl_label, "Shift")


class TestTwistOperator(unittest.TestCase):
    """Test the Twist operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Twist()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_applies_twist(self):
        """Test execute method applies twist"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.addTwist.assert_called()
        mock_functions.cutLineWithDir.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Twist.bl_idname, "ronge_adt.twist")
        self.assertEqual(Twist.bl_label, "Twist")


class TestCarveOperator(unittest.TestCase):
    """Test the Carve operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Carve()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_with_successful_intersection(self):
        """Test execute when intersection is found"""
        mock_functions.isIntersect.return_value = True
        mock_functions.isInside.return_value = (False, "")
        
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.randomCube.assert_called()
        mock_functions.calBool.assert_called_with(self.mock_basebox, mock_functions.randomCube.return_value, "sub")
    
    @patch('operators.fun', mock_functions)
    def test_execute_handles_max_attempts(self):
        """Test execute when max attempts are reached"""
        mock_functions.isIntersect.return_value = False
        
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"CANCELLED"})
    
    @patch('operators.fun', mock_functions)
    def test_execute_skips_when_inside(self):
        """Test execute when cube is inside basebox"""
        mock_functions.isIntersect.return_value = True
        mock_functions.isInside.return_value = (True, "boxA")
        
        result = self.operator.execute(self.context)
        
        # Should delete the cube and continue
        mock_functions.delobj.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Carve.bl_idname, "ronge_adt.carve")
        self.assertEqual(Carve.bl_label, "Carve")


class TestFratureOperator(unittest.TestCase):
    """Test the Frature operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Frature()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_creates_fracture(self):
        """Test execute method creates fracture"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.centerPos.assert_called()
        mock_functions.randomVector.assert_called()
        mock_functions.meshTowall.assert_called()
        mock_functions.calBool.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Frature.bl_idname, "ronge_adt.frature")
        self.assertEqual(Frature.bl_label, "Frature")


class TestExplandOperator(unittest.TestCase):
    """Test the Expland operator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operator = Expland()
        self.context = mock_bpy.context
        self.mock_basebox = Mock()
        mock_bpy.context.active_object = self.mock_basebox
    
    @patch('operators.fun', mock_functions)
    def test_execute_performs_expand(self):
        """Test execute method performs expand operation"""
        result = self.operator.execute(self.context)
        
        self.assertEqual(result, {"FINISHED"})
        mock_functions.centerPos.assert_called()
        mock_functions.randomVector.assert_called()
        mock_functions.crateBoxWithDir.assert_called()
        mock_functions.calBool.assert_called()
    
    def test_bl_idname_and_label(self):
        """Test operator identification"""
        self.assertEqual(Expland.bl_idname, "ronge_adt.expland")
        self.assertEqual(Expland.bl_label, "Expland")


class TestOperatorIntegration(unittest.TestCase):
    """Test operator integration and workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.context = mock_bpy.context
    
    @patch('operators.fun', mock_functions)
    def test_auto_workflow_calls_operators(self):
        """Test that Auto operator workflow calls appropriate operators"""
        auto_op = Auto()
        
        # Configure mock to return merge
        mock_functions.randomInt.return_value = 1
        
        result = auto_op.execute(self.context)
        
        # Should call merge operator
        mock_bpy.ops.ronge_adt.merge.assert_called()
        
        # Should call onePass for each iteration
        expected_calls = mock_props.auto_count
        self.assertEqual(mock_functions.onePass.call_count, expected_calls)
    
    def test_all_operators_have_proper_identification(self):
        """Test that all operators have proper bl_idname and bl_label"""
        operators_to_test = [
            (Setbase, "ronge_adt.setbase", "SetBase"),
            (Auto, "ronge_adt.auto", "Auto"),
            (Merge, "ronge_adt.merge", "Merge"),
            (Branch, "ronge_adt.branch", "Branch"),
            (Extract, "ronge_adt.extract", "Extract"),
            (Offset, "ronge_adt.offset", "Offset"),
            (Shift, "ronge_adt.shift", "Shift"),
            (Twist, "ronge_adt.twist", "Twist"),
            (Carve, "ronge_adt.carve", "Carve"),
            (Frature, "ronge_adt.frature", "Frature"),
            (Expland, "ronge_adt.expland", "Expland"),
        ]
        
        for operator_class, expected_idname, expected_label in operators_to_test:
            with self.subTest(operator=operator_class.__name__):
                self.assertEqual(operator_class.bl_idname, expected_idname)
                self.assertEqual(operator_class.bl_label, expected_label)


def run_all_operator_tests():
    """Run all operator test suites"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSetbaseOperator,
        TestAutoOperator,
        TestMergeOperator,
        TestBranchOperator,
        TestExtractOperator,
        TestOffsetOperator,
        TestShiftOperator,
        TestTwistOperator,
        TestCarveOperator,
        TestFratureOperator,
        TestExplandOperator,
        TestOperatorIntegration,
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
    print("Architectural Design Tool - Operator Tests")
    print("=" * 50)
    print("Running comprehensive operator test suite...")
    print()
    
    result = run_all_operator_tests()
    
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
        print("\n✅ All operator tests passed!")
    else:
        print("\n❌ Some operator tests failed. Check the output above for details.")