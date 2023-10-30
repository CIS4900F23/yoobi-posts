"""docstring"""

class Config:
    """_summary_
    """
    TESTING = False

class DevelopmentConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """

class TestingConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """
    Testing = True

class ProductionConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """