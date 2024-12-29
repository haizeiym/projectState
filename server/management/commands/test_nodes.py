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

        # # 获取节点
        # node = Node.get(1)
        # self.stdout.write(f"获取节点: {node.node_name}")

        # # 更新属性
        # node.update(name="新名称", state=1, description="新描述")
        # self.stdout.write("更新节点成功")

        # # 添加子节点
        # child = Node(2, "子节点")
        # node.add_child(child)
        # self.stdout.write("添加子节点成功")

        # # 添加子节点
        # child = Node(3, "子节点3", state=3)
        # node.add_child(child)
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

        # 获取节点
        node = Node.get(100000007)
        node.update(name="新节点666ssssdf试试", description="描述测试")
        self.stdout.write(f"获取节点: {node.node_name}")
