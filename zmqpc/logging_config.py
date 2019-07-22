import colorlog
import logging.config

LOG_LEVEL = 'DEBUG'

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'simple': {
            'class': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)s:%(name)s:%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': f'{LOG_LEVEL}',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'zmqpc': {
            'level': f'{LOG_LEVEL}',
            'handlers': ['console'],
            'propagate': False,
        },
    }
})
