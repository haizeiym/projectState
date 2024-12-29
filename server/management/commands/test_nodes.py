from django.core.management.base import BaseCommand
from server.api.Node import Node
from server.api.Project import Project


class Command(BaseCommand):
    help = "测试 Node 类的功能"

    def handle(self, *args, **options):
        # # 创建和保存节点
        # node = Node(1, "测试节点")
        # node.save()
        # self.stdout.write(self.style.SUCCESS("创建节点成功"))

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
        # Project.create(1000, "测试项目100012")
        # self.stdout.write(self.style.SUCCESS("创建项目成功23"))
        # Project.update(
        #     1000, project_name="新名称qwe", state=6, description="新描述123", node_id=2
        # )
        project = Project.get(1000)
        self.stdout.write(
            f"获取项目: {project.project_name,project.state,project.node_id}"
        )
        # 获取节点
        node = Node.get(2)
        node.update(name="新节点666ssssdf试试", description="描述测试")
        self.stdout.write(f"获取节点: {node.node_name}")
