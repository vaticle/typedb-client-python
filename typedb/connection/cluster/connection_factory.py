#   Copyright (C) 2021 Vaticle
#
#   Licensed to the Apache Software Foundation (ASF) under one
#   or more contributor license agreements.  See the NOTICE file
#   distributed with this work for additional information
#   regarding copyright ownership.  The ASF licenses this file
#   to you under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in compliance
#   with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing,
#   software distributed under the License is distributed on an
#   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#   KIND, either express or implied.  See the License for the
#   specific language governing permissions and limitations
#   under the License.

from grpc import Channel

from typedb.api.connection.credential import TypeDBCredential
from typedb.common.rpc.stub import TypeDBStub
from typedb.connection.cluster.stub import _ClusterServerStub
from typedb.connection.connection_factory import _TypeDBConnectionFactory


class _ClusterConnectionFactory(_TypeDBConnectionFactory):

    def __init__(self, credential: TypeDBCredential):
        self._credential = credential

    def newChannel(self, address: str) -> Channel:
        # TODO implement new ssl secured channel
        return None

    def newTypeDBStub(self, channel: Channel) -> TypeDBStub:
        return _ClusterServerStub.create(channel, self._credential)
