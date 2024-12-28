from django.core.exceptions import ObjectDoesNotExist
from ..model.models import NodeModel


class Node:
    def __init__(self, node_id, node_name="", description="", state=0, parent_id=0):
        self.parent_id = parent_id
        self.node_id = node_id
        self.state = state
        self.node_name = node_name
        self.description = description
        self.children_state = 0
        self.state_change_callback = None

    @classmethod
    def get(cls, node_id):
        """
        从数据库获取节点
        :param node_id: 节点id
        :return: Node对象或None
        """
        try:
            node_data = NodeModel.objects.get(node_id=node_id)
            return cls.create_from_db(node_data)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        """
        获取所有节点
        :return: Node对象列表
        """
        nodes = NodeModel.objects.all()
        return [cls.create_from_db(node) for node in nodes]

    def save(self):
        """
        保存或更新节点到数据库
        """
        node_data = {
            "parent_id": self.parent_id,
            "node_id": self.node_id,
            "state": self.state,
            "node_name": self.node_name,
            "description": self.description,
            "children_state": self.children_state,
        }
        NodeModel.objects.update_or_create(node_id=self.node_id, defaults=node_data)

    def delete(self):
        """
        从数据库删除节点
        :return: 是否删除成功
        """
        try:
            NodeModel.objects.get(node_id=self.node_id).delete()
            return True
        except ObjectDoesNotExist:
            return False

    def update(self, **kwargs):
        """
        更新节点属性
        :param kwargs: 要更新的属性和值
        例如:node.update(name="新名称", state=1)
        """
        valid_fields = {
            "name": "node_name",
            "state": "state",
            "description": "description",
            "parent_id": "parent_id",
        }

        updates = {}
        for key, value in kwargs.items():
            if key in valid_fields:
                db_field = valid_fields[key]
                setattr(self, db_field, value)
                updates[db_field] = value

        if updates:
            NodeModel.objects.filter(node_id=self.node_id).update(**updates)
            if "state" in kwargs:
                self._check_children_states()

    @property
    def children(self):
        """
        获取子节点列表
        :return: 子节点列表
        """
        children = NodeModel.objects.filter(parent_id=self.node_id)
        return [self.create_from_db(child) for child in children]

    def add_child(self, child_node):
        """
        添加子节点
        :param child_node: Node对象
        """
        child_node.update(parent_id=self.node_id)
        child_node.save()
        self._check_children_states()

    def remove_child(self, child_id):
        """
        删除子节点
        :param child_id: 子节点id
        :return: 是否删除成功
        """
        deleted = NodeModel.objects.filter(
            node_id=child_id, parent_id=self.node_id
        ).delete()[0]
        if deleted:
            self._check_children_states()
            return True
        return False

    def on_children_state_change(self, callback):
        """
        设置子节点状态变更回调
        :param callback: 回调函数
        """
        self.state_change_callback = callback

    def _check_children_states(self):
        """
        检查子节点状态一致性
        """
        children = NodeModel.objects.filter(parent_id=self.node_id)
        if not children.exists():
            return

        first_state = children.first().state
        all_same = all(child.state == first_state for child in children)

        if all_same:
            self.children_state = first_state
            NodeModel.objects.filter(node_id=self.node_id).update(
                children_state=first_state
            )
            if self.state_change_callback:
                self.state_change_callback(first_state)

    @classmethod
    def create_from_db(cls, node_data):
        """
        从数据库记录创建Node实例
        """
        return cls(
            node_id=node_data.node_id,
            node_name=node_data.node_name,
            description=node_data.description,
            state=node_data.state,
            parent_id=node_data.parent_id,
        )
