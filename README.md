# projectState


# 要求Node.py中字段编写API:
# 1,根据节点id获取当前对象
# 2,根据节点id获取当前对象的子节点列表
# 3,根据节点id修改父节点
# 4,根据节点id修改节点状态
# 5,根据节点id修改节点描述
# 6,根据节点id添加子节点
# 7,根据节点id删除子节点
# 8,根据节点id获取所有子节点状态(要求有方法回调,当所有子节点状态统一时调用,并传入状态信息)
# 9,根据节点id修改节点名称
# 10,根据节点id获取节点名称
# 11,使用Django对Node进行CRUD操作要求使用数据库为mongodb

补充以下方法
ProjectModel.get_by_id
ProjectModel.get_all
ProjectModel.update
ProjectModel.create
ProjectModel.delete
ProjectModel.update
ProjectModel.add_node
ProjectModel.remove_node
ProjectModel.get_node