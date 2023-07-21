#
# Copyright (C) 2022 Vaticle
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

from typing import TYPE_CHECKING, Iterator

import typedb_protocol.common.transaction_pb2 as transaction_proto
from grpc import RpcError
from typedb.api.connection.options import TypeDBOptions
from typedb.api.connection.transaction import Transaction, TransactionType
from typedb.api.query.future import QueryFuture
from typedb.common.exception import TypeDBClientException, TRANSACTION_CLOSED, TRANSACTION_CLOSED_WITH_ERRORS
from typedb.common.rpc.request_builder import transaction_commit_req, transaction_rollback_req, transaction_open_req
from typedb.concept.concept_manager import _ConceptManager
from typedb.logic.logic_manager import _LogicManager
from typedb.query.query_manager import _QueryManager
from typedb.stream.bidirectional_stream import BidirectionalStream

if TYPE_CHECKING:
    from typedb.connection.session import _TypeDBSessionImpl

from typedb.typedb_client_python import transaction_new, transaction_commit, transaction_rollback, transaction_is_open, transaction_on_close, transaction_force_close, TransactionCallbackDirector


class _TransactionImpl(Transaction):

    def __init__(self, session: "_TypeDBSessionImpl", transaction_type: TransactionType, options: TypeDBOptions = None):
        if not options:
            options = TypeDBOptions.core()
        self._transaction_type = transaction_type
        self._options = options
        self._transaction = transaction_new(session, transaction_type, options)
        self._concept_manager = _ConceptManager(self)
        self._query_manager = _QueryManager(self)
        self._logic_manager = _LogicManager(self)

    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    def options(self) -> TypeDBOptions:
        return self._options

    def is_open(self) -> bool:
        if not self._transaction.thisown:
            return False
        return transaction_is_open(self._transaction)

    def concepts(self) -> _ConceptManager:
        return self._concept_manager

    def logic(self) -> _LogicManager:
        return self._logic_manager

    def query(self) -> _QueryManager:
        return self._query_manager

    def on_close(self, function: callable):
        transaction_on_close(self._transaction, _TransactionImpl.TransactionOnClose().callback(function))

    class TransactionOnClose(TransactionCallbackDirector):
        pass

    def execute(self, request: transaction_proto.Transaction.Req,
                batch: bool = True) -> transaction_proto.Transaction.Res:
        return self.run_query(request, batch).get()

    def run_query(self, request: transaction_proto.Transaction.Req, batch: bool = True) -> QueryFuture[
        transaction_proto.Transaction.Res]:
        if not self.is_open():
            self._raise_transaction_closed()
        return self._bidirectional_stream.single(request, batch)

    def stream(self, request: transaction_proto.Transaction.Req) -> Iterator[transaction_proto.Transaction.ResPart]:
        if not self.is_open():
            self._raise_transaction_closed()
        return self._bidirectional_stream.stream(request)

    def commit(self):
        try:
            self.execute(transaction_commit_req())
        finally:
            self.close()

    def rollback(self):
        self.execute(transaction_rollback_req())

    def close(self):
        self._bidirectional_stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_tb is not None:
            return False

    def _raise_transaction_closed(self):
        error = self._bidirectional_stream.get_error()
        if error is None:
            raise TypeDBClientException.of(TRANSACTION_CLOSED)
        else:
            raise TypeDBClientException.of(TRANSACTION_CLOSED_WITH_ERRORS, error)
