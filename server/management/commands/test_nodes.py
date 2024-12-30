from django.core.management.base import BaseCommand
from server.api.Node import Node
from server.api.Project import Project


class Command(BaseCommand):
    help = "测试 Node 类的功能"

    def handle(self, *args, **options):
        # # 创建和保存节点
        # node = Node.create(node_name="测试节点阿斯顿发", description="测试描述阿斯顿发")
        # self.stdout.write(
        #     self.style.SUCCESS(f"创建节点成功: {node.node_id}，{node.node_name}")
        # )

        # 获取节点
        node = Node.get(100000013)
        self.stdout.write(f"获取节点: {node.node_id}")

        # # 更新属性
        # node.update(name="新名称", state=1, description="新描述")
        # self.stdout.write("更新节点成功")

        # 添加子节点
        child = Node.create(node_name="子1", description="测试描述阿斯顿发")
        isSuccess = Node.add_child(parent_id=node.node_id, child_id=child.node_id)
        self.stdout.write(f"添加子节点成功: {isSuccess}")

        # # 添加子节点
        # child = Node.create(node_name="子2", description="测试描述阿斯顿发")
        # Node.add_child(node_id=child.node_id, parent_id=node.node_id)
        # self.stdout.write("添加子节点成功")

        # # 获取子节点
        # children = node.children
        # self.stdout.write(f"子节点数量: {len(children)}")

        # # 获取所有节点
        # all_nodes = Node.get_all()
        # self.stdout.write(f"总节点数量: {len(all_nodes)}")

        # # 创建项目
        # project = Project.create(project_name="测试项目100012")
        # self.stdout.write(self.style.SUCCESS(f"创建项目成功 {project.project_id}"))

        # isSuccess = Project.update(100000013, project_name="测试项目1003332", node_id=2)
        # self.stdout.write(self.style.SUCCESS(f"更新项目成功: {isSuccess}"))

        # # 获取节点
        # node = Node.get(100000007)
        # if node:
        #     isSuccess = Node.update(node.node_id, node_name="测试节点")
        #     self.stdout.write(self.style.SUCCESS(f"更新节点: {isSuccess}"))
        # else:
        #     self.stdout.write(self.style.ERROR("获取节点失败"))

        # # 获取项目列表
        # try:
        #     projects = Project.list()
        #     self.stdout.write(self.style.SUCCESS(f"获取项目列表成功: {projects}"))
        # except Exception as e:
        #     self.stdout.write(self.style.ERROR(f"获取项目列表失败: {str(e)}"))
        # project = Project.create(project_name="测试项目100")
        # self.stdout.write(self.style.SUCCESS(f"创建项目成功: {project.project_id}"))
        # # 删除项目
        # success = Project.delete(100000014)
        # if success:
        #     self.stdout.write(self.style.SUCCESS("删除项目成功"))
        # else:
        #     self.stdout.write(self.style.ERROR("删除项目失败"))
        node_tree = Node.get_tree(node_id=100000013)
        if node_tree:
            self.stdout.write(self.style.SUCCESS(f"获取节点树成功: {node_tree}"))
        else:
            self.stdout.write(self.style.ERROR("获取节点树失败"))
