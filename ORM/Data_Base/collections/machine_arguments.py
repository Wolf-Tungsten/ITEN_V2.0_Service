from ..collections.base import CollectionBase


class MachineArguments(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'machine_arguments')
        self.default = {
            'machine_id': '',
            'arguments': ''  # 此处为JSON字符串
        }

    async def add_arguments(self, machine_id, args):
        arguments = {
            'machine_id': machine_id,
            'arguments': args
        }
        await self.insert_one(arguments)

    async def get_arguments(self, machine_id):
        condition = {'machine_id': machine_id}
        result = await self.collection.find_one(condition)
        if result is not None:
            result = result['arguments']
        return result

    async def update_arguments(self, machine_id, args):
        condition = {'machine_id': machine_id}
        update = {'$set': {'arguments': args}}
        await self.collection.update_one(condition, update)

    def get_default(self):
        return self.default
