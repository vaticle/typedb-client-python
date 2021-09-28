#
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
#

from grpc import Channel

from typedb.api.connection.credential import TypeDBCredential
from typedb.common.rpc.stub import TypeDBStub
from typedb.connection.client import _TypeDBClientImpl
from typedb.connection.cluster.connection_factory import _ClusterConnectionFactory
from typedb.connection.connection_factory import _TypeDBConnectionFactory


class _ClusterServerClient(_TypeDBClientImpl):

    def __init__(self, address: str, credential: TypeDBCredential, parallelisation: int = 2):
        super(_ClusterServerClient, self).__init__(address, parallelisation)
        self._connection_factory = _ClusterConnectionFactory(credential)
        self._channel = self._connection_factory.newChannel(self._address)
        self._stub = self._connection_factory.newTypeDBStub(self._channel)

    def channel(self) -> Channel:
        return self._channel

    def stub(self) -> TypeDBStub:
        return self._stub

    def connection_factory(self) -> _TypeDBConnectionFactory:
        return self._connection_factory
