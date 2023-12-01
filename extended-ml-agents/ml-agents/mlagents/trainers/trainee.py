import time
from web3 import Web3, HTTPProvider
import json

from mlagents_envs.logging_util import get_logger

logger = get_logger(__name__)

class Trainee:
    def __init__(self):
        self.trainee_url = "http://127.0.0.1:5200/"             


