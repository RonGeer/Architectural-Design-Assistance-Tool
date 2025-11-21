# Architectural-Design-Assistance-Tool
Blender-based Architectural Design Assistant Tool

基型规则：
    Merge
        合并两个或多个随机方体
    Branch
        增加分叉并合并
    Extract
        合并并掏空重叠部分

形变规则：
    Offset
        各面沿着面方向扩展或收缩一定距离
    Twist
        沿着某个轴扭曲
    Shift
        随机沿轴切刀，滑移后合并

剔除规则：
    Carve
        一次或多次扣除随机方体的体积
    Frature
        扣除一定厚度的多面一体墙
    Expland
        一次性“改变”某个面或多个面，使其变为斜面
    