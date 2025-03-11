import asyncio
import logging
import os

import replicate
from apps.ai.models import Category, Model
from apps.ai.schemas import VersionSchema
from fastapi_mongo_base.core import db
from replicate.model import Model as ReplicateModel
from server.config import Settings
from utils.ai import PromptlyClient

client = replicate.Client(api_token=os.getenv("REPLICATE_API_KEY"))
promptly_client = PromptlyClient()

check_m = None
check_c = None


async def insert_model(model: ReplicateModel, cat: Category):
    try:
        for k in model.dict().keys():
            if not hasattr(Model, k) and k not in [
                "cover_image_url",
                "default_example",
                "latest_version",
                "url",
            ]:
                raise Exception(f"{k} is not a valid model attribute")

        m = await Model.find_one({"source_url": model.url})
        if m and m.versions and model.latest_version.id in [v.id for v in m.versions]:
            logging.info(f"Model {model.url} already exists")
            return

        if not m:
            if not model.name:
                logging.warning(f"Model {model.url} has no name")
            if not model.description:
                logging.warning(f"Model {model.url} has no description")

            m = Model(
                name={
                    "en": model.name,
                    "fa": (
                        await promptly_client.translate(model.name)
                        if model.name
                        else None
                    ),
                },
                description=(
                    {
                        "en": model.description,
                        "fa": (await promptly_client.translate(model.description)),
                    }
                    if model.description
                    else None
                ),
                category=cat,
                chat_based=False,
                source="replicate",
                **model.dict(
                    exclude={
                        "cover_image_url",
                        "latest_version",
                        "url",
                        "name",
                        "description",
                    }
                ),
                versions=[],
                user_id=None,
                source_url=model.url,
                api_available=(
                    model.latest_version.openapi_schema is not None
                    if model.latest_version
                    else False
                ),
                pixy_available=False,
                pixy_url=None,
                pixy_pricing=None,
            )

        m.versions = m.versions or []
        if model.latest_version:
            m.versions.append(VersionSchema(**model.latest_version.dict()))
        await m.save()
    except Exception as e:
        import traceback

        global check_c, check_m
        check_c = cat.slug
        check_m = model
        traceback_str = "".join(traceback.format_tb(e.__traceback__))
        logging.error(
            f"Error inserting model {cat.slug} {model.url}:\n{traceback_str}\n{type(e)} {e}"
        )
        raise e


async def insert_category_models(cat: Category):
    models = await client.collections.async_get(cat.slug)
    for i, model in enumerate(models):

        logging.info(f"Inserting model {i+1}/{len(models)}, {cat.slug} {model.name}")

        await insert_model(model, cat)

    # await asyncio.gather(*models_tasks)


async def fetch_categories():
    collections = await client.collections.async_list()
    for collection in collections:
        cat = await Category.find_one({"slug": collection.slug})
        if not cat:
            if not collection.name:
                logging.warning(f"Category {collection.slug} has no name")
            if not collection.description:
                logging.warning(f"Category {collection.slug} has no description")

            cat = Category(
                slug=collection.slug,
                name={
                    "en": collection.name,
                    "fa": await promptly_client.translate(collection.name),
                },
                description={
                    "en": collection.description,
                    "fa": await promptly_client.translate(collection.description),
                },
            )
            await cat.save()

        await insert_category_models(cat)

        logging.info(cat.name)
        logging.info(cat.slug)
        logging.info(cat.description)


async def main():
    Settings.config_logger()
    await db.init_mongo_db()
    await fetch_categories()


if __name__ == "__main__":
    asyncio.run(main())
