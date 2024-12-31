from ..models import NodeModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder


class NodeJSONEncoder(DjangoJSONEncoder):
    """自定义JSON编码器，处理特殊类型的序列化"""

    def default(self, obj):
        # 处理 ObjectId 类型
        if hasattr(obj, "_id"):
            return str(obj._id)
        return super().default(obj)


class Node:
    def __init__(
        self,
        node_id,
        node_name="",
        description="",
        state=0,
        parent_id=0,
    ):
        self.node_id = node_id
        self.node_name = node_name
        self.description = description
        self.state = state
        self.parent_id = parent_id
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
    def get(request=None, node_id=None):
        """
        获取节点信息
        :param request: HTTP请求对象（可选）
        :param node_id: 节点ID
        :return: JsonResponse 或 Node对象
        """
        try:
            # 如果是通过 URL 参数传入的 node_id
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            node_model = Node._get_node_model(node_id)
            if not node_model:
                if request:
                    return JsonResponse({"error": "Node not found"}, status=404)
                return None

            node = Node.create_from_db(node_model)
            if request:
                return JsonResponse(
                    {
                        "node_id": node.node_id,
                        "node_name": node.node_name,
                        "description": node.description,
                        "state": node.state,
                        "parent_id": node.parent_id,
                    }
                )
            return node

        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            return None

    @staticmethod
    def create(request=None, **kwargs):
        """
        创建节点
        :param request: HTTP请求对象（可选）
        :param kwargs: 节点参数
        :return: JsonResponse 或 Node对象
        """
        try:
            with transaction.atomic():
                node_id = NodeModel.get_next_id() or 1

                # 如果是HTTP请求
                if request is not None:
                    if request.method != "POST":
                        return JsonResponse({"error": "Method not allowed"}, status=405)
                    try:
                        data = json.loads(request.body)
                    except json.JSONDecodeError:
                        return JsonResponse({"error": "Invalid JSON"}, status=400)
                else:
                    data = kwargs

                node_model = NodeModel(
                    node_id=node_id,
                    node_name=data.get("node_name"),
                    description=data.get("description"),
                    state=data.get("state", 0),
                    parent_id=data.get("parent_id", 0),
                    children_state=data.get("children_state", 0),
                )
                node_model.save()
                node = Node.create_from_db(node_model)
                node.node_id = node_id
                if request is not None:
                    return JsonResponse(
                        {
                            "node_id": node.node_id,
                            "node_name": node.node_name,
                            "description": node.description,
                            "state": node.state,
                            "parent_id": node.parent_id if node.parent_id else 0,
                        }
                    )
                return node

        except Exception as e:
            import traceback

            print(f"Error in create: {str(e)}")
            print(traceback.format_exc())
            if request is not None:
                return JsonResponse({"error": str(e)}, status=500)
            raise e

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
            }

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
                        setattr(node_model, field_mapping[key], value)

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
    def delete(request=None, node_id=None):
        """
        删除节点及其所有子节点
        :param request: HTTP请求对象（可选）
        :param node_id: 节点ID
        :return: JsonResponse 或 bool
        """
        try:
            # 如果是通过 URL 参数传入的 node_id
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            def delete_node_and_children(node_id):
                node_model = Node._get_node_model(node_id)
                if not node_model:
                    return

                # 递归删除所有子节点
                children = list(NodeModel.objects.filter(parent_id=node_id))
                for child in children:
                    delete_node_and_children(child.node_id)

                # 更新父节点的 childrens
                if node_model.parent_id:
                    parent = Node._get_node_model(node_model.parent_id)
                    if parent:
                        parent_childrens = list(
                            NodeModel.objects.filter(parent_id=node_model.parent_id)
                        )
                        if node_id in parent_childrens:
                            parent_childrens.remove(node_id)
                            parent.set_childrens(parent_childrens)
                            parent.save()

                # 删除当前节点
                node_model.delete()

            with transaction.atomic():
                delete_node_and_children(node_id)
                if request:
                    return JsonResponse({"status": "success"})
                return True

        except Exception as e:
            import traceback

            print(f"Error in delete: {str(e)}")
            print(traceback.format_exc())
            if request:
                return JsonResponse({"error": str(e)}, status=500)
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
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            def get_node_with_children(node_id):
                node = NodeModel.objects.get(node_id=node_id)
                children = list(NodeModel.objects.filter(parent_id=node_id))

                node_data = {
                    "node_id": node.node_id,
                    "node_name": node.node_name,
                    "description": node.description,
                    "state": node.state,
                    "parent_id": node.parent_id,
                    "children_state": node.children_state,
                    "children": [
                        get_node_with_children(child.node_id) for child in children
                    ],
                }
                return node_data

            result = get_node_with_children(node_id)
            if request:
                return JsonResponse(result, encoder=NodeJSONEncoder)
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
    def get_children(node_id):
        """
        获取节点的所有子节点
        :param node_id: 节点ID
        :return: list[Node] 子节点列表或None
        """
        try:
            children = NodeModel.objects.filter(parent_id=node_id)
            return [Node.create_from_db(child) for child in children]
        except Exception:
            return None
