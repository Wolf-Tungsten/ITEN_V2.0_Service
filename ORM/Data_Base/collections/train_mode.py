from ..collections.base import CollectionBase


class TrainMode(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'train_mode')

    async def add_train_mode(self, train_name, train_data):
        train_mode = {
            'train_name': train_name,
            'train_data': train_data
        }
        await self.insert_one(train_mode)

    async def get_train_data(self, train_id):
        train_mode = await self.find_one_by_id(train_id)
        return {
            'train_name': train_mode['train_name'],
            'train_data': train_mode['train_data']
        }

    async def update_train_mode(self, train_id, train_name, train_data):
        train_mode = {
            'train_name': train_name,
            'train_data': train_data
        }
        pass
        await self.update_one_by_id(train_id, train_mode)

    async def get_train_mode_list(self):
        all_train_modes = await self.find_all()
        for item in all_train_modes:
            item.pop('train_data')
        return all_train_modes

