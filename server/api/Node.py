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
                # 如果有父节点，检查父节点状态
                if node_model.parent_id:
                    Node._check_parent_state(node_model.parent_id)

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
            # 如果是通过 URL 参数传入的 node_id
            if node_id is None and request is not None:
                node_id = request.resolver_match.kwargs.get("node_id")

            print(f"Updating node {node_id} with data:", kwargs)  # 添加调试日志

            # 获取节点
            node_model = Node._get_node_model(node_id)
            if node_model is None:
                if request:
                    return JsonResponse({"error": "Node not found"}, status=404)
                return False

            # 获取请求数据
            if request and request.method == "POST":
                try:
                    data = json.loads(request.body)
                    print(f"Received request data:", data)  # 添加调试日志
                    kwargs = data
                except json.JSONDecodeError as e:
                    print(f"JSON decode error:", str(e))  # 添加调试日志
                    return JsonResponse({"error": "Invalid JSON"}, status=400)

            # 定义可更新的字段
            allowed_fields = ["node_name", "description", "state"]

            try:
                with transaction.atomic():
                    # 更新字段
                    updated = False
                    for field in allowed_fields:
                        if field in kwargs:
                            print(f"Setting {field} to {kwargs[field]}")
                            setattr(node_model, field, kwargs[field])
                            updated = True

                    if updated:
                        node_model.save()
                        # 如果更新了状态，检查父节点状态
                        if "state" in kwargs:
                            Node._check_parent_state(node_model.parent_id)

                    if request:
                        return JsonResponse({"status": "success"})
                    return True

            except Exception as e:
                print(f"Transaction error:", str(e))
                raise

        except Exception as e:
            import traceback

            print(f"Error in update: {str(e)}")
            print(traceback.format_exc())
            if request:
                return JsonResponse(
                    {"error": str(e), "details": traceback.format_exc()}, status=500
                )
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

                # 保存父节点ID，用于后续检查状态
                parent_id = node_model.parent_id

                # 递归删除所有子节点
                children = list(NodeModel.objects.filter(parent_id=node_id))
                for child in children:
                    delete_node_and_children(child.node_id)

                # 删除当前节点
                node_model.delete()

                # 删除完成后检查父节点状态
                if parent_id:
                    Node._check_parent_state(parent_id)

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
    def _check_parent_state(parent_id):
        """
        递归检查父节点状态
        :param parent_id: 父节点ID
        """
        if not parent_id:
            return

        try:
            # 获取父节点
            parent = NodeModel.objects.get(node_id=parent_id)
            if not parent:
                return

            # 使用 values_list 直接获取子节点状态列表
            children_states = list(
                NodeModel.objects.filter(parent_id=parent_id).values_list(
                    "state", flat=True
                )
            )

            if not children_states:
                return

            # 检查所有子节点状态是否一致
            first_state = children_states[0]
            all_same = all(state == first_state for state in children_states)

            if all_same:
                # 只有当状态不同时才更新
                if parent.state != first_state:
                    parent.state = first_state
                    parent.save()

                    # 递归检查上层父节点
                    if parent.parent_id:
                        Node._check_parent_state(parent.parent_id)

        except Exception as e:
            print(f"Error checking parent state: {str(e)}")
            import traceback

            print(traceback.format_exc())

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
