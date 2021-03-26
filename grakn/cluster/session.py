#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from typing import TYPE_CHECKING

from grakn.api.options import GraknClusterOptions, GraknOptions
from grakn.api.session import GraknSession
from grakn.api.transaction import GraknTransaction
from grakn.cluster.database import _ClusterDatabase
from grakn.cluster.failsafe_task import _FailsafeTask
from grakn.core.database import _CoreDatabase
from grakn.core.transaction import _CoreTransaction

if TYPE_CHECKING:
    from grakn.cluster.client import _ClusterClient


class _ClusterSession(GraknSession):

    def __init__(self, cluster_client: "_ClusterClient", server_address: str, database: str, session_type: GraknSession.Type, options: GraknClusterOptions):
        self.cluster_client = cluster_client
        self.core_client = cluster_client.core_client(server_address)
        print("Opening a session to '%s'" % server_address)
        self.core_session = self.core_client.session(database, session_type, options)
        self._options = options

    def transaction(self, transaction_type: GraknTransaction.Type, options: GraknClusterOptions = None) -> _CoreTransaction:
        if not options:
            options = GraknOptions.cluster()
        return self._transaction_any_replica(transaction_type, options) if options.read_any_replica else self._transaction_primary_replica(transaction_type, options)

    def _transaction_primary_replica(self, transaction_type: GraknTransaction.Type, options: GraknClusterOptions) -> _CoreTransaction:
        return _TransactionFailsafeTask(self, transaction_type, options).run_primary_replica()

    def _transaction_any_replica(self, transaction_type: GraknTransaction.Type, options: GraknClusterOptions) -> _CoreTransaction:
        return _TransactionFailsafeTask(self, transaction_type, options).run_any_replica()

    def session_type(self) -> GraknSession.Type:
        return self.core_session.session_type()

    def options(self) -> GraknClusterOptions:
        return self._options

    def is_open(self) -> bool:
        return self.core_session.is_open()

    def close(self) -> None:
        self.core_session.close()

    def database(self) -> _CoreDatabase:
        return self.core_session.database()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_tb is not None:
            return False


class _TransactionFailsafeTask(_FailsafeTask):

    def __init__(self, cluster_session: _ClusterSession, transaction_type: GraknTransaction.Type, options: GraknClusterOptions):
        super().__init__(cluster_session.cluster_client, cluster_session.database().name())
        self.cluster_session = cluster_session
        self.transaction_type = transaction_type
        self.options = options

    def run(self, replica: _ClusterDatabase.Replica):
        return self.cluster_session.core_session.transaction(self.transaction_type, self.options)

    def rerun(self, replica: _ClusterDatabase.Replica):
        if self.cluster_session.core_session:
            self.cluster_session.core_session.close()
        self.cluster_session.core_client = self.cluster_session.cluster_client.core_client(replica.address())
        self.cluster_session.core_session = self.cluster_session.core_client.session(self.database, self.cluster_session.session_type(), self.cluster_session.options())
        return self.cluster_session.core_session.transaction(self.transaction_type, self.options)
