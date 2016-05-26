# Copyright 2016 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast ZeroMQ message broker.

This broker provides the static point in the nowcast messaging framework,
allowing the nowcast manager to be restarted more or less at will.
"""
import logging
import logging.config
import os

import zmq

from nemo_nowcast import lib

NAME = 'message_broker'

logger = logging.getLogger(NAME)

context = zmq.Context()


def main():
    parser = lib.basic_arg_parser(NAME, description=__doc__)
    parsed_args = parser.parse_args()
    config = lib.load_config(parsed_args.config_file)
    logging.config.dictConfig(config['logging'])
    logger.info('running in process {}'.format(os.getpid()))
    logger.info('read config from {.config_file}'.format(parsed_args))

    # Create sockets and bind them to ports
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend_port = config['zmq']['ports']['frontend']
    frontend.bind('tcp://*:{}'.format(frontend_port))
    logger.info('frontend bound to port {}'.format(frontend_port))
    backend_port = config['zmq']['ports']['backend']
    backend.bind('tcp://*:{}'.format(backend_port))
    logger.info('backend bound to port {}'.format(backend_port))

if __name__ == '__main__':
    main()
