from app.dao.database_dao import DatabaseDAO
from config import Config
from pprint import pprint as pp

directory = Config()
database_manager = DatabaseDAO(directory.DATABASE)

pp(database_manager.get_actors("Jack Black", "Dustin Hoffman"))
pp(database_manager.get_title_by_options("TV Show", "2019", "TV"))
