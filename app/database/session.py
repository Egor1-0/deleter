from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import URL


engine = create_async_engine(URL)

async_session = async_sessionmaker(engine)

# создание происходит через миграции алембик