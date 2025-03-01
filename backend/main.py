import os
import uvicorn
import click

from core.config import config

from core.db import init_db  # noqa: E402
# from core.helpers.utils.estimate import manager  # noqa: E402
# from core.helpers.utils.tijmen import tijmens_tests  # noqa: E402
# from core.helpers.utils.thijs import thijs_tests  # noqa: E402


@click.command()
@click.option(
    "--tijmen",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(tijmen: bool = False):
    app = os.getenv("APP")

    if tijmen or app == "TIJMEN":
        init_db(delete=False)
        # tijmens_tests()
        return

    if app == "THIJS":
        init_db(delete=False)
        # thijs_tests()
        return
    
    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.ENV != "production",
        workers=1,
    )


if __name__ == "__main__":
    # try:
        main()
    # except Exception as exc:
    #     manager.handle_exc(exc)
