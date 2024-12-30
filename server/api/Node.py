from ..models import NodeModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse


class Node:
    def __init__(self, node_id, node_name="", description="", state=0, parent_id=0):
        self.parent_id = parent_id
        self.node_id = node_id
        self.state = state
        self.node_name = node_name
        self.description = description
        self.children_state = 0

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
                node_model.node_id = node_id
                return Node.create_from_db(node_model)
            except Exception:
                return None

    @staticmethod
    def update(node_id, **kwargs):
        """
        更新节点信息
        :param node_id: 节点ID
        :param kwargs: 要更新的字段和值
        :return: 是否更新成功
        """
        node_model = Node._get_node_model(node_id)
        if node_model is None:
            return False

        field_mapping = {
            "node_name": "node_name",
            "description": "description",
            "state": "state",
            "parent_id": "parent_id",
            "children_state": "children_state",
        }

        try:
            for key, value in kwargs.items():
                if key in field_mapping:
                    setattr(node_model, field_mapping[key], value)
            node_model.save()
            Node._check_children_states(node_id)
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def delete(node_id):
        """
        删除节点
        :param node_id: 节点ID
        :return: 是否删除成功
        """
        node_model = Node._get_node_model(node_id)
        if not node_model:
            return False
        try:
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
            # 如果是通过 URL 参数传入的 node_id
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            def get_node_with_children(node_id):
                node = NodeModel.objects.get(node_id=node_id)
                children = NodeModel.objects.filter(parent_id=node_id)

                node_data = {
                    "node_id": node.node_id,
                    "node_name": node.node_name,
                    "description": node.description,
                    "state": node.state,
                    "children": [
                        get_node_with_children(child.node_id) for child in children
                    ],
                }
                return node_data

            result = get_node_with_children(node_id)

            # 如果是 HTTP 请求，返回 JsonResponse
            if request:
                return JsonResponse(result)
            # 如果是直接调用，返回字典
            return result

        except NodeModel.DoesNotExist:
            if request:
                return JsonResponse({"error": "Node not found"}, status=404)
            return None
        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            raise e
