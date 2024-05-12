from pathlib import Path
import xnippet as xnippet
import logging


if __name__ == "__main__":
    xnippet.setup_logging(default_path='./logging.yaml')    
    logger = logging.getLogger()
    example = {"package_name": "xnippet-live",
            "package_version": xnippet.__version__,
            "package__file__": Path(__file__).parent,
            "config_path": 'examples',
            "config_filename": 'example_config.yaml'}
    logger.info('this is test logging')
    mng = xnippet.XnippetManager(**example)