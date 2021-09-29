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

import grpc

from typedb.api.connection.credential import TypeDBCredential
from typedb.connection.client import _TypeDBClientImpl
from typedb.connection.cluster.stub import ClusterServerStub
from typedb.connection.database_manager import _TypeDBDatabaseManagerImpl


class _ClusterServerClient(_TypeDBClientImpl):

    def __init__(self, address: str, credential: TypeDBCredential, parallelisation: int = 2):
        super(_ClusterServerClient, self).__init__(address, parallelisation)
        self._credential = credential
        self._channel = self._new_channel()
        self._stub = ClusterServerStub.create(self._channel)
        self._databases = _TypeDBDatabaseManagerImpl(self.stub())

    def databases(self) -> _TypeDBDatabaseManagerImpl:
        return self._databases

    def channel(self) -> grpc.Channel:
        return self._channel

    def stub(self) -> ClusterServerStub:
        return self._stub

    def _new_channel(self) -> grpc.Channel:
        if self._credential.tls_root_ca_path() is not None:
            with open(self._credential.tls_root_ca_path(), 'rb') as root_ca:
                channel_credentials = grpc.ssl_channel_credentials(root_ca.read())
        else:
            channel_credentials = grpc.ssl_channel_credentials()
        combined_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            grpc.metadata_call_credentials(_CredentialAuth(self._credential.username(), self._credential.password()))
        )
        return grpc.secure_channel(self._address, combined_credentials)

    def close(self) -> None:
        super().close()
        self._channel.close()


class _CredentialAuth(grpc.AuthMetadataPlugin):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __call__(self, context, callback):
        callback((('username', self._username), ('password', self._password)), None)
