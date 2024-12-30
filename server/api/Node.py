from ..models import NodeModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
import json


class Node:
    def __init__(
        self,
        node_id,
        node_name="",
        description="",
        state=0,
        parent_id=0,
        childrens=None,
    ):
        self.node_id = node_id
        self.node_name = node_name
        self.description = description
        self.state = state
        self.parent_id = parent_id
        self.children_state = 0
        self.childrens = childrens or []

    @staticmethod
    def _get_node_model(node_id):
        """
        获取节点模型的辅助方法
        :param node_id: 节点ID
        :return: NodeModel实例或None
        """
        try:
            node = NodeModel.objects.get(node_id=node_id)
            return node
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get(node_id):
        """
        获取节点信息
        :param node_id: 节点ID
        :return: Node对象或None
        """
        node_model = Node._get_node_model(node_id)
        return Node.create_from_db(node_model)

    @staticmethod
    def create(**kwargs):
        """
        创建节点
        :param kwargs: 节点参数
        :return: Node对象或None
        """
        with transaction.atomic():
            try:
                node_id = NodeModel.get_next_id() or 1
                node_model = NodeModel(
                    node_id=node_id,
                    node_name=kwargs.get("node_name"),
                    description=kwargs.get("description"),
                    state=kwargs.get("state", 0),
                    parent_id=kwargs.get("parent_id", 0),
                    children_state=kwargs.get("children_state", 0),
                )
                node_model.save()

                # 如果有父节点，更新父节点的 childrens
                if node_model.parent_id:
                    parent = NodeModel.objects.get(node_id=node_model.parent_id)
                    if parent:
                        childrens = parent.get_childrens()
                        childrens.append(node_id)
                        parent.set_childrens(childrens)
                        parent.save()
                node_model.node_id = node_id
                return Node.create_from_db(node_model)
            except Exception:
                return None

    @staticmethod
    def update(request=None, node_id=None, **kwargs):
        """
        更新节点信息
        :param request: HTTP请求对象（可选）
        :param node_id: 节点ID
        :param kwargs: 要更新的字段和值
        :return: JsonResponse 或 bool
        """
        try:
            # 如果是通过 URL 参数传入的 node_id
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            node_model = Node._get_node_model(node_id)
            if node_model is None:
                if request:
                    return JsonResponse({"error": "Node not found"}, status=404)
                return False

            field_mapping = {
                "node_name": "node_name",
                "description": "description",
                "state": "state",
                "parent_id": "parent_id",
                "children_state": "children_state",
                "childrens": "childrens",
            }

            # 如果是 HTTP 请求，从请求体获取数据
            if request and request.method == "POST":
                try:
                    data = json.loads(request.body)
                    kwargs.update(data)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON"}, status=400)

            with transaction.atomic():
                # 更新字段
                for key, value in kwargs.items():
                    if key in field_mapping:
                        if key == "childrens":
                            # 特殊处理 childrens 字段
                            node_model.set_childrens(value)
                        else:
                            setattr(node_model, field_mapping[key], value)

                # 如果更新了 parent_id，需要更新旧父节点和新父节点的 childrens
                if (
                    "parent_id" in kwargs
                    and kwargs["parent_id"] != node_model.parent_id
                ):
                    # 从旧父节点的 childrens 中移除
                    old_parent = Node._get_node_model(node_model.parent_id)
                    if old_parent:
                        old_childrens = old_parent.get_childrens()
                        if node_id in old_childrens:
                            old_childrens.remove(node_id)
                            old_parent.set_childrens(old_childrens)
                            old_parent.save()

                    # 添加到新父节点的 childrens 中
                    new_parent = Node._get_node_model(kwargs["parent_id"])
                    if new_parent:
                        new_childrens = new_parent.get_childrens()
                        if node_id not in new_childrens:
                            new_childrens.append(node_id)
                            new_parent.set_childrens(new_childrens)
                            new_parent.save()

                node_model.save()
                Node._check_children_states(node_id)

                if request:
                    return JsonResponse({"status": "success"})
                return True

        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            return False

    @staticmethod
    def delete(node_id):
        """
        删除节点
        :param node_id: 节点ID
        :return: 是否删除成功
        """
        with transaction.atomic():
            node_model = Node._get_node_model(node_id)
            if not node_model:
                return False
            try:
                # 更新父节点的 childrens
                if node_model.parent_id:
                    parent = NodeModel.objects.get(node_id=node_model.parent_id)
                    if parent:
                        childrens = parent.get_childrens()
                        childrens.remove(node_id)
                        parent.set_childrens(childrens)
                        parent.save()

                node_model.delete()
                return True
            except ObjectDoesNotExist:
                return False

    @staticmethod
    def _check_children_states(node_id):
        """
        检查子节点状态一致性
        :param node_id: 节点ID
        """
        children = NodeModel.objects.filter(parent_id=node_id)
        if not children.exists():
            return

        first_state = children.first().state
        all_same = all(child.state == first_state for child in children)

        if all_same:
            NodeModel.objects.filter(node_id=node_id).update(children_state=first_state)

    @staticmethod
    def create_from_db(node_model):
        """
        从数据库模型创建Node对象
        :param node_model: NodeModel实例
        :return: Node对象
        """
        if not node_model:
            return None
        return Node(
            node_id=node_model.node_id,
            node_name=node_model.node_name,
            description=node_model.description,
            state=node_model.state,
            parent_id=node_model.parent_id,
            childrens=node_model.get_childrens(),
        )

    @staticmethod
    def get_tree(request=None, node_id=None):
        """
        获取节点及其所有子节点
        :param request: HTTP请求对象（可选）
        :param node_id: 节点ID
        :return: JsonResponse 或 dict
        """
        try:
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            def get_node_with_children(node_id):
                node = NodeModel.objects.get(node_id=node_id)
                childrens = node.get_childrens()

                node_data = {
                    "node_id": node.node_id,
                    "node_name": node.node_name,
                    "description": node.description,
                    "state": node.state,
                    "parent_id": node.parent_id,
                    "children_state": node.children_state,
                    "childrens": childrens,
                    "children": [
                        get_node_with_children(child_id) for child_id in childrens
                    ],
                }
                return node_data

            result = get_node_with_children(node_id)
            if request:
                return JsonResponse(result)
            return result

        except NodeModel.DoesNotExist:
            if request:
                return JsonResponse({"error": "Node not found"}, status=404)
            return None
        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            raise e

    @staticmethod
    def add_child(parent_id, child_id):
        """
        向节点添加子节点
        :param parent_id: 父节点ID
        :param child_id: 子节点ID
        :return: bool 是否添加成功
        """
        try:
            with transaction.atomic():
                # 验证父节点和子节点是否存在
                parent = Node._get_node_model(parent_id)
                child = Node._get_node_model(child_id)

                if not parent or not child:
                    print(f"Parent or child not found: parent={parent}, child={child}")
                    return False

                # 获取当前子节点列表
                childrens = parent.get_childrens()
                print(f"Current childrens: {childrens}")

                # 如果子节点已存在，直接返回成功
                if child_id in childrens:
                    print(f"Child {child_id} already exists in parent's children")
                    return True

                # 添加新的子节点ID
                childrens.append(child_id)
                parent.set_childrens(childrens)
                print(f"Updated childrens: {parent.get_childrens()}")

                # 更新子节点的父节点ID
                child.parent_id = parent_id

                # 保存更改
                parent.save()
                child.save()

                return True

        except Exception as e:
            import traceback

            print(f"Error in add_child: {str(e)}")
            print(traceback.format_exc())  # 打印完整的错误堆栈
            return False

    @staticmethod
    def remove_child(parent_id, child_id):
        """
        从节点移除子节点
        :param parent_id: 父节点ID
        :param child_id: 子节点ID
        :return: bool 是否移除成功
        """
        try:
            with transaction.atomic():
                # 验证父节点和子节点是否存在
                parent = Node._get_node_model(parent_id)
                child = Node._get_node_model(child_id)

                if not parent or not child:
                    return False

                # 获取当前子节点列表
                childrens = parent.get_childrens()

                # 如果子节点不存在，直接返回成功
                if child_id not in childrens:
                    return True

                # 移除子节点ID
                childrens.remove(child_id)
                parent.set_childrens(childrens)

                # 重置子节点的父节点ID
                child.parent_id = 0

                # 保存更改
                parent.save()
                child.save()

                # 检查子节点状态一致性
                Node._check_children_states(parent_id)

                return True

        except Exception:
            return False

    @staticmethod
    def get_children(node_id):
        """
        获取节点的所有子节点
        :param node_id: 节点ID
        :return: list[Node] 子节点列表或None
        """
        try:
            node = Node._get_node_model(node_id)
            if not node:
                return None

            childrens = node.get_childrens()
            return [Node.get(child_id) for child_id in childrens]

        except Exception:
            return None
