from ..models import NodeModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse


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
